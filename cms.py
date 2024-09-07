"""
CMS class modeled after the `Flask` class from Flask.
"""

import os

class CMSRoute:
    def __init__(self, renderFn):
        """
        renderFn: should handle rendering the route end to end, including
        writing to the destination folder.

        So, we don't expect the function to return anything, as the intended
        effect is writing to files.
        """
        self.renderFn = renderFn

    def renderSelf(self):
        self.renderFn()

class CMS:
    def __init__(self):
        """
        routes: Set of routes that we dynamically build up at runtime
        """
        self.routes: list[CMSRoute] = []

    """
    renderAll: build all routes
    """
    def renderAll(self):
        for route in self.routes:
            route.renderSelf()

    """
    route: Modeled after Flask's app.route pattern - this method is meant to
    be used as a decorator.
    """
    def route(self):
        """
        Since we have custom arguments, we now need to return a function that
        takes the decorated function itself as an argument.
        """
        def routeDecorator(renderFn):
            # Initialize a CMSRoute
            newRoute = CMSRoute(renderFn)

            # Add it to our state
            self.routes.append(newRoute)

            """
            We don't actually care about calling the function directly any more,
            so we'll overwrite the function with `None` to prevent it from being
            called directly.
            """
            return None

        return routeDecorator


def writeOutputFile(relativePath, content):
    fileName = f"output/{relativePath}"

    # Create folder if it does not exist
    os.makedirs(os.path.dirname(fileName), exist_ok=True)

    with open(fileName, mode="w") as outputFile:
        outputFile.write(content)


cms = CMS()
