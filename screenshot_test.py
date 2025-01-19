import tkinter as tk
import screeninfo

from PIL import ImageGrab
from datetime import datetime


class MyCanvasApp:
    def __init__(self, root):
        self.root = root

        # Set Variables
        self.rect_id = None
        self.topx, self.topy, self.botx, self.boty = 0, 0, 0, 0
        # Get the current screen width and height
        screen = screeninfo.get_monitors()[0]
        self.screen_width = screen.width
        self.screen_height = screen.height
        # Create root window
        root_geometry = (
            str(self.screen_width) + "x" + str(self.screen_height)
        )  # Creates a geometric string argument
        root.geometry(root_geometry)  # Sets the geometry string value

        root.overrideredirect(True)
        root.wait_visibility(root)
        root.attributes("-alpha", 0.25)  # Set windows transparent

        # Create canvas on root windows
        self.canvas = tk.Canvas(
            root, width=self.screen_width, height=self.screen_height
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
            "<Button-2>", lambda x: root.destroy()
        )  # Quit without screenshot with middle click

    # Get mouse position function
    def get_mouse_posn(self, event):
        self.topx, self.topy = event.x, event.y

    # Update selection rectangle function
    def update_sel_rect(self, event):
        self.botx, self.boty = event.x, event.y
        self.canvas.coords(
            self.rect_id, self.topx, self.topy, self.botx, self.boty
        )  # Update selection rect.

    # Get screenshot function
    def get_screenshot(self, event):

        if self.topx > self.botx:
            self.topx, self.botx = self.botx, self.topx

        if self.topy > self.boty:
            self.topy, self.boty = self.boty, self.topy
        # self.root.after(
        #     15
        # )  ##### Wait for tkinter destruction, increase if you see a tint in your screenshots
        self.root.destroy()  # Destroy tkinter, otherwise a transparent window will be on top of desktop
        filename = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S.png"
        )  # filename determine
        img = ImageGrab.grab(
            bbox=(self.topx, self.topy, self.botx, self.boty)
        )  # Actual screenshot
        img.save(filename)  # Screenshot save to file


def main():
    root = tk.Tk()
    app = MyCanvasApp(root)
    app.root.mainloop()


if __name__ == "__main__":
    main()