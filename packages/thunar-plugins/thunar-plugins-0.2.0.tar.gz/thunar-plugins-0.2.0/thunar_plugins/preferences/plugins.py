# system modules
import logging
import re
import pkg_resources
import collections
import random

# internal modules
import thunar_plugins

# external modules
import gi

from gi.repository import GObject, Gtk, Thunarx

logger = logging.getLogger(__name__)


class PluginPreferences(GObject.GObject, Thunarx.PreferencesProvider):
    def __init__(self):
        logger.debug(self.__init__)

    @property
    def config(self):
        try:
            return self._config
        except AttributeError:
            self._config = thunar_plugins.config.Configuration()
            self._config.load()
        return self._config

    @property
    def ui(self):
        try:
            return self._ui
        except AttributeError:
            self._ui = Gtk.Builder()
            self._ui.set_translation_domain(thunar_plugins.l10n.GETTEXT_DOMAIN)
            self._ui.add_from_file(
                pkg_resources.resource_filename(
                    "thunar_plugins.ui", "plugin-preferences.glade"
                )
            )

            handlers = {
                "hideInfoBar": lambda i, *a, **kw: i.set_revealed(False),
                "onPluginRowActivated": (
                    lambda t, p, c: self.on_plugin_row_activated(t, p)
                ),
            }
            self._ui.connect_signals(handlers)
        return self._ui

    name = _("Python Plugin Preferences")

    description = _(
        "This plugin adds a preference menu to "
        "Thunar enabling the (de)activation "
        "of specific Thunar Python plugins."
    )

    def children_activation_states(self, row):
        states = []
        for child in row.iterchildren():
            states.append(child[0])
            states.extend(self.children_activation_states(child))
        return states

    def children_activation_state(self, row):
        states = self.children_activation_states(row)
        if all(states):
            return True
        if all(s is False for s in states):
            return False
        return None

    def update_inconsistent_state(self, row):
        children_state = self.children_activation_state(row)
        row[0] = children_state
        row[2] = True if children_state is None else False

    def update_blacklist_config(self, treestore):
        # set the blacklist config, first clear it
        self.config.blacklist_section.clear()
        for package_row in treestore:
            package = (
                "?"
                if package_row[3] == _("unknown package")
                else package_row[3]
            )
            if not package_row[2]:  # not inconsistent
                if not package_row[0]:
                    self.config.blacklist(package=package)
            # TODO: Remember, we're only recursing one layer here!
            for plugin_row in package_row.iterchildren():
                if not plugin_row[0]:
                    self.config.blacklist(
                        package=package,
                        entry_point_name=plugin_row[4],
                    )
        self.config.save()

    def show_infobar(
        self,
        markup,
        message_type=Gtk.MessageType.INFO,
    ):
        infobox = self.ui.get_object("plugin-preferences-infobox")
        infobox_label = self.ui.get_object("plugin-preferences-infobox-label")
        infobox.set_message_type = message_type
        infobox_label.set_markup(markup)
        if infobox.props.revealed:
            infobox.props.revealed = False
        infobox.props.revealed = True

    def on_plugin_row_activated(self, treeview, path):
        treestore = treeview.get_model()
        row = treestore[path]
        # Prevent un-deactivatable plugins from deactivation
        if not row[1] and row[0]:
            self.show_infobar(
                _("You can't disable this plugin.")
                if row.get_parent()
                else _("You can't disable this package."),
                Gtk.MessageType.ERROR,
            )
            return
        self.set_plugin_row_recursively(row, not row[0])
        parent = row.get_parent()
        if parent:
            self.update_inconsistent_state(parent)
        self.update_blacklist_config(treestore)
        self.show_infobar(
            _(
                "You will need to <i>completely</i> close "
                "Thunar in order for the changes to take effect. "
                "You can do that by either logging out or running "
                "<b><tt>thunar -q</tt></b> in a terminal."
            ),
        )

    def set_plugin_row_recursively(self, row, state):
        row[0] = state
        row[2] = False
        for nested_row in row.iterchildren():
            self.set_plugin_row_recursively(nested_row, state)

    def get_preferences_menu_items(self, window):
        item = Thunarx.MenuItem(
            name="Preferences::Plugins",
            label=_("Plugins"),
            tooltip=_("Configure installed Python plugins"),
            icon="preferences-activities",
        )
        item.connect("activate", self.__open_plugin_preferences, window)
        return (item,)

    def __open_plugin_preferences(self, action, window):
        dialog = self.ui.get_object("plugin-preferences-dialog")
        plugins_treestore = self.ui.get_object("plugins-treestore")
        plugins_treestore.clear()
        plugins_by_package = collections.defaultdict(list)
        for (
            entry_point,
            plugin,
        ) in thunar_plugins.get_available_plugins().items():
            plugins_by_package[entry_point.dist].append((entry_point, plugin))
        self.config.load()
        for dist, entry_points in plugins_by_package.items():
            dist_iter = plugins_treestore.append(
                None,
                (
                    None,  # don't know activation state yet, will be updated later
                    dist.key
                    != "thunar-plugins",  # You can disable any package except the core package
                    True,  # just say it's inconsistent for now...
                    dist.key if dist else _("unknown package"),
                    None,
                    None,
                    None,
                ),
            )
            for entry_point, plugin in entry_points:
                plugin_activated = not self.config.plugin_is_blacklisted(
                    entry_point
                )
                plugins_treestore.append(
                    dist_iter,
                    (
                        plugin_activated,
                        plugin is not type(self),
                        False,
                        dist.key if dist else _("unknown package"),
                        entry_point.name,
                        str(getattr(plugin, "name"))
                        if hasattr(plugin, "name")
                        else plugin.__name__,
                        str(
                            re.sub(
                                r"[\r\n]+",
                                r" ",
                                getattr(plugin, "description"),
                            )
                        )
                        if hasattr(plugin, "description")
                        else "",
                    ),
                )
            self.update_inconsistent_state(plugins_treestore[dist_iter])
        self.ui.get_object("plugins-treeview").expand_all()
        for row in plugins_treestore:
            logger.debug(row[:])
            for nestedrow_row in row.iterchildren():
                logger.debug("    {}".format(nestedrow_row[:]))
        dialog.set_transient_for(window)
        response = dialog.run()
        dialog.hide()
