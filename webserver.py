from http.server import SimpleHTTPRequestHandler

OUTPUT_DIRECTORY="output"

"""
This lets us point the webserver at the output directory
"""
class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=OUTPUT_DIRECTORY, **kwargs)
