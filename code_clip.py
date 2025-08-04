import tkinter as tk
from tkinter import filedialog, messagebox
import pyautogui
import time
import threading




def start_typing():
    def type_code():
        time.sleep(5)  # Time to focus the editor
        code = text_box.get("1.0", tk.END)
        lines = code.splitlines()
        for line in lines:
            pyautogui.write(line, interval=0.03)
            pyautogui.press("enter")
    threading.Thread(target=type_code).start()  # Run in thread to avoid UI freeze



def load_file():
    filepath = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if filepath:
        with open(filepath, "r") as file:
            text_box.delete("1.0", tk.END)
            text_box.insert(tk.END, file.read())

root = tk.Tk()
root.title("Auto Typing Tool")
root.geometry("600x400")



text_box = tk.Text(root, wrap=tk.WORD, font=("Courier", 12))
text_box.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)



button_frame = tk.Frame(root)
button_frame.pack(pady=10)



load_button = tk.Button(button_frame, text="Load File", command=load_file)
load_button.pack(side=tk.LEFT, padx=10)



start_button = tk.Button(button_frame, text="Start Typing", command=start_typing, bg="green", fg="white")
start_button.pack(side=tk.LEFT, padx=10)



info_label = tk.Label(root, text="Focus on your code editor within 5 seconds after clicking 'Start Typing'")
info_label.pack(pady=5)



root.mainloop()
