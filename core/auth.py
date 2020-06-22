
import http.server
import socketserver


class Authenticator:

    authenticator = None
    login_url = "localhost:8000"

    def start_login_process():
        if(Authenticator.authenticator == None):
            Authenticator.authenticator = Authenticator()
        auth = Authenticator.authenticator

        #TODO: Start the server on a different thread, and send responses
        #back to the main thread so it can interact with the rest of blender
        #authenticator.setup_server()
        


    def __init__(self):
        pass

    def setup_server(self):
        PORT = 8000

        Handler = http.server.SimpleHTTPRequestHandler
        self.httpd = socketserver.TCPServer(("", PORT), Handler)
        print("serving at port", PORT)
        self.httpd.serve_forever()

    def shutdown_server(self):
        self.httpd.shutdown()

    #For use with with statement
    def __enter__(self):
        return self
    
    #For use with with statement
    def __exit__(self, type, value, traceback):
        self.httpd.shutdown()

    