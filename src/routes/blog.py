import datetime
import os
import frontmatter
from jinja2 import Environment, FileSystemLoader
import markdown
from cms import cms, writeOutputFile

sourcePath = 'templates'
destPath = ''

@cms.route()
def renderHomePage():
    environmentRoute = f"src/{sourcePath}/"
    
    # We also depend on the components folder
    componentsRoute = "src/components"

    environment = Environment(
        loader=FileSystemLoader([
            environmentRoute,
            componentsRoute,
        ])
    )

    year = datetime.date.today().year

    posts = []
    for fileName in os.listdir("src/posts"):
        if not fileName.endswith(".md"): continue

        with open(f"src/posts/{fileName}", "r") as post:
            post = frontmatter.load(post)

            # Generate the HTML for each individual post
            postTemplate = environment.get_template("blog_post.html")
            postContent = postTemplate.render(
                post=post,
                content=markdown.markdown(post.content),
                year=year
            )
            newFileName = "posts/" + fileName[:-3] + ".html"
            writeOutputFile(newFileName, postContent)

            post.fileName = newFileName
            posts.append(post)

    posts.sort(key=lambda p: p['date'], reverse=True)

    blogTemplate = environment.get_template("blog.html")
    blogContent = blogTemplate.render(posts=posts, year=year)
    writeOutputFile("blog.html", blogContent)
