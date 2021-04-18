"""Code Generator base module.
"""
import base64
import io
import shutil
import tarfile
import zipfile
from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class CodeGenerator:
    def __init__(self, templates_dir: str = "./templates", dist_dir: str = "./dist"):
        self.templates_dir = Path(templates_dir)
        self.dist_dir = Path(dist_dir)
        self.dist_dir.mkdir(parents=True, exist_ok=True)
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

    def write_archive(self, template_name, archive_format, dest_path):
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

    def writes_archive(self, template_name, archive_format):
        """Writes archive as Base64 string."""
        arch_buffer = io.BytesIO()

        if archive_format == "zip":
            with zipfile.ZipFile(arch_buffer, "w", zipfile.ZIP_DEFLATED) as arch:
                for fname, code in self.rendered_code.items():
                    arch.writestr(f"{template_name}/{fname}", code)

        elif archive_format == "tar.gz":
            with tarfile.open(fileobj=arch_buffer, mode="w:gz") as arch:
                for fname, code in self.rendered_code.items():
                    tarinfo = tarfile.TarInfo(name=f"{template_name}/{fname}")
                    code_fileobj = io.BytesIO(code.encode())
                    tarinfo.size = len(code_fileobj.getvalue())
                    arch.addfile(tarinfo, code_fileobj)
        else:
            raise ValueError(f"Wrong archive format '{archive_format}', use one of available formats: zip, tar.gz")

        arch_str = base64.b64encode(arch_buffer.getvalue()).decode()

        return arch_str
