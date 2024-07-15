from PIL import Image
import numpy as np
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

def load_image(image_path):
    return Image.open(image_path)

def save_image(image, image_path):
    image.save(image_path)

def encrypt_image(image, key):
    image_array = np.array(image)
    key_array = np.full_like(image_array, key, dtype=np.uint8)
    encrypted_array = np.bitwise_xor(image_array, key_array)
    
    np.random.seed(key)
    indices = np.arange(image_array.size)
    np.random.shuffle(indices)
    encrypted_array_flat = encrypted_array.flatten()
    encrypted_array_flat = encrypted_array_flat[indices]
    encrypted_array = encrypted_array_flat.reshape(image_array.shape)
    
    encrypted_image = Image.fromarray(encrypted_array)
    return encrypted_image, indices

def decrypt_image(encrypted_image, key, indices):
    encrypted_array = np.array(encrypted_image)
    
    decrypted_array_flat = np.zeros_like(encrypted_array.flatten())
    decrypted_array_flat[indices] = encrypted_array.flatten()
    decrypted_array = decrypted_array_flat.reshape(encrypted_array.shape)
    
    key_array = np.full_like(decrypted_array, key, dtype=np.uint8)
    decrypted_array = np.bitwise_xor(decrypted_array, key_array)
    
    decrypted_image = Image.fromarray(decrypted_array)
    return decrypted_image

def encrypt_action():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            key = int(key_entry.get())
            image = load_image(file_path)
            encrypted_image, indices = encrypt_image(image, key)
            save_image(encrypted_image, "encrypted_image.png")
            np.save("indices.npy", indices)  # Save indices to a file
            messagebox.showinfo("Success", "Image encrypted and saved as encrypted_image.png")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid key (integer).")

def decrypt_action():
    file_path = filedialog.askopenfilename()
    if file_path:
        try:
            key = int(key_entry.get())
            encrypted_image = load_image(file_path)
            indices = np.load("indices.npy")  # Load indices from the file
            decrypted_image = decrypt_image(encrypted_image, key, indices)
            save_image(decrypted_image, "decrypted_image.png")
            messagebox.showinfo("Success", "Image decrypted and saved as decrypted_image.png")
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid key (integer).")
        except FileNotFoundError:
            messagebox.showerror("Error", "Indices file not found. Ensure you have encrypted an image first.")

root = tk.Tk()
root.title("Image Encryption Tool")

tk.Label(root, text="Enter Encryption Key:").pack(pady=10)
key_entry = tk.Entry(root)
key_entry.pack(pady=10)

tk.Button(root, text="Encrypt Image", command=encrypt_action).pack(pady=10)
tk.Button(root, text="Decrypt Image", command=decrypt_action).pack(pady=10)

root.mainloop()
