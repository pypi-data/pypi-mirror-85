import argparse
import logging
import asyncio
import socket
import yaml
import sys
import re
import ssl
import pkgutil
import ipaddress

from datetime import datetime, timezone

# python3 -m pip dnspython
import dns.rcode
import dns.rdatatype
import dns.message

# wget https://raw.githubusercontent.com/dnstap/dnstap.pb/master/dnstap.proto
# wget https://github.com/protocolbuffers/protobuf/releases/download/v3.13.0/protoc-3.13.0-linux-x86_64.zip
# python3 -m pip install protobuf
# bin/protoc --python_out=. dnstap.proto

from dnstap_receiver import dnstap_pb2 # more informations on dnstap http://dnstap.info/
from dnstap_receiver import fstrm  # framestreams decoder

from dnstap_receiver import output_stdout
from dnstap_receiver import output_syslog
from dnstap_receiver import output_tcp
from dnstap_receiver import output_metrics

from dnstap_receiver import api_server
from dnstap_receiver import statistics

class UnknownValue:
    name = "-"

DNSTAP_TYPE = dnstap_pb2._MESSAGE_TYPE.values_by_number
DNSTAP_FAMILY = dnstap_pb2._SOCKETFAMILY.values_by_number
DNSTAP_PROTO = dnstap_pb2._SOCKETPROTOCOL.values_by_number  

# command line arguments definition
parser = argparse.ArgumentParser()
parser.add_argument("-l", 
                    help="IP of the dnsptap server to receive dnstap payloads (default: %(default)r)",
                    default="0.0.0.0")
parser.add_argument("-p", type=int,
                    help="Port the dnstap receiver is listening on (default: %(default)r)",
                    default=6000)               
parser.add_argument("-u", help="read dnstap payloads from unix socket")
parser.add_argument('-v', action='store_true', help="verbose mode")   
parser.add_argument("-c", help="external config file")   

import dns.exception
import dns.opcode
import dns.flags

# waiting fix with dnspython 2.1
# will be removed in the future
class _WireReader(dns.message._WireReader):
    def read(self):
        """issue fixed - waiting fix with dnspython 2.1"""
        if self.parser.remaining() < 12:
            raise dns.message.ShortHeader
        (id, flags, qcount, ancount, aucount, adcount) = \
            self.parser.get_struct('!HHHHHH')
        factory = dns.message._message_factory_from_opcode(dns.opcode.from_flags(flags))
        self.message = factory(id=id)
        self.message.flags = flags
        self.initialize_message(self.message)
        self.one_rr_per_rrset = \
            self.message._get_one_rr_per_rrset(self.one_rr_per_rrset)
        self._get_question(dns.message.MessageSection.QUESTION, qcount)
        
        return self.message

# waiting fix with dnspython 2.1
# will be removed in the future
def from_wire(wire, question_only=True):
    """decode wire message - waiting fix with dnspython 2.1"""
    raise_on_truncation=False
    def initialize_message(message):
        message.request_mac = b''
        message.xfr = False
        message.origin = None
        message.tsig_ctx = None

    reader = _WireReader(wire, initialize_message, question_only=question_only,
                 one_rr_per_rrset=False, ignore_trailing=False,
                 keyring=None, multi=False)
    try:
        m = reader.read()
    except dns.exception.FormError:
        if reader.message and (reader.message.flags & dns.flags.TC) and \
           raise_on_truncation:
            raise dns.message.Truncated(message=reader.message)
        else:
            raise
    # Reading a truncated message might not have any errors, so we
    # have to do this check here too.
    if m.flags & dns.flags.TC and raise_on_truncation:
        raise dns.message.Truncated(message=m)

    return m
    
async def cb_ondnstap(dnstap_decoder, payload, cfg, queue, metrics):
    """on dnstap"""
    # decode binary payload
    dnstap_decoder.ParseFromString(payload)
    dm = dnstap_decoder.message
    
    # filtering by dnstap identity ?
    tap_ident = dnstap_decoder.identity.decode()
    if not len(tap_ident):
        tap_ident = UnknownValue.name
    if cfg["filter"]["dnstap-identities"] is not None:
        if re.match(cfg["filter"]["dnstap-identities"], dnstap_decoder.identity.decode()) is None:
            del dm
            return
            
    tap = { "identity": tap_ident, "query-name": UnknownValue.name, 
            "query-type": UnknownValue.name, "source-ip": UnknownValue.name}
    
    # decode type message
    tap["message"] = DNSTAP_TYPE.get(dm.type, UnknownValue).name
    tap["family"] = DNSTAP_FAMILY.get(dm.socket_family, UnknownValue).name
    tap["protocol"] = DNSTAP_PROTO.get(dm.socket_protocol, UnknownValue).name

    # decode query address
    if len(dm.query_address) and dm.socket_family == 1:
        tap["source-ip"] = socket.inet_ntoa(dm.query_address)
    if len(dm.query_address) and dm.socket_family == 2:
        tap["source-ip"] = socket.inet_ntop(socket.AF_INET6, dm.query_address)
    tap["source-port"] = dm.query_port
    if tap["source-port"] == 0:
        tap["source-port"] = UnknownValue.name
        
    # handle query message
    if (dm.type % 2 ) == 1 :
        dnstap_parsed = from_wire(dm.query_message,
                                  question_only=True)
        tap["length"] = len(dm.query_message)
        d1 = dm.query_time_sec +  (round(dm.query_time_nsec ) / 1000000000)
        tap["timestamp"] = datetime.fromtimestamp(d1, tz=timezone.utc).isoformat()
        
    # handle response message
    if (dm.type % 2 ) == 0 :
        dnstap_parsed = from_wire(dm.response_message,
                                  question_only=True)
        tap["length"] = len(dm.response_message)
        d2 = dm.response_time_sec + (round(dm.response_time_nsec ) / 1000000000) 
        tap["timestamp"] = datetime.fromtimestamp(d2, tz=timezone.utc).isoformat()
        
    # common params
    if len(dnstap_parsed.question):
        tap["query-name"] = dnstap_parsed.question[0].name.to_text()
        tap["query-type"] = dns.rdatatype.to_text(dnstap_parsed.question[0].rdtype)
    tap["code"] = dns.rcode.to_text(dnstap_parsed.rcode())
    
    # filtering by qname ?
    if cfg["filter"]["qname-regex"] is not None:
        if re.match(cfg["filter"]["qname-regex"], tap["query-name"]) is None:
            del dm; del tap;
            return

    # update metrics 
    metrics.record_dnstap(dnstap=tap)
        
    # append the dnstap message to the queue
    queue.put_nowait(tap)

async def cb_onconnect(reader, writer, cfg, queue, metrics):
    """callback when a connection is established"""
    # get peer name
    peername = writer.get_extra_info('peername')
    if not len(peername):
        peername = "(unix-socket)"
    logging.debug(f"Input handler: new connection from {peername}")

    # access control list check
    if len(writer.get_extra_info('peername')):
        acls_network = []
        for a in cfg["input"]["tcp-socket"]["access-control-list"]:
            acls_network.append(ipaddress.ip_network(a))
            
        acl_allow = False
        for acl in acls_network:
            if ipaddress.ip_address(peername[0]) in acl:
                acl_allow = True
        
        if not acl_allow:
            writer.close()
            logging.debug("Input handler: checking acl refused")
            return
        
        logging.debug("Input handler: checking acl allowed")
        
    # prepare frame streams decoder
    fstrm_handler = fstrm.FstrmHandler()
    loop = asyncio.get_event_loop()
    dnstap_decoder = dnstap_pb2.Dnstap()

    try: 
        # syntax only works with python 3.8
        # while data := await reader.read(fstrm_handler.pending_nb_bytes()) 
        running = True
        while running:
            # read bytes
            data = await reader.read(fstrm_handler.pending_nb_bytes()) 
            if not len(data):
                running = False
                break
                
            # append data to the buffer
            fstrm_handler.append(data=data)
            
            # process the buffer, check if we have received a complete frame ?
            if fstrm_handler.process():
                # Ok, the frame is complete so let's decode it
                fs, payload  = fstrm_handler.decode()

                # handle the DATA frame
                if fs == fstrm.FSTRM_DATA_FRAME:
                    loop.create_task(cb_ondnstap(dnstap_decoder, payload, cfg, queue, metrics))
                    
                # handle the control frame READY
                if fs == fstrm.FSTRM_CONTROL_READY:
                    logging.debug(f"Input handler: control ready received from {peername}")
                    ctrl_accept = fstrm_handler.encode(fs=fstrm.FSTRM_CONTROL_ACCEPT)
                    # respond with accept only if the content type is dnstap
                    writer.write(ctrl_accept)
                    await writer.drain()
                    logging.debug(f"Input handler: sending control accept to {peername}")
                    
                # handle the control frame READY
                if fs == fstrm.FSTRM_CONTROL_START:
                    logging.debug(f"Input handler: control start received from {peername}")
   
                # handle the control frame STOP
                if fs == fstrm.FSTRM_CONTROL_STOP:
                    logging.debug(f"Input handler: control stop received from {peername}")
                    fstrm_handler.reset()           
    except asyncio.CancelledError:
        logging.debug(f'Input handler: {peername} - closing connection.')
        writer.close()
        await writer.wait_closed()
    except asyncio.IncompleteReadError:
        logging.debug(f'Input handler: {peername} - disconnected')
    finally:
        logging.debug(f'Input handler: {peername} - closed')

def merge_cfg(u, o):
    """merge config"""
    for k,v in u.items():
        if k in o:
            if isinstance(v, dict):
                merge_cfg(u=v,o=o[k])
            else:
                o[k] = v
                
def start_receiver():
    """start dnstap receiver"""
    # Handle command-line arguments.
    args = parser.parse_args()

    # set default config
    try:
        cfg =  yaml.safe_load(pkgutil.get_data(__package__, 'dnstap.conf')) 
    except FileNotFoundError:
        logging.error("default config file not found")
        sys.exit(1)
    except yaml.parser.ParserError:
        logging.error("invalid default yaml config file")
        sys.exit(1)
    
    # update default config with command line arguments
    cfg["verbose"] = args.v
    cfg["input"]["unix-socket"]["path"] = args.u
    cfg["input"]["tcp-socket"]["local-address"] = args.l
    cfg["input"]["tcp-socket"]["local-port"] = args.p

    # overwrite config with external file ?    
    if args.c:
        try:
            with open(args.c) as file:
                merge_cfg(u=yaml.safe_load(file),o=cfg)
        except FileNotFoundError:
            logging.error("external config file not found")
            sys.exit(1)
        except yaml.parser.ParserError:
            logging.error("external invalid yaml config file")
            sys.exit(1)
            
    # init logging
    level = logging.INFO
    if cfg["verbose"]:
        level = logging.DEBUG
    logging.basicConfig(format='%(asctime)s %(message)s', 
                        stream=sys.stdout, level=level)

    if args.c:
        logging.debug("external config file loaded")
    # start receiver and get event loop
    logging.debug("Start receiver...")
    loop = asyncio.get_event_loop()

    # prepare output
    queue = asyncio.Queue()
    stats = statistics.Stats()
    stats.prepare()
    
    if cfg["output"]["syslog"]["enable"]:
        logging.debug("Output handler: syslog")
        loop.create_task(output_syslog.handle(cfg["output"]["syslog"], 
                                              queue,
                                              stats))
        
    if cfg["output"]["tcp-socket"]["enable"]:
        logging.debug("Output handler: tcp")
        loop.create_task(output_tcp.handle(cfg["output"]["tcp-socket"],
                                           queue,
                                           stats))

    if cfg["output"]["stdout"]["enable"]:
        logging.debug("Output handler: stdout")
        loop.create_task(output_stdout.handle(cfg["output"]["stdout"],
                                              queue,
                                              stats))

    
    if cfg["output"]["metrics"]["enable"]:
        logging.debug("Output handler: metrics")
        loop.create_task(output_metrics.handle(cfg["output"]["metrics"],
                                              queue,
                                              stats))

    # asynchronous unix socket
    if cfg["input"]["unix-socket"]["path"] is not None:
        logging.debug("Input handler: unix socket")
        logging.debug("Input handler: listening on %s" % args.u)
        socket_server = asyncio.start_unix_server(lambda r, w: cb_onconnect(r, w, cfg, queue, stats),
                                                  path=cfg["input"]["unix-socket"]["path"],
                                                  loop=loop)
    # default mode: asynchronous tcp socket
    else:
        logging.debug("Input handler: tcp socket")
        
        ssl_context = None
        if cfg["input"]["tcp-socket"]["tls-support"]:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(certfile=cfg["input"]["tcp-socket"]["tls-server-cert"], 
                                        keyfile=cfg["input"]["tcp-socket"]["tls-server-key"])
            logging.debug("Input handler - tls support enabled")
        logging.debug("Input handler: listening on %s:%s" % (cfg["input"]["tcp-socket"]["local-address"],
                                              cfg["input"]["tcp-socket"]["local-port"])), 
        socket_server = asyncio.start_server(lambda r, w: cb_onconnect(r, w, cfg, queue, stats),
                                             cfg["input"]["tcp-socket"]["local-address"],
                                             cfg["input"]["tcp-socket"]["local-port"],
                                             ssl=ssl_context,
                                             loop=loop)

    # run until complete
    loop.run_until_complete(socket_server)
                                                  

    # start the restapi
    if cfg["web-api"]["enable"]:
        api_svr = api_server.create_server(loop, cfg=cfg["web-api"], stats=stats)
        loop.run_until_complete(api_svr)

    # run event loop 
    try:
       loop.run_forever()
    except KeyboardInterrupt:
        pass
