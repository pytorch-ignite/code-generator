"""Code Generator base module.
"""
import shutil
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class CodeGenerator:
    def __init__(self, templates_dir: str = "./templates", dist_dir: str = "./dist"):
        self.templates_dir = Path(templates_dir)
        self.dist_dir = Path(dist_dir)
        self.template_list = [p.stem for p in self.templates_dir.iterdir() if p.is_dir() and not p.stem.startswith("_")]
        self.rendered_code = {t: {} for t in self.template_list}
        self.available_archive_formats = sorted(map(lambda x: x[0], shutil.get_archive_formats()), reverse=True)

    def render_templates(self, template_name: str, config: dict):
        """Renders all the templates files from template folder for the given config."""
        self.rendered_code[template_name] = {}  # clean up the rendered code for given template
        # loading the template files based on given template
        env = Environment(
            loader=FileSystemLoader(self.templates_dir / template_name),
            trim_blocks=True,
            lstrip_blocks=True,
        )
        for fname in env.list_templates(filter_func=lambda x: not x.startswith("_")):
            code = env.get_template(fname).render(**config)
            fname = fname.replace(".pyi", ".py")
            self.rendered_code[template_name][fname] = code
            yield fname, code

    def mk_dist_template_dir(self, template_name: str):
        self.dist_template_dir = Path(f"{self.dist_dir}/{template_name}")
        self.dist_template_dir.mkdir(parents=True, exist_ok=True)

    def write_file(self, fname: str, code: str) -> None:
        """Creates `fname` with content `code` in `dist_dir/template_name`."""
        (self.dist_template_dir / fname).write_text(code)

    def write_files(self, template_name):
        """Writes all rendered code for the specified template."""
        # Save files with rendered code to the disk
        for fname, code in self.rendered_code[template_name].items():
            self.write_file(fname, code)

    def make_archive(self, template_name, archive_format):
        """Creates dist dir with generated code, then makes the archive."""
        self.mk_dist_template_dir(template_name)
        self.write_files(template_name)
        archive_fname = shutil.make_archive(
            base_name=str(self.dist_template_dir),
            format=archive_format,
            base_dir=self.dist_template_dir,
        )
        return archive_fname
