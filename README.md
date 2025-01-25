スクリーンショットを連続で撮影するスクリプト

## 設定

config.json に記述する

-   play_sound: 撮影時に音を出すか

keymap 以下にはキーコードを記述する

-   full_screenshot: フルスクリーンショット
-   mouse_screenshot: マウスでスクリーンショット
-   back: 前の項番に戻る
-   forward: 次の項番に進む
-   exit: 終了

デフォルトではテンキーを割り当てる

## 起動

```bash
python screenshot.py --numbers {1..5} --start 3 --dirname testdir
```

-   --numbers / -n: 項番（必須）
-   --start / -s: 最初の項番（任意）
-   --dirname / -d: 保存先の親ディレクトリ(任意)

## 起動後

マウスで領域を選択するときの操作

-   左ボタン押下：選択開始
-   左ボタンリリース：選択を終了し撮影
-   ホイールクリック：選択中止
