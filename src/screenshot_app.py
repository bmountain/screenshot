import asyncio
import glob
import os
import platform
import re
import tkinter as tk
import winsound
from pathlib import Path
from typing import Any

import screeninfo
from PIL import ImageGrab
from pynput import keyboard
from pynput.keyboard import Key, KeyCode

from .screenshot_utils import Config, Keymap


async def play_sound() -> None:
    """
    スクショした時の音を鳴らす
    """
    if platform.system() == "Windows":
        winsound.PlaySound(
            r"C:\Windows\Media\Windows Notify System Generic.wav",
            winsound.SND_FILENAME | winsound.SND_ASYNC,
        )


class KeyboardListener(keyboard.Listener):
    """
    テンキー押下を検出してScreenshotAppにイベントを送信する
    """

    def __init__(self, root: tk.Tk, keymap: Keymap) -> None:
        super().__init__(
            win32_event_filter=self.win32_event_filter, on_press=self.on_press
        )
        self.keymap = keymap
        self.daemon = True
        self.root = root

    def on_press(self, key: Key | KeyCode | None) -> None:
        """
        キー押下時の処理。
        キーコードがマップされたものであればScreenshotAppにイベントを送信する。

        Args:
            key: 押されたキー
        """
        if not isinstance(key, KeyCode):
            return None

        match key.vk:
            case self.keymap.full_screenshot:
                self.root.event_generate("<<FullScreenshotEvent>>")
            case self.keymap.mouse_screenshot:
                self.root.event_generate("<<MouseScreenshotEvent>>")
            case self.keymap.back:
                self.root.event_generate("<<BackEvent>>")
            case self.keymap.forward:
                self.root.event_generate("<<ForwardEvent>>")
            case self.keymap.exit:
                self.root.event_generate("<<ExitEvent>>")

    def win32_event_filter(self, msg: int, data: Any) -> bool:
        """
        マップされたキーの入力を他のアプリケーションから隠す。
        Windowsでのみ動作する。

        Args:
            msg: 詳細不明
            data: キーに関する情報
        """
        if data.vkCode in self.keymap.model_dump().values():
            self._suppress = True
        else:
            self._suppress = False
        return True


class ScreenshotApp:
    """スクリーンショットをとる"""

    def __init__(
        self, root: tk.Tk, dirs: list[Path], dir_idx: int, config: Config
    ) -> None:
        self.dirs = dirs
        self.dir_idx = dir_idx
        self.play_sound = config.play_sound
        self.root = root
        self.rect_id: int
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.set_root_appearance()
        self.set_canvas_appearance()
        self.make_app_invisible(event=None)
        self.reset_cord()
        self.set_bind()
        keyboard_listener = KeyboardListener(self.root, config.keymap)
        keyboard_listener.start()
        self.prompt()

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

    def make_app_invisible(self, event: tk.Event | None) -> None:
        """アプリを非表示にする"""
        self.root.withdraw()

    def reset_cord(self) -> None:
        """座標の初期化"""
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.canvas.coords(self.rect_id, 0, 0, 0, 0)
        self.root.update()

    def set_bind(self) -> None:
        """イベントに関数をバインド"""
        # マウスイベント
        self.canvas.bind("<Button-1>", self.get_mouse_posn)
        self.canvas.bind("<B1-Motion>", self.update_sel_rect)
        self.canvas.bind("<ButtonRelease-1>", self.get_mouse_screenshot)
        self.canvas.bind("<Button-2>", self.make_app_invisible)
        # キーボードイベント（KeyboardListenerから取得）
        self.root.bind("<<MouseScreenshotEvent>>", self.on_mouse_screenshot_event)
        self.root.bind("<<FullScreenshotEvent>>", self.on_full_screenshot_event)
        self.root.bind("<<BackEvent>>", self.on_back_event)
        self.root.bind("<<ForwardEvent>>", self.on_forward_event)
        self.root.bind("<<ExitEvent>>", self.on_exit_event)

    def on_mouse_screenshot_event(self, event: tk.Event) -> None:
        """アプリを表示する"""
        self.root.deiconify()

    def get_mouse_posn(self, event: tk.Event) -> None:
        """マウスの座標を記録する"""
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event: tk.Event) -> None:
        """マウス選択領域を更新する"""
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)

    def get_mouse_screenshot(self, event: tk.Event) -> None:
        """選択領域をスクショ"""
        topx, botx = min(self.topx, self.botx), max(self.topx, self.botx)
        topy, boty = min(self.topy, self.boty), max(self.topy, self.boty)
        self.reset_cord()
        self.root.withdraw()

        filepath = self.get_filename(fullpath=True)
        self.save_screenshot(filepath, bbox=[topx, topy, botx, boty])
        self.prompt()

    def on_full_screenshot_event(self, event: tk.Event) -> None:
        """全画面スクショ"""
        filepath = self.get_filename(fullpath=True)
        self.save_screenshot(filepath)
        self.prompt()

    def save_screenshot(self, filepath, bbox=None) -> None:
        """
        スクショ保存、サウンド、メッセージ

        Args:
            filepath: 保存先ファイルパス
            bbox: 保存する領域
        """
        if self.play_sound:
            asyncio.run(play_sound())
        ImageGrab.grab(bbox=bbox).save(filepath, quality=100)
        print("保存しました > " + str(filepath))

    def prompt(self) -> None:
        """撮影を促すメッセージを出す"""
        print(str(self.get_filename()) + "を撮影してください")

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
        print("終了します")
        self.root.destroy()

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


def start_app(dirs: list[Path], dir_idx: int, config: Config) -> None:
    """アプリを起動する"""
    root = tk.Tk()
    app = ScreenshotApp(root, dirs, dir_idx, config)
    app.root.mainloop()
