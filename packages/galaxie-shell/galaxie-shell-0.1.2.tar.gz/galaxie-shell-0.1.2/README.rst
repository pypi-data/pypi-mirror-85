.. image:: https://codecov.io/gl/Tuuux/galaxie-shell/branch/master/graph/badge.svg?token=MK6WWGAL5M
   :target: https://codecov.io/gl/Tuuux/galaxie-shell

.. image:: https://readthedocs.org/projects/galaxie-shell/badge/?version=latest
   :target: https://galaxie-shell.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation Status

GLXSH - Galaxie Shell
=====================

.. figure::  https://galaxie-shell.readthedocs.io/en/latest/_images/logo_galaxie.png
   :align:   center

Galaxie Shell is a Reliable Event Logging Protocol (`RELP <https://en.wikipedia.org/wiki/Reliable_Event_Logging_Protocol>`_) write with `python <https://www.python.org/>`_ and based on top cmd2.

Home page: `https://gitlab.com/Tuuux/galaxie-shell <https://gitlab.com/Tuuux/galaxie-shell>`_

The Galaxie Shell use a  a **builtins plugin** and `GNU Core Utils <https://www.maizure.org/projects/decoded-gnu-coreutils/>`_ command's set as specs.

All ready implemented features
------------------------------
* History files respect the Freedesktop requirements
* All unknown command's are send to the sub shell system
* Capability to build a **one-file** static binary file
* Can load a script file as argument
* Can execute command from passing arguments
* Interactive shell when call without arguments
* Plugins Manager
* Builtins Plugin (arch, cat, cd, mkdir, pwd, rmdir, uname, which, etc ...)

Application
------------
* Use on front of a [Unikernel](https://fr.wikipedia.org/wiki/Unikernel)
* Use on front of a minimal Alpine Linux or OpenWrt
* Simplify CI CD
* Project starter

Installation via pip
--------------------

.. code:: bash

    pip install galaxie-shell

Installation via pip (test)
---------------------------

.. code:: bash

    pip install -i https://test.pypi.org/simple/ galaxie-shell


Next Step:
----------

Now you can the start the **glxsh** entry point

.. code:: bash

  $> glxsh
  ******************************* GLXSHELL V0.1A5 *******************************


  GNU GENERAL PUBLIC LICENSE GPL-3.0
  LOADER #1 SMP DEBIAN 4.19.146-1 (2020-09-17)
  EXEC VENV PYTHON 3.7.3
  31.36GB RAM SYSTEM
  22.70GB FREE
  NO HOLOTAPE FOUND
  LOAD ROM(1): DEITRIX 303

  >

or use the python package

.. code-block:: python

  #!/usr/bin/env python

  import os
  import sys
  import argparse

  from GLXShell.libs.shell import GLXShell

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

      shell = GLXShell()

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




Builtins Plugin implemented implemented command's
-------------------------------------------------
* arch
* `cat <https://galaxie-shell.readthedocs.io/en/latest/mans/cat.html>`_
* `cd <https://galaxie-shell.readthedocs.io/en/latest/mans/cd.html>`_
* mkdir
* `pwd <https://galaxie-shell.readthedocs.io/en/latest/mans/pwd.html>`_
* rmdir
* uname
* which

Roadmap
-------
* implement the core util's
* plugins installation system based on pip
* permit **&&** and **||**
* deal with **env** and **ewport**
* deal with exit code
* better onefile binary distrinution