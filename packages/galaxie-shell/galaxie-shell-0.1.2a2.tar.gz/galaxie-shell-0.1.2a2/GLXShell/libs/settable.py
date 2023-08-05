import cmd2


class GLXShSettable(object):
    def __init__(self, *args, **kwargs):
        self.shell = kwargs.get("shell", args[0])

    def load_settable(self):
        """
        Set every settable for the shell object
        """

        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_exec",
                bool,
                "Show the exec information line",
                onchange_cb=self.shell.onchange_intro_show_exec,
            )
        )
        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_holotape",
                bool,
                "Show the holotape information line",
                onchange_cb=self.shell.onchange_intro_show_holotape,
            )
        )
        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_license",
                bool,
                "Show the license information line",
                onchange_cb=self.shell.onchange_intro_show_license,
            )
        )
        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_loader",
                bool,
                "Show the loader information line",
                onchange_cb=self.shell.onchange_intro_show_loader,
            )
        )
        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_memory_free",
                bool,
                "Show the memory_free information line",
                onchange_cb=self.shell.onchange_intro_show_memory_free,
            )
        )
        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_memory_total",
                bool,
                "Show the memory_total information line",
                onchange_cb=self.shell.onchange_intro_show_memory_total,
            )
        )

        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_rom",
                bool,
                "Show the rom information line",
                onchange_cb=self.shell.onchange_intro_show_rom,
            )
        )
        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_spacing",
                bool,
                "Show the spacing information line",
                onchange_cb=self.shell.onchange_intro_show_spacing,
            )
        )
        self.shell.add_settable(
            cmd2.Settable(
                "intro_show_title",
                bool,
                "Show the first line into with version information",
                onchange_cb=self.shell.onchange_intro_show_title,
            )
        )
        # PROMPT
        # self.set_window_title(self.window_title)
        self.shell.shortcuts.update({"ll": "shell ls -lah --color=auto"})
        self.shell.add_settable(
            cmd2.Settable(
                "prompt_show_info",
                bool,
                "Show prompt information line",
                onchange_cb=self.shell.onchange_prompt_show_info,
            )
        )
        self.shell.add_settable(
            cmd2.Settable(
                "prompt_show_cursor",
                bool,
                "Show cursor line",
                onchange_cb=self.shell.onchange_prompt_show_cursor,
            )
        )
