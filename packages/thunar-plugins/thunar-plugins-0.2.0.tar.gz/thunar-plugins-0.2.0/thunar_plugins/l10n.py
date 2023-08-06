# system modules
import locale
import gettext
from pkg_resources import resource_filename

# internal modules

# external modules


GETTEXT_DOMAIN = "thunar-plugins"
LOCALEDIR = resource_filename("thunar_plugins", "locale")

# set up localization
locale.setlocale(locale.LC_ALL, "")
for mod in [locale, gettext]:
    mod.bindtextdomain(GETTEXT_DOMAIN, LOCALEDIR)
gettext.textdomain(GETTEXT_DOMAIN)
gettext.install(GETTEXT_DOMAIN, localedir=LOCALEDIR)
