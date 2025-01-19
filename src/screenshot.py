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


async def get_sound():
    winsound.PlaySound(
        "C:\Windows\Media\Windows Notify System Generic.wav",
        winsound.SND_FILENAME | winsound.SND_ASYNC,
    )


class KeyboardListener(keyboard.Listener):
    """テンキーを取得してtkinterにイベントを送信"""

    def __init__(self, root):
        super().__init__(on_press=self.on_press)
        self.daemon = True
        self.stop_event = threading.Event()
        self.mouse_screenshot = threading.Event()
        self.root = root

    def on_press(self, key):
        if hasattr(key, "vk") and 96 <= key.vk <= 105:
            if key.vk == 96:
                self.root.event_generate("<<FullScreenshotEvent>>")
            if key.vk == 97:
                self.root.event_generate("<<MouseScreenshotEvent>>")
            if key.vk == 100:
                self.root.event_generate("<<BackEvent>>")
            if key.vk == 102:
                self.root.event_generate("<<ForwardEvent>>")
            if key.vk == 105:
                self.root.event_generate("<<ExitEvent>>")


class MouseScreenshot:
    def __init__(self, root, dirs, dir_idx=0):
        self.dirs = dirs
        self.dir_idx = dir_idx
        self.root = root
        self.rect_id = None
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.set_root_appearance()
        self.set_canvas_appearance()
        self.reset_cord()
        self.set_bind()
        self.make_app_invisible()
        keyboard_listener = KeyboardListener(self.root)
        keyboard_listener.start()
        self.prompt()

    def reset_cord(self):
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
        self.root.bind("<<MouseScreenshotEvent>>", self.on_mouse_screenshot_event)
        self.root.bind("<<FullScreenshotEvent>>", self.on_full_screenshot_event)
        self.root.bind("<<BackEvent>>", self.on_back_event)
        self.root.bind("<<ForwardEvent>>", self.on_forward_event)
        self.root.bind("<<ExitEvent>>", self.on_exit_event)

    def set_root_appearance(self):
        """外観の設定"""
        screen = screeninfo.get_monitors()[0]
        self.screen_width = screen.width
        self.screen_height = screen.height
        self.root.geometry(str(self.screen_width) + "x" + str(self.screen_height))
        self.root.overrideredirect(True)
        self.root.wait_visibility(self.root)
        self.root.attributes("-alpha", 0.25)

    def set_canvas_appearance(self):
        """マウスキャプチャモード時の外観設定"""
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

    def make_app_invisible(self, event=None):
        self.root.withdraw()

    def on_mouse_screenshot_event(self, event):
        self.root.deiconify()

    def on_full_screenshot_event(self, event):
        filepath = self.get_filename(fullpath=True)
        self.save_full_screenshot(filepath)
        asyncio.run(get_sound())
        print("保存しました > " + str(filepath))
        self.prompt()

    def on_back_event(self, event):
        if self.dir_idx > 0:
            self.dir_idx -= 1
        self.prompt()

    def on_forward_event(self, event):
        if self.dir_idx < len(self.dirs) - 1:
            self.dir_idx += 1
        self.prompt()

    def on_exit_event(self, event):
        print("Exit")
        self.root.destroy()

    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y

    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(self.rect_id, self.topx, self.topy, self.botx, self.boty)

    def get_mouse_screenshot(self, event):
        self.topx, self.botx = min(self.topx, self.botx), max(self.topx, self.botx)
        self.topy, self.boty = min(self.topy, self.boty), max(self.topy, self.boty)
        self.root.withdraw()
        filepath = self.get_filename(fullpath=True)
        self.save_mouse_screenshot(filepath)
        asyncio.run(get_sound())
        print("保存しました > " + str(filepath))
        self.prompt()
        self.reset_cord()

    def save_mouse_screenshot(self, filepath):
        ImageGrab.grab(bbox=(self.topx, self.topy, self.botx, self.boty)).save(
            filepath, quality=100
        )

    def save_full_screenshot(self, filepath):
        ImageGrab.grab().save(filepath, quality=100)

    def prompt(self):
        print(self.get_filename() + "を撮影してください")


def start(dirs, dir_idx):
    root = tk.Tk()
    app = MouseScreenshot(root, dirs, dir_idx)
    app.root.mainloop()
