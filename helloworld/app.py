from http.server import BaseHTTPRequestHandler, HTTPServer


class HelloWorldHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        message = "Hello, World!"
        self.wfile.write(bytes(message, "utf8"))
        return

def run():
  server_address = ('', 8000)
  httpd = HTTPServer(server_address, HelloWorldHandler)
  print('Running server...')
  httpd.serve_forever()

run()