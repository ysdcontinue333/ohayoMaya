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
    # ウィンドウサイズ
    DEFAULT_WINDOW_WIDTH = 600
    DEFAULT_WINDOW_HEIGHT = 600
    DEFAULT_WINDOW_POSX = (1920 / 2.0) - (DEFAULT_WINDOW_WIDTH / 2.0)
    DEFAULT_WINDOW_POSY = (1080 / 2.0) - (DEFAULT_WINDOW_HEIGHT / 2.0)
    # 「タイムレンジ」の定数
    DEFAULT_TIME_START_VALUE = 0.0      # 開始時間 デフォルト値
    STEP_TIME_START_VALUE = 1.0         # 開始時間 SpinBoxのステップ値
    MAX_TIME_START_VALUE = 999999.0     # 開始時間 最大値
    MIN_TIME_START_VALUE = 0.0          # 開始時間 最小値
    DEFAULT_TIME_FINISH_VALUE = 0.0     # 終了時間 デフォルト値
    STEP_TIME_FINISH_VALUE = 1.0        # 終了時間 SpinBoxのステップ値
    MAX_TIME_FINISH_VALUE = 999999.0    # 終了時間 最大値
    MIN_TIME_FINISH_VALUE = 0.0         # 終了時間 最小値
    # 「しきい値」の定数
    DEFAULT_TTOL_VALUE = 0.01           # TimeTolerance  デフォルト値
    STEP_TTOL_VALUE = 0.01              # TimeTolerance  SpinBoxのステップ値
    MAX_TTOL_VALUE = 999999.0           # TimeTolerance  最大値
    MIN_TTOL_VALUE = 0.0                # TimeTolerance  最小値
    DEFAULT_VTOL_VALUE = 0.05           # ValueTolerance デフォルト値
    STEP_VTOL_VALUE = 0.01              # ValueTolerance SpinBoxのステップ値
    MAX_VTOL_VALUE = 999999.0           # ValueTolerance 最大値
    MIN_VTOL_VALUE = 0.0                # ValueTolerance 最小値

    def __init__(self, parent=None):
        """コンストラクタ
        """
        super().__init__(parent)
        # 初期化処理
        self.setObjectName(self.objName_)
        self.setupUi()
        # シグナル接続 (ウィジェットの初期化後に行う)
        self.radioButtonTimeAll.toggled.connect(self.on_timeStartRadioButton_changed)
        self.radioButtonTimeSelect.toggled.connect(self.on_timeStartRadioButton_changed)
        self.executeBtn.clicked.connect(self.on_executeBtn_clicked)
        self.cancelBtn.clicked.connect(self.reject)
        # 初期値
        self.radioButtonTimeAll.setChecked(True)

    def setupUi(self):
        """UIまわりの構築
        """
        windowWidth_ = self.DEFAULT_WINDOW_WIDTH
        windowHeight_ = self.DEFAULT_WINDOW_HEIGHT
        windowPosX_ = self.DEFAULT_WINDOW_POSX
        windowPosY_ = self.DEFAULT_WINDOW_POSY
        self.setWindowTitle(self.objName_)
        self.setGeometry(windowPosX_, windowPosY_, windowWidth_, windowHeight_)
        self.setFixedSize(windowWidth_, windowHeight_)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)
        self.setWindowFlags(QtCore.Qt.Window)

        centralLayout_ = QtWidgets.QVBoxLayout()

        # 「タイムレンジ」
        timeGroupBox_ = QtWidgets.QGroupBox("タイムレンジ")
        timeGroupLayout_ = QtWidgets.QVBoxLayout()
        # 「タイムレンジ」ラジオボタン
        radioButtonTimeGroup_ = QtWidgets.QButtonGroup()
        radioButtonTimeAll_ = QtWidgets.QRadioButton("すべて")
        radioButtonTimeSelect_ = QtWidgets.QRadioButton("時間指定")
        radioButtonTimeGroup_.addButton(radioButtonTimeAll_)
        radioButtonTimeGroup_.addButton(radioButtonTimeSelect_)
        timeRadioLayout_ = QtWidgets.QHBoxLayout()
        timeRadioLayout_.addWidget(radioButtonTimeAll_)
        timeRadioLayout_.addWidget(radioButtonTimeSelect_)
        timeRadioLayout_.addStretch()
        setattr(self, 'radioButtonTimeAll', radioButtonTimeAll_)
        setattr(self, 'radioButtonTimeSelect', radioButtonTimeSelect_)
        # 「タイムレンジ」時間指定
        timeStartLayout_ = QtWidgets.QHBoxLayout()
        timeFinishLayout_ = QtWidgets.QHBoxLayout()
        timeStartLabel_ = QtWidgets.QLabel("開始時間：")
        timeFinishLabel_ = QtWidgets.QLabel("終了時間：")
        timeStartSpinBox_ = QtWidgets.QDoubleSpinBox()
        timeFinishSpinBox_ = QtWidgets.QDoubleSpinBox()
        timeStartSpinBox_.setValue(self.DEFAULT_TIME_START_VALUE)
        timeStartSpinBox_.setSingleStep(self.STEP_TIME_START_VALUE)
        timeStartSpinBox_.setRange(self.MIN_TIME_START_VALUE, self.MAX_TIME_START_VALUE)
        timeFinishSpinBox_.setValue(self.DEFAULT_TIME_FINISH_VALUE)
        timeFinishSpinBox_.setSingleStep(self.STEP_TIME_FINISH_VALUE)
        timeFinishSpinBox_.setRange(self.MIN_TIME_FINISH_VALUE, self.MAX_TIME_FINISH_VALUE)
        timeStartLayout_.addWidget(timeStartLabel_)
        timeStartLayout_.addWidget(timeStartSpinBox_)
        timeFinishLayout_.addWidget(timeFinishLabel_)
        timeFinishLayout_.addWidget(timeFinishSpinBox_)
        setattr(self, 'timeStartLabel', timeStartLabel_)
        setattr(self, 'timeStartSpinBox', timeStartSpinBox_)
        setattr(self, 'timeFinishLabel', timeFinishLabel_)
        setattr(self, 'timeFinishSpinBox', timeFinishSpinBox_)
        #「タイムレンジ」レイアウトを統合する
        timeGroupLayout_.addLayout(timeRadioLayout_)
        timeGroupLayout_.addLayout(timeStartLayout_)
        timeGroupLayout_.addLayout(timeFinishLayout_)
        timeGroupBox_.setLayout(timeGroupLayout_)
        centralLayout_.addWidget(timeGroupBox_)

        #「アトリビュート」
        attrGroupBox_ = QtWidgets.QGroupBox("アトリビュート")
        attrGroupLayout_ = QtWidgets.QVBoxLayout()
        attrCheckBoxes_ = [
            ("移動X", "checkboxAttrTransX"),
            ("移動Y", "checkboxAttrTransY"),
            ("移動Z", "checkboxAttrTransZ"),
            ("回転X", "checkboxAttrRotX"),
            ("回転Y", "checkboxAttrRotY"),
            ("回転Z", "checkboxAttrRotZ")
        ]
        for attrLabel_, attrVariable_ in attrCheckBoxes_:
            cb = QtWidgets.QCheckBox(attrLabel_)
            cb.setChecked(True)
            setattr(self, attrVariable_, cb)  # self.checkboxAttrTransX などの属性で再定義
            attrGroupLayout_.addWidget(cb)
        attrGroupBox_.setLayout(attrGroupLayout_)
        centralLayout_.addWidget(attrGroupBox_)

        # 「しきい値」
        toleranceGroupBox_ = QtWidgets.QGroupBox("しきい値")
        toleranceGroupLayout_ = QtWidgets.QVBoxLayout()
        ttolLayout_ = QtWidgets.QHBoxLayout()
        ttolLabel_ = QtWidgets.QLabel("時間しきい値 [sec] ：")
        vtolLayout_ = QtWidgets.QHBoxLayout()
        vtolLabel_ = QtWidgets.QLabel("変化量しきい値 [float] ：")
        ttolSpinBox_ = QtWidgets.QDoubleSpinBox()
        ttolSpinBox_.setValue(self.DEFAULT_TTOL_VALUE)
        ttolSpinBox_.setSingleStep(self.STEP_TTOL_VALUE)
        ttolSpinBox_.setRange(self.MIN_TTOL_VALUE, self.MAX_TTOL_VALUE)
        ttolSpinBox_.setToolTip("キーフレームの時間の差がこの数値より小さいとき、同じとみなされます。")
        vtolSpinBox_ = QtWidgets.QDoubleSpinBox()
        vtolSpinBox_.setValue(self.DEFAULT_VTOL_VALUE)
        vtolSpinBox_.setSingleStep(self.STEP_VTOL_VALUE)
        vtolSpinBox_.setRange(self.MIN_VTOL_VALUE, self.MAX_VTOL_VALUE)
        vtolSpinBox_.setToolTip("キーフレームの値の差がこの数値より小さいとき、同じとみなされます。")
        ttolLayout_.addWidget(ttolLabel_)
        ttolLayout_.addWidget(ttolSpinBox_)
        vtolLayout_.addWidget(vtolLabel_)
        vtolLayout_.addWidget(vtolSpinBox_)
        toleranceGroupLayout_.addLayout(ttolLayout_)
        toleranceGroupLayout_.addLayout(vtolLayout_)
        toleranceGroupBox_.setLayout(toleranceGroupLayout_)
        centralLayout_.addWidget(toleranceGroupBox_)
        setattr(self, 'ttolSpinBox', ttolSpinBox_)
        setattr(self, 'vtolSpinBox', vtolSpinBox_)

        # 「実行」「キャンセル」ボタン
        btnLayout_ = QtWidgets.QHBoxLayout()
        executeBtn_ = QtWidgets.QPushButton("実行")
        cancelBtn_ = QtWidgets.QPushButton("キャンセル")
        btnLayout_.addWidget(executeBtn_)
        btnLayout_.addWidget(cancelBtn_)
        centralLayout_.addLayout(btnLayout_)
        setattr(self, 'executeBtn', executeBtn_)
        setattr(self, 'cancelBtn', cancelBtn_)

        self.setLayout(centralLayout_)
        return

    def on_executeBtn_clicked(self):
        """「実行」ボタンが押下されたときに実行される関数
        """
        # 時間指定のフィルタ設定に不備がないか確認
        if self.radioButtonTimeSelect.isChecked():
            startTime_ = self.timeStartSpinBox.value()
            finishTime_ = self.timeFinishSpinBox.value()
            if startTime_ >= finishTime_:
                QtWidgets.QMessageBox.warning(self, "警告", "開始時間は終了時間より小さい値にしてください。")
                return
        # アトリビュートが1つも選択されていないときは警告を表示して処理を中断
        translateChecked_ = self.checkboxAttrTransX.isChecked() or self.checkboxAttrTransY.isChecked() or self.checkboxAttrTransZ.isChecked()
        rotateChecked_ = self.checkboxAttrRotX.isChecked() or self.checkboxAttrRotY.isChecked() or self.checkboxAttrRotZ.isChecked()
        if not (translateChecked_ or rotateChecked_):
            QtWidgets.QMessageBox.warning(self, "警告", "最適化するアトリビュートを1つ以上選択してください。")
            return

        # キーフレーム数の分析
        originalKeys_ = kfo_logic.analyze_selection()
        # デフォルト値を取得
        settings_ = kfo_logic.get_default_settings()
        # デフォルト値をGUIの選択状態で上書き
        settings_["radioButtonTimeSelect"] = self.radioButtonTimeSelect.isChecked()
        settings_["timeStartSpinBox"] = self.timeStartSpinBox.value()
        settings_["timeFinishSpinBox"] = self.timeFinishSpinBox.value()
        settings_["checkboxAttrTransX"] = self.checkboxAttrTransX.isChecked()
        settings_["checkboxAttrTransY"] = self.checkboxAttrTransY.isChecked()
        settings_["checkboxAttrTransZ"] = self.checkboxAttrTransZ.isChecked()
        settings_["checkboxAttrRotX"] = self.checkboxAttrRotX.isChecked()
        settings_["checkboxAttrRotY"] = self.checkboxAttrRotY.isChecked()
        settings_["checkboxAttrRotZ"] = self.checkboxAttrRotZ.isChecked()
        settings_["valueTolerance"] = self.vtolSpinBox.value()
        settings_["timeTolerance"] = self.ttolSpinBox.value()
        result_ = kfo_logic.execute_optimize(originalKeys_, settings_)
        if result_ == None:
            QtWidgets.QMessageBox.warning(self, "警告", "フィルタ設定に不備があります。設定を見直してください。")
            return
        QtWidgets.QMessageBox.information(self, "完了", f"キーフレームを最適化しました。{result_}個のアニメーションカーブが最適化されました。")
        # 最適化後のキーフレーム数を分析
        optimizedKeys_ = kfo_logic.analyze_selection()
        # 結果を表示
        resultMessage_ = []
        for obj_ in originalKeys_.keys():    
            originalCount_ = originalKeys_[obj_]["KeyCounts"]
            optimizedCount_ = optimizedKeys_[obj_]["KeyCounts"]
            resultMessage_.append(f"[{obj_}:{originalCount_}→{optimizedCount_}]")
        print("最適化前後のキーフレーム総数：" + ",".join(resultMessage_))

    def on_timeStartRadioButton_changed(self):
        """「タイムレンジ」画面のラジオボタンが変更されたときに実行する関数
        """
        isTimeSelectChecked_ = self.radioButtonTimeSelect.isChecked()
        self.timeStartLabel.setEnabled(isTimeSelectChecked_)
        self.timeStartSpinBox.setEnabled(isTimeSelectChecked_)
        self.timeFinishLabel.setEnabled(isTimeSelectChecked_)
        self.timeFinishSpinBox.setEnabled(isTimeSelectChecked_)
        return

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
