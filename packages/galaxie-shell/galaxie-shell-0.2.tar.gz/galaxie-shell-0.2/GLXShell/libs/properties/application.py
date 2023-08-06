from GLXShell import APPLICATION_AUTHORS
from GLXShell import APPLICATION_DESCRIPTION
from GLXShell import APPLICATION_LICENSE
from GLXShell import APPLICATION_NAME
from GLXShell import APPLICATION_VERSION
from GLXShell import APPLICATION_WARRANTY


class GLXShPropertyApplication(object):
    def __init__(self):

        self.__authors = None
        self.__description = None
        self.__license = None
        self.__name = None
        self.__version = None
        self.__warranty = None

        self.authors = None
        self.description = None
        self.license = None
        self.name = None
        self.version = None
        self.warranty = None

    @property
    def authors(self):
        """
        it property store authors of the application.

        .. note:: if ``authors`` property value is set to None it return APPLICATION_AUTHORS from
                  Galaxie Shell __init__.py file.

        :return: the authors of the application
        :rtype: list
        """
        return self.__authors

    @authors.setter
    def authors(self, value=None):
        if value is None:
            value = APPLICATION_AUTHORS
        if type(value) != list:
            raise TypeError("'authors' property value must be a list or None")
        if self.authors != value:
            self.__authors = value

    @property
    def description(self):
        """
        it property store description of the application.

        .. note:: if ``description`` property value is set to None it return APPLICATION_DESCRIPTION from
                  Galaxie Shell __init__.py file.

        :return: the description of the application
        :rtype: str
        """
        return self.__description

    @description.setter
    def description(self, value=None):
        if value is None:
            value = APPLICATION_DESCRIPTION
        if type(value) != str:
            raise TypeError("'description' property value must be a str or None")
        if self.description != value:
            self.__description = value

    @property
    def license(self):
        """
        it property store license of the application.

        .. note:: if ``license`` property value is set to None it return APPLICATION_LICENSE from
                  Galaxie Shell __init__.py file.

        :return: the license of the application
        :rtype: str
        """
        return self.__license

    @license.setter
    def license(self, value=None):
        if value is None:
            value = APPLICATION_LICENSE
        if type(value) != str:
            raise TypeError("'license' property value must be a str or None")
        if self.license != value:
            self.__license = value

    @property
    def name(self):
        """
        it property store name of the application.

        .. note:: if ``name`` property value is set to None it return APPLICATION_NAME from
                  Galaxie Shell __init__.py file.

        :return: the name of the application
        :rtype: str
        """
        return self.__name

    @name.setter
    def name(self, value=None):
        if value is None:
            value = APPLICATION_NAME
        if type(value) != str:
            raise TypeError("'name' property value must be a str or None")
        if self.name != value:
            self.__name = value

    @property
    def version(self):
        """
        it property store version of the application.

        .. note:: if ``version`` property value is set to None it return APPLICATION_VERSION from
                  Galaxie Shell __init__.py file.

        :return: the version of the application
        :rtype: str
        """
        return self.__version

    @version.setter
    def version(self, value=None):
        if value is None:
            value = APPLICATION_VERSION
        if type(value) != str:
            raise TypeError("'version' property value must be a str or None")
        if self.version != value:
            self.__version = value

    @property
    def warranty(self):
        """
        it property store warranty of the application.

        .. note:: if ``warranty`` property value is set to None it return APPLICATION_WARRANTY from
                  Galaxie Shell __init__.py file.

        :return: the warranty of the application
        :rtype: str
        """
        return self.__warranty

    @warranty.setter
    def warranty(self, value=None):
        if value is None:
            value = APPLICATION_WARRANTY
        if type(value) != str:
            raise TypeError("'warranty' property value must be a str or None")
        if self.warranty != value:
            self.__warranty = value
