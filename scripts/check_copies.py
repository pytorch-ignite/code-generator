# check copies of utils.py up-to-date or not

from pathlib import Path


def check(fname):
    red = "\033[31m"
    green = "\033[32m"
    reset = "\033[0m"

    with open(f"./src/templates/template-common/{fname}", "r") as f:
        common = f.readlines()

    path = Path("./src/templates/")

    for file in path.rglob(f"**/{fname}"):
        if str(file).find("common") > -1:
            continue
        else:
            template = file.read_text("utf-8")

            match = []
            for c in common:
                match.append(template.find(c) > -1)

            if all(match):
                print(green, "Matched", file, reset)
            else:
                print(red, "Unmatched", file, reset)


if __name__ == "__main__":
    check("utils.py")
    print()
    check("README.md")
    print()
    check("requirements.txt")
    print()
    check("main.py")
    print()
