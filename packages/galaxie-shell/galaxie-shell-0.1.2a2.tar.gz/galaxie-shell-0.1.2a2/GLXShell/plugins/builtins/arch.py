import os
import argparse
import cmd2

from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY
from GLXShell.plugins.builtins import PLUGIN_VERSION
arch_parser = argparse.ArgumentParser(description="Print machine architecture.")
#      --help               display this help and exit
#      --version            output version information and exit
arch_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXArch(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @property
    def result(self):
        return f"{os.uname().machine}"

    @staticmethod
    def arch_print_version():
        cmd2.Cmd().poutput(
            "arch ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    def arch(self):
        cmd2.Cmd().last_result = self.result
        cmd2.Cmd().poutput(self.result)

    @cmd2.with_argparser(arch_parser)
    @cmd2.with_category("Builtins")
    def do_arch(self, args):
        if args.version:  # pragma: no cover
            self.arch_print_version()
            return

        self.arch()  # pragma: no cover
