import os
import cmd2
import argparse
import sys

# https://www.maizure.org/projects/decoded-gnu-coreutils/
# https://www.maizure.org/projects/decoded-gnu-coreutils/cat.html

from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

cat_parser = argparse.ArgumentParser()
cat_parser.add_argument(
    "file",
    nargs="*",
    type=argparse.FileType("r"),
    default=sys.stdin,
    help="with no FILE, or when FILE is -, read standard input.",
)
cat_parser.add_argument(
    "-A",
    "--show-all",
    action="store_true",
    help="equivalent to -vET",
)
cat_parser.add_argument(
    "-b",
    "--number-nonblank",
    action="store_true",
    help="number nonempty output lines, overrides -n",
)
cat_parser.add_argument(
    "-e",
    action="store_true",
    help="equivalent to -vE",
)
cat_parser.add_argument(
    "-E",
    "--show-ends",
    action="store_true",
    help="display $ at end of each line",
)
cat_parser.add_argument(
    "-n",
    "--number",
    action="store_true",
    help="number all output lines",
)
cat_parser.add_argument(
    "-s",
    "--squeeze-blank",
    action="store_true",
    help="suppress repeated empty output lines",
)
#   -t                       equivalent to -vT
cat_parser.add_argument(
    "-t",
    action="store_true",
    help="equivalent to -vT",
)
#   -T, --show-tabs          display TAB characters as ^I
cat_parser.add_argument(
    "-T",
    "--show-tabs",
    action="store_true",
    help="display TAB characters as ^I",
)
#   -u                       (ignored)
cat_parser.add_argument(
    "-u",
    action="store_true",
    help="(ignored)",
)
#   -v, --show-nonprinting   use ^ and M- notation, except for LFD and TAB
cat_parser.add_argument(
    "-v",
    "--show-nonprinting",
    action="store_true",
    help="use ^ and M- notation, except for LFD and TAB",
)
#      --help               display this help and exit
#      --version            output version information and exit
cat_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXCat(cmd2.CommandSet):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.stdout = kwargs.get("stdout", sys.stdout)
        self.stdin = kwargs.get("stdin", sys.stdin)
        self.stderr = kwargs.get("stdin", sys.stderr)

    @staticmethod
    def cat_print_version():
        cmd2.Cmd().poutput(
            "cat ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )

    @staticmethod
    def cat(file, number_nonblank, number, show_tabs, squeeze_blank, show_ends):
        if number_nonblank:
            number = False

        file_data = []
        for file_object in file:
            file_data.append(file_object.read().split("\n"))

        think_to_display = []
        line_number = 1
        blank_line_allowed = True

        for file in file_data:
            if not blank_line_allowed:
                blank_line_allowed = True

            for line in file:
                if show_tabs:
                    line = line.replace("\t", "^I")
                if number:
                    if len(line) > 0:
                        think_to_display.append(
                            "{0:>6d}  {1}".format(line_number, line)
                        )
                        line_number += 1
                        if not blank_line_allowed:
                            blank_line_allowed = True
                    else:
                        if blank_line_allowed:
                            think_to_display.append(
                                "{0:>6d}  {1}".format(line_number, "")
                            )
                            line_number += 1
                            if squeeze_blank and blank_line_allowed:
                                blank_line_allowed = False
                elif number_nonblank:
                    if len(line) > 0:
                        think_to_display.append(
                            "{0:>6d}  {1}".format(line_number, line)
                        )
                        line_number += 1
                        if not blank_line_allowed:
                            blank_line_allowed = True
                    else:
                        if blank_line_allowed:
                            think_to_display.append("")
                            if squeeze_blank and blank_line_allowed:
                                blank_line_allowed = False
                else:
                    if len(line) > 0:
                        think_to_display.append(line)
                        if not blank_line_allowed:
                            blank_line_allowed = True
                    else:
                        if blank_line_allowed:
                            think_to_display.append(line)
                            if squeeze_blank and blank_line_allowed:
                                blank_line_allowed = False

        if show_ends:
            last_result = "$\n".join(think_to_display)
        else:
            last_result = "\n".join(think_to_display)

        cmd2.Cmd().last_result = last_result
        cmd2.Cmd().poutput(msg=last_result, end="")

    @cmd2.with_argparser(cat_parser)
    @cmd2.with_category("Builtins")
    def do_cat(self, args):
        """Concatenate FILE(s) to standard output"""
        if args.version:  # pragma: no cover
            self.cat_print_version()
            return

        self.cat(
            file=args.file,
            number_nonblank=args.number_nonblank,
            number=args.number,
            show_tabs=args.show_tabs,
            squeeze_blank=args.squeeze_blank,
            show_ends=args.show_ends,
        )  # pragma: no cover

    @staticmethod
    def complete_cat(text, line, begidx, endidx):
        return cmd2.Cmd().path_complete(
            text, line, begidx, endidx, path_filter=os.path.exists
        )  # pragma: no cover
