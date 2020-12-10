
import http.server
import socketserver


import http.server
import json
import requests
import socketserver
import threading
import time
from datetime import datetime, timedelta

from ..logger import Logger

COGNITO_ENDPOINT = "https://blender-stats-staging.auth.ap-southeast-2.amazoncognito.com"
COGNITO_CLIENT_ID = "5guehm086k0ur6mb59spbovuqv"
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
        function getParameterByName(name, url = window.location.href) {
            name = name.replace(/[\[\]]/g, '\\$&');
            var regex = new RegExp('[?&]' + name + '(=([^&#]*)|&|#|$)'),
                results = regex.exec(url);
            if (!results) return null;
            if (!results[2]) return '';
            return decodeURIComponent(results[2].replace(/\+/g, ' '));
        }

        window.onload = function() {
            var code = getParameterByName('code');
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 201) {
                    document.getElementById("status").innerHTML = "You can close this tab!";
                }
            };
            xhttp.open("PUT", "", true);
            xhttp.send(JSON.stringify({code}));
            console.log(code);
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
            logger = Logger()

            content_len = int(self.headers.get('Content-Length'))
            body = self.rfile.read(content_len)

            cognito_code = json.loads(body)
            code = cognito_code["code"]
            logger.debug("code: {}".format(code))
            oauth_url = "{}/oauth2/token?grant_type=authorization_code&code={}&redirect_uri=http://localhost:{}&client_id={}".format(
                COGNITO_ENDPOINT, code, PORT, COGNITO_CLIENT_ID)
            x = requests.post(oauth_url,  headers={
                              "Content-Type": "application/x-www-form-urlencoded"})
            logger.debug("response: {}".format(x.text))

            response = json.loads(x.text)
            response["expiration_date"] = datetime.now(
            ) + timedelta(seconds=response["expires_in"])

            cognito["tokens"] = response
            self.send_response(201)
            self.end_headers()

            return
    return Handler


class Authenticator:

    login_url = "{}/login?response_type=code&client_id={}&redirect_uri=http://localhost:{}".format(
        COGNITO_ENDPOINT, COGNITO_CLIENT_ID, PORT)

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
