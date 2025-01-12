import sys

sys.coinit_flags = 2
from pywinauto.win32_hooks import KeyboardEvent
from pathlib import Path
from threading import Thread

from PIL import ImageGrab
import tkinter as tk
import screeninfo
import glob
import re
import os
import tkinter as tk
import screeninfo

from PIL import Image, ImageGrab
from datetime import datetime
import os


class MyCanvasApp:
    def __init__(self, master):
        self.master = master

        # Set Variables
        self.rect_id = None
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        # Get the current screen width and height
        screen = screeninfo.get_monitors()[0]
        self.screen_width = screen.width
        self.screen_height = screen.height
        # Create master window
        master_geometry = (
            str(self.screen_width) + "x" + str(self.screen_height)
        )  # Creates a geometric string argument
        master.geometry(master_geometry)  # Sets the geometry string value

        master.overrideredirect(True)
        master.wait_visibility(master)
        master.attributes("-alpha", 0.25)  # Set windows transparent

        # Create canvas on root windows
        self.canvas = tk.Canvas(
            master, width=self.screen_width, height=self.screen_height
        )  # Create canvas
        self.canvas.config(cursor="cross")  # Change mouse pointer to cross
        self.canvas.pack()

        # Create selection rectangle (invisible since corner points are equal).
        self.rect_id = self.canvas.create_rectangle(
            self.topx,
            self.topy,
            self.botx,
            self.boty,
            dash=(8, 8),
            fill="gray",
            outline="",
        )

        self.canvas.bind(
            "<Button-1>", self.get_mouse_posn
        )  # Left click gets mouse position
        self.canvas.bind(
            "<B1-Motion>", self.update_sel_rect
        )  # Mouse drag updates selection area
        self.canvas.bind(
            "<ButtonRelease-1>", self.get_screenshot
        )  # Right click gets screenshıt, no selection will result full
        self.canvas.bind(
            "<Button-2>", lambda x: master.destroy()
        )  # Quit without screenshot with middle click
        print("init", self.topx, self.topy, self.botx, self.boty)

    # Get mouse position function
    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y
        print("mouse position event:", event)

    # Update selection rectangle function
    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(
            self.rect_id, self.topx, self.topy, self.botx, self.boty
        )  # Update selection rect.
        print("update event:", event)
        print(self.topx, self.topy, self.botx, self.boty)

    # Get screenshot function
    def get_screenshot(self, event):
        print("in get", self.topx, self.topy, self.botx, self.boty)

        if self.topx > self.botx:
            self.topx, self.botx = self.botx, self.topx

        if self.topy > self.boty:
            self.topy, self.boty = self.boty, self.topy
        # self.master.after(
        #     15
        # )  ##### Wait for tkinter destruction, increase if you see a tint in your screenshots
        self.master.destroy()  # Destroy tkinter, otherwise a transparent window will be on top of desktop
        filename = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S.png"
        )  # filename determine
        img = ImageGrab.grab(
            bbox=(self.topx, self.topy, self.botx, self.boty)
        )  # Actual screenshot
        img.save(filename)  # Screenshot save to file


def take_screenshot_full():
    """全画面スクリーンショットをとる"""
    return ImageGrab.grab()


def take_screenshot_area():
    """マウスで選択した範囲のスクリーンショットをとる"""
    print("in take_screenshot_area")
    img = None
    root = tk.Tk()
    rect_id = None
    # Set Variables
    topx, topy, botx, boty = 0, 0, 0, 0

    # Get the current screen width and height
    screen = screeninfo.get_monitors()[0]
    screen_width = screen.width
    screen_height = screen.height

    print("Screen:", screen_width, screen_height)

    # Get mouse position function
    def get_mouse_posn(event):
        print("in get_mouse_posn")
        nonlocal topy, topx
        topx, topy = event.x, event.y

    # Update selection rectangle function
    def update_sel_rect(event):
        print("update_sel_rect")
        nonlocal topy, topx, botx, boty, rect_id, canvas
        botx, boty = event.x, event.y
        canvas.coords(rect_id, topx, topy, botx, boty)  # Update selection rect.

    # Get screenshot function
    def get_screenshot(event):
        print("in get_screenshot")
        nonlocal topx, topy, botx, boty, root, img

        if topx > botx:  # If mouse drag was right to left
            topx, botx = botx, topx  # Correction for coordinates

        if topy > boty:  # If mouse drag was bottom to top
            topy, boty = boty, topy  # Correction for coordinates

        if topx == botx and topy == boty:  # If no selection was made
            topx, topy = 0, 0
            botx, boty = screen_width, screen_height  # Coordinates for fullscreen

        # root.after(
        #     30
        # )  ##### Wait for tkinter destruction, increase if you see a tint in your screenshots
        img = ImageGrab.grab(bbox=(topx, topy, botx, boty))  # Actual screenshot
        img.save("hoge.png")  # Screenshot save to file
        root.destroy()  # Destroy tkinter, otherwise a transparent window will be on top of desktop

    # Create root window
    root_geometry = (
        str(screen_width) + "x" + str(screen_height)
    )  # Creates a geometric string argument
    root.geometry(root_geometry)  # Sets the geometry string value

    root.overrideredirect(True)
    root.wait_visibility(root)
    root.attributes("-alpha", 0.25)  # Set windows transparent

    # Create canvas on root windows
    canvas = tk.Canvas(root, width=screen_width, height=screen_height)  # Create canvas
    canvas.config(cursor="cross")  # Change mouse pointer to cross
    canvas.pack()

    # Create selection rectangle (invisible since corner points are equal).
    rect_id = canvas.create_rectangle(
        topx, topy, topx, topy, dash=(8, 8), fill="gray", outline=""
    )
    canvas.bind("<Button-1>", get_mouse_posn)  # Left click gets mouse position
    canvas.bind("<B1-Motion>", update_sel_rect)  # Mouse drag updates selection area
    canvas.bind(
        "<Button-3>", get_screenshot
    )  # Right click gets screenshıt, no selection will result full
    canvas.bind(
        "<Button-2>", lambda x: root.destroy()
    )  # Quit without screenshot with middle click
    return root


def get_filename(dirs, dir_idx):
    dir = dirs[dir_idx]
    os.chdir(dir)
    png_list = glob.glob("*.png")
    if len(png_list) == 0:
        idx = 1
    else:
        pattern = r"(\d+)(?!.*\d)"
        img_indexes = [int(re.search(pattern, s).group()) for s in png_list]
        idx = max(img_indexes) + 1
    res = str(os.path.basename(dir)) + "-" + str(idx) + ".png"
    return res


class ScreenShot:
    def __init__(self, dirs, dir_idx=0):
        self.dirs = dirs
        self.dir_idx = dir_idx
        print(get_filename(self.dirs, self.dir_idx) + "を撮影してください")

    def on_event(self, event):
        if isinstance(event, KeyboardEvent):
            save_dir_path = self.dirs[self.dir_idx]
            file_name = get_filename(self.dirs, self.dir_idx)
            file_path = save_dir_path / Path(file_name)
            print(f"{file_name}を撮影してください")

            # メインディスプレイの全体を取得
            if event.current_key == "Numpad0" and event.event_type == "key down":

                img = take_screenshot_full()
                img.save(file_path, quality=100)
                print("保存しました > " + str(file_path))

            # TODO: 0を押した後で1を押すと動作がおかしくなる
            # 選択範囲を取得
            if event.current_key == "Numpad1" and event.event_type == "key down":
                print("1 pressed")

                root = tk.Tk()
                app = MyCanvasApp(root)
                print("befor main loop")
                app.master.mainloop()
                print("after mainloop")

            if event.current_key == "Numpad4" and event.event_type == "key down":
                if self.dir_idx == 0:
                    pass
                else:
                    self.dir_idx -= 1

            if event.current_key == "Numpad6" and event.event_type == "key down":
                if self.dir_idx == len(self.dirs) - 1:
                    pass
                else:
                    self.dir_idx += 1


if __name__ == "__main__":
    take_screenshot_area()
