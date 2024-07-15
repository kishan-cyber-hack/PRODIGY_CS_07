import tkinter as tk
from tkinter import messagebox

def encrypt(text, shift):
    encrypted_text = ""
    for char in text:
        if char.isalpha():
            shift_base = 65 if char.isupper() else 97
            encrypted_text += chr((ord(char) - shift_base + shift) % 26 + shift_base)
        else:
            encrypted_text += char
    return encrypted_text

def decrypt(text, shift):
    return encrypt(text, -shift)

def perform_action(action):
    text = message_entry.get()
    try:
        shift = int(shift_entry.get())
    except ValueError:
        messagebox.showerror("Invalid Input", "Shift value must be an integer.")
        return
    
    if action == "encrypt":
        result = encrypt(text, shift)
    elif action == "decrypt":
        result = decrypt(text, shift)
    
    result_label.config(text=f"Result: {result}")

# GUI setup
root = tk.Tk()
root.title("Text Encryptor/Decryptor")

# Message input
tk.Label(root, text="Enter your message:").pack(pady=5)
message_entry = tk.Entry(root, width=50)
message_entry.pack(pady=5)

# Shift value input
tk.Label(root, text="Enter the shift value (integer):").pack(pady=5)
shift_entry = tk.Entry(root, width=10)
shift_entry.pack(pady=5)

# Action buttons
tk.Button(root, text="Encrypt", command=lambda: perform_action("encrypt")).pack(pady=5)
tk.Button(root, text="Decrypt", command=lambda: perform_action("decrypt")).pack(pady=5)

# Result label
result_label = tk.Label(root, text="Result: ")
result_label.pack(pady=10)

root.mainloop()
