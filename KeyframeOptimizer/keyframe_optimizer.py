# -*- coding: utf-8 -*-
import maya.cmds as cmds

class KeyframeOptimizer:
    """キーフレーム最適化(ロジックのみ)
    メンバ関数を持たず、すべて静的関数として実装
    """

    @staticmethod
    def get_default_settings():
        """デフォルト値を取得する関数

        Returns:
            dict : キーフレーム最適化のデフォルト設定値の連想配列
        """
        return {
            "radioButtonTimeSelect" : False,
            "timeStartSpinBox": 0.0,
            "timeFinishSpinBox": 0.0, 
            "checkboxAttrTransX": True,
            "checkboxAttrTransY": True,
            "checkboxAttrTransZ": True,
            "checkboxAttrRotX": True,
            "checkboxAttrRotY": True,
            "checkboxAttrRotZ": True,
            "timeTolerance": 0.05,  # maya.cmds.simplifyのデフォルト値
            "valueTolerance": 0.01  # maya.cmds.simplifyのデフォルト値
        }

    @staticmethod
    def analyze_selection():
        """アウトラインで選択されているオブジェクトのキーフレーム数を分析する

        Returns:
            成功: {string: {"KeyCounts": int}} : オブジェクト別のキーフレーム数の連想配列
            失敗: None
        """
        selection_ = cmds.ls(sl=True)
        if not selection_:
            return None
        keys_ = {}
        for obj_ in selection_:
            # [時間, 値]のリストを取得
            keysInfo_ = cmds.keyframe(
                obj_, 
                query=True, 
                valueChange=True, 
                timeChange=True ) or [0]
            keys_[obj_] = {"KeyCounts": len(keysInfo_[::2])}
        return keys_

    @staticmethod
    def execute_optimize(keys, filterSettings):
        """キーフレーム最適化の実行

        Args:
            keys (obj)              : analyze_selection()の実行結果
            filterSettings (dict)   : get_default_settings()の実行結果

        Returns:
            成功: int               : 最適化されたアニメーションカーブの数
            失敗: None              : オブジェクトが未選択
        """
        if not keys:
            return None
        # フィルタを適用するオブジェクトが存在するか確認
        selection_ = list(keys.keys())
        for obj_ in selection_:
            if cmds.objExists(obj_) == False:
                return None
        # すべてのキーが含まれているか
        defaultSettings_ = KeyframeOptimizer.get_default_settings()
        for key_ in defaultSettings_.keys():
            if key_ not in filterSettings:
                return None
        # キーフレームの最適化を実行
        ## 時間指定には秒数やフレーム数があるが、数値のみ指定したときは現在時間の単位で解釈される
        startTime_ = filterSettings["timeStartSpinBox"] if filterSettings["radioButtonTimeSelect"] else None
        endTime_ = filterSettings["timeFinishSpinBox"] if filterSettings["radioButtonTimeSelect"] else None
        curvNum_ = cmds.simplify(
            selection_,
            attribute=[
                "translateX" if filterSettings["checkboxAttrTransX"] else None,
                "translateY" if filterSettings["checkboxAttrTransY"] else None,
                "translateZ" if filterSettings["checkboxAttrTransZ"] else None,
                "rotateX" if filterSettings["checkboxAttrRotX"] else None,
                "rotateY" if filterSettings["checkboxAttrRotY"] else None,
                "rotateZ" if filterSettings["checkboxAttrRotZ"] else None
            ],
            time=(startTime_, endTime_),
            timeTolerance=filterSettings["timeTolerance"],
            valueTolerance=filterSettings["valueTolerance"])
        return curvNum_
