# system modules
import logging
import os

# internal modules
from thunar_plugins import l10n

# external modules
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import GObject, Gtk, Thunarx

logger = logging.getLogger(__name__)


class LinkSubmenu(GObject.GObject, Thunarx.MenuProvider):
    name = _("Link Context-Menu")

    description = _(
        "This plugin adds a context menu "
        "for creating symbolic links to files."
    )

    def __init__(self):
        pass

    def get_file_menu_items(self, window, files):
        if len(files) > 1:  # For now only consider single files
            return

        link_menuitem = Thunarx.MenuItem(
            name="ContextMenu::Link",
            label=_("Link"),
            # tooltip="?",
            icon="link",
        )

        link_submenu = Thunarx.Menu()

        link_to_this_file_item = Thunarx.MenuItem(
            name="ContextMenu::Link::ToThisFile",
            icon="insert-link",
            label=_("To this file"),
            tooltip=_("Create a link somewhere else pointing to this file"),
        )
        link_to_this_file_item.connect(
            "activate",
            self.create_link_to_file,
            {"window": window, "files": files},
        )
        link_submenu.append_item(link_to_this_file_item)

        link_menuitem.set_menu(link_submenu)

        return (link_menuitem,)

    def create_link_to_file(self, item, info):
        target_location = info["files"][0].get_location().get_path()
        filechooserdialog = Gtk.FileChooserDialog(
            title=_("Where to create the link?"),
            action=Gtk.FileChooserAction.SAVE,
        )
        filechooserdialog.set_filename(target_location)
        create_link_button = filechooserdialog.add_button(
            _("Create _Link"), Gtk.ResponseType.OK
        )
        cancel_button = filechooserdialog.add_button(
            _("_Cancel"), Gtk.ResponseType.CANCEL
        )
        filechooserdialog.set_default_response(Gtk.ResponseType.CANCEL)
        filechooserdialog.props.do_overwrite_confirmation = True

        relative_checkbutton = Gtk.CheckButton.new_with_mnemonic(
            _("Create a _relative link")
        )

        filechooserdialog.props.extra_widget = relative_checkbutton

        def update_accept_button_text(filechooser, create_link_button):
            if filechooser.get_filename() is not None:
                create_link_button.set_sensitive(True)
                if os.path.exists(filechooser.get_filename()):
                    if os.path.isdir(filechooser.get_filename()):
                        create_link_button.set_label(_("Open _Folder"))
                    else:
                        create_link_button.set_label(_("_Overwrite with Link"))
                else:
                    create_link_button.set_label(_("Create _Link"))
            else:
                create_link_button.set_label(_("Create _Link"))
                create_link_button.set_sensitive(False)

        filechooserdialog.connect(
            "selection-changed", update_accept_button_text, create_link_button
        )

        response = filechooserdialog.run()
        if response == Gtk.ResponseType.OK:
            link_location = filechooserdialog.get_filename()
            if relative_checkbutton.get_active():
                target_location = os.path.relpath(
                    target_location, start=os.path.dirname(link_location)
                )
            filechooserdialog.destroy()
            try:
                if os.path.exists(link_location):
                    logger.info("Removing {}".format(repr(link_location)))
                    os.remove(link_location)
                os.symlink(target_location, link_location)
                logger.info(
                    "Successfully created a link at {} pointing to {}".format(
                        link_location, target_location
                    )
                )
            except OSError as e:
                logger.error(
                    "Couldn't create a link at {} pointing to {}: {}".format(
                        link_location, target_location, e
                    )
                )
                dialog = Gtk.MessageDialog(
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text=_("Couldn't create the link"),
                )
                dialog.format_secondary_markup(
                    _(
                        "While creating a link at\n\n"
                        "<tt><b>{link_location}</b></tt>\n\n"
                        "pointing to\n\n"
                        "<tt><b>{target_location}</b></tt>\n\n"
                        " the following error occured:\n\n"
                        "<b>{error}</b>"
                    ).format(
                        link_location=link_location,
                        target_location=target_location,
                        error=e,
                    )
                )
                dialog.run()
                dialog.destroy()
        else:
            filechooserdialog.destroy()
