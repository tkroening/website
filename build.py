import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import webbrowser  # for optional webserver
import threading

from cms import cms
from webserver import Handler

from src.routes import *

# Flag for webserver
webserver = False

# Class to handle file changes and trigger rebuild
class Watcher(FileSystemEventHandler):
  def __init__(self):
    self.allowed_paths = ["src"]  # Add more paths as needed

  def on_any_event(self, event):
    if event.is_directory:
      return None
    elif event.event_type == 'modified':
        if not any(event.src_path.startswith(os.getcwd() + "/" + path) for path in self.allowed_paths):
            return None  # Ignore modified files outside of allowed paths

        print(f"File '{event.src_path}' changed. Rebuilding website...")
        cms.renderAll()

# Build website initially
cms.renderAll()

# Check for webserver flag
if "--webserver" in os.sys.argv:
  webserver = True

# Start webserver if flag is set
if webserver:
  print("Starting webserver (SimpleHTTPServer) on port 8000...")
  from http.server import HTTPServer, SimpleHTTPRequestHandler
  port = 8000  # Replace with your desired port

  # Make an output directory to point at if one does not exist
  os.makedirs("output/", exist_ok=True)

  def serve_files():
    with HTTPServer(("", port), Handler) as httpd:
      print(f"Serving at http://localhost:{port}")
      httpd.serve_forever()

  # Create a new thread for the webserver
  webserver_thread = threading.Thread(target=serve_files)
  webserver_thread.daemon = True # Thread dies with main thread
  webserver_thread.start()

  # Open a web browser
  webbrowser.open("http://localhost:8000")

# Start watching for file changes
observer = Observer()
observer.schedule(Watcher(), path=".", recursive=True)
observer.start()

# Keep the script running for automatic rebuilds
try:
  while webserver:
    observer.join(timeout=1)
except KeyboardInterrupt:
    observer.stop()
    observer.join()

print("Exiting...")
