"""Code Generator base module.
"""
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class CodeGenerator:
    def __init__(self, templates_dir: str = "./templates", target_dir: str = "./dist"):
        self.templates_dir = Path(templates_dir)
        self.target_dir = Path(target_dir)
        self.template_list = [p.stem for p in self.templates_dir.iterdir() if p.is_dir()]
        self.env = Environment(loader=FileSystemLoader(self.templates_dir), trim_blocks=True, lstrip_blocks=True)
        self.rendered_code = {t: {} for t in self.template_list}
        self.available_archive_formats = sorted(map(lambda x: x[0], shutil.get_archive_formats()), reverse=True)

    def render_template(self, template_name: str, fname: str, config: dict):
        """Renders single template file `fname` of the template `template_name`."""
        # Get template
        template = self.env.get_template(fname)
        # Render template
        code = template.render(**config)
        # Store rendered code
        fname = fname.rstrip(".jinja").lstrip(f"{template_name}/")
        self.rendered_code[template_name][fname] = code
        return fname, code

    def render_templates(self, template_name: str, config: dict):
        """Renders all the templates files from template folder for the given config."""
        self.rendered_code[template_name] = {}
        for fname in filter(lambda t: t.startswith(template_name), self.env.list_templates(".jinja")):
            fname, code = self.render_template(template_name, fname, config)
            yield fname, code

    def create_target_template_dir(self, template_name: str):
        self.target_template_path = Path(f"{self.target_dir}/{template_name}")
        self.target_template_path.mkdir(parents=True, exist_ok=True)

    def write_file(self, fname: str, code: str) -> None:
        """Creates `fname` with content `code` in `target_dir/template_name`."""
        (self.target_template_path / fname).write_text(code)

    def write_files(self, template_name):
        """Writes all rendered code for the specified template."""
        # Save files with rendered code to the disk
        for fname, code in self.rendered_code[template_name].items():
            self.write_file(fname, code)

    def make_archive(self, template_name, archive_format):
        """Creates target dir with generated code, then makes the archive."""
        self.create_target_template_dir(template_name)
        self.write_files(template_name)
        archive_fname = shutil.make_archive(
            base_name=str(self.target_template_path), format=archive_format, base_dir=self.target_template_path,
        )
        return archive_fname
