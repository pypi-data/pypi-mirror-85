import functools
import argparse
import sys
import os
import subprocess
import pkgutil
from packaging.version import Version
from . import install_pip_package

try:
    from . import ctext
except ImportError:
    import ctext

print = ctext.print
input = ctext.input

__version__ = "1.0.0"


def requires_version(version: str):
    if Version(version) >= Version(__version__):
        raise EnvironmentError(f"autopyb>={version} is required, install by installing latest version of 'denver-api'")


def run_command(command):
    if isinstance(command, str):
        return_code = os.system(command)
    else:
        return_code = subprocess.run(command)
    return return_code


def get_module_list():
    return [x.name for x in pkgutil.iter_modules()]


def ensure_pip_package(package, t="STABLE"):
    if t.lower() == "stable":
        install_pip_package(package)
    elif t.lower() == "pre":
        install_pip_package(package, pre=True)
    elif t.lower() == "latest":
        install_pip_package(package, update=True)
    elif t.lower() == "pre-latest":
        install_pip_package(package, pre=True, update=True)
    else:
        print(f"type '{t}' is not a valid option, skipping installation for '{package}'", fore="yellow")


def make_platform_executable(name: str, script: str, t="ONEFILE", extras=None, hidden=None, *aflags):
    if 'pyinstaller' not in get_module_list():
        install_pip_package("pyinstaller")
    if hidden is None:
        hidden = []
    if extras is None:
        extras = []
    t = [x.lower() for x in t.split('-')]
    print(f"Making platform executable '{name}'")
    flags: list = list(aflags)
    flags.extend(["-n", name])
    for x in extras:
        flags.extend(["--add-data", x])
    for x in hidden:
        flags.extend(["--hidden-import", x])
    if "onefile" in t:
        flags.append("--onefile")
    if "noconsole" in t:
        flags.append("-w")
    if run_command([sys.executable, "-m", "pyinstaller", script, *flags]) != 0:
        raise EnvironmentError("PyInstaller Failed")


# noinspection PyCallByClass
class BuildTasks:
    def __init__(self):
        self.ignored_tasks = []
        self.accomplished = []
        self.tasks = []

    def task(self, *dependencies, forced=False, ignored=False, uses_commandline=False):
        def decorator(function):
            @functools.wraps(function)
            def wrapper_function(arguments=None):
                print(f'-------------{function.__name__}-------------', fore="green")
                for x in dependencies:
                    if x not in self.accomplished:
                        print(f"Running Task {x.__name__} (from {function.__name__})", fore="magenta")
                        if x not in self.ignored_tasks:
                            self.accomplished.append(x)
                        if not uses_commandline:
                            x()
                        else:
                            x(arguments)
                    else:
                        print(f"Skipped Task {x.__name__} (from {function.__name__})", fore="cyan")
                function()
                print(ctext.ColoredText.escape(
                    f"{{fore_yellow}}----{{back_red}}end{{reset_all}}{{style_bright}}{{fore_yellow}}------{function.__name__}-------------"
                ))

            if forced:
                self.ignored_tasks.append(wrapper_function)

            if not ignored:
                self.tasks.append(wrapper_function)

            return wrapper_function

        return decorator

    def interact(self, arguments=None):
        if arguments is None:
            arguments = sys.argv[1:]
        parser = argparse.ArgumentParser()
        parser.add_argument("sub_arguments", nargs="*", default=[])
        command = parser.add_subparsers(dest="command_")
        for x in self.tasks:
            command.add_parser(x.__name__, description=x.__doc__)
        args = parser.parse_args(arguments)
        for x in self.tasks:
            if args.command_ == x.__name__:
                x(args.sub_arguments)
