import cmd2


class GLXShPropertyShortcuts(object):
    def __init__(self):
        self.__shortcuts = None
        self.shortcuts = dict(cmd2.DEFAULT_SHORTCUTS)

    @property
    def shortcuts(self):
        """
        Store the shortcuts

        :return: dictionary containing shortcuts for commands. If not supplied,
                 then defaults to cmd2.DEFAULT_SHORTCUTS. If you do not want
                 any shortcuts, pass an empty dictionary.
        :rtype: dict
        """
        return self.__shortcuts

    @shortcuts.setter
    def shortcuts(self, value=None):
        """
        Set the ``shortcuts`` property value

        Notes: ``None`` will restore default value cmd2.DEFAULT_SHORTCUTS

        :param value: dictionary containing shortcuts for commands. If not supplied,
                      then defaults to cmd2.DEFAULT_SHORTCUTS. If you do not want
                      any shortcuts, pass an empty dictionary
        :type value: dict or None
        """
        if value is None:
            value = {}
        if type(value) != dict:
            raise TypeError("'shortcuts' must be a dict type or None")
        if value != self.shortcuts:
            self.__shortcuts = value
