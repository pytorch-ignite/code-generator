"""Controller.
"""
from model import Model
from view import View
from utils import import_from_file


class Controller:
    def __init__(self):
        self.model = Model()
        self.view = View()

    def run(self):
        self.add_sidebar()
        self.add_content()

    def add_sidebar(self):
        config = lambda task: import_from_file("template_config", f"./templates/{task}/config.py")
        self.view.sidebar(self.model.task_list, config)

    def add_content(self):
        """Get generated/rendered code from the model.
        """
        content = [*self.model.render_templates(self.view.task, self.view.config)]
        # Expand by default for single file template
        if len(content) == 1:
            fold = False
        else:
            fold = True
        for fname, code in content:
            self.view.render_code(fname, code, fold)
