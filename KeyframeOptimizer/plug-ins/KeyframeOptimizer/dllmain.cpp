/*------------------------------------------------------------------------------------------------
    @author : KaiYoshida
    @note   : 使用方法
              プロジェクトをビルドしてプラグイン( MLL ファイル)を生成する。
              Maya の plug-ins フォルダにプラグインを配置して Maya を起動する。
              'PluginInfo_Name' を MEL コマンドとして実行すると、ここで定義した処理が実行される。
------------------------------------------------------------------------------------------------*/

#include "pch.h"
#include <maya/MFnPlugin.h>
#include <maya/MPxCommand.h>
#include <maya/MGlobal.h>

#include <maya/MItSelectionList.h>
#include <maya/MAnimUtil.h>
#include <maya/MFnAnimCurve.h>
#include <string>


// 定数定義
const char* PluginInfo_Vender = "KaiYoshida";   // 制作元
const char* PluginInfo_Version = "0.0.1";       // バージョン番号
const char* PluginInfo_Name = "KeyframeOptimizer";   // MELコマンド名

// プロトタイプ宣言
MStatus checkData();


/// @param 独自のMELコマンドクラス
class KeyframeOptimizer : public MPxCommand {
public:
    // MPxCommandクラスのdoItメソッドをオーバーライド
    virtual MStatus doIt(const MArgList& args) {
        checkData();
        return MStatus::kSuccess;
    }
};

/// @brief プラグインの登録処理
MStatus initializePlugin(MObject obj) {
    MFnPlugin plugin(obj, PluginInfo_Vender, PluginInfo_Version);
    MStatus status = plugin.registerCommand(PluginInfo_Name, []()->void* { return new KeyframeOptimizer; });
    CHECK_MSTATUS(status);
    return status;
}

/// @brief プラグインの解放処理
MStatus uninitializePlugin(MObject obj) {
    MFnPlugin plugin(obj);
    MStatus status = plugin.deregisterCommand(PluginInfo_Name);
    CHECK_MSTATUS(status);
    return status;
}

/// @brief  キーフレーム最適化を考える
/// @return MStatus 成功時にMStatus::kSuccess、失敗時にそれ以外を返す
MStatus checkData() {
    MStatus status;             // Mayaのステータスコード
    MSelectionList sel;         // 選択対象のMObjectのリスト
    MPlugArray animatedPlugs;   // MPlugsの配列, オブジェクトのアトリビュート情報
    MObjectArray outCurves;     // MObjectの配列, アトリビュートのキーフレーム情報
    MTime animTime;             // キーフレームの時間
    double animValue;           // キーフレームの値
    unsigned int i, j;

    // 選択状態になっているオブジェクトのリストを取得
    status = MGlobal::getActiveSelectionList(sel);
    if (!status) {
        return MStatus::kFailure;
    }

    // オブジェクトのアトリビュートの配列を取得
    if (!MAnimUtil::findAnimatedPlugs(sel, animatedPlugs, false, &status)) {
        return status;
    }

    // アトリビュートのキーフレームを取得する
    for (i = 0; i < animatedPlugs.length(); ++i) {
        //MString plugName = animatedPlugs[i].name();
        //MGlobal::displayInfo(plugName);
        MObjectArray animNodes;
        if (!MAnimUtil::findAnimation(animatedPlugs[i], animNodes, &status)) {
            continue;
        }
        for (j = 0; j < animNodes.length(); ++j) {
            if (animNodes[j].hasFn(MFn::kAnimCurve)) {
                outCurves.append(animNodes[j]);
            }
        }
    }

    // アトリビュートのキーフレームを出力する
    for (i = 0; i < outCurves.length(); ++i) {
        MFnAnimCurve fn(outCurves[i], &status);
        if (!status) {
            continue;
        }
        for (i = 0; i < fn.numKeys(); ++i) {
            animTime = fn.time(i);
            animValue = fn.value(i);
            MGlobal::displayInfo(fn.name() + " key " + i + " time=" + animTime.value() + " value=" + animValue);
        }
    }

    return MStatus::kSuccess;
}

