import re
import tkinter as tk
from tkinter import messagebox

def check_password_strength(password):
    # Initialize the strength counter and feedback list
    strength = 0
    feedback = []

    # Criteria checks
    length_criteria = len(password) >= 8
    uppercase_criteria = re.search(r'[A-Z]', password) is not None
    lowercase_criteria = re.search(r'[a-z]', password) is not None
    number_criteria = re.search(r'[0-9]', password) is not None
    special_char_criteria = re.search(r'[@$!%*?&]', password) is not None

    # Increment strength counter based on criteria
    if length_criteria:
        strength += 1
    else:
        feedback.append("Password should be at least 8 characters long.")
        
    if uppercase_criteria:
        strength += 1
    else:
        feedback.append("Password should contain at least one uppercase letter.")
        
    if lowercase_criteria:
        strength += 1
    else:
        feedback.append("Password should contain at least one lowercase letter.")
        
    if number_criteria:
        strength += 1
    else:
        feedback.append("Password should contain at least one number.")
        
    if special_char_criteria:
        strength += 1
    else:
        feedback.append("Password should contain at least one special character (@$!%*?&).")

    # Provide feedback based on strength
    if strength == 5:
        feedback.insert(0, "Password strength: Very Strong")
    elif strength == 4:
        feedback.insert(0, "Password strength: Strong")
    elif strength == 3:
        feedback.insert(0, "Password strength: Moderate")
    elif strength == 2:
        feedback.insert(0, "Password strength: Weak")
    else:
        feedback.insert(0, "Password strength: Very Weak")

    return feedback

def check_password():
    password = password_entry.get()
    feedback = check_password_strength(password)
    messagebox.showinfo("Password Strength", "\n".join(feedback))

# GUI setup
root = tk.Tk()
root.title("Password Complexity Checker")

tk.Label(root, text="Enter your password:").pack(pady=10)
password_entry = tk.Entry(root, show='*', width=50)
password_entry.pack(pady=10)

tk.Button(root, text="Check Password Strength", command=check_password).pack(pady=20)

root.mainloop()
