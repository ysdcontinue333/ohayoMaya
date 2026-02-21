# -*- coding: utf-8 -*-
import maya.cmds as cmds

class KeyframeOptimizer:
    """キーフレーム最適化(ロジックのみ)
    メンバ関数を持たず、すべて静的関数として実装
    """

    @staticmethod
    def analyze_selection():
        """アウトラインで選択されているオブジェクトのキーフレーム数を分析する

        Returns:
            成功: {string: {"current": int}} : オブジェクト別のキーフレーム数の連想配列
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
            keys_[obj_] = {"current": len(keysInfo_[::2])}
        return keys_
    
    @staticmethod
    def preview_optimize(keys, tolerance):
        """キーフレーム最適化のプレビューを生成する

        Args:
            keys (obj): analyze_selectionの実行結果
            tolerance (int): 精度(0.01〜0.1推奨,値が大きいほどキーフレームが減る)

        Returns:
            成功: {obj: {"current": int, "after": int, "reduced": int}} : オブジェクト別の最適化前後と削減数の連想配列
            失敗: None : オブジェクトが未選択
        """
        if not keys:
            return None
        preview_ = {}
        for obj_, info in keys.items():
            # toleranceが10%ならキーフレームは30%削減と仮定
            reduceRate_ = tolerance * 0.3  # 10%→30%目安
            estimated_ = max(3, int(info["current"] * (1.0 - reduceRate_)))  # 最低3キーは残る想定
            preview_[obj_] = {
                "current": info["current"], 
                "after": estimated_,
                "reduced": info["current"] - estimated_
            }
        return preview_

    @staticmethod
    def execute_optimize(keys, tolerance):
        """キーフレーム最適化の実行

        Args:
            keys (obj): analyze_selectionの実行結果
            tolerance (int): 精度(0.01〜0.1推奨,値が大きいほどキーフレームが減る)

        Returns:
            成功: True : キーフレーム最適化した
            失敗: False : オブジェクトが未選択

        tolerance: 0.01〜0.1推奨
        return: True if success, False if no selection
        """
        if not keys:
            return False
        selection_ = list(keys.keys())
        cmds.simplify(
            selection_, 
            time=(None, None),
            valueTolerance=tolerance)
        return True
