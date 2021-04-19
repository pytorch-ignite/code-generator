import os
import shutil
import tempfile
from pathlib import Path

import streamlit as st
from codegen import CodeGenerator
from utils import import_from_file

__version__ = "0.1.0"
DEV_MODE = int(os.getenv("DEV_MODE", 0)) == 1

FOLDER_TO_TEMPLATE_NAME = {
    "Image Classification": "image_classification",
    "Text Classification": "text_classification",
    "Generative Adversarial Network": "gan",
    "Single Model, Single Optimizer": "single",
}

TIP = """
**💡 TIP**

To quickly adapt to the generated code structure, there are TODOs in the files that are needed to be edited.
[PyCharm TODO comments](https://www.jetbrains.com/help/pycharm/using-todo.html) or
[VSCode Todo Tree](https://marketplace.visualstudio.com/items?itemName=Gruntfuggly.todo-tree)
can help you find them easily.
"""


class App:
    page_title = "Code Generator"
    page_icon = "https://raw.githubusercontent.com/pytorch/ignite/master/assets/logo/ignite_logomark.svg"
    description = f"""
<div align='center'>
<img src="{page_icon}"
width="100" height="100">

# Code Generator

Application to generate your training scripts with [PyTorch-Ignite](https://github.com/pytorch/ignite).

[![Twitter](https://badgen.net/badge/icon/Twitter?icon=twitter&label)](https://twitter.com/pytorch_ignite)
[![GitHub](https://badgen.net/badge/icon/GitHub?icon=github&label)](https://github.com/pytorch-ignite/code-generator)
[![Release](https://badgen.net/github/tag/pytorch-ignite/code-generator?label=release)](https://github.com/pytorch-ignite/code-generator/releases/latest)

</div>

<details>

<summary>
<samp>Learn More</samp>
</summary>

#### Code Generator, what is it ?

- "Code Generator" is a streamlit application to produce quick-start python code
for common training tasks in deep learning.
- Code is using PyTorch framework and PyTorch-Ignite library can be configured using the UI.

#### Why to use Code Generator ?

- Start working on a task without rewriting everything from scratch: Kaggle competition, client prototype project, etc.

</details>

<details open="true">
<summary>
<samp>Get Started</samp>
</summary>

#### How to use it ?

1. 📃 Choose a Template.
2. ⚙️ Adjust the configuration in the left sidebar. _(click on > if closed)_
3. 🔬 Inspect the code in the central widget.
4. 📦 Download the source code.
5. 🚀 Use it for your project.

</details>

---
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
        with st.beta_expander(fname):
            if fname.endswith(".md"):
                st.markdown(code, unsafe_allow_html=True)
            else:
                col1, col2 = st.beta_columns([1, 20])
                with col1:
                    st.code("\n".join(map("{:>3}".format, range(1, code.count("\n") + 1))))
                with col2:
                    st.code(code)

    def render_directory(self, dir):
        """tree command is not available in all systems."""
        output = f"{dir}\n"
        # https://stackoverflow.com/questions/9727673/list-directory-tree-structure-in-python
        # prefix components:
        space = "    "
        branch = "│   "
        # pointers:
        tee = "├── "
        last = "└── "
        file_count = 0
        dir_count = 0

        def tree(dir_path: Path, prefix: str = ""):
            """A recursive generator, given a directory Path object
            will yield a visual tree structure line by line
            with each line prefixed by the same characters
            """
            nonlocal file_count
            nonlocal dir_count
            contents = sorted(dir_path.iterdir())
            # contents each get pointers that are ├── with a final └── :
            pointers = [tee] * (len(contents) - 1) + [last]
            for pointer, path in zip(pointers, contents):
                if path.is_file():
                    file_count += 1
                yield prefix + pointer + path.name
                if path.is_dir():  # extend the prefix and recurse:
                    dir_count += 1
                    extension = branch if pointer == tee else space
                    # i.e. space because last, └── , above so no more |
                    yield from tree(path, prefix=prefix + extension)

        for line in tree(dir):
            output += line + "\n"
        output += f"\n{dir_count} directories, {file_count} files"
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

    def download_panel_dev(self):
        st.markdown("")
        col1, col2 = st.beta_columns(2)
        with col1:
            archive_format = st.radio("Archive formats", self.codegen.available_archive_formats)
            # temporary hack until streamlit has official download option
            # https://github.com/streamlit/streamlit/issues/400
            # https://github.com/streamlit/streamlit/issues/400#issuecomment-648580840
            if st.button("Generate an archive"):
                tmp_dir = tempfile.TemporaryDirectory(prefix="", dir=self.codegen.dist_dir)
                tmp_dir = Path(tmp_dir.name)

                archive_fname = self.codegen.write_archive(self.template_name, archive_format, tmp_dir)
                # this is where streamlit serves static files
                # ~/site-packages/streamlit/static/static/
                dist_path = Path(st.__path__[0]) / "static/static" / tmp_dir

                if not dist_path.is_dir():
                    dist_path.mkdir(parents=True, exist_ok=True)

                shutil.copy(archive_fname, dist_path)
                st.success(f"Download link : [{archive_fname}](./static/{archive_fname})")

                with col2:
                    self.render_directory(Path(tmp_dir, self.template_name))

    def download_panel(self):
        st.markdown("")
        archive_format = None
        mimetype = ""

        _, zip_col, tar_col, _ = st.beta_columns(4)
        if zip_col.button("📦 Download zip"):
            archive_format = "zip"
            mimetype = "application/zip"

        if tar_col.button("📦 Download tar"):
            archive_format = "tar.gz"
            mimetype = "application/x-tar"

        if archive_format is not None:
            archive = self.codegen.writes_archive(self.template_name, archive_format)

            download_link = (
                f'Download link: <a href="data:{mimetype};base64,{archive}" '
                f'download="{self.template_name}.{archive_format}">'
                f"{self.template_name}.{archive_format}</a>"
            )

            st.markdown(download_link, unsafe_allow_html=True)

    def add_download_panel(self):
        if DEV_MODE:
            self.download_panel_dev()
        else:
            self.download_panel()

    def run(self):
        self.add_sidebar()
        self.add_content()
        self.add_download_panel()
        st.info(TIP)


def main():
    App().run()


if __name__ == "__main__":
    main()
