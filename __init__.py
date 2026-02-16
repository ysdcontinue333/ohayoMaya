# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

from . import ScriptLauncher as scl_gui

# すべてのモジュールはランチャーから起動できるようにする
def main():
    scl_gui.ScriptLauncher_build_gui()
