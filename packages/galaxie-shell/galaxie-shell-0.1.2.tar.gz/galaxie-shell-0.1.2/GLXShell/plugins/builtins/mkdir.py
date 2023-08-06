import os
import cmd2
import argparse

from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

mkdir_parser = argparse.ArgumentParser(
    description="Create the DIRECTORY(ies), if they do not already exist."
)
mkdir_parser.add_argument(
    "DIRECTORY",
    nargs=argparse.ZERO_OR_MORE,
    help="DIRECTORY(ies), to create",
)
mkdir_parser.add_argument(
    "-m",
    "--mode",
    nargs="?",
    const=1,
    type=str,
    default="755",
    help="set file mode (as in chmod), not a=rwx - umask",
)
mkdir_parser.add_argument(
    "-p",
    "--parents",
    action="store_true",
    default=False,
    help="no error if existing, make parent directories as needed",
)
mkdir_parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    default=False,
    help="print a message for each created directory",
)
#
# mkdir_parser.add_argument(
#     "-Z",
#     action="store_true",
#     default=False,
#     help="set SELinux security context of each created directory to the default type"
# )
# mkdir_parser.add_argument(
#     "--context",
#     action="store_true",
#     type=str,
#     default="",
#     help="like -Z, or if CTX is specified then set the SELinux or SMACK security context to CTX"
# )
mkdir_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXMkdir(cmd2.CommandSet):
    def __init__(self):
        super().__init__()

    @staticmethod
    def mkdir_print_version():
        cmd2.Cmd().poutput(
            "mkdir ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    @staticmethod
    def mkdir_print_created_directory(directory, verbose):
        if verbose:
            cmd2.Cmd().poutput("mkdir: created directory '{0}'".format(directory))

    @staticmethod
    def mkdir_print_cannot_create_directory(directory):
        cmd2.Cmd().perror(
            "mkdir: cannot create directory '{0}': File exists".format(directory)
        )
        return

    def mkdir_with_no_parents(self, directory, mode, verbose):
        if mode:
            mode = int(mode, 8)
        if os.path.exists(directory):
            self.mkdir_print_cannot_create_directory(directory=directory)
        else:
            self.mkdir_print_created_directory(directory=directory, verbose=verbose)
            os.mkdir(path=directory, mode=mode)

    def mkdir_with_parents(self, directory, mode, verbose):
        if mode:
            mode = int(mode, 8)
        directory_to_create = ""
        for sub_directory in directory.split(os.path.sep):
            directory_to_create = os.path.join(directory_to_create, sub_directory)
            if not os.path.isdir(directory):
                self.mkdir_print_created_directory(
                    directory=directory_to_create, verbose=verbose
                )
                os.mkdir(path=directory_to_create, mode=mode)
            else:
                self.mkdir_print_cannot_create_directory(directory=directory_to_create)

    def mkdir(self, directories, parents, mode, verbose):
        for directory in directories:
            if parents:
                self.mkdir_with_parents(directory=directory, mode=mode, verbose=verbose)
            else:
                self.mkdir_with_no_parents(
                    directory=directory, mode=mode, verbose=verbose
                )

    @cmd2.with_argparser(mkdir_parser)
    @cmd2.with_category("Builtins")
    def do_mkdir(self, args):
        if args.version:  # pragma: no cover
            self.mkdir_print_version()
            return

        if not args.DIRECTORY:  # pragma: no cover
            mkdir_parser.print_help()
            return

        self.mkdir(
            directories=args.DIRECTORY,
            parents=args.parents,
            mode=args.mode,
            verbose=args.verbose,
        )  # pragma: no cover

    @staticmethod
    def complete_mkdir(text, line, begidx, endidx):  # pragma: no cover
        return cmd2.Cmd().path_complete(
            text=text,
            line=line,
            begidx=begidx,
            endidx=endidx,
            path_filter=os.path.isdir,
        )
