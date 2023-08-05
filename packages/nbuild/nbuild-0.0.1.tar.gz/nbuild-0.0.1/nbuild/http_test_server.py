
"""
The http_test_server module holds an HTTP
server capable of accepting Deliverables
and producing reports from them.
"""

from functools import partial
from http.server import BaseHTTPRequestHandler, HTTPServer
from datetime import datetime

# Parts inspired from https://www.schemecolor.com/navy-combat-uniform-pattern-colors.php
SERVER_CSS_STYLE = """
html, body {
  background-color: #e0e0e0;
  color: #020202;
}
fieldset {
  margin-bottom: 40pt;
}
fieldset, legend {
  background-color: #fefefe;
  border: 1px solid black;
}
legend {
  padding: 4pt 8pt;
  border-bottom-width: 0px;
  font-weight: bold;
}
#last_report {
  width: 100%;
  min-height: 300pt;
  border: 1px solid black;
}
"""

class Server(BaseHTTPRequestHandler):
    """
    This is not _technically_ the server, it is an HTTP request handler which
    performs tasks on POST/GET requests. This means self.* data will
    not persist from one GET to the next GET request.
    """
    def __init__(self, project, *args, **kwargs):
        print("Server __init__")
        self.project = project
        self.deliverables_form = None
        self.last_report_html = "No reports generated."
        super().__init__(*args, **kwargs)

    def _reply_with_html(self, html, code=200):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.send_header('Cache-Control', 'no-cche, no-store, must-revalidate')
        self.send_header('Expires', '0')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))

    def do_GET(self): # pylint: disable=invalid-name
        """Handles HTTP get requests and serves .html/.js/.css data"""
        path = self.path.lower()
        if path == "/" or path == "/index.html" or "index.html" in path:
            self._reply_with_html("""<DOCTYPE html>
<html>
  <head>
    <title>{name} Test Portal</title>
    <style>{css}</style>
  </head>
  <body>
    <h2>{name} Test Portal</h2>
    
    <fieldset>
      <legend>Upload Deliverables</legend>
      <form action="upload-deliverables" method="POST" enctype="multipart/form-data">
        {deliverables_form}
        <input type="submit" value="Upload">
      </form>
    </fieldset>

    <fieldset>
      <legend>Last Report</legend>
      <a href="last-report.html" target="_blank">Open report in new tab</a><br>
      <iframe id="last_report" src="last-report.html"></iframe>
    </fieldset>

  </body>
</html>""".format(
                name=self.project.name,
                css=SERVER_CSS_STYLE,
                deliverables_form=self.get_deliverables_form()
            ))

        elif path == "/last-report.html" or "last-report.html" in path:
            self._reply_with_html(self.last_report_html)

        else:
            self._reply_with_html("""<h1>404 Not Found</h1>
            """, code=404)

    def do_POST(self): # pylint: disable=invalid-name
        """Handles HTTP post requests and records form submissions"""
        content_length = abs( int(self.headers['Content-Length']) )
        # Do not accept files > 1gb large (small security check we can bump later)
        if content_length > 1_200_000_000:
            self._reply_with_html("Error, current upload limit is 1,200,000,000 bytes (approx. 1gb), you sent {} bytes.".format(content_length), code=413)
            return
        
        post_data = self.rfile.read(content_length)
        
        path = self.path.lower()
        if "upload-deliverables" in path:
            self.process_deliverables(post_data)
            self._reply_with_html("""<h2>Deliverable received</h2>
              <p>Return to the previous page to read report. Note that for large projects reports may take 3-4 minutes to generate.</p>
              <p>You may also <a href="last-report.html">open the report directly using this link</a>.</p>
            """) # TO DO can we predict time?



    def process_deliverables(self, post_data):
        """Given some uploaded deliverables, start a test and save report data"""
        self.last_report_html = "TODO report generated at {} ({})".format( datetime.now(), post_data )

    def get_deliverables_form(self):
        """
        Given self.project, create a suitable form to receive deliverables with
        (eg .zip upload, .exe upload, checkbox that physical goods were dropped off)
        """
        if self.deliverables_form:
            return self.deliverables_form

        if self.project.deliverables_in._type == "directory":
            # Build form to upload .zip / .tar file
            self.deliverables_form = """
              <p>Upload .zip / .tar archive: <input name="directory" type="file" accept="application/zip, application/tar, application/gzip"></p>
            """

        elif self.project.deliverables_in._type == "file":
            # Build form to upload a single file (likely .exe)
            self.deliverables_form = """
              <p>Upload file: <input name="file" type="file"></p>
            """

        else:
            raise Exception("Unknown delivery form for type {}".format(self.project.deliverables_in._type))

        return self.deliverables_form


def run_http_server(project, port=8080):
    """
    Runs an HTTP server and blocks until process exits.
    The server will have a form for project deliverables
    and upon deliverables being uploaded the server will
    run builds and tests, returning a report of the project.
    """
    server_address = ('', port)
    handler = partial(Server, project) # partial() is respnsible for passing project to Server.__init__
    httpd = HTTPServer(server_address, handler)
    print('Starting HTTP server on http://localhost:{}'.format(port))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()

