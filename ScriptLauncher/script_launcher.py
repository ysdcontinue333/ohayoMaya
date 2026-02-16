import maya.cmds as cmds
import maya.OpenMayaUI as omui 
from shiboken6 import wrapInstance
from PySide6 import QtCore, QtWidgets

# LauncherのGUIから起動させたいツールのインポート
import ohayoMAYA.KeyframeOptimizer as kfo_gui

class ScriptLauncher(QtWidgets.QMainWindow):
    objName_ ='ScriptLauncher'

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setupUi()
        
    def setupUi(self):
        self.setObjectName(self.objName_)
        self.setWindowTitle(self.objName_)
        self.setGeometry(1920/2.0, 1080/2.0, 300, 450)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window)
        
        centralWidget_ = QtWidgets.QWidget()
        self.setCentralWidget(centralWidget_)
        centralLayout_ = QtWidgets.QVBoxLayout(centralWidget_)

        self.button_Kof = QtWidgets.QPushButton('KeyframeOptimizer')
        self.button_Kof.clicked.connect(self.on_button_Kof_clicked)
        centralLayout_.addWidget(self.button_Kof)
        # レイアウト調整でスペーサーを追加
        verticalSpacer_ = QtWidgets.QWidget()
        verticalSpacer_.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        centralLayout_.addWidget(verticalSpacer_)

    def on_button_Kof_clicked(self):
        kfo_gui.KeyframeOptimizerGUI_build_gui()

def ScriptLauncher_build_gui():
    objName_ = ScriptLauncher.objName_
    if cmds.window(objName_, exists=True):
        cmds.deleteUI(objName_, window=True)
    parent_ = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    if parent_:
        window_ = ScriptLauncher(parent=parent_)
        window_.show()
    return
