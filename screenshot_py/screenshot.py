from pywinauto.win32_hooks import KeyboardEvent
from PIL import ImageGrab

import glob, re, os
from pathlib import Path


class ScreenShot:
    def __init__(self, dirs, dir_idx=0):
        self.dirs = dirs
        self.dir_idx = dir_idx
        self.explain()
        self.prompt()

    def explain(self):
        explanation = """
#####
テンキーで操作します
0: 撮影
4: 前のディレクトリへ
6: 次のディレクトリへ
#####
"""
        print(explanation)

    def take_screenshot_full(self):
        """全画面スクリーンショットをとる"""
        return ImageGrab.grab()

    def get_filename(self, fullpath=False):
        """ディレクトリリストとインデックスを渡すと次に取得するスクショのファイル名を返す。
        fullpath=Trueならそのパスを返す。
        """
        dir = self.dirs[self.dir_idx]
        os.chdir(dir)
        png_list = glob.glob("*.png")
        # ファイル名は<ディレクトリ>-<番号>とする
        if len(png_list) == 0:
            idx = 1
        else:
            pattern = r"(\d+)(?!.*\d)"
            img_indexes = [int(re.search(pattern, s).group()) for s in png_list]
            idx = max(img_indexes) + 1
        res = str(os.path.basename(dir)) + "-" + str(idx) + ".png"
        if fullpath:
            res = dir / Path(res)
        return res

    def prompt(self):
        print(self.get_filename() + "を撮影してください")

    def on_event(self, event):
        if isinstance(event, KeyboardEvent):

            # メインディスプレイの全体を取得
            if event.current_key == "Numpad0" and event.event_type == "key down":
                filepath = self.get_filename(fullpath=True)
                self.take_screenshot_full().save(filepath, quality=100)
                print("保存しました > " + str(filepath))
                self.prompt()

            if event.current_key == "Numpad4" and event.event_type == "key down":
                if self.dir_idx == 0:
                    pass
                else:
                    self.dir_idx -= 1
                self.prompt()

            if event.current_key == "Numpad6" and event.event_type == "key down":
                if self.dir_idx == len(self.dirs) - 1:
                    pass
                else:
                    self.dir_idx += 1
                self.prompt()


if __name__ == "__main__":
    pass
