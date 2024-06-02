import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import subprocess

window = tk.Tk()
window.title("Project")
window.geometry("850x650")

args = []

def handle_args(args):
    subprocess.call(f"python3 src/parse.py {args[0]}, {args[1]}, {args[2]}", shell=True)
    subprocess.call(f"python3 src/classify.py {args[1]} {args[1]}", shell=True)

def show_message():
    args.clear()
    for i in labels:
        args.append(i.get())

    handle_args(args)
    window.destroy()

tk.Label(window, text="Protocol classifier", font=("Arial, 25")).pack()
tk.Label(window, text="Input file").pack()
l1 = ttk.Entry(window)
l1.pack()
tk.Label(window, text="Output file").pack()
l2 = ttk.Entry(window)
l2.pack()
tk.Label(window, text="How much packages in stream to classify").pack()
l3 = ttk.Entry(window)
l3.pack()


image = Image.open('photos/2-removebg-preview (2).png')
image = ImageTk.PhotoImage(image)

btn = tk.Button(text = "Classify", command = show_message, pady=6)
btn.pack()
image_label = tk.Label(window, image=image).pack()

labels = [l1, l2, l3]

window.mainloop()


# tk.Label(window, text="Done").pack()

