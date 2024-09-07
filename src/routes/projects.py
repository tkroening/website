import datetime
import os
from jinja2 import Environment, FileSystemLoader
from cms import cms, writeOutputFile

sourcePath = 'templates'
destPath = ''

@cms.route()
def renderHomePage():
    environmentRoute = f"src/{sourcePath}/"
    
    # We also depend on the components folder
    componentsRoute = "src/components"

    # We also want the project source files
    projectsRoute = "src/projects"

    environment = Environment(
        loader=FileSystemLoader([
            environmentRoute,
            componentsRoute,
            projectsRoute

        ])
    )

    year = datetime.date.today().year

    templateName = "projects.html"
    template = environment.get_template(templateName)
    content = template.render(year=year)

    writeOutputFile(templateName, content)

    # Render the project pages
    for projectFile in os.listdir("src/projects"):
        if not projectFile.endswith(".html"):
            continue

        projectTemplate = environment.get_template(projectFile)
        content = projectTemplate.render(year=year)

        writeOutputFile(f'projects/{projectFile}', content)
