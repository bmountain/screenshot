import queue
import keyboard  
import threading
import time
import datetime
import tkinter as tk
# from pynput import keyboard, mouse

def app_main_loop(my_label):
    # Create another thread that monitors the keyboard
    input_queue = queue.Queue()
    kb_input_thread = threading.Thread(target=_check_esc_pressed, args=(input_queue,))
    kb_input_thread.daemon = True
    kb_input_thread.start()
    
    # Main logic loop
    run_active = True
    while True:
        if not input_queue.empty():
            if (run_active) and (input_queue.get() == "esc"):
                # run_active = False
                Lap(my_label)
                # Stop()
        time.sleep(0.1)  # seconds

def _check_esc_pressed(input_queue):
    while True:
        if keyboard.is_pressed('esc'):
            input_queue.put("esc")
        time.sleep(0.1) # seconds

def Lap(my_label):
    my_label.configure(text = datetime.datetime.now())

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