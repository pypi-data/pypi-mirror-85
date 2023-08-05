#!/usr/bin/env python
# -*- coding: utf-8 -*-

# It script it publish under GNU GENERAL PUBLIC APPLICATION_LICENSE
# http://www.gnu.org/licenses/gpl-3.0.en.html
# Author: the Galaxie Shell Team, all rights reserved
import os
import sys
import argparse

# Require when you haven't GLXCurses as default Package
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(current_dir))

from GLXShell.libs.shell import GLXShell


# https://fallout.fandom.com/wiki/Pip-OS_v7.1.0.8
# https://fallout.fandom.com/wiki/Terminal
# https://fallout.fandom.com/wiki/Unified_Operating_System
# https://fallout.fandom.com/wiki/RETROS_BIOS
# https://fallout.fandom.com/wiki/MF_Boot_Agent


def main(argv=None):
    """Run when invoked from the operating system shell"""

    glxsh_parser = argparse.ArgumentParser(description="Commands as arguments")
    glxsh_parser.add_argument(
        "command",
        nargs="?",
        help="optional commands or file to run, if no commands given, enter an interactive shell",
    )
    glxsh_parser.add_argument(
        "command_args",
        nargs=argparse.REMAINDER,
        help="if commands is not a file use optional arguments for commands",
    )

    args = glxsh_parser.parse_args(argv)

    shell = GLXShell(auto_load_plugins=True)

    sys_exit_code = 0
    if args.command:
        if os.path.isfile(args.command):
            # we have file to execute
            shell.onecmd_plus_hooks("@{command}".format(command=args.command))
        else:
            # we have a commands, run it and then exit
            shell.onecmd_plus_hooks(
                "{command} {args}".format(
                    command=args.command, args=" ".join(args.command_args)
                )
            )
    else:
        # we have no commands, drop into interactive mode
        sys_exit_code = shell.cmdloop()

    return sys_exit_code


if __name__ == "__main__":
    sys.exit(main())
