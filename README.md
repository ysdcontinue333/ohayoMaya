# ohayoMaya

## モジュール概要
- Mayaスクリプトを追加するリポジトリです。

## 動作環境
- Maya 2026 以上
- Python 3.11.4 以上

## 使用方法
- ohayoMAYAを `~\Documents\maya\2026\scripts` にクローンします。
- Mayaを起動してスクリプトエディタを開きます。
- スクリプトエディタでPythonスクリプトとして「Mayaスクリプト実行例」を実行します。
- "ScriptLauncher"ウィンドウが表示されたら、目的に適したツールをボタンから起動してください。

## Mayaスクリプト実行例 (日常利用)
```
#パッケージ読み込み
import importlib
import ohayoMAYA

#ランチャー起動
ohayoMAYA.main()
```

## Mayaスクリプト実行例 (開発向け)
```
#パッケージ読み込み
import importlib
import ohayoMAYA

#モジュール再読み込み(開発時はスクリプト変更後に実行)
importlib.reload( ohayoMAYA.ScriptLauncher.script_launcher )
importlib.reload( ohayoMAYA.KeyframeOptimizer.keyframe_optimizer )
importlib.reload( ohayoMAYA.KeyframeOptimizer.keyframe_optimizer_gui )

#ランチャー起動
ohayoMAYA.main()

#ツール単体で起動
import ohayoMAYA.KeyframeOptimizer
ohayoMAYA.KeyframeOptimizer.KeyframeOptimizerGUI_build_gui()
```
