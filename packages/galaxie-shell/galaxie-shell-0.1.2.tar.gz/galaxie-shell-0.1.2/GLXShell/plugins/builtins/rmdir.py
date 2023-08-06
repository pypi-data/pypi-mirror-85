import os
import cmd2
import argparse

from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

rmdir_parser = argparse.ArgumentParser(
    prog="RMDIR", description="Remove the DIRECTORY(ies), if they are empty."
)
rmdir_parser.add_argument(
    "DIRECTORY",
    nargs=argparse.ZERO_OR_MORE,
    help="DIRECTORY(ies), to create",
)

rmdir_parser.add_argument(
    "--ignore-fail-on-non-empty",
    action="store_true",
    default=False,
    help="ignore each failure that is solely because a directory is non-empty",
)

rmdir_parser.add_argument(
    "-p",
    "--parents",
    action="store_true",
    default=False,
    help="remove DIRECTORY and its ancestors; e.g., 'rmdir -p a/b/c' is similar to 'rmdir a/b/c a/b a'",
)
rmdir_parser.add_argument(
    "-v",
    "--verbose",
    action="store_true",
    default=False,
    help="output a diagnostic for every directory processed",
)
rmdir_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXRmDir(cmd2.CommandSet):
    exit_code: int

    @staticmethod
    def rmdir_print_version():
        cmd2.Cmd().poutput(
            "rmdir ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    @staticmethod
    def rmdir_print_removing_directory(directory, verbose):
        if verbose:
            cmd2.Cmd().poutput("rmdir: removing directory '{0}'".format(directory))

    @staticmethod
    def rmdir_print_directory_not_empty(directory, ignore_fail_on_non_empty):
        if not ignore_fail_on_non_empty:
            cmd2.Cmd().perror(
                "rmdir: failed to remove '{0}': Directory not empty".format(directory)
            )
            return

    @staticmethod
    def rmdir_print_no_such_file_or_directory(directory):
        cmd2.Cmd().perror(
            "rmdir: failed to remove '{0}': No such file or directory".format(directory)
        )
        return

    def rmdir_with_parent(self, directory, verbose, ignore_fail_on_non_empty):
        # Create a list item for each directories
        directory_to_remove = ""
        directory_to_remove_list = []
        for sub_directory in directory.split(os.path.sep):
            directory_to_remove = os.path.join(directory_to_remove, sub_directory)
            directory_to_remove_list.append(directory_to_remove)

        # Work with the reversed directories list
        for reversed_dir in reversed(directory_to_remove_list):
            if os.path.exists(reversed_dir) and os.path.isdir(reversed_dir):
                if not os.listdir(reversed_dir):
                    self.rmdir_print_removing_directory(
                        directory=reversed_dir, verbose=verbose
                    )
                    os.rmdir(path=reversed_dir)
                else:
                    self.rmdir_print_directory_not_empty(
                        directory=reversed_dir,
                        ignore_fail_on_non_empty=ignore_fail_on_non_empty,
                    )
            else:
                self.rmdir_print_no_such_file_or_directory(directory=reversed_dir)

    def rmdir_with_not_parent(self, directory, verbose, ignore_fail_on_non_empty):
        if os.path.exists(directory) and os.path.isdir(directory):
            if not os.listdir(directory):
                self.rmdir_print_removing_directory(
                    directory=directory, verbose=verbose
                )
                os.rmdir(path=directory)
            else:
                self.rmdir_print_directory_not_empty(
                    directory=directory,
                    ignore_fail_on_non_empty=ignore_fail_on_non_empty,
                )
        else:
            self.rmdir_print_no_such_file_or_directory(directory=directory)

    def rmdir(self, directories, parents, verbose, ignore_fail_on_non_empty):
        for directory in directories:
            if parents:
                self.rmdir_with_parent(
                    directory=directory,
                    verbose=verbose,
                    ignore_fail_on_non_empty=ignore_fail_on_non_empty,
                )
            else:
                self.rmdir_with_not_parent(
                    directory=directory,
                    verbose=verbose,
                    ignore_fail_on_non_empty=ignore_fail_on_non_empty,
                )

    @cmd2.with_argparser(rmdir_parser)
    @cmd2.with_category("Builtins")
    def do_rmdir(self, args):
        if args.version:  # pragma: no cover
            self.rmdir_print_version()
            return

        if not args.DIRECTORY:  # pragma: no cover
            rmdir_parser.print_help()
            return

        self.rmdir(
            directories=args.DIRECTORY,
            parents=args.parents,
            verbose=args.verbose,
            ignore_fail_on_non_empty=args.ignore_fail_on_non_empty,
        )  # pragma: no cover
