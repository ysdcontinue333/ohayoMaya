import maya.cmds as cmds
import maya.OpenMayaUI as omui 
from shiboken6 import wrapInstance
from PySide6 import QtCore, QtWidgets
from .keyframe_optimizer import KeyframeOptimizer as kfo_logic

"""キーフレーム最適化(GUI)
"""
class KeyframeOptimizerGUI(QtWidgets.QDialog):
    objName_ = 'KeyframeOptimizerGUI'
    originalKeys = None
    previewTable_ = None
    toleranceSpinBox_ = None

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName(self.objName_)
        self.setupUi()

    def setupUi(self):
        self.setWindowTitle(self.objName_)
        self.setGeometry(1920/2, 1080/2, 450, 400)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window)

        centralLayout_ = QtWidgets.QVBoxLayout()

        # 分析ボタン
        analyzeBtn_ = QtWidgets.QPushButton("Analyze Selection")
        analyzeBtn_.clicked.connect(self.analyze_keys)
        centralLayout_.addWidget(analyzeBtn_)
        # 許容値
        toleranceLayout_ = QtWidgets.QHBoxLayout()
        toleranceLayout_.addWidget(QtWidgets.QLabel("Tolerance:"))
        self.toleranceSpinBox_ = QtWidgets.QDoubleSpinBox()
        self.toleranceSpinBox_.setValue(0.1)
        self.toleranceSpinBox_.setRange(0.001, 10.0)
        self.toleranceSpinBox_.valueChanged.connect(self.update_preview)
        toleranceLayout_.addWidget(self.toleranceSpinBox_)
        toleranceLayout_.addStretch()
        centralLayout_.addLayout(toleranceLayout_)
        # プレビュー
        self.previewTable_ = QtWidgets.QTableWidget(0, 4)
        self.previewTable_.setHorizontalHeaderLabels(["Object", "Current", "After", "Reduced"])
        self.previewTable_.setMaximumHeight(200)
        centralLayout_.addWidget(QtWidgets.QLabel("プレビュー:"))
        centralLayout_.addWidget(self.previewTable_)
        # 実行
        btnLayout_ = QtWidgets.QHBoxLayout()
        executeBtn_ = QtWidgets.QPushButton("実行")
        executeBtn_.clicked.connect(self.execute_optimize)
        cancelBtn_ = QtWidgets.QPushButton("キャンセル")
        cancelBtn_.clicked.connect(self.reject)
        btnLayout_.addWidget(executeBtn_)
        btnLayout_.addWidget(cancelBtn_)
        centralLayout_.addLayout(btnLayout_)

        self.setLayout(centralLayout_)
        return
    
    def analyze_keys(self):
        print("Analyze clicked")
        self.originalKeys = kfo_logic.analyze_selection()
        if self.originalKeys == None:
            QtWidgets.QMessageBox.warning(self, "警告", "アウトラインでオブジェクトを選択してください。")
            return
        self.update_preview_table(self.originalKeys)
        return

    def update_preview(self):
        if self.originalKeys == None:
            return
        tolerance_ = self.toleranceSpinBox_.value()
        preview_ = kfo_logic.preview_optimize(self.originalKeys, tolerance_)
        self.update_preview_table(preview_)

    def execute_optimize(self):
        tolerance_ = self.toleranceSpinBox_.value()
        if kfo_logic.execute_optimize(tolerance_):
            QtWidgets.QMessageBox.information(self, "完了", "キーフレームを最適化しました。")
            self.close()

    def update_preview_table(self, keys):   
        self.previewTable_.setRowCount(len(keys))
        for i, (obj, info) in enumerate(keys.items()):
            self.previewTable_.setItem(i, 0, QtWidgets.QTableWidgetItem(obj))
            self.previewTable_.setItem(i, 1, QtWidgets.QTableWidgetItem(str(info.get("current", -1))))
            self.previewTable_.setItem(i, 2, QtWidgets.QTableWidgetItem(str(info.get("after", -1))))
            self.previewTable_.setItem(i, 3, QtWidgets.QTableWidgetItem(str(info.get("reduced", -1))))

def KeyframeOptimizerGUI_build_gui():
    objName_ = KeyframeOptimizerGUI.objName_
    if cmds.window(objName_, exists=True):
        cmds.deleteUI(objName_, window=True)
    parent_ = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    if parent_:
        window_ = KeyframeOptimizerGUI(parent=parent_)
        window_.show()
    return
