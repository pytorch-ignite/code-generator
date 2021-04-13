"""Code Generator base module.
"""
import shutil
import tempfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class CodeGenerator:
    def __init__(self, templates_dir: str = "./templates", dist_dir: str = "./dist"):
        self.templates_dir = Path(templates_dir)
        self.dist_dir = Path(dist_dir)
        self.rendered_code = {}
        self.available_archive_formats = [x[0] for x in shutil.get_archive_formats()[::-1]]

    def render_templates(self, template_name: str, config: dict):
        """Renders all the templates files from template folder for the given config."""
        # loading the template files based on given template and from the _base folder
        # since we are using some templates from _base folder
        loader = FileSystemLoader([self.templates_dir / "_base", self.templates_dir / template_name])
        env = Environment(
            loader=loader,
            trim_blocks=True,
            lstrip_blocks=True,
        )
        for fname in env.list_templates(filter_func=lambda x: not x.startswith("_")):
            code = env.get_template(fname).render(**config)
            self.rendered_code[fname] = code
            yield fname, code

    def make_and_write(self, template_name: str, dest_path: Path):
        """Make the directories first and write to the files"""
        for p in (self.templates_dir / template_name).rglob("*"):
            if not p.stem.startswith("_") and p.is_dir():
                # p is templates/template_name/...
                # remove "templates" from p.parts and join with "/", so we'll have
                # template_name/...
                p = "/".join(p.parts[1:])
            else:
                p = template_name

            if not (dest_path / p).is_dir():
                (dest_path / p).mkdir(parents=True, exist_ok=True)

        for fname, code in self.rendered_code.items():
            (dest_path / template_name / fname).write_text(code)

    def make_archive(self, template_name, archive_format, dest_path):
        """Creates dist dir with generated code, then makes the archive."""
        self.make_and_write(template_name, dest_path)
        archive_fname = shutil.make_archive(
            base_name=template_name,
            root_dir=dest_path,
            format=archive_format,
            base_dir=template_name,
        )
        archive_fname = shutil.move(archive_fname, dest_path / archive_fname.split("/")[-1])
        return archive_fname
