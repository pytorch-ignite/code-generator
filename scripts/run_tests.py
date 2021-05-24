import os
import zipfile
from pathlib import Path
from subprocess import run


def unzip():
    dist_tests = Path("./dist-tests")

    for zip in dist_tests.rglob("*.zip"):
        with zipfile.ZipFile(zip, "r") as f:
            f.extractall(f"./dist-tests/{zip.stem}")
            zip.unlink()


def run_simple():
    simple = Path("./dist-tests/")

    for p in simple.rglob("*-simple"):
        os.chdir(p)
        run(["python", "main.py", "--data_path", "~/data"])


if __name__ == "__main__":
    unzip()
    run_simple()
