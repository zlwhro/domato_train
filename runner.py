import http.server
import urllib.parse
import sys
from pathlib import Path
sys.path.append('/home/hoon/runner/domato')
from domato.generator import generate_samples

output_dir = str(Path(__file__).resolve().parent)+"/generated"

class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        query_params = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        path  = urllib.parse.urlparse(self.path).path

        if path == "/runner":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("runner.html",'rb') as f:
                self.wfile.write(f.read())

        elif path == "/generate":
            with open("domato/template.html","r") as f:
                template = f.read()
            outfile = f"{output_dir}/sample.html"
            out = query_params.get('outfile')[0]
            if(out):
                outfile = f"{output_dir}/{out}"
            else:
                out = "sample.html"
            generate_samples(template, [outfile])
            self.send_response(302)
            self.send_header('Location', f"/generated/{out}")
            self.end_headers()
            

        elif path.startswith("/generated/"):
            file_name = output_dir + '/' +path[len('/generated/'):]
            if(Path.exists(Path(file_name))):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                with open(file_name,'rb') as f:
                    self.wfile.write(f.read())
            else:
                self.send_response(404)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(b"file not found")

        elif path == "/usage":
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            with open("usage.html",'rb') as f:
                self.wfile.write(f.read())

if __name__ == "__main__":
    if not Path.exists(Path(output_dir)):
        Path.mkdir(Path(output_dir))
    server = http.server.HTTPServer(('localhost', 8000), MyHandler)
    print("Server started at http://localhost:8000")
    server.serve_forever()