# check copies of utils.py up-to-date or not

from pathlib import Path


def check_utils():
    red = "\033[31m"
    green = "\033[32m"
    reset = "\033[0m"

    with open("./src/templates/template-common/utils.py", "r") as f:
        common_utils = f.read()

    path = Path("./src/templates/")

    for file in path.rglob("**/utils.py"):
        utils = file.read_text("utf-8")
        if utils.find(common_utils) > -1:
            print(green, "Matched", file, reset)
        else:
            print(red, "Unmatched", file, reset)


if __name__ == "__main__":
    check_utils()
