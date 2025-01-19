import keyboard  
import threading
import tkinter as tk
from pynput import keyboard, mouse

class KeyboardLister(keyboard.Listener):
    """テンキーを取得する"""
    def __init__(self):
        super().__init__(on_press=self.on_press)
        self.daemon = True
    def on_press(self, key):
        if hasattr(key, 'vk') and 96 <= key.vk <= 105:
            print(f'{key} pressed!')

class MouseListener(mouse.Listener):
    """マウスを取得する"""
    def __init__(self):
        super().__init__(on_move=self.on_move, on_click=self.on_click)
        self.daemon = True
    def on_move(self, x, y):
        print('Pointer moved to {0}'.format(
            (x, y)))
    def on_click(self, x, y, button, pressed):
        print('{0} at {1}'.format(
            'Pressed' if pressed else 'Released',
            (x, y)))

def app_main_loop(my_label):
    keyboard_listener = KeyboardLister()
    keyboard_listener.start()
    mouse_listener = MouseListener()
    mouse_listener.start()
    
if __name__ == "__main__":
    # Create the ui
    root = tk.Tk()
    # root.attributes("-fullscreen", True)
    my_label = tk.Label(root, text="Hello World!")
    my_label.pack()
    
    # Run the app's main logic loop in a different thread
    main_loop_thread = threading.Thread(target=app_main_loop, args=(my_label, ))
    main_loop_thread.daemon = True
    main_loop_thread.start()
    
    # Run the UI's main loop
    root.mainloop()