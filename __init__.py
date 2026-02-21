# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

from . import ScriptLauncher as scl_gui

def main():
    """すべてのモジュールはランチャーから起動する
    """
    scl_gui.ScriptLauncher_build_gui()
