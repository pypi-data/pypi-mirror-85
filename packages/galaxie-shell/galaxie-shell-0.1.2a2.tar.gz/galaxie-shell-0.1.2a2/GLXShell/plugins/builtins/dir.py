import os
import cmd2
import argparse

from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

dir_parser = argparse.ArgumentParser()
dir_parser.add_argument(
    "-l",
    "--long",
    action="store_true",
    help="display in long format with one item per line",
)
dir_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXDir(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @staticmethod
    def dir_print_version():
        cmd2.Cmd().poutput(
            "dir ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    @staticmethod
    def dir():
        # Get the contents as a list
        contents = os.listdir(os.getcwd())
        for f in contents:
            cmd2.Cmd().poutput(f"{f}")

        cmd2.Cmd().last_result = contents

    @cmd2.with_argparser(dir_parser, with_unknown_args=True)
    @cmd2.with_category("Builtins")
    def do_dir(self, args, unknown):
        """List contents of current directory."""
        if args.version:  # pragma: no cover
            self.dir_print_version()
            return

        # No arguments for this commands
        if unknown:  # pragma: no cover
            cmd2.Cmd().perror("dir does not take any positional arguments:")
            dir_parser.print_help()
            cmd2.Cmd().last_result = "Bad arguments"
            return

        self.dir()  # pragma: no cover
