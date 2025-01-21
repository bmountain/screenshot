import asyncio
import glob
import os
import re
import threading
import tkinter as tk
import winsound
from pathlib import Path

import screeninfo
from PIL import ImageGrab
from pynput import keyboard


async def play_sound() -> None:
    """
    スクショした時の音を鳴らす
    """
    winsound.PlaySound(
        r"C:\Windows\Media\Windows Notify System Generic.wav",
        winsound.SND_FILENAME | winsound.SND_ASYNC,
    )


class KeyboardListener(keyboard.Listener):
    """
    テンキー押下を検出してScreenshotAppにイベントを送信する
    """

    def __init__(self, root: tk.Tk) -> None:
        super().__init__(on_press=self.on_press)
        self.daemon = True
        self.root = root

    def on_press(self, key: keyboard.Key | keyboard.KeyCode | None) -> None:
        """
        テンキー押下を検出してScreenshotAppにイベントを送信する

        Args:
            key: 押されたテンキーのキーコード
        """
        if isinstance(key, keyboard.KeyCode):
            if key.vk == 96:
                self.root.event_generate("<<FullScreenshotEvent>>")
            if key.vk == 97:
                self.root.event_generate("<<ScreenshotAppEvent>>")
            if key.vk == 100:
                self.root.event_generate("<<BackEvent>>")
            if key.vk == 102:
                self.root.event_generate("<<ForwardEvent>>")
            if key.vk == 105:
                self.root.event_generate("<<ExitEvent>>")


class ScreenshotApp:
    """スクリーンショットをとる"""

    def __init__(self, root: tk.Tk, dirs: list[Path], dir_idx: int) -> None:
        self.dirs = dirs
        self.dir_idx = dir_idx
        self.root = root
        self.rect_id: int
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.set_root_appearance()
        self.set_canvas_appearance()
        self.reset_cord()
        self.set_bind()
        self.make_app_invisible(event=None)
        keyboard_listener = KeyboardListener(self.root)
        keyboard_listener.start()
        self.prompt()

    def reset_cord(self) -> None:
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.canvas.coords(self.rect_id, 0, 0, 0, 0)

    def set_bind(self):
        """イベントに関数をバインド"""
        # マウスイベント
        self.canvas.bind("<Button-1>", self.get_mouse_posn)
        self.canvas.bind("<B1-Motion>", self.update_sel_rect)
        self.canvas.bind("<ButtonRelease-1>", self.get_mouse_screenshot)
        self.canvas.bind("<Button-2>", self.make_app_invisible)
        # キーボードイベント（KeyboardListenerから取得）
        self.root.bind("<<ScreenshotAppEvent>>", self.on_mouse_screenshot_event)
        self.root.bind("<<FullScreenshotEvent>>", self.on_full_screenshot_event)
        self.root.bind("<<BackEvent>>", self.on_back_event)
        self.root.bind("<<ForwardEvent>>", self.on_forward_event)
        self.root.bind("<<ExitEvent>>", self.on_exit_event)

    def set_root_appearance(self) -> None:
        """外観の設定"""
        # ディスプレイ情報を取得
        screen = screeninfo.get_monitors()[0]
        self.screen_width = screen.width
        self.screen_height = screen.height
        # アプリの外観設定
        self.root.geometry(str(self.screen_width) + "x" + str(self.screen_height))
        self.root.overrideredirect(True)
        self.root.wait_visibility(self.root)
        self.root.attributes("-alpha", 0.25)

    def set_canvas_appearance(self) -> None:
        """マウスでキャプチャする領域の外観設定"""
        self.canvas = tk.Canvas(
            self.root, width=self.screen_width, height=self.screen_height
        )
        self.canvas.config(cursor="cross")
        self.canvas.pack()
        self.rect_id = self.canvas.create_rectangle(
            self.topx,
            self.topy,
            self.botx,
            self.boty,
            dash=(8, 8),
            fill="gray",
            outline="",
        )

    def get_filename(self, fullpath: bool = False) -> str | Path:
        """
        次に保存するファイルの名前またはパスを返す
        ファイル名は<ディレクトリ>-<番号>.pngとする

        Args:
            fullpath: パスを返すか

        Returns:
            ファイル名かパス
        """
        dir = self.dirs[self.dir_idx]
        os.chdir(dir)
        png_list = glob.glob("*.png")

        # 新規ファイルにつける番号は既存ファイルに含まれる最後の数字のうち最大のもの+1
        img_indices: list[int] = []
        pattern = r"(\d+)(?!.*\d)"
        for png in png_list:
            search_result = re.search(pattern, png)
            if search_result is not None:
                img_indices.append(int(search_result.group()))
        if img_indices:
            idx = max(img_indices) + 1
        else:
            idx = 1

        res = str(os.path.basename(dir)) + "-" + str(idx) + ".png"
        if fullpath:
            res = dir / Path(res)
        return res

    def make_app_invisible(self, event: tk.Event | None) -> None:
        """アプリを非表示にする"""
        self.root.withdraw()

    def on_mouse_screenshot_event(self, event: tk.Event) -> None:
        """アプリを表示する"""
        self.root.deiconify()

    def on_full_screenshot_event(self, event: tk.Event) -> None:
        """全画面スクショをとる"""
        filepath = self.get_filename(fullpath=True)
        self.save_full_screenshot(filepath)
        asyncio.run(play_sound())
        print("保存しました > " + str(filepath))
        self.prompt()

    def on_back_event(self, event: tk.Event) -> None:
        """前のディレクトリに戻る"""
        if self.dir_idx > 0:
            self.dir_idx -= 1
        self.prompt()

    def on_forward_event(self, event: tk.Event) -> None:
        """次のディレクトリに進む"""
        if self.dir_idx < len(self.dirs) - 1:
            self.dir_idx += 1
        self.prompt()

    def on_exit_event(self, event: tk.Event) -> None:
        """アプリを終了する"""
        print("Exit")
        self.root.destroy()

    def get_mouse_posn(self, event: tk.Event) -> None:
        """マウスの座標を記録する"""
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event: tk.Event) -> None:
        """マウス選択領域を更新する"""
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)

    def get_mouse_screenshot(self, event: tk.Event) -> None:
        """マウス選択領域をスクショする"""
        self.topx, self.botx = min(self.topx, self.botx), max(self.topx, self.botx)
        self.topy, self.boty = min(self.topy, self.boty), max(self.topy, self.boty)
        self.root.withdraw()
        filepath = self.get_filename(fullpath=True)
        self.save_mouse_screenshot(filepath)
        asyncio.run(play_sound())
        print("保存しました > " + str(filepath))
        self.prompt()
        self.reset_cord()

    def save_mouse_screenshot(self, filepath) -> None:
        """マウススクショの保存"""
        ImageGrab.grab(bbox=(self.topx, self.topy, self.botx, self.boty)).save(
            filepath, quality=100
        )

    def save_full_screenshot(self, filepath) -> None:
        """全画面スクショの保存"""
        ImageGrab.grab().save(filepath, quality=100)

    def prompt(self) -> None:
        """撮影を促すメッセージを出す"""
        print(str(self.get_filename()) + "を撮影してください")


def start_app(dirs, dir_idx) -> None:
    """アプリを起動する"""
    root = tk.Tk()
    app = ScreenshotApp(root, dirs, dir_idx)
    app.root.mainloop()
