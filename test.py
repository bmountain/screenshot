import tkinter as tk
from PIL import ImageGrab


class ScreenshotApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=500, height=300, bg="white")
        self.canvas.pack()

        self.start_x = None
        self.start_y = None
        self.rect = None

        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<B1-Motion>", self.on_drag)
        self.canvas.bind("<ButtonRelease-1>", self.on_release)

    def on_click(self, event):
        self.start_x = event.x
        self.start_y = event.y

    def on_drag(self, event):
        if self.rect:
            self.canvas.delete(self.rect)
        self.rect = self.canvas.create_rectangle(
            self.start_x, self.start_y, event.x, event.y
        )

    def on_release(self, event):
        x1 = min(self.start_x, event.x)
        y1 = min(self.start_y, event.y)
        x2 = max(self.start_x, event.x)
        y2 = max(self.start_y, event.y)

        # ウィンドウ全体の座標を取得
        x = self.root.winfo_rootx() + self.canvas.winfo_x()
        y = self.root.winfo_rooty() + self.canvas.winfo_y()

        # 画像の切り抜き
        im = ImageGrab.grab(bbox=(x + x1, y + y1, x + x2, y + y2))
        im.save("screenshot.png")


if __name__ == "__main__":
    root = tk.Tk()
    app = ScreenshotApp(root)
    root.mainloop()  #!/usr/bin/env python
