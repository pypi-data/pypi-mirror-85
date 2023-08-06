from essentials import socket_ops_v2 as socket_ops
from essentials import network_ops
import threading, time
from http.server import BaseHTTPRequestHandler
from io import BytesIO
import json
import os
import mimetypes
from essentials import file_ops, time_events, TimeStamp
from urllib.parse import parse_qs, urlsplit, unquote
from MkIOT.discovery import broadcast as ds_broadcast
import colorama
import re
import ssl
import psutil
import datetime
import zlib

def get_memory_usage():
    process = psutil.Process(os.getpid())
    return round((process.memory_info().rss) * 0.000001, 3)

FILE_CACHE = {}


class Cookie_Object(object):
    def __init__(self, name, value, expires=None, sameSite=None, strict=False, HTTP_Only=False, domain=None, path=None):
        self.name = name
        self.value = value
        self.expires = expires
        self.sameSite = sameSite
        self.strict = strict
        self.HTTP_Only = HTTP_Only
        self.domain = domain
        self.path = path

    def __repr__(self):
        return f"< Mako Cookie Object instance - Name={self.name}; Value={self.value} >"

    def __str__(self):
        return f"< Mako Cookie Object instance - Name={self.name}; Value={self.value} >"

    def __prep__(self):
        base = f"Set-Cookie: {self.name}={self.value}; "
        if self.expires is not None:
            base += f"Expires={self.expires}; "
        if self.sameSite is not None:
            base += f"SameSite={self.SameSite}; "
        if self.strict:
            base += "Strict; "
        if self.HTTP_Only:
            base += "HttpOnly; "
        if self.domain is not None:
            base += f"Domain={self.domain}; "
        if self.path is not None:
            base += f"Path={self.path}"
        return base

class Cookie_Jar(object):

    def __init__(self):
        self.cookies = {}

    def add_cookie(self, cookie_object=Cookie_Object):
        self.cookies[cookie_object.name] = cookie_object

    def get(self, name):
        cookie = Cookie_Object

        if name in self.cookies:
            return self.cookies[name]
        else:
            return None
        return cookie

class Time_Units(object):
    MILLISECONDS = 1000
    SECONDS = 1
    MINUTES = 1/60

class File_Object(object):

    def __new__(cls, *args, **kwargs):
        try:
            fp = args[0]
        except:
            fp = None
        if 'file_path' in kwargs:
            fp = kwargs['file_path']
        if 'no_cache' not in kwargs:
            if fp in FILE_CACHE:
                return FILE_CACHE[fp]
        return super(File_Object, cls).__new__(cls)

    def __init__(self, file_path=None, file_name=None, extension=None, mimetype=None, client_download_on_receive=False, data=None, from_client=False, cache=False, no_cache=False):
        self.file_path = file_path
        self.file_name = file_name
        self.extension = extension
        self.mimetype = mimetype
        self.cache = cache
        self.client_download_on_receive = client_download_on_receive
        self.from_client = from_client
        self.data = data
        self.header_data = None
        self.form_input_name = None

        if self.file_path is not None:
            if file_name is None:
                self.file_name = os.path.split(self.file_path)[1]

            if self.mimetype is None:
                self.mimetype = mimetypes.guess_type(self.file_name)[0]

            self.data = file_ops.read_file(self.file_path, True)

        if from_client:
            self.extension = os.path.splitext(self.file_name)[1]

        if cache:
            FILE_CACHE[self.file_path] = self

    def save(self, path):
        file_ops.write_file(path, self.data, byte=True)

class Redirect(object):

    def __init__(self, location, status_code=None, permanent=False):
        self.status_code = status_code
        self.permanent = permanent
        self.headers = {}
        self.cookies = []
        self.headers['server'] = "MkNxGn Mako - Python3;"
        self.headers['status'] = status_code
        self.headers['Location'] = location
        if status_code is None:
            if self.permanent:
                self.status_code = 301
            else:
                self.status_code = 307

    def add_header(self, header, value):
        self.headers[header] = value

    def add_cookie(self, cookie_object=Cookie_Object):
        self.cookies.append(cookie_object)

class Response(object):

    def __init__(self, response=None, status_code=200, file_object=None, redirect=None, ignore_and_drop=False, gzip=False):
        self.response = response
        self.response_type = type(self.response)
        self.status_code = status_code
        self.headers = {}
        self.cookies = []
        self.headers['server'] = "MkNxGn Mako - Python3;"
        self.headers['status'] = status_code
        self.access_control_allow_origin = None
        self.content_type = None
        self.file_object = file_object
        self.redirect = redirect
        self.ignore_and_drop = ignore_and_drop
        self.gzip = gzip
        if self.redirect is not None:
            if isinstance(self.redirect, Redirect) == False:
                raise ValueError("You tried to give a non-redirect object to response")
            self.response = None
            self.status_code = self.redirect.status_code

    def attach_user(self, user_object):
        pass

    def add_header(self, header, value):
        self.headers[header] = value

    def add_cookie(self, cookie_object=Cookie_Object):
        self.cookies.append(cookie_object)

    def format(self):
        if self.file_object is not None:
            self.response = self.file_object.data
            if self.file_object.client_download_on_receive:
                self.headers["content-disposition"] = 'attachment; filename="' + self.file_object.file_name + '"'
            self.headers["content-type"] = self.file_object.mimetype
            if self.gzip == False:
                self.headers["content-transfer-encoding"] = "binary"
            else:
                self.headers['content-transfer-encoding'] = "gzip"
        elif self.redirect is not None:
            if isinstance(self.redirect, Redirect) == False:
                raise ValueError("You tried to give a non-redirect object to response")
            for header in self.redirect.headers:
                self.add_header(header, self.redirect.headers[header])
            for cookie in self.redirect.cookies:
                self.add_cookie(cookie)

        if self.response is None:
            self.response = b""

        self.headers["content-length"] = len(self.response)
        formatted = []

        for header in self.headers:
            formatted.append(str(header) + ": " + str(self.headers[header]).format(current_time=time.strftime("%a, %d %b %Y %H:%M:%S GMT", time.gmtime())))
        if self.access_control_allow_origin is not None:
            formatted.append("access_control_allow_origin: " + self.access_control_allow_origin)

        if self.content_type is not None:
            formatted.append("content-type: " + self.content_type)

        for cookie in self.cookies:
            formatted.append(cookie.__prep__())
        
        if self.response_type == type(""):
            self.response = self.response.encode()
        elif self.response_type == type({}) or self.response_type == type([]):
            self.response = json.dumps(self.response)

        if self.gzip:
            comp = zlib.compress(self.response)
            print(comp)
            return Error_Codes.Get_Response_Line(self.status_code).encode() + b"\r\n", ("\r\n".join(formatted)).encode() + b"\r\n\r\n" + comp + b"\r\n\r\n"

        else:
            return Error_Codes.Get_Response_Line(self.status_code).encode() + b"\r\n", (("\r\n".join(formatted)).encode() + b"\r\n\r\n" + self.response + b"\r\n\r\n")

class Error_Codes(object):
    CODES = {"100": "Continue", "101": "Switching Protocols", "102": "Processing", "103": "Early Hints", "200": "OK", "201": "Created", "202": "Accepted", "203": "Non-Authoritative Information", "204": "No Content", "205": "Reset Content", "206": "Partial Content", "207": "Multi-Status", "208": "Already Reported", "226": "IM Used", "300": "Multiple Choices", "301": "Moved Permanently", "302": "Found", "303": "See Other", "304": "Not Modified", "305": "Use Proxy", "307": "Temporary Redirect", "308": "Permanent Redirect", "400": "Bad Request", "401": "Unauthorized", "402": "Payment Required", "403": "Forbidden", "404": "Not Found", "405": "Method Not Allowed", "406": "Not Acceptable", "407": "Proxy Authentication Required", "408": "Request Timeout", "409": "Conflict", "410": "Gone", "411": "Length Required", "412": "Precondition Failed", "413": "Payload Too Large", "414": "URI Too Long", "415": "Unsupported Media Type", "416": "Range Not Satisfiable", "417": "Expectation Failed", "421": "Misdirected Request", "422": "Unprocessable Entity", "423": "Locked", "424": "Failed Dependency", "425": "Too Early", "426": "Upgrade Required", "428": "Precondition Required", "429": "Too Many Requests", "431": "Request Header Fields Too Large", "451": "Unavailable For Legal Reasons", "500": "Internal Server Error", "501": "Not Implemented", "502": "Bad Gateway", "503": "Service Unavailable", "504": "Gateway Timeout", "505": "HTTP Version Not Supported", "506": "Variant Also Negotiates", "507": "Insufficient Storage", "508": "Loop Detected", "510": "Not Extended", "511": "Network Authentication Required"}

    def Get_Response_Line(code):
        try:
            return  "HTTP/1.0 " + str(code) + " " + Error_Codes.CODES[str(code)]
        except:
            raise ValueError("Code not found")

class Discovery(object):

    def __init__(self, domain, block_list, server_ip="AUTO", server_ports=[80], broadcast_port=6256, broadcast_alive=True, broadcast_address="AUTO", discovery_data=None):
        self.domain = domain
        self.auto_broadcast_ip = network_ops.Get_All_IP_Stat()['ext'][0]['broadcast']
        self.auto_server_ip = network_ops.Get_IP()['ext'][0]
        self.broadcast_port = broadcast_port
        self.broadcast_alive = broadcast_alive
        self.block_list = block_list
        self.server_ip = server_ip
        self.server_ports = server_ports
        if type(self.server_ports) == type(""):
            self.server_ports = [self.server_ports]
        self.discovery_data = discovery_data

        if discovery_data == None:
            self.discovery_data = {
                "Mako": {
                    "domain": self.domain,
                    "ip": server_ip,
                    "ports": server_ports,
                    "block_list": block_list
                }
            }

        self.discovery_data = json.dumps(self.discovery_data)

        self.broadcast_address = broadcast_address

        if server_ip == "AUTO":
            server_ip = network_ops.Get_IP()['ext'][0]

        self.__broadcast_catcher__ = ds_broadcast.Discovery_Server(server_ip, broadcast_port, "Mako", self.discovery_data.encode())
        
        if broadcast_alive:
            threading.Thread(target=self.broadcast, daemon=True).start()

    def get_config(self):
        data = {
            "discovery_data": json.loads(self.discovery_data),
            "domain": self.domain,
            "block_list": self.block_list,
            "broadcast_port": self.broadcast_port,
            "broadcast_address": self.broadcast_address,
            "broadcast_alive": self.broadcast_alive
        }
        return data

    def broadcast(self):
        if self.broadcast_address == "AUTO":
            self.__connector__ = socket_ops.UDP_Connector(self.auto_broadcast_ip, self.broadcast_port)
        else:
            self.__connector__ = socket_ops.UDP_Connector(self.broadcast_address, self.broadcast_port)
        self.__connector__.send(self.discovery_data.encode())

class HTTP_Request(BaseHTTPRequestHandler):
    def __init__(self, server, request_text=b"", user_socket=None, addr=None):
        self.raw_request = request_text
        self.rfile = BytesIO(request_text)
        self.raw_requestline = self.rfile.readline()
        self.error_code = self.error_message = None
        self.parse_request()
        self.method = self.command
        self.client_socket = user_socket
        self.client_address = addr[0]
        path_args = urlsplit(self.path)
        self.query = parse_qs(path_args.query, keep_blank_values=True)
        self.args = self.query
        self.path = unquote(path_args.path)
        self.files = []
        self.form_data = {}
        self.json = None
        self.data = None
        self.cookies = Cookie_Jar()
        self.body = self.raw_body = request_text.split(b"\r\n\r\n", 1)[1]
        self.host = self.headers.get("host")

        if self.headers.get("mako_reverse_proxy"):
            pass
            # TODO Impliment this

        if self.headers.get("Cookie"):
            for cookie in self.headers.get("Cookie").split("; "):
                if server.advanced_user_system:
                    if cookie.split('=')[0] == "mako_did":
                        self.user_device = users.User_Device(cookie.split("=")[1], self.client_address)
                        self.user_device.new_log_entry(self.path)
                self.cookies.add_cookie(Cookie_Object(cookie.split('=')[0], cookie.split("=")[1]))

        if server.advanced_user_system:
            if self.cookies.get("mako_device") is None:
                did = None
            else:
                did = self.cookies.get("mako_device").value
            self.mako_device = users.User_Device(did, self.client_address)
            self.mako_device.new_log_entry(f"{str(datetime.datetime.now().timestamp()).ljust(17)} - [ {self.method} ] > {self.path}")

        if self.headers.get("Content-Type"):
            if "multipart/form-data" in self.headers.get("Content-Type"):
                self.__message_boundary__ = self.headers.get("Content-Type").split("; ")[1].split("=", 1)[1]
                self.message_parts = self.raw_body.split(b"--" + self.__message_boundary__.encode())
                for part in self.message_parts:
                    if b"filename" in part:
                        headers, body = part.split(b"\r\n\r\n")
                        if b'name="' in headers:
                            input_name = headers.split(b'name="')[1].split(b'"')[0].decode()
                        elif b"name='" in headers:
                            input_name = headers.split(b"name='")[1].split(b"'")[0].decode()
                        else:
                            input_name = None

                        if b'filename="' in headers:
                            file_name = headers.split(b'filename="')[1].split(b'"')[0].decode()
                        elif b"filename='" in headers:
                            file_name = headers.split(b"filename='")[1].split(b"'")[0].decode()
                        else:
                            file_name = None

                        file_object = File_Object(file_name=file_name, data=body, from_client=True)
                        file_object.header_data = headers.decode()
                        self.files.append(file_object)

                        if input_name and b"form-data" in headers:
                            self.form_data[input_name] = file_object
                    elif b"form-data" in part:
                        headers, body = part.split(b"\r\n\r\n")
                        if b'name="' in headers:
                            input_name = headers.split(b'name="')[1].split(b'"')[0].decode()
                        elif b"name='" in headers:
                            input_name = headers.split(b"name='")[1].split(b"'")[0].decode()
                        else:
                            input_name = None
                        self.form_data[input_name] = body.decode()[:-2]
            else:
                if len(self.raw_body) > 0:
                    try:
                        self.data = self.body.decode()
                    except:
                        self.data = self.raw_body
                    try:
                        if self.headers.get("Content-Type") == "application/x-www-form-urlencoded":
                            temp = self.data.split("&")
                            temp = [x.split("=") for x in temp]
                            self.form_data = {}
                            for item in temp:
                                self.form_data[unquote(item[0])] = unquote(item[1])
                    except:
                        pass

                    try:
                        self.json = json.loads(self.body)
                    except:
                        self.json = None
                    
    def get_file_from_form(self, input_name):
        file = File_Object

        if input_name not in self.form_data:
            raise ValueError("Couldn't find '" + input_name + "' in form data")
        else:
            file = self.form_data[input_name]
        
        return file
        
class Resolver(object):

    def __init__(self, urls=None, methods=["GET"], function=None, ignore_case=False):
        self.urls = urls
        self.function = function
        self.methods = methods
        self.ignore_case = ignore_case

        if type(self.urls) == type(""):
            path = self.urls
            if "**" in path:
                if path[-2:] != "**":
                    raise ValueError("** wildcard needs to be the last characters of the matching url")
                ending = ""
                path = path.replace("**", ".+")
            else:
                ending = "$"

            self.urls = path.replace("*", ".+") + ending
        elif type(self.urls) == type([]):
            urls = []
            for path in self.urls:
                if "**" in path:
                    if path[-2:] != "**":
                        raise ValueError("** wildcard needs to be the last characters of the matching url")
                    ending = ""
                    path = path.replace("**", ".+")
                else:
                    ending = "$"

                path = path.replace("*", ".+")
                urls.append(path + ending)

            self.urls = urls

    def check_match(self, request=HTTP_Request):
        if request.method not in self.methods:
            return False

        if type(self.urls) == type(""):
            if self.ignore_case:
                if re.match(self.urls, request.path.lower()):
                    return self.urls
            else:
                if re.match(self.urls, request.path):
                    return self.urls
        elif type(self.urls) == type([]):
            for path in self.urls:
                if self.ignore_case:
                    if re.match(path, request.path.lower()):
                        return path
                else:
                    if re.match(path, request.path):
                        return path
        
        return False

    def resolve(self, request=HTTP_Request):
        matching_url = self.check_match(request).replace(".+/", "*/").replace("/.+$", "/*").replace("/.+", "/**")
        req_parts = request.path.split("/")[1:]
        i = 0
        args = []
        for part in matching_url.split("/")[1:]:
            if part == "*":
                args.append(req_parts[i])
            if part == "**":
                args.append("/".join(req_parts[i:]))
            i += 1
        if len(args) == 0:
            try:
                return self.function(request)
            except:
                return self.function()
        else:
            try:
                return self.function(request, *args)
            except:
                return self.function(*args)

class Error_Resolver(object):

    def __init__(self, code, function):
        self.code = code
        self.function = function

    def check_match(self, code):
        return self.code == code

    def resolve(self, request=HTTP_Request):
        return self.function(request)

class Analytical_Data(object):

    def __init__(self, time_unit=Time_Units.SECONDS, server=None):
        self.start_time = datetime.datetime.now()
        self.request_count = 0
        self.request_times = []
        self.server = server

        self.average_time = 0

        self.url_times = {}
        self.__url_times__ = {}
        self.save_path = None
        self.save_every = None

        self.time_unit = time_unit
    
    @property 
    def get_config(self):
        data = {
            "auto_save": {
                "save_path": self.save_path,
                "save_every": self.save_every
            },
            "time_unit": self.time_unit
        }
        return data
    
    def build_from_config(self, data):
        self.time_unit = data['time_unit']
        if data['auto_save']:
            self.save_path = data['auto_save']['save_path']
            self.save_every = data['auto_save']['save_every']
            self.setup_autosave(self.save_every, self.save_path)
    
    def setup_autosave(self, every_X=time_events.EVERY_HOUR, save_path=None):
        if save_path == None:
            save_path = self.server.system_path + "/analytics/"

        os.makedirs(save_path, exist_ok=True)
        self.save_path = save_path
        self.save_every = every_X
        self.__event_listener__ = time_events.EventListener()
        self.__event_listener__.RegisterEvent(self.save_every, self.__merge__)

    @property
    def up_time(self):
        self.up_time = (datetime.datetime.now() - self.start_time)
    
    def add_time(self, time, url, method):
        self.request_count += 1
        self.request_times.append(time)
        self.average_time = sum(self.request_times)/len(self.request_times)*self.time_unit

        if url not in self.url_times:
            self.url_times[url]  = {}
            self.__url_times__[url] = {}
            self.__url_times__[url][method] = []

        self.__url_times__[url][method].append(time)
        self.url_times[url][method] = sum(self.__url_times__[url][method])/len(self.__url_times__[url][method])*self.time_unit

    def __merge__(self, _, time=datetime.datetime):
        if self.save_path is not None:
            self.save(self.save_path + datetime.datetime.now().strftime("SF-Mako_%y_%m_%d_%H_%M.json"))
        self.average_time = 0
        self.request_times = []
        self.request_count = 0
        self.url_times = {}
        self.__url_times__ = {}

    def save(self, path):
        os.makedirs(os.path.split(path)[0], exist_ok=True)
        data = {
            "Requests": self.request_count,
            "AverageResponseTime": self.average_time,
            "ResponseTimeByURL": self.url_times,
            "TimeUnit": self.time_unit
        }
        file_ops.write_json(path, data)

class HTTP_Server(object):

    def __init__(self, HOST="AUTO", PORTS=None, max_connections=5, favicon=None, use_analytics=False, ssl_context=None, buffer_size=16384):
        self.auto_ip = network_ops.Get_IP()['ext'][0]
        self.HOST = HOST
        self.PORTS = PORTS

        if type(self.PORTS) == type(""):
            self.PORTS = [self.PORTS]
        self.running = False
        self.max_connections = max_connections

        self.block_list = []
        self.resolvers = []
        self.error_resolvers = {}

        self.buffer_size = buffer_size
        self.socket_ttl = 10

        self.add_server_timing_header = False

        self.favicon = favicon
        self.discovery_server = None
        
        self.attempt_file_retrieval = False
        self.attempt_file_retrieval_directory = "."

        self.force_port = None

        self.ssl_context = ssl_context

        self.advanced_user_system = False

        if self.PORTS is None:
            if self.ssl_context is not None:
                self.PORTS = [443]
            else:
                self.PORTS = [80]

        self.__run_on_directory__ = False

        self.server_headers = {
            "date": "{current_time}"
        }
        

        # Diag Prints

        self.print_on_request = True
        self.print_on_request_format = "[ {resp_code} - {method} ] {addr[0]} > {path}"

        self.print_system_messages = False

        self.time_format = "%H:%M:%S"

        self.ssl_socket = None
        self.socket = None
        self.open_sockets = 0

        self.system_path = "mako_data"
        

        # ______ END

        if use_analytics:
            self.analytics = Analytical_Data(server=self)
        else:
            self.analytics = None

    def build_from_config(self, path=None):

        if path is None:
            path = self.system_path + "/SF_Mako_Config.json"

        data = file_ops.read_json(path)

        self.HOST = data['host']
        self.PORTS = data['ports']
        self.add_server_timing_header = data['add_server_timing_header']
        self.socket_ttl = data['socket_ttl']
        self.buffer_size = data['buffer_size']
        self.favicon = data['favicon']
        self.print_on_request = data['debug']['print_requests']['print_on_request']
        self.print_on_request_format = data['debug']['print_requests']['format']
        self.print_system_messages = data['debug']['system_messages']['print_system_messages']
        self.time_format = data['debug']['time_format']
        self.block_list = data['block_list']
        self.max_connections = data['max_connections']
        self.ssl_context = data['ssl_context']
        self.force_port = data['force_port']

        if self.ssl_context is not None:
            self.ssl_loaded_context = ssl.SSLContext.load_cert_chain(certfile=self.ssl_context, keyfile=self.ssl_context)

        if data['analytics']:
            self.analytics = Analytical_Data(server=self)
            self.analytics.build_from_config(data['analytics'])

        if data['discovery_server']:
            data['discovery_server']['block_list'] = self.block_list
            self.discovery_server = Discovery(**data['discovery_server'])

        if data['attempt_file_retrieval'] == "":
            data['attempt_file_retrieval'] = "."

        if data['attempt_file_retrieval']:
            self.attempt_file_retrieval = True
            self.attempt_file_retrieval_directory = data['attempt_file_retrieval']

    def save_config(self, path=None):
        data = {
            "host": self.HOST,
            "ports": self.PORTS,
            "favicon": self.favicon,
            "add_server_timing_header": self.add_server_timing_header,
            "buffer_size": self.buffer_size,
            "socket_ttl": self.socket_ttl,
            "debug": {
                "print_requests": {
                    "print_on_request": self.print_on_request,
                    "format": self.print_on_request_format
                },
                "system_messages": {
                    "print_system_messages": self.print_system_messages
                },
                "time_format": self.time_format
            },
            "block_list": self.block_list,
            "max_connections": self.max_connections,
            "server_headers": self.server_headers,
            "ssl_context": self.ssl_context,
            "force_port": self.force_port
        }

        if self.attempt_file_retrieval:
            data['attempt_file_retrieval'] = self.attempt_file_retrieval_directory
        else:
            data['attempt_file_retrieval'] = False

        if self.analytics is not None:
            data["analytics"] = self.analytics.get_config()
        else:
            data['analytics'] = False

        if self.discovery_server is not None:
            data["discovery_server"] = self.discovery_server.get_config()
        else:
            data['discovery_server'] = False

        if path is None:
            path = self.system_path + "/SF_Mako_Config.json"

        if ".json" not in path:
            path += ".json"
        file_ops.write_json(path, data)

    def run_discovery_server(self, domain, broadcast_port=6256, broadcast_alive=True, broadcast_address="AUTO"):
        self.discovery_server = Discovery(domain, self.block_list, self.HOST, self.PORTS, broadcast_port, broadcast_alive, broadcast_address)

    def add_analytics(self):
        self.analytics = Analytical_Data(server=self)

    def __system_message__(self, message):
        if self.print_system_messages:
            print("[", datetime.datetime.now().strftime(self.time_format), "] -", message)
    
    def __request_message__(self, method, addr, path, resp_code):
        if self.print_on_request:
            if resp_code == 200:
                resp_code = f"{colorama.Fore.GREEN}{resp_code}{colorama.Fore.RESET}"
            elif resp_code == 404:
                resp_code = f"{colorama.Fore.YELLOW}{resp_code}{colorama.Fore.RESET}"
            elif resp_code == 500:
                resp_code = f"{colorama.Fore.RED}{resp_code}{colorama.Fore.RESET}"
            elif resp_code == 302:
                resp_code = f"{colorama.Fore.YELLOW}{resp_code}{colorama.Fore.RESET}"
            elif resp_code == 301:
                resp_code = f"{colorama.Fore.BLUE}{resp_code}{colorama.Fore.RESET}"

            if method == "BLOCKED":
                method = f"{colorama.Fore.RED}{method}{colorama.Fore.RESET}"

            print("[", datetime.datetime.now().strftime(self.time_format), "] -", self.print_on_request_format.format(method=method, addr=addr, path=path, resp_code=resp_code))   

    def shutdown(self):
        self.socket.shutdown()
        self.running = False

    def add_resolver_direct(self, resolver=Resolver):
        for rslv in self.resolvers:
            if rslv.urls == resolver.urls and resolver.methods == rslv.methods:
                print("\n")
                raise ValueError("URL is already registered to another Resolver.")
        self.resolvers.append(resolver)

    def add_resolver(self, resolver=Resolver):
        def add_to_resolvers(func):
            resolver.function = func
            self.add_resolver_direct(resolver)
            return func
        return add_to_resolvers

    def add_error_resolver_direct(self, resolver=Error_Resolver):
        if resolver.code in self.error_resolvers:
            print("\n")
            raise ValueError("Error Code is already registered to another Resolver.")
        self.resolvers.append(resolver)

    def add_error_resolver(self, resolver=Error_Resolver):
        def add_to_error_resolvers(func):
            resolver.function = func
            self.add_error_resolver_direct(resolver)
            return func
        return add_to_error_resolvers

    def add_server_header(self, header, value):
        self.server_headers[header] = value

    def __broker__(self):
        
        self.__system_message__("Connection Broker Started")

        while self.running:
            try:
                user_socket, addr = self.socket.accept()
                if addr[0] in self.block_list:
                    user_socket.close()
                    self.__request_message__("BLOCKED", addr, "/", 511)
                    continue
                self.__system_message__("Connection Accepted: " + str(addr))
                threading.Thread(target=self.__client_responses__, args=[user_socket, addr], daemon=True).start()
            except:
                pass

    def __broker_Secure_(self):
        
        self.__system_message__("Secure Connection Broker Started")

        self.secure_socket = self.ssl_loaded_context.wrap_socket(self.ssl_socket, server_side=True)

        while self.running:
            try:
                user_socket, addr = self.secure_socket.accept()
                if addr[0] in self.block_list:
                    user_socket.close()
                    self.__request_message__("BLOCKED", addr, "/", 511)
                    continue
                self.__system_message__("Connection Accepted: " + str(addr))
                threading.Thread(target=self.__client_responses__, args=[user_socket, addr], daemon=True).start()
            except:
                pass

    def __find_resolver__(self, request):
        for resolver in self.resolvers:
            if resolver.check_match(request):
                return resolver
        return None

    def __add_server_headers_to_resp__(self, resp=Response, request=HTTP_Request):
        if self.advanced_user_system:
            exp = (datetime.datetime.utcnow() + datetime.timedelta(days=365)).strftime("%a, %d %b %Y %H:%M:%S GMT")
            resp.add_cookie(cookie_object=Cookie_Object("mako_device", request.mako_device.DID, exp))
        for header in self.server_headers:
            resp.add_header(header, self.server_headers[header])

    def __client_responses__(self, user_socket=socket_ops.socket.socket, addr=None):

        user_socket.settimeout(0.1)
        self.open_sockets += 1
        socket_opened = TimeStamp()

        code = None
        resp = None

        time_start = TimeStamp()

        while True:
            timing_start = None
            dl_time = None
            if self.add_server_timing_header:
                timing_start = TimeStamp()

            data = b""
            do_end = False
            while True:
                try:
                    temp = user_socket.recv(self.buffer_size)
                except Exception as e:
                    temp = b""

                if temp != b"":
                    data += temp
                else:
                    if data != b"":
                        break
                    else:
                        time.sleep(0.25)
                        if TimeStamp() - socket_opened >= self.socket_ttl:
                            print(self.socket_ttl, TimeStamp() - socket_opened)
                            print("TTL Exceeded. Closing this socket")
                            do_end = True
                            break

            if do_end or data == b"":
                user_socket.shutdown(socket_ops.socket.SHUT_RDWR)
                user_socket.close()
                self.open_sockets -= 1
                return

            # _______________________ PROCESS AN ACTUAL REQUEST

            if self.add_server_timing_header:
                dl_time = TimeStamp()
                dl_time = f'RX;dur={(dl_time - timing_start)*1000};desc="Download Request Time"'
                timing_start = TimeStamp()

            request = HTTP_Request(self, data, user_socket, addr)  # Convert bytes to HTTP Request

            keep_alive = False

            

            # CHECK IF THEY WANT THE FAVICON
            if request.path in ['/favicon.ico', '/apple-touch-icon.png', '/favicon'] and self.favicon is not None:
                resp = Response(file_object=File_Object(file_path=self.favicon))
                self.__request_message__(request.method, addr, request.path, resp.status_code)
                self.__add_server_headers_to_resp__(resp, request)
                if self.add_server_timing_header:
                    rsp_time = TimeStamp()
                    rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                    del timing_start
                    resp.add_header("Server-Timing", dl_time + ", " + rsp_time)

                if keep_alive:
                    resp.add_header("Keep-Alive", f"timeout={self.socket_ttl}, max=4")

                code, resp = resp.format()

                if keep_alive:
                    continue
                else:
                    break

            if self.__run_on_directory__ == False:
                # Normal Server

                resolver = self.__find_resolver__(request)      # Find the function the request calls for
                if resolver is None:                            # If it doesnt exist, 
                    if self.attempt_file_retrieval:             # Check to see if we are allowed to pull files
                        req_path = os.path.join(self.attempt_file_retrieval_directory, request.path[1:])
                        if os.path.isfile(req_path):
                            resp = Response(file_object=File_Object(req_path))
                            self.__add_server_headers_to_resp__(resp, request)
                            self.__request_message__(request.method, addr, request.path, resp.status_code)
                            if self.add_server_timing_header:
                                rsp_time = TimeStamp()
                                rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                                del timing_start
                                resp.add_header("Server-Timing", dl_time + ", " + rsp_time)
                            if keep_alive:
                                resp.add_header("Keep-Alive", f"timeout={self.socket_ttl}, max=4")
                            
                            code, resp = resp.format()

                            if keep_alive:
                                continue
                            else:
                                break
                    resp = Response("", 404)
                    if self.add_server_timing_header:
                        rsp_time = TimeStamp()
                        rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                        del timing_start
                        resp.add_header("Server-Timing", dl_time + ", " + rsp_time)
                    if keep_alive:
                        resp.add_header("Keep-Alive", f"timeout={self.socket_ttl}, max=4")
                    self.__request_message__(request.method, addr, request.path, 404)

                    code, resp = resp.format()

                    if keep_alive:
                        continue
                    else:
                        break

                resp = resolver.resolve(request)

                if isinstance(resp, Response):
                    if resp.ignore_and_drop:
                        user_socket.close()
                        return
                    else:
                        code, resp = resp.format()

                        if keep_alive:
                            continue
                        else:
                            break
                elif resp is None:
                    print(f"\n{colorama.Fore.RED}WARNING: You have enrolled a resolver that did not return anything.{colorama.Fore.RESET} Function:", str(resolver.function.__name__))
                    self.__request_message__(request.method, addr, request.path, 500)
                    resp = Response("", 500)
                    if self.add_server_timing_header:
                        rsp_time = TimeStamp()
                        rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                        del timing_start
                        resp.add_header("Server-Timing", dl_time + ", " + rsp_time)
                    
                    code, resp = resp.format()

                    if keep_alive:
                        continue
                    else:
                        break

                elif type(resp) == type("") or type(resp) == type(1):
                    resp = Response(str(resp))
                elif type(resp) == type([]) or type(resp) == type({}):
                    resp = Response(json.dumps(resp))
                elif isinstance(resp, File_Object):
                    resp = Response(file_object=resp)
                elif isinstance(resp, Redirect):
                    resp = Response(redirect=resp)

                self.__add_server_headers_to_resp__(resp, request)
                self.__request_message__(request.method, addr, request.path, resp.status_code)
                if self.add_server_timing_header:
                    rsp_time = TimeStamp()
                    rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                    del timing_start
                    resp.add_header("Server-Timing", dl_time + ", " + rsp_time)

                code, resp = resp.format()

                if keep_alive:
                    continue
                else:
                    break
            else:
                # FTP like server
                if ":" in request.path or "//" in request.path:
                    resp = Response(status_code=404)
                    self.__add_server_headers_to_resp__(resp, request)
                    self.__request_message__(request.method, addr, request.path, 404)
                    if self.add_server_timing_header:
                        rsp_time = TimeStamp()
                        rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                        del timing_start
                        resp.add_header("Server-Timing", dl_time + ", " + rsp_time)

                    code, resp = resp.format()

                    if keep_alive:
                        continue
                    else:
                        break

                req_path = os.path.join(self.directory, request.path[1:])
                if os.path.exists(req_path):
                    if os.path.isdir(req_path):
                        try:
                            files = os.listdir(req_path)
                        except:
                            resp = "<html><body><h1>No Files or Folders Found</h1><a href='/'>Return Home</a></body></html>"
                            resp = Response(resp)
                            self.__add_server_headers_to_resp__(resp, request)
                            if self.add_server_timing_header:
                                rsp_time = TimeStamp()
                                rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                                del timing_start
                                resp.add_header("Server-Timing", dl_time + ", " + rsp_time)

                            self.__request_message__(request.method, addr, request.path, 404)

                            code, resp = resp.format()

                            if keep_alive:
                                continue
                            else:
                                break

                        resp = "<html><body><h1>Files/Folders in this Directory</h1>"
                        dirs = []
                        a_files = []
                        for file in files:
                            if os.path.isdir(os.path.join(req_path, file)):
                                dirs.append(f"<span class='folder'><b>Folder</b>: <a href='{os.path.join(request.path, file)}'>{file}</a><br></span>")
                            else:
                                a_files.append(f"<span class='file'><b>File</b>: <a href='{os.path.join(request.path, file)}'>{file}</a><br></span>")
                        dirs.sort()
                        a_files.sort()
                        resp += "".join(dirs) + "".join(a_files)
                        resp += "</body></html>"

                        resp = Response(resp)
                        self.__add_server_headers_to_resp__(resp, request)
                        if self.add_server_timing_header:
                            rsp_time = TimeStamp()
                            rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                            del timing_start
                            resp.add_header("Server-Timing", dl_time + ", " + rsp_time)

                        self.__request_message__(request.method, addr, request.path, 200)

                        code, resp = resp.format()

                        if keep_alive:
                            continue
                        else:
                            break
                    else:
                        self.__request_message__(request.method, addr, request.path, 200)
                        resp = Response(file_object=File_Object(req_path))
                        self.__add_server_headers_to_resp__(resp, request)
                        if self.add_server_timing_header:
                            rsp_time = TimeStamp()
                            rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                            del timing_start
                            resp.add_header("Server-Timing", dl_time + ", " + rsp_time)
                        
                        code, resp = resp.format()

                        if keep_alive:
                            continue
                        else:
                            break
                else:
                    resp = Response(status_code=404)
                    
                    self.__add_server_headers_to_resp__(resp, request)
                    self.__request_message__(request.method, addr, request.path, 404)
                    if self.add_server_timing_header:
                        rsp_time = TimeStamp()
                        rsp_time = f'Resp;dur={(rsp_time - timing_start)*1000};desc="How long it took to create a response and send it"'
                        del timing_start
                        resp.add_header("Server-Timing", dl_time + ", " + rsp_time)
                    
                    code, resp = resp.format()
                    
                    if keep_alive:
                        continue
                    else:
                        break

        if self.analytics is not None:
            self.analytics.add_time(TimeStamp() - time_start, request.path, request.method)

        try:
            user_socket.sendall(code)
            time.sleep(0.25)
            user_socket.sendall(resp)
        except ConnectionAbortedError:
            pass

        try:
            user_socket.shutdown(socket_ops.socket.SHUT_RDWR)
            user_socket.close()
        except:
            pass
        
        self.__system_message__("Connection Closed: " + str(addr))
        self.open_sockets -= 1
        return

    def __run_nonssl__(self, HOST=None, PORT=80):

        self.__system_message__("Building HTTP Server")

        if HOST is not None:
            self.HOST = HOST

        if self.HOST == "AUTO":
            host = self.auto_ip
        else:
            host = self.HOST

        if len(self.resolvers) == 0 and self.__run_on_directory__ == False:
            raise ValueError("You did not add any resolvers. Help: server.add_resolver(Resolvers('/', function))")

        self.running = True

        self.__system_message__("Building Socket Server")
        self.socket = socket_ops.HostServer(host, PORT, self.max_connections)
        self.__system_message__("Build Complete - Server Hosting URL: http://" + host + ":" + str(PORT))
        threading.Thread(target=self.__broker__, daemon=True).start()

    def __run_ssl__(self, HOST=None, PORT=443):
        if self.ssl_context is None:
            raise AttributeError("Server missing .pem context.")

        self.__system_message__("Building HTTP and HTTPS Server")

        if HOST is not None:
            self.HOST = HOST

        if self.HOST == "AUTO":
            host = self.auto_ip
        else:
            host = self.HOST

        if len(self.resolvers) == 0 and self.__run_on_directory__ == False:
            raise ValueError("You did not add any resolvers. Help: server.add_resolver(Resolvers('/', function))")

        self.running = True


        self.__system_message__("Building SSL Socket Server")
        self.ssl_loaded_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        self.ssl_loaded_context.load_cert_chain(certfile=self.ssl_context, keyfile=self.ssl_context)

        self.ssl_socket = socket_ops.HostServer(host, PORT, self.max_connections)
        self.__system_message__("Secure Build Complete - SSL Server Hosting URL: https://" + host + ":" + str(PORT))
        threading.Thread(target=self.__broker_Secure_, daemon=True).start()

    def run(self, HOST=None, PORTS=None, loop=False):
        self.__system_message__("Building HTTP Server")

        if self.advanced_user_system:
            from .. import users

        os.makedirs(self.system_path, exist_ok=True)

        if HOST is not None:
            self.HOST = HOST
        if PORTS is not None:
            self.PORTS = PORTS

        if type(self.PORTS) == type(""):
            self.PORTS = [self.PORTS]
        elif type(self.PORTS) == type(8):
            self.PORTS = [self.PORTS]

        if self.HOST == "AUTO":
            host = self.auto_ip
        else:
            host = self.HOST

        if len(self.resolvers) == 0:
            raise ValueError("You did not add any resolvers. Help: server.add_resolver(Resolvers('/', function))")

        
        for port in self.PORTS:
            if type(port) == type([]):
                port, ssl = port
                if ssl:
                    self.__run_ssl__(host, port)
                else:
                    self.__run_nonssl__(host, port)
            else:
                if port == 443:
                    self.__run_ssl__(host, port)
                else:
                    self.__run_nonssl__(host, port)

        if loop:
            while self.running:
                time.sleep(10)

    def run_on_directory(self, directory, HOST=None, PORTS=None, loop=False):
        if HOST is not None:
            self.HOST = HOST
        if PORTS is not None:
            self.PORTS = PORTS

        if type(self.PORTS) == type(""):
            self.PORTS = [self.PORTS]

        if self.HOST == "AUTO":
            host = self.auto_ip
        else:
            host = self.HOST


        self.directory = os.path.abspath(directory)

        if os.path.exists(self.directory) == False:
            raise NotADirectoryError("This directory doesn't exist")

        self.__run_on_directory__ = True

        self.running = True

        for port in self.PORTS:
            if type(port) == type([]):
                port, ssl = port
                if ssl:
                    self.__run_ssl__(host, port)
                else:
                    self.__run_nonssl__(host, port)
            else:
                if port == 443:
                    self.__run_ssl__(host, port)
                else:
                    self.__run_nonssl__(host, port)
        
        if loop:
            while True:
                time.sleep(10)

    def shutdown(self):
        self.running = False
        self.socket.shutdown()
        self.ssl_socket.shutdown()
        


#  How Mako Works
#  Process         Client (browser) > Server - 192.168.0.3 > client_socket > Resolver > Usercode > Response > Resolver > client_socket > Client (browser)

