#!/usr/bin/env python3
import sys
import glob
import subprocess
from setuptools import setup

# TODO: This is a really bulky solution... Rather use SCons here for example.
if glob.glob("thunar_plugins/locale/*.po"):
    cmd = ["make", "-C", "thunar_plugins/locale"]
    print("Running «{}»".format(" ".join(cmd)))
    subprocess.check_output(cmd)

setup()
