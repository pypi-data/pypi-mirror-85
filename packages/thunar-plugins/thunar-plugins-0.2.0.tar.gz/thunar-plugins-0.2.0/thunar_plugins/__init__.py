# system modules
import logging
import warnings
import os
import pkg_resources

# GObject Introspection
import gi

gi.require_version("Thunarx", "3.0")
gi.require_version("Gtk", "3.0")

# internal modules
import thunar_plugins.version
from thunar_plugins.version import __version__
import thunar_plugins.l10n
import thunar_plugins.menus
import thunar_plugins.config

# external modules

THUNAR_PLUGIN_ENTRY_POINT_NAME = "thunar_plugin"


logging.basicConfig(
    level=logging.DEBUG
    if os.environ.get("THUNAR_PLUGINS_DEBUG")
    else logging.WARNING
)

logger = logging.getLogger(__name__)


def get_available_plugins(also_blacklisted=True):
    available_plugins = {}
    if not also_blacklisted:
        config = thunar_plugins.config.Configuration()
        config.load()
    for entry_point in filter(
        (lambda x: True)
        if also_blacklisted
        else lambda e: not config.plugin_is_blacklisted(e),
        pkg_resources.iter_entry_points(THUNAR_PLUGIN_ENTRY_POINT_NAME),
    ):
        try:
            entry_point_obj = entry_point.load()
        except BaseException as e:
            warnings.warn(
                "Couldn't load {} entry-point {} from {}: {}".format(
                    repr(THUNAR_PLUGIN_ENTRY_POINT_NAME),
                    repr(entry_point.name),
                    repr(entry_point.dist or "unknown distribution"),
                    e,
                )
            )
            continue
        logger.info(
            "Found {} entry-point {} ({}) from {}".format(
                repr(THUNAR_PLUGIN_ENTRY_POINT_NAME),
                repr(entry_point.name),
                repr(entry_point_obj),
                repr(entry_point.dist or "unknown distribution"),
            )
        )
        available_plugins[entry_point] = entry_point_obj
    return available_plugins
