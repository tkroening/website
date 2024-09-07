import datetime
from jinja2 import Environment, FileSystemLoader
from cms import cms, writeOutputFile

sourcePath = 'templates'
destPath = ''

@cms.route()
def renderHomePage():
    environmentRoute = f"src/{sourcePath}/"
    
    # We also depend on the components folder
    componentsRoute = "src/components"

    environment = Environment(loader=FileSystemLoader([environmentRoute, componentsRoute]))

    year = datetime.date.today().year

    templateName = "index.html"
    template = environment.get_template(templateName)
    content = template.render(year=year)

    writeOutputFile(templateName, content)
