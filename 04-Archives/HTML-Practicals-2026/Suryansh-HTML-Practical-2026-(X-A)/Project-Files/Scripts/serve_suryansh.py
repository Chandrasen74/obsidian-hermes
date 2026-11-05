# Local file server for the Suryansh practical archive: the phone auto-downloads
# the PDF when the URL is opened (Content-Disposition: attachment on .pdf, and
# "/" redirects straight to the PDF). Run:  python serve_suryansh.py
# Portable: paths are derived from this script's location in the archive.
import http.server
import os
import socketserver

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))  # archive root
PDF = "/Output/Grade_10_HTML_Practical_File_with_outputs.pdf"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kw):
        super().__init__(*args, directory=ROOT, **kw)

    def do_GET(self):
        if self.path in ("", "/"):
            self.send_response(302)
            self.send_header("Location", PDF)
            self.end_headers()
            return
        super().do_GET()

    def end_headers(self):
        if self.path.lower().split("?")[0].rstrip("/").endswith(".pdf"):
            self.send_header("Content-Disposition",
                             'attachment; filename="Suryansh_HTML_Practical_File.pdf"')
        super().end_headers()


socketserver.ThreadingTCPServer.allow_reuse_address = True
with socketserver.ThreadingTCPServer(("0.0.0.0", 8890), Handler) as httpd:
    print("serving", ROOT, "on 0.0.0.0:8890")
    httpd.serve_forever()
