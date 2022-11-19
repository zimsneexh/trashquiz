from http.server import BaseHTTPRequestHandler, HTTPServer
from log import blog

import cgi
import os
import traceback


#
# Registered HTTP endpoints
#
endpoint_register = [ ]
endpoint_post_register = [ ]

#
# Register API endpoint
#
def register_endpoint(endpoint):
    blog.info("Registered endpoint for path: {}".format(endpoint.path))
    endpoint_register.append(endpoint)

def register_post_endpoint(endpoint):
    blog.info("Registered POST endpoint for path: {}".format(endpoint.path))
    endpoint_post_register.append(endpoint)

#
# Remove API endpoint
#
def remove_endpoint(endpoint):
    endpoint_register.remove(endpoint)

def remove_post_endpoint(endpoint):
    endpoint_post_register.remove(endpoint)

#
# Web Server class
#
class web_server(BaseHTTPRequestHandler):

    
    # send html lol
    def send_html(self, file, file_len):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        while True:
            bytes_read = file.read(4096)

            if(not bytes_read):
                break

            self.wfile.write(bytes_read)

    # send a file response to the current http handler
    def send_file(self, file, file_len):
        self.send_response(200)
        self.send_header("Content-type", "application/octet-stream")
        self.send_header("Content-Length", file_len)
        self.end_headers()

        while True:
            bytes_read = file.read(4096)

            if(not bytes_read):
                break

            self.wfile.write(bytes_read)


    # send generic malformed request response
    def generic_malformed_request(self):
        self.send_response(400)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.write_answer_encoded("Request zur sau")

    # send a raw string without wrapping it in a webresponse object 
    def send_str_raw(self, http_status, msg):
        self.send_response(http_status)
        self.send_header("Content-type", "text/html")
        self.end_headers()

        self.write_answer_encoded(msg)

    # pass httpserver log messages to blog
    def log_message(self, format, *args):
        blog.info("[http-server] {}".format(*args))

    # utility to encode and send a message to the current http handler
    def write_answer_encoded(self, message):
        blog.info("Sending message: {}".format(message))
        self.wfile.write(bytes(message, "utf-8"))

    # add CORS if needed
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', "*")
        self.send_header('Access-Control-Allow-Methods', "*")
        self.send_header('Access-Control-Allow-Headers', "*")
        return super(web_server, self).end_headers()

    # 
    # handle the get request
    #
    def do_GET(self):
        blog.web_log("Handling API-get request from {}..".format(self.client_address))

        # strip /
        self.path = self.path[1:len(self.path)]        

        form_dict = None
        real_path = "" 

        if(self.path):
            # if char 0 is ? we have form data to parse
            if(self.path[0] == '?' and len(self.path) > 1):
                form_dict = parse_form_data(self.path[1:len(self.path)])
                if(not form_dict is None):
                    real_path = list(form_dict.keys())[0]
            else:
                real_path = self.path
        else:
            real_path = self.path

        for endpoint in endpoint_register:
            if(endpoint.path == real_path):
                # handle
                try:
                    endpoint.handlerfunc(self, form_dict)
                    return
                except Exception as ex:
                    blog.warn("Exception raised in endpoint function for {}: {}".format(real_path, ex))
                    blog.warn("Errors from the webserver are not fatal to the quizserver lol.")
                    blog.warn("Connection reset.")
                    
                    traceback.print_exc()
                    return
       
        self.generic_malformed_request()        
        return

    #
    # handle a post request
    #
    def do_POST(self):
        blog.web_log("Handling API-post request from {}..".format(self.client_address))

        # strip /
        self.path = self.path[1:len(self.path)]        

        form_dict = None
        real_path = "" 

        if(self.path):
            # if char 0 is ? we have form data to parse
            if(self.path[0] == '?' and len(self.path) > 1):
                form_dict = parse_form_data(self.path[1:len(self.path)])
                if(not form_dict is None):
                    real_path = list(form_dict.keys())[0]
            else:
                real_path = self.path
        else:
            real_path = self.path

       
        if(self.headers["Content-Length"] is None):
            blog.info("Empty post body received.")
            self.generic_malformed_request()
            return

        form = cgi.FieldStorage(
            fp=self.rfile,
            headers=self.headers,
            environ={'REQUEST_METHOD':'POST',
                 'CONTENT_TYPE':self.headers['Content-Type']
            }
        )

        post_data = {}
        for f_obj in form.list:
            post_data[f_obj.name] = f_obj.value
        
        for endpoint in endpoint_post_register:
            if(endpoint.path == real_path):
                # handle
                try:
                    endpoint.handlerfunc(self, form_dict, post_data)
                    return
                except Exception as ex:
                    blog.warn("Exception raised in endpoint function for {}: {}".format(real_path, ex))
                    blog.warn("Errors from the webserver are not fatal to the quizserver lol.")
                    blog.warn("Connection reset.")
                    
                    traceback.print_exc()

                    return
        self.generic_malformed_request()
        return 


def parse_form_data(str_form):
    form_val = str_form.split("&")

    _dict = { }

    for dataset in form_val:
        split = dataset.split("=")
        if(not "=" in dataset):
            continue

        key = split[0]
        val = split[1]
        
        val = val.replace("+", " ")

        _dict[key] = val

    return _dict


def start_web_server(hostname, serverport):
    web_serv = None
    
    try:
        web_serv = HTTPServer((hostname, serverport), web_server)
    except Exception as ex:
        blog.error("Webserver failed to initialize: {}".format(ex))
        blog.error("Thread exiting.")
        return

    # We don't handle keyboardInterrupt for the webserver,
    # it's killed once the main thread exits
    try:
        web_serv.serve_forever()
    except KeyboardInterrupt:
        web_serv.server_close()
