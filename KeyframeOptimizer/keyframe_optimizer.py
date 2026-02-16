import maya.cmds as cmds

"""キーフレーム最適化(ロジックのみ)
"""
class KeyframeOptimizer:
    """test function
    """
    @staticmethod
    def test():
        cmds.sphere(r=10)

    """analyze selection
    return: {obj: {"current": int}}
    """
    @staticmethod
    def analyze_selection():
        selection_ = cmds.ls(sl=True)
        if not selection_:
            return None
        keys_ = {}
        for obj_ in selection_:
            # [時間, 値]のリストを取得
            keysInfo_ = cmds.keyframe( obj_, query=True, valueChange=True, timeChange=True ) or [0]
            keys_[obj_] = {"current": len(keysInfo_[::2])}
        return keys_
    
    """preview optimize
    keys: analyze_selectionの結果
    tolerance: 0.01〜0.1推奨
    return: {obj: {"before": int, "after": int, "reduced": int, "rate": str}}
    """
    @staticmethod
    def preview_optimize(keys, tolerance):
        if not keys:
            return None
        preview_ = {}
        for obj_, info in keys.items():
            # tolerance10%なら30%削減と仮定
            reduceRate_ = tolerance * 0.3  # 10%→30%目安
            estimated_ = max(3, int(info["current"] * (1 - reduceRate_)))  # 最低3キーは残す
            preview_[obj_] = {
                "before": info["current"], 
                "after": estimated_,
                "reduced": info["current"] - estimated_,
                "rate": f"{reduceRate_*100:.0f}%"
            }
        return preview_
        

    """optimize
    tolerance: 0.01〜0.1推奨
    return: True if success, False if no selection
    """
    @staticmethod
    def execute_optimize(tolerance):
        selection = cmds.ls(sl=True)
        if not selection:
            return False
        cmds.simplify(selection, 
                    time=(None, None),          # 全タイムレンジ
                    valueTolerance=tolerance)   # 許容誤差（0.01〜0.1推奨）
        return True
