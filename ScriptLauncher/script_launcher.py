# -*- coding: utf-8 -*-
"""Script Launcher
Mayaのスクリプトをまとめて起動するためのランチャー。
ツール名のボタンを押下すると、対応するツールが起動する。
"""
import maya.cmds as cmds
import maya.OpenMayaUI as omui 
from shiboken6 import wrapInstance
from PySide6 import QtCore, QtWidgets

# ランチャーから起動させたいモジュール
import ohayoMAYA.KeyframeOptimizer as kfo_gui

class ScriptLauncher(QtWidgets.QMainWindow):
    """スクリプトランチャー(GUI)
    """
    objName_ ='ScriptLauncher'

    def __init__(self, parent=None):
        """コンストラクタ
        """
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        """UIまわりの構築
        """
        windowWidth_ = 300
        windowHeight_ = 450
        windowPosX_ = (1920 / 2.0) - (windowWidth_ / 2.0)
        windowPosY_ = (1080 / 2.0) - (windowHeight_ / 2.0)
        self.setObjectName(self.objName_)
        self.setWindowTitle(self.objName_)
        self.setGeometry(windowPosX_, windowPosY_, windowWidth_, windowHeight_)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window)
        
        centralWidget_ = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget_)
        centralLayout_ = QtWidgets.QVBoxLayout(centralWidget_)

        self.buttonKof = QtWidgets.QPushButton('KeyframeOptimizer')
        self.buttonKof.clicked.connect(self.on_buttonKof_clicked)
        centralLayout_.addWidget(self.buttonKof)
        # レイアウト調整でスペーサーを追加
        verticalSpacer_ = QtWidgets.QWidget()
        verticalSpacer_.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        centralLayout_.addWidget(verticalSpacer_)

    def on_buttonKof_clicked(self):
        """「KeyframeOptimizer」ボタンが押されたときの処理
        """
        kfo_gui.KeyframeOptimizerGUI_build_gui()

def ScriptLauncher_build_gui():
    """ランチャーのGUIを表示する関数
    """
    objName_ = ScriptLauncher.objName_
    if cmds.window(objName_, exists=True):
        cmds.deleteUI(objName_, window=True)
    parent_ = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    if parent_:
        window_ = ScriptLauncher(parent=parent_)
        window_.show()
    return
