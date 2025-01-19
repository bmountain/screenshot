import keyboard
import threading
import tkinter as tk
from pynput import keyboard, mouse


class KeyboardLister(keyboard.Listener):
    """テンキーを取得する"""

    def __init__(self):
        super().__init__(on_press=self.on_press)
        self.daemon = True
        self.stop_event = threading.Event()
        self.mouse_screenshot = threading.Event()

    def on_press(self, key):
        if hasattr(key, "vk") and 96 <= key.vk <= 105:
            print(f"{key} pressed!")
            if key.vk == 97:
                print("1 pressed!")
                self.mouse_screenshot.set()
            if key.vk == 105:
                print("9 pressed! Sending stop request!")
                self.send_stop_signal()

    def send_stop_signal(self):
        self.stop_event.set()


class MouseListener(mouse.Listener):
    """マウスを取得する"""

    def __init__(self):
        super().__init__(on_move=self.on_move, on_click=self.on_click)
        self.daemon = True

    def on_move(self, x, y):
        print("Pointer moved to {0}".format((x, y)))

    def on_click(self, x, y, button, pressed):
        print(
            "{0} {1} at {2}".format(
                button, "Pressed" if pressed else "Released", (x, y)
            )
        )


class App:
    def __init__(self):
        pass

    def run(self):
        keyboard_listener = KeyboardLister()
        mouse_listener = MouseListener()
        keyboard_listener.start()
        mouse_listener.start()
        while True:
            if keyboard_listener.mouse_screenshot.is_set():
                print("would take mouse screenshot")
            if keyboard_listener.stop_event.is_set():
                break
        keyboard_listener.stop_event.wait()


if __name__ == "__main__":
    pass
