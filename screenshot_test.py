import tkinter as tk
import screeninfo

from PIL import ImageGrab
from datetime import datetime
import threading
from pynput import keyboard


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
            if key.vk == 97:
                self.root.event_generate("<<MouseScreenshotEvent>>")
            if key.vk == 96:
                self.root.event_generate("<<FullScreenshotEvent>>")
            if key.vk == 105:
                self.root.event_generate("<<ExitEvent>>")
            if key.vk == 100:
                self.root.event_generate("<<BackEvent>>")
            if key.vk == 102:
                self.root.event_generate("<<ForwardEvent>>")


class MouseScreenshot:
    def __init__(self, root):
        self.root = root
        self.rect_id = None
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        self.set_root_appearance()
        self.set_canvas_appearance()
        self.set_bind()
        self.make_app_invisible()
        keyboard_listener = KeyboardListener(self.root)
        keyboard_listener.start()

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
        self.root_geometry = str(self.screen_width) + "x" + str(self.screen_height)
        self.root.geometry(self.root_geometry)
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

    def make_app_invisible(self, event=None):
        self.root.withdraw()

    def on_mouse_screenshot_event(self, event):
        self.root.deiconify()

    def on_full_screenshot_event(self, event):
        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")
        img = ImageGrab.grab()
        img.save(filename)

    def on_back_event(self, event):
        print("back event!")

    def on_forward_event(self, event):
        print("forward event!")

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

        filename = datetime.now().strftime("%Y-%m-%d_%H-%M-%S.png")
        img = ImageGrab.grab(bbox=(self.topx, self.topy, self.botx, self.boty))
        img.save(filename)


def main():
    root = tk.Tk()
    app = MouseScreenshot(root)
    app.root.mainloop()


if __name__ == "__main__":
    main()
