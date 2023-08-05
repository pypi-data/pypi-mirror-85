import configparser
import os
from abc import abstractmethod, ABC
from pathlib import Path


class AbstractConfig(ABC):
    @abstractmethod
    def _getitem(self, item):
        pass

    def __getitem__(self, item):
        if isinstance(item, int):
            return self.items()[item]
        return self._getitem(item)

    def items(self):
        return [(key, self[key]) for key in self.keys()]

    def __len__(self):
        return len(self.items())

    @abstractmethod
    def keys(self):
        pass

    def family(self, cls):
        for cls in family(cls):
            key = cls.__name__
            try:
                return self[key]
            except (KeyError, configparser.NoOptionError):
                pass
        raise KeyError(
            f"No configuration found for {cls.__name__}"
        )


class SectionConfig(AbstractConfig):
    def __init__(self, path, section):
        self.path = path
        self.section = section
        self.parser = configparser.ConfigParser()
        self.parser.read(path)

    def keys(self):
        return [item[0] for item in self.parser.items(self.section)]

    def _getitem(self, item):
        try:
            result = self.parser.get(
                self.section,
                item
            )
            if result.lower() == "true":
                return True
            if result.lower() == "false":
                return False
            if result.lower() in ("none", "null"):
                return None
            if result.isdigit():
                return int(result)
            try:
                return float(result)
            except ValueError:
                return result
        except (configparser.NoSectionError, configparser.NoOptionError):
            raise KeyError(
                f"No configuration found for {item} at path {self.path}"
            )


class NamedConfig(AbstractConfig):
    """Parses generic config"""

    def __init__(self, config_path):
        """
        Parameters
        ----------
        config_path: String
            The path to the config file
        """
        self.path = config_path
        self.parser = configparser.ConfigParser()
        self.parser.read(self.path)

    def keys(self):
        return self.parser.sections()

    def _getitem(self, item):
        return SectionConfig(
            self.path,
            item,
        )


class RecursiveConfig(AbstractConfig):
    def keys(self):
        return [
            path.split(".")[0]
            for path
            in os.listdir(self.path)
        ]

    def __init__(self, path):
        self.path = Path(path)

    def __str__(self):
        return str(self.path)

    def __repr__(self):
        return f"<{self.__class__.__name__} {self.path}>"

    def _getitem(self, item):
        item_path = self.path / f"{item}"
        file_path = f"{item_path}.ini"
        if os.path.isfile(file_path):
            return NamedConfig(
                file_path
            )
        if os.path.isdir(item_path):
            return RecursiveConfig(
                item_path
            )
        raise KeyError(
            f"No configuration found for {item} at path {self.path}"
        )


class PriorConfigWrapper:
    def __init__(self, prior_configs):
        self.prior_configs = prior_configs

    def for_class_and_suffix_path(self, cls, path):
        for config in self.prior_configs:
            try:
                return config.for_class_and_suffix_path(
                    cls, path
                )
            except KeyError:
                pass
        directories = ' '.join(
            str(config.directory) for config in self.prior_configs
        )
        raise KeyError(
            f"No prior config found for class {cls.__name__} and path {'.'.join(path)} in directories {directories}"
        )


class ConfigWrapper(AbstractConfig):
    def __init__(self, configs):
        self.configs = configs

    @property
    def paths(self):
        return [
            config.path
            for config
            in self.configs
        ]

    def __applicable(self, item):
        __applicable = list()
        for config in self.configs:
            try:
                __applicable.append(config[item])
            except KeyError:
                pass
        return __applicable

    def items(self):
        item_dict = {}
        for config in reversed(
                self.configs
        ):
            for key, value in config.items():
                item_dict[key] = value
        return list(item_dict.items())

    def keys(self):
        keys = set()
        for config in self.configs:
            keys.update(config.keys())
        return list(keys)

    def _getitem(self, item):
        configs = self.__applicable(item)
        if len(configs) == 0:
            paths = '\n'.join(map(str, self.paths))
            raise KeyError(
                f"No configuration for {item} in {paths}"
            )
        for config in configs:
            if not isinstance(
                    config, AbstractConfig
            ):
                return config
        return ConfigWrapper(configs)


def family(current_class):
    yield current_class
    for next_class in current_class.__bases__:
        for val in family(next_class):
            yield val
