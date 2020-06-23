
import http.server
import socketserver


import http.server
import json
import requests
import socketserver
import threading
import time

PORT = 41669
HTML = """
<!DOCTYPE html>
<html>

<head>
    <title>
        Blender Stats Login
    </title>
</head>

<body style = "text-align:center;">
    <p id="status">Setting up...</p>

    <script>
        window.onload = function() {
            var cognitoToken = {};
            urlFragment = window.location.hash.replace(/^#/,"");
            fragments = urlFragment.split("&");
            for (i = 0; i < fragments.length; i++) {
                s = fragments[i].split("=");
                cognitoToken[s[0]] = s[1];
            }
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 201) {
                    document.getElementById("status").innerHTML = "You can close this tab!";
                }
            };
            xhttp.open("PUT", "", true);
            xhttp.send(JSON.stringify(cognitoToken));
        }
    </script>
</body>

</html>"""


def MakeHandler(cognito):
    class Handler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            return

        def do_GET(self):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(str.encode(HTML))
            return

        def do_PUT(self):
            content_len = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_len)
            cognito["token"] = body
            self.send_response(201)
            self.end_headers()

            return
    return Handler


class Authenticator:

    login_url = "https://blender-stats-staging.auth.ap-southeast-2.amazoncognito.com/login?response_type=token&client_id=5guehm086k0ur6mb59spbovuqv&redirect_uri=http://localhost:" + \
        str(PORT)

    def start_login_process(self, cognito):
        self.httpd = http.server.HTTPServer(("", PORT), MakeHandler(cognito))
        thread = threading.Thread(target=self.httpd.serve_forever)
        thread.daemon = True
        thread.start()
        return self.httpd

    def __init__(self):
        self.httpd = None

    def shutdown_server(self):
        self.httpd.shutdown()

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.httpd.shutdown()
