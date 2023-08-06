# system modules
import os
import configparser

# internal modules

# external modules


class Configuration(configparser.ConfigParser):
    def __init__(self, *args, **kwargs):
        configparser.ConfigParser.__init__(
            self, *args, **{**{"allow_no_value": True}, **kwargs}
        )

    @property
    def path(cls):
        return os.path.join(
            os.environ.get("XDG_CONFIG_HOME")
            or os.path.join(os.path.expanduser("~"), ".config"),
            "Thunar",
            "plugins.conf",
        )

    @property
    def blacklist_section(self):
        if "blacklist" not in self:
            self.add_section("blacklist")
        return self["blacklist"]

    def plugin_is_blacklisted(self, entry_point):
        package = entry_point.dist.key or "?"
        for item in self.blacklist_section:
            if (
                ".".join([package, entry_point.name]) == item
                or (entry_point.dist.key or "?") == item
            ):
                return True
        return False

    def blacklist(self, package, entry_point_name=None):
        if entry_point_name is None:
            self.blacklist_section[str(package)] = "all"
        else:
            self.blacklist_section[
                ".".join(map(str, (package, entry_point_name)))
            ] = "yes"

    def save(self):
        if not os.path.isdir(os.path.dirname(self.path)):
            os.makedirs(os.path.dirname(self.path))
        with open(self.path, "w") as fh:
            self.write(fh)

    def load(self):
        self.read(self.path)
