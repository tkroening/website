from jinja2 import Environment, FileSystemLoader, Template
import os
import markdown
import frontmatter
import datetime

environment = Environment(loader=FileSystemLoader(["templates/", "components/", "projects/src/"]))

mainPages = [
        "index.html",
        "projects.html",
]

# Get the current year
year = datetime.date.today().year

# Generate the main pages
for templateName in mainPages:
    template = environment.get_template(templateName)
    content = template.render(year=year)
    with open(templateName, mode="w") as outputFile:
        outputFile.write(content)

# Generate the blog page
posts = []
for fileName in os.listdir("posts"):
    if not fileName.endswith(".md"): continue

    with open(f"posts/{fileName}", "r") as post:
        post = frontmatter.load(post)

        # Generate the HTML for each individual post
        postTemplate = environment.get_template("blog_post.html")
        postContent = postTemplate.render(
            post = post,
            content = markdown.markdown(post.content),
            year = year
        )
        newFileName = "posts/" + fileName[:-3] + ".html"
        with open(newFileName, "w") as blogPostFile:
            blogPostFile.write(postContent)

        post.fileName = newFileName
        posts.append(post)

posts.sort(key = lambda p : p['date'], reverse=True)

blogTemplate = environment.get_template("blog.html")
blogContent = blogTemplate.render(posts=posts, year=year)
with open("blog.html", "w") as blogHTMLFile:
    blogHTMLFile.write(blogContent)


# Render the project pages
for projectFile in os.listdir("projects/src"):
    if not projectFile.endswith(".html"):
        continue

    projectTemplate = environment.get_template(projectFile)
    content = projectTemplate.render(year = year)

    with open(f"projects/{projectFile}", "w") as outputFile:
        outputFile.write(content)
