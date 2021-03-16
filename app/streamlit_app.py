import shutil
from pathlib import Path
from datetime import datetime

import streamlit as st
from codegen import CodeGenerator
from utils import import_from_file

__version__ = f"0.1.0.dev{datetime.now().strftime('%Y%m%d')}"
# __version__ = "0.1.0"


class App:
    page_title = "Code Generator"
    page_icon = "https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg"
    description = """
<div align='center'>
<img src="https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg"
width="100" height="100">

# Code Generator

Application to generate your training scripts with [PyTorch-Ignite](https://github.com/pytorch/ignite).
</div>
"""

    def __init__(self):
        st.set_page_config(page_title=self.page_title, page_icon=self.page_icon)
        st.write(self.description, unsafe_allow_html=True)

        self.codegen = CodeGenerator()

    def sidebar(self, template_list=None, config=None):
        """Sidebar on the left."""
        template_list = template_list or []
        with st.sidebar:
            self.template_name = st.selectbox("Templates", template_list)
            if self.template_name:
                config = config(self.template_name)
                self.config = config.get_configs()
            else:
                self.config = {}

    def render_code(self, fname="", code="", fold=False):
        """Main content with the code."""
        if fold:
            with st.beta_expander(f"View generated {fname}"):
                st.code(code)
        else:
            st.code(code)

    def add_sidebar(self):
        def config(template_name):
            return import_from_file("template_config", f"./templates/{template_name}/sidebar.py")

        self.sidebar(self.codegen.template_list, config)

    def add_content(self):
        """Get generated/rendered code from the codegen."""
        content = [*self.codegen.render_templates(self.template_name, self.config)]
        # Expand by default for single file template
        if len(content) == 1:
            fold = False
        else:
            fold = True
        for fname, code in content:
            self.render_code(fname, code, fold)

    def add_download(self):
        st.markdown("")
        archive_format = st.radio("Archive format", self.codegen.available_archive_formats)
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

    def run(self):
        self.add_sidebar()
        self.add_content()
        self.add_download()
        st.markdown(f"Release: v{__version__}")


def main():
    App().run()


if __name__ == "__main__":
    main()
