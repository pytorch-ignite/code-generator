import shutil
from pathlib import Path
from subprocess import check_output

import streamlit as st
from codegen import CodeGenerator
from utils import import_from_file

__version__ = "0.1.0"


FOLDER_TO_TEMPLATE_NAME = {
    "Single Model, Single Optimizer": "single",
    "Generative Adversarial Network": "gan",
    "Image Classification": "image_classification",
}

TIP = """
**A WORD OF TIP:**

_To adapt the generate code structure quickly, there are TODOs in the files that are needed to be edited.
PyCharm TODO feature or
[VSCode Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)
can easily help you detect them._
"""


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
        self.template_name = FOLDER_TO_TEMPLATE_NAME[self.template_name]
        with st.sidebar:
            if self.template_name:
                config = config(self.template_name)
                self.config = config.get_configs()
            else:
                self.config = {}

    def render_code(self, fname: str = "", code: str = ""):
        """Main content with the code."""
        with st.beta_expander(f"View rendered {fname}", expanded=fname.endswith(".md")):
            if fname.endswith(".md"):
                st.markdown(code, unsafe_allow_html=True)
            else:
                st.code(code)

    def render_directory(self, dir):
        output = check_output(["tree", dir], encoding="utf-8")
        st.markdown("Generated files and directory structure")
        st.code(output)

    def add_sidebar(self):
        def config(template_name):
            return import_from_file("template_config", f"./templates/{template_name}/_sidebar.py")

        self.sidebar([*FOLDER_TO_TEMPLATE_NAME], config)

    def add_content(self):
        """Get generated/rendered code from the codegen."""
        content = [*self.codegen.render_templates(self.template_name, self.config)]
        if st.checkbox("View rendered code ?", value=True):
            for fname, code in content:
                if len(code):  # don't show files which don't have content in them
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
                    self.render_directory(Path(self.codegen.dist_dir, self.template_name))

    def run(self):
        self.add_sidebar()
        self.add_content()
        self.add_download()
        st.info(TIP)


def main():
    App().run()


if __name__ == "__main__":
    main()
