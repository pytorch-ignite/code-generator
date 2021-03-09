"""Code Generator main module.
"""
from pathlib import Path
from jinja2 import Environment, FileSystemLoader


class Model:
    def __init__(self, templates_dir=None):
        templates_dir = templates_dir or "./templates"
        self.task_list = [p.stem for p in Path(templates_dir).iterdir() if p.is_dir()]
        self.env = Environment(
            loader=FileSystemLoader(templates_dir), trim_blocks=True, lstrip_blocks=True
        )

    def render_templates(self, task: str, config: dict):
        """Renders all the templates from task folder for the given config.
        """
        templates_list = (
            template
            for template in self.env.list_templates(".jinja")
            if template.startswith(task)
        )
        for fname in templates_list:
            # Get template
            template = self.env.get_template(fname)
            # Render template
            code = template.render(**config)
            # Write python file
            fname = fname.strip(f"{task}/").strip(".jinja")
            self.generate(task, fname, code)
            yield fname, code

    def generate(self, task: str, fname: str, code: str) -> None:
        """Generates `fname` with content `code` in `path`.
        """
        path = Path(f"dist/{task}")
        path.mkdir(parents=True, exist_ok=True)
        (path / fname).write_text(code)

    def make_archive(self):
        raise NotImplementedError
