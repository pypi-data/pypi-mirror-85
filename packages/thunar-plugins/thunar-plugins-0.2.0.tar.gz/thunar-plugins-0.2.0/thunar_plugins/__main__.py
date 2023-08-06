# system modules
import os
import sys
import argparse
from pkg_resources import resource_filename

# internal modules

# external modules


def main():
    extension_dirs = [
        os.path.join(
            d,
            "thunarx-python",
            "extensions",
        )
        for d in (
            [
                os.environ.get(
                    "XDG_DATA_HOME",
                    os.path.join(os.path.expanduser("~"), ".local", "share"),
                )
            ]
            + os.environ.get(
                "XDG_DATA_DIRS", "/usr/local/share:/usr/share"
            ).split(":")
        )
    ]

    activator_link_filename = "thunar-plugins.py"

    parser = argparse.ArgumentParser(
        description="(De)Activate these Thunar plugins"
    )
    parser.add_argument("action", choices={"activate", "deactivate"})
    parser.add_argument(
        "--extensions-dir",
        default=next(
            filter(
                lambda d: os.path.isfile(
                    os.path.join(d, activator_link_filename)
                ),
                extension_dirs,
            ),
            None,
        )
        or extension_dirs[0],
    )
    args = parser.parse_args()

    if args.action == "activate":
        if os.path.exists(args.extensions_dir):
            if not os.path.isdir(args.extensions_dir):
                print(
                    "Thunarx-Python extension directory {} is a file!?".format(
                        repr(args.extensions_dir)
                    )
                )
                sys.exit(1)
        else:
            try:
                os.makedirs(args.extensions_dir)
            except OSError as e:
                print(
                    "Couldn't create Thunarx plugin directory {}: {}".format(
                        repr(args.extensions_dir, e)
                    )
                )
                sys.exit(1)
        activator = resource_filename("thunar_plugins", "activator.py")
        if not os.path.isfile(activator):
            print(
                "The activator {} could not be found. "
                "Is this package properly installed?".format(repr(activator))
            )
            sys.exit(1)
        activator_symlink = os.path.join(
            args.extensions_dir, activator_link_filename
        )
        if os.path.exists(activator_symlink):
            if os.path.islink(activator_symlink):
                if os.path.realpath(activator_symlink) == os.path.realpath(
                    activator
                ):
                    print(
                        "There already is "
                        "an appropriate link {} pointing to {}.".format(
                            repr(activator_symlink), repr(activator)
                        )
                    )
                    sys.exit(0)
                else:
                    print(
                        "There already is link {}, "
                        "but it points to {} instead of {}. "
                        "I'll better leave it that way.".format(
                            repr(activator_symlink),
                            os.path.realpath(activator_symlink),
                            repr(activator),
                        )
                    )
                    sys.exit(1)
            else:
                print(
                    "There is already something at {}, "
                    "but it's not a link to {}. "
                    "I'll stop here...".format(
                        repr(activator_symlink), repr(activator)
                    )
                )
                sys.exit(1)
        else:
            try:
                os.symlink(
                    activator,
                    activator_symlink,
                )
                print(
                    "Created symlink {} pointing to {}".format(
                        repr(activator_symlink), repr(activator)
                    )
                )
            except OSError as e:
                print(
                    "Couldn't symlink {} to {}: {}".format(
                        activator, activator_symlink, e
                    )
                )
                sys.exit(1)
        print("Successfully activated Thunar plugins.")
    elif args.action == "deactivate":
        removed = 0
        for d in filter(os.path.isdir, extension_dirs):
            activator_link = os.path.join(d, activator_link_filename)
            if os.path.exists(activator_link):
                if os.path.islink(activator_link):
                    try:
                        os.remove(activator_link)
                        removed += 1
                        print("Removed {}".format(repr(activator_link)))
                    except OSError as e:
                        print(
                            "Couldn't remove {}: {}".format(
                                repr(activator_link), e
                            )
                        )
                        sys.exit(1)
                else:
                    print(
                        "{} is not a link!? "
                        "I'll better keep my hands off of that...".format(
                            repr(activator_link)
                        )
                    )
        if removed:
            print("Successfully deactivated Thunar plugins.")
        else:
            print("It seems the Thunar plugins weren't even activated...")
            sys.exit(0)
    else:
        print("WTF")
        sys.exit(1)
    print("Please run `thunar -q` (or log out) to close all Thunar instances.")
