import cmd2
import sys
import platform

from GLXShell.plugins.builtins import PLUGIN_VERSION
from GLXShell.plugins.builtins import PLUGIN_DESCRIPTION
from GLXShell.plugins.builtins import PLUGIN_WARRANTY

uname_parser = cmd2.Cmd2ArgumentParser()
uname_parser.add_argument(
    "-a",
    "--all",
    action="store_true",
    help="print all information, in the following order, except omit -p and -i if unknown",
)
uname_parser.add_argument(
    "-s", "--kernel-name", action="store_true", help="print the kernel name"
)
uname_parser.add_argument(
    "-n", "--nodename", action="store_true", help="print the network node hostname"
)
uname_parser.add_argument(
    "-r", "--kernel-release", action="store_true", help="print the kernel release"
)
uname_parser.add_argument(
    "-v", "--kernel-version", action="store_true", help="print the kernel version"
)
uname_parser.add_argument(
    "-m", "--machine", action="store_true", help="print the machine hardware name"
)
uname_parser.add_argument(
    "-p",
    "--processor",
    action="store_true",
    help="print the processor type (non-portable)",
)
uname_parser.add_argument(
    "-i",
    "--hardware-platform",
    action="store_true",
    help="print the hardware platform (non-portable)",
)
uname_parser.add_argument(
    "-o", "--operating-system", action="store_true", help="print the operating system"
)
uname_parser.add_argument(
    "--version", action="store_true", help="output version information and exit"
)


class GLXUname(cmd2.CommandSet):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.stdout = kwargs.get("stdout", sys.stdout)
        self.stdin = kwargs.get("stdin", sys.stdin)
        self.stderr = kwargs.get("stdin", sys.stderr)

    def uname_print_version(self):
        cmd2.Cmd().poutput(
            "uname ({name}) v{version}\n{licence}".format(
                name=PLUGIN_DESCRIPTION,
                version=PLUGIN_VERSION,
                licence=PLUGIN_WARRANTY,
            )
        )
        self.stdout.flush()

    @staticmethod
    def uname(
        all_info=False,
        kernel_name=False,
        nodename=False,
        kernel_release=False,
        kernel_version=False,
        machine=False,
        processor=False,
        hardware_platform=False,
        operating_system=False,
    ):
        line = []
        if all_info:
            kernel_name = True
            nodename = True
            kernel_release = True
            kernel_version = True
            machine = True
            processor = False
            hardware_platform = False
            operating_system = True

        if kernel_name:
            line.append(platform.uname().system)

        if nodename:
            line.append(platform.uname().node)

        if kernel_release:
            line.append(platform.uname().release)

        if kernel_version:
            line.append(platform.uname().version)

        if machine:
            line.append(platform.uname().machine)

        if processor:
            if len(platform.uname().processor) <= 0:
                line.append("unknown")
            else:  # pragma: no cover
                line.append(platform.uname().processor)

        if hardware_platform:
            line.append("unknown")

        if operating_system:
            line.append(sys.platform)

        # print the default value
        if len(line) <= 0:
            line.append(platform.uname().system)

        if line:
            cmd2.Cmd().poutput(f'{" ".join(line)}')
            cmd2.Cmd().last_result = f'{" ".join(line)}'

    @cmd2.with_argparser(uname_parser)
    @cmd2.with_category("Builtins")
    def do_uname(self, args):
        """
        Print certain system information.

        :param args: Arguments like -a
        :type args: args or None
        """
        if args.version:  # pragma: no cover
            self.uname_print_version()
            return

        self.uname(
            all_info=args.all,
            kernel_name=args.kernel_name,
            nodename=args.nodename,
            kernel_release=args.kernel_release,
            kernel_version=args.kernel_version,
            machine=args.machine,
            processor=args.processor,
            hardware_platform=args.hardware_platform,
            operating_system=args.operating_system,
        )  # pragma: no cover
