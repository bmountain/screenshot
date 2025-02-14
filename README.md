スクリーンショットを連続で撮影するスクリプトです。

### 設定

config.json に記述します。

-   play_sound: 撮影時に音を出すか

keymap にキーコードを記述する

-   full_screenshot: フルスクリーンショット
-   mouse_screenshot: マウスでスクリーンショット
-   back: 前の項番に戻る
-   forward: 次の項番に進む
-   exit: 終了

デフォルトではテンキーを使用する設定にしています。

### 起動

起動時に以下のオプションを設定します。

-   --numbers / -n: 項番
-   --dirname / -d: 保存先の親ディレクトリ
-   --start / -s: 開始時の項番
-   --help / -h: ヘルプ表示

--numbers か--dirname の少なくとも一方は指定しなければエラーになります。

--numbers オプションの有無で動作が変わります。

#### 新規撮影

```bash
python screenshot.py --dirname testdir --numbers 1 2 3
```

-   このように--numbers オプションをつけると新規撮影を開始します。
-   カレントディレクトリ配下に testdir とその子ディレクトリ 1, 2, 3 が作成されます。

注：

-   --numbers を指定した場合、--dirname は省略できて現在時刻がディレクトリ名となります。
-   --start を指定できます。

#### 撮影継続

```bash
python screenshot.py --dirname testdir --start 2
```

-   このように--numbers オプションがないと testdir の子ディレクトリを項番とみなして撮影を行います。
-   --start オプションに 2 が渡されているので、項番 2 から撮影が始まります。

### 起動後

マウスで領域を選択するときの操作

-   左ボタン押下：選択開始
-   左ボタンリリース：選択を終了し撮影
-   ホイールクリック：選択中止

### 環境

Windows11, GitBash で作成しました。
