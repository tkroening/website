from jinja2 import Environment, FileSystemLoader
import os
import markdown
import frontmatter
import datetime
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import webbrowser  # for optional webserver
import threading

# Flag for webserver
webserver = False

# Class to handle file changes and trigger rebuild
class Watcher(FileSystemEventHandler):
  def __init__(self):
    self.allowed_paths = ["templates/", "components/", "projects/src/", "posts/src"]  # Add more paths as needed

  def on_any_event(self, event):
    if event.is_directory:
      return None
    elif event.event_type == 'modified':
      if not any(event.src_path.startswith(os.getcwd() + "/" + path) for path in self.allowed_paths):
        return None  # Ignore modified files outside of allowed paths

      print(f"File '{event.src_path}' changed. Rebuilding website...")
      build_website()

def build_website():
  global year

  environment = Environment(loader=FileSystemLoader(["templates/", "components/", "projects/src/"]))

  year = datetime.date.today().year

  # Generate main pages
  mainPages = [
      "index.html",
      "projects.html",
  ]
  for templateName in mainPages:
    template = environment.get_template(templateName)
    content = template.render(year=year)
    with open(templateName, mode="w") as outputFile:
      outputFile.write(content)

  # Generate blog page
  posts = []
  for fileName in os.listdir("posts/src"):
    if not fileName.endswith(".md"): continue

    with open(f"posts/src/{fileName}", "r") as post:
      post = frontmatter.load(post)

      # Generate the HTML for each individual post
      postTemplate = environment.get_template("blog_post.html")
      postContent = postTemplate.render(
          post=post,
          content=markdown.markdown(post.content),
          year=year
      )
      newFileName = "posts/" + fileName[:-3] + ".html"
      with open(newFileName, "w") as blogPostFile:
        blogPostFile.write(postContent)

      post.fileName = newFileName
      posts.append(post)

  posts.sort(key=lambda p: p['date'], reverse=True)

  blogTemplate = environment.get_template("blog.html")
  blogContent = blogTemplate.render(posts=posts, year=year)
  with open("blog.html", "w") as blogHTMLFile:
    blogHTMLFile.write(blogContent)

  # Render the project pages
  for projectFile in os.listdir("projects/src"):
    if not projectFile.endswith(".html"):
      continue

    projectTemplate = environment.get_template(projectFile)
    content = projectTemplate.render(year=year)

    with open(f"projects/{projectFile}", "w") as outputFile:
      outputFile.write(content)

  print(f"Website build complete!")

# Build website initially
build_website()

# Check for webserver flag
if "--webserver" in os.sys.argv:
  webserver = True

# Start webserver if flag is set
if webserver:
  print("Starting webserver (SimpleHTTPServer) on port 8000...")
  from http.server import HTTPServer, SimpleHTTPRequestHandler
  port = 8000  # Replace with your desired port

  def serve_files():
    with HTTPServer(("", port), SimpleHTTPRequestHandler) as httpd:
      print(f"Serving at http://localhost:{port}")
      httpd.serve_forever()

  # Create a new thread for the webserver
  webserver_thread = threading.Thread(target=serve_files)
  webserver_thread.daemon = True # Thread dies with main thread
  webserver_thread.start()

  # Open a web browser
  webbrowser.open("http://localhost:8000")  # Replace 8000 with your desired port

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
