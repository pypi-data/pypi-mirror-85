# from __future__ import unicode_literals

# import argparse
import platform
import os
import re
import sys
import errno
from shutil import copy2

# /users/me/Conductor/ciomaya
PKG_DIR = os.path.dirname(os.path.abspath(__file__))
MODULE_DIR = PKG_DIR
PKGNAME = os.path.basename(PKG_DIR)  # ciomaya
MODULE_FILENAME = "conductor.mod"

PLATFORM = sys.platform

def main():
    if not PLATFORM in ["darwin", "win32", "linux"]:
        sys.stderr.write("Unsupported platform: {}".format(PLATFORM))
        sys.exit(1)

    module_dirs = get_maya_module_dirs()
    transform_maya_mod_file(module_dirs)
    sys.stdout.write("Completed Maya Module setup!\n")


def get_maya_module_dirs():
    """Get places to write a modules file."""

    if PLATFORM == "darwin":
        app_dir = "~/Library/Preferences/Autodesk/maya"
    elif PLATFORM == "linux":
        app_dir = "~/maya"
    else:  # windows
        app_dir = "~\Documents\maya"

    # If Maya app dir is set, add it
    mod_dirs = filter(None, [os.environ.get(
        "MAYA_APP_DIR"), os.path.expanduser(app_dir)])

    return [os.path.join(d, "modules") for d in mod_dirs]


def transform_maya_mod_file(module_paths):

    mod_file = os.path.join(MODULE_DIR, MODULE_FILENAME)

    lines = []
    with open(mod_file) as f:
        for i, line in enumerate(f):
            if i == 0:
                lines.append(re.sub(r" \.$",  " {}".format(MODULE_DIR), line))
            else:
                lines.append(line)

    for dest in module_paths:
        try:
            ensure_directory(dest)
        except BaseException:
            sys.stderr.write("Invalid directory: {}\n".format(dest))
            continue

        fn = os.path.join(dest, MODULE_FILENAME)
        with open(fn, "w") as f:
            for line in lines:
                f.write(unicode(line))
        sys.stdout.write("Wrote Maya module file: {}\n".format(fn))


def ensure_directory(directory):
    try:
        os.makedirs(directory)
    except OSError as ex:
        if ex.errno == errno.EEXIST and os.path.isdir(directory):
            pass
        else:
            raise

if __name__ == '__main__':
    main()
