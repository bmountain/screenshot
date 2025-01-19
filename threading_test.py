import keyboard  
import threading
import tkinter as tk
from pynput import keyboard, mouse


def on_press(key):
    if hasattr(key, 'vk') and 96 <= key.vk <= 105:
        print(f'{key} pressed!')

def on_move(x, y):
    print('Pointer moved to {0}'.format(
        (x, y)))

def on_click(x, y, button, pressed):
    print('{0} at {1}'.format(
        'Pressed' if pressed else 'Released',
        (x, y)))

def app_main_loop(my_label):
    keyboard_listener = keyboard.Listener(
        on_press=on_press,
     )
    keyboard_listener.daemon = True
    keyboard_listener.start()
    mouse_listener = mouse.Listener(
        on_move=on_move, on_click=on_click
    )
    mouse_listener.daemon = True
    mouse_listener.start()
    
def record_event(input_queue):
    """キーボード・マウスのイベントを記録する"""
    pass
    

def show_message(message):
    my_label.configure(text = message)

def Stop():
    print("Stopped")

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