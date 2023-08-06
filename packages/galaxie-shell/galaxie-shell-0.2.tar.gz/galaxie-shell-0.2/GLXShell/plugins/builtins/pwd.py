import os
import cmd2
import argparse

from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

pwd_parser = argparse.ArgumentParser(
    description="The pwd utility shall write to standard output an absolute pathname of the current working "
    "directory, which does not contain the filenames dot or dot-dot. "
)
pwd_parser.add_argument(
    "-L",
    "--logical",
    action="store_true",
    help="If the PWD environment variable contains an absolute pathname of the current directory that does not "
    "contain the filenames dot or dot-dot, pwd shall write this pathname to standard output. Otherwise, "
    "the -L option shall behave as the -P option.",
)
pwd_parser.add_argument(
    "-P",
    "--physical",
    action="store_true",
    help="The absolute pathname written shall not contain filenames that, in the context of the pathname, "
    "refer to files of type symbolic link. ",
)
pwd_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXPwd(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @staticmethod
    def pwd_print_version():
        cmd2.Cmd().poutput(
            "pwd ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    @staticmethod
    def pwd_print_logical():
        cmd2.Cmd().poutput("{pwd}".format(pwd=os.path.normpath(os.getcwd())))

    @staticmethod
    def pwd_print_not_logical():
        cmd2.Cmd().poutput("{pwd}".format(pwd=os.path.realpath(os.getcwd())))

    def pwd(self, logical, physical):
        if logical:
            self.pwd_print_logical()
        else:
            self.pwd_print_not_logical()
        return

    @cmd2.with_argparser(pwd_parser)
    @cmd2.with_category("Builtins")
    def do_pwd(self, args):
        if args.version:  # pragma: no cover
            self.pwd_print_version()
            return

        self.pwd(logical=args.logical, physical=args.physical)  # pragma: no cover
