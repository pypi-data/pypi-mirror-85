from configparser import ConfigParser
import pkg_resources

class ConfigManager:
    def __init__(self) -> None:
        """**\_\_init\_\_**: Creates a ConfigManager object."""
        self.__path = pkg_resources.resource_filename('compling', 'config.ini')
        self.load()

    def load(self) -> None:
        """Loads content of the _config.ini_ file."""
        self.config = ConfigParser(interpolation=None)
        self.config.read(self.__path)

    def cat(self) -> None:
        """Shows the content of the _config.ini_ file as plain-text."""
        with open(self.__path, mode='r') as f:
            cat = f.read()
        print(cat)

    def updates(self, config:dict) -> None:
        """Updates some values of some sections of the _config.ini_ file.

        Args:
           config (dict): New values for some sections.

                    Example:
                    {
                     section1: {
                                k1:v1,
                                k2:v2,
                                ...
                                },
                    ...
                    }
        """
        for section in config:
            for k,v in config[section].items():
                self.config.set(section, k, v)

        # Write changes back to file
        with open(self.__path, mode='w') as f_config:
            self.config.write(f_config)

    def update(self, section, k, v) -> None:
        """Update a _k_ field with a _v_ value in the _s_ section of the _config.ini_ file.

        Args:
           section (str): Section name.
           k (str): Section key.
           v (str): New k value.
        """

        self.config.set(section, k, v)

        # Write changes back to file
        with open(self.__path, mode='w') as f_config:
            self.config.write(f_config)

    def reset(self) -> None:
        """Reset the _config.ini_ file to default conditions."""

        with open(pkg_resources.resource_filename('compling', 'default_config.ini'), mode='r') as f:
            default = f.read()
        with open(self.__path, mode='w') as f:
            f.write(default)

    def whereisconfig(self) -> str:
        """Shows the _config.ini_ file location."""

        return pkg_resources.resource_filename('compling', self.__path)