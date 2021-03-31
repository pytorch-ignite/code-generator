import os
import shutil
from pathlib import Path
from subprocess import check_output

import streamlit as st
from codegen import CodeGenerator
from utils import import_from_file

__version__ = "0.1.0"


class App:
    page_title = "Code Generator"
    page_icon = "https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg"
    description = f"""
<div align='center'>
<img src="https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg"
width="100" height="100">

# Code Generator

Application to generate your training scripts with [PyTorch-Ignite](https://github.com/pytorch/ignite).

[Twitter](https://twitter.com/pytorch_ignite) •
[GitHub](https://github.com/pytorch-ignite/code-generator) •
[Release: v{__version__}](https://github.com/pytorch-ignite/code-generator/releases)
</div>
"""

    def __init__(self):
        st.set_page_config(page_title=self.page_title, page_icon=self.page_icon)
        st.write(self.description, unsafe_allow_html=True)

        self.codegen = CodeGenerator()

    def sidebar(self, template_list=None, config=None):
        """Sidebar on the left."""
        template_list = template_list or []
        st.markdown("### Choose a Template")
        self.template_name = st.selectbox("Available Templates are:", options=template_list)
        with st.sidebar:
            if self.template_name:
                config = config(self.template_name)
                self.config = config.get_configs()
            else:
                self.config = {}

    def render_code(self, fname="", code=""):
        """Main content with the code."""
        with st.beta_expander(f"View rendered {fname}"):
            if fname.endswith(".md"):
                st.markdown(code)
            else:
                col1, col2 = st.beta_columns([1, 20])
                with col1:
                    st.code("\n".join(map("{:>3}".format, range(1, code.count("\n") + 1))))
                with col2:
                    st.code(code)

    def render_directory(self, dir):
        output = check_output(["tree", dir], encoding="utf-8")
        st.markdown("Generated files and directory structure")
        st.code(output)

    def add_sidebar(self):
        def config(template_name):
            return import_from_file("template_config", f"./templates/{template_name}/_sidebar.py")

        self.sidebar(self.codegen.template_list, config)

    def add_content(self):
        """Get generated/rendered code from the codegen."""
        content = [*self.codegen.render_templates(self.template_name, self.config)]
        if st.checkbox("View rendered code ?"):
            for fname, code in content:
                self.render_code(fname, code)

    def add_download(self):
        st.markdown("")
        col1, col2 = st.beta_columns(2)
        with col1:
            archive_format = st.radio("Archive formats", self.codegen.available_archive_formats)
            # temporary hack until streamlit has official download option
            # https://github.com/streamlit/streamlit/issues/400
            # https://github.com/streamlit/streamlit/issues/400#issuecomment-648580840
            if st.button("Generate an archive"):
                archive_fname = self.codegen.make_archive(self.template_name, archive_format)
                # this is where streamlit serves static files
                # ~/site-packages/streamlit/static/static/
                dist_path = Path(st.__path__[0]) / "static/static/dist"
                if not dist_path.is_dir():
                    dist_path.mkdir()
                shutil.copy(archive_fname, dist_path)
                st.success(f"Download link : [{archive_fname}](./static/{archive_fname})")
                with col2:
                    self.render_directory(os.path.join(self.codegen.dist_dir, self.template_name))

    def run(self):
        self.add_sidebar()
        self.add_content()
        self.add_download()


def main():
    App().run()


if __name__ == "__main__":
    main()
