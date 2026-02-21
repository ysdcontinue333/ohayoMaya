# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.OpenMayaUI as omui 
from shiboken6 import wrapInstance
from PySide6 import QtCore, QtWidgets
from .keyframe_optimizer import KeyframeOptimizer as kfo_logic

class KeyframeOptimizerGUI(QtWidgets.QDialog):
    """キーフレーム最適化(GUI)
    """
    objName_ = 'KeyframeOptimizerGUI'
    originalKeys = None
    previewTable_ = None
    toleranceSpinBox_ = None

    def __init__(self, parent=None):
        """コンストラクタ
        """
        super().__init__(parent)
        self.setObjectName(self.objName_)
        self.setupUi()

    def setupUi(self):
        """UIまわりの構築
        """
        windowWidth_ = 600
        windowHeight_ = 450
        windowPosX_ = (1920 / 2.0) - (windowWidth_ / 2.0)
        windowPosY_ = (1080 / 2.0) - (windowHeight_ / 2.0)
        self.setWindowTitle(self.objName_)
        self.setGeometry(windowPosX_, windowPosY_, windowWidth_, windowHeight_)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window)

        centralLayout_ = QtWidgets.QVBoxLayout()

        # 分析ボタン
        analyzeBtn_ = QtWidgets.QPushButton("選択中のオブジェクトを分析")
        analyzeBtn_.clicked.connect(self.on_analyzeBtn_clicked)
        centralLayout_.addWidget(analyzeBtn_)
        # 許容値
        toleranceLayout_ = QtWidgets.QHBoxLayout()
        toleranceLayout_.addWidget(QtWidgets.QLabel("Tolerance:"))
        self.toleranceSpinBox_ = QtWidgets.QDoubleSpinBox()
        self.toleranceSpinBox_.setValue(0.01)
        self.toleranceSpinBox_.setSingleStep(0.01)
        self.toleranceSpinBox_.setRange(0.01, 100.0)
        self.toleranceSpinBox_.valueChanged.connect(self.on_toleranceSpinBox_changed)
        toleranceLayout_.addWidget(self.toleranceSpinBox_)
        toleranceLayout_.addStretch()
        centralLayout_.addLayout(toleranceLayout_)
        # プレビュー
        previewLabel_ = QtWidgets.QLabel("最適化のプレビュー")
        centralLayout_.addWidget(previewLabel_)
        self.previewTable_ = QtWidgets.QTableWidget(0, 4)
        self.previewTable_.setHorizontalHeaderLabels(["オブジェクト名", "適用前", "適用後", "差分"])
        self.previewTable_.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        centralLayout_.addWidget(self.previewTable_)
        # 実行
        btnLayout_ = QtWidgets.QHBoxLayout()
        executeBtn_ = QtWidgets.QPushButton("実行")
        executeBtn_.clicked.connect(self.on_executeBtn_clicked)
        cancelBtn_ = QtWidgets.QPushButton("キャンセル")
        cancelBtn_.clicked.connect(self.reject)
        btnLayout_.addWidget(executeBtn_)
        btnLayout_.addWidget(cancelBtn_)
        centralLayout_.addLayout(btnLayout_)

        self.setLayout(centralLayout_)
        return
    
    def on_analyzeBtn_clicked(self):
        """「分析」ボタンが押下されたときに実行される関数
        """
        self.originalKeys = kfo_logic.analyze_selection()
        if self.originalKeys == None:
            QtWidgets.QMessageBox.warning(self, "警告", "アウトラインでオブジェクトを選択してください。")
            return
        self.update_preview_table(self.originalKeys)
        return

    def on_toleranceSpinBox_changed(self):
        """SpinBoxの値が変更されたときに実行される関数
        """
        if self.originalKeys == None:
            QtWidgets.QMessageBox.warning(self, "警告", "アウトラインでオブジェクトを選択してください。")
            return
        tolerance_ = self.toleranceSpinBox_.value()
        preview_ = kfo_logic.preview_optimize(self.originalKeys, tolerance_)
        self.update_preview_table(preview_)

    def on_executeBtn_clicked(self):
        """「実行」ボタンが押下されたときに実行される関数
        """
        tolerance_ = self.toleranceSpinBox_.value()
        result_ = kfo_logic.execute_optimize(self.originalKeys, tolerance_)
        if result_ == None:
            QtWidgets.QMessageBox.warning(self, "警告", "オブジェクトが存在しないか、選択されていません。")
            return
        QtWidgets.QMessageBox.information(self, "完了", f"キーフレームを最適化しました。{result_}個のアニメーションカーブが最適化されました。")
        self.close()

    def update_preview_table(self, keys):
        """プレビューテーブルを更新する関数
        """
        self.previewTable_.setRowCount(len(keys))
        for i, (obj, info) in enumerate(keys.items()):
            self.previewTable_.setItem(i, 0, QtWidgets.QTableWidgetItem(obj))
            self.previewTable_.setItem(i, 1, QtWidgets.QTableWidgetItem(str(info.get("current", -1))))
            self.previewTable_.setItem(i, 2, QtWidgets.QTableWidgetItem(str(info.get("after", -1))))
            self.previewTable_.setItem(i, 3, QtWidgets.QTableWidgetItem(str(info.get("reduced", -1))))

def KeyframeOptimizerGUI_build_gui():
    """キーフレーム最適化GUIを表示する関数
    """
    objName_ = KeyframeOptimizerGUI.objName_
    if cmds.window(objName_, exists=True):
        cmds.deleteUI(objName_, window=True)
    parent_ = wrapInstance(int(omui.MQtUtil.mainWindow()), QtWidgets.QMainWindow)
    if parent_:
        window_ = KeyframeOptimizerGUI(parent=parent_)
        window_.show()
    return
