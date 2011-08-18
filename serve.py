import check
import SimpleHTTPServer
import SocketServer

PORT = 8000

class Proxy(SimpleHTTPServer.SimpleHTTPRequestHandler):
    def do_GET(self):
        try:
            url = 'http://' + self.path[1:]
            check.dash(url)
            self.send_response(200)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write("it works")
        except Exception, e:
            self.send_response(500)
            self.send_header('Content-type','text/plain')
            self.end_headers()
            self.wfile.write("Error: %s" % e)

httpd = SocketServer.ForkingTCPServer(("", PORT), Proxy)

print "serving at port", PORT
httpd.serve_forever()

