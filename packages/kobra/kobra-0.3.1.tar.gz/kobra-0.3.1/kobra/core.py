from kobra import __version__, __logo__
from colorama import init

import argparse
import os

init()


def getModuleName(filelist):
    folders = []
    for file in filelist:
        if os.path.isdir(file):
            folders.append(file)

    for folder in folders:
        files = os.listdir(folder)
        for file in files:
            if file == "__init__.py":
                return folder


def kobra():
    for line in __logo__:
        print(f"\033[32m{line}\033[0m")

    parser = argparse.ArgumentParser()

    parser.add_argument("command",
                        nargs="?",
                        default="install",
                        help="Run command (publish, install, develop)")

    parser.add_argument("-v",
                        "--version",
                        action="store_true",
                        help="Show version")

    args = parser.parse_args()

    if args.version:
        print("Kobra v" + __version__)
        quit()

    if args.command == "publish":
        cwd = os.getcwd()
        moduleName = getModuleName(os.listdir("."))

        if moduleName is None:
            print("Program can't find module folder")
            quit()
        else:
            with open(f'{cwd}\\{moduleName}\\__init__.py') as init:
                moduleVersion = (init.read()
                                     .replace("__version__", "")
                                     .replace(" ", "")
                                     .replace("\"", "")
                                     .replace("=", "")
                                     .replace("\n", ""))

            os.system("git restore --staged .")

            version = input("Enter version (current: " + moduleVersion + ") ")

            with open(f"{cwd}\\{moduleName}\\__init__.py", "w") as init:
                init.write("__version__ = \"" + version + "\"")

            if os.path.exists("dist"):
                for file in os.listdir("dist"):
                    os.remove("dist" + "\\" + file)

            os.system("python setup.py sdist")
            os.system("twine upload dist\\*")
            os.system("git add " + moduleName + "\\" + "__init__.py")
            os.system(f"git commit -m \"{moduleName} v{version} released\"")

            if input("git push?(y/n)") == "y":
                os.system("git push")

    elif args.command == "install":
        os.system("python setup.py install")

    elif args.command == "develop":
        os.system("python setup.py develop")

    else:
        print("Enter command!")
