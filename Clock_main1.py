import sys

sys.path.append('/Users/akhilupadhyaya/Library/Python/3.11/lib/python/site-packages')

import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
import time
from time import strftime

def update_time():
    current_time = strftime('%H:%M:%S')
    print("Updating:", current_time)
    time_label.configure(text=current_time)
    root.after(1000, update_time)

def update_date():
    current_date = time.strftime('%A, %B %d, %Y')
    print("Updating:", current_date)
    date_label.configure(text=current_date)
    date_label.after(60000, update_date)

# Basic theme
cor1 = "#0B123B" # Midnight Blue
cor2 = "#EAA221" # Marigold

window_width = 770
window_height = 550

root = tk.Tk()
root.title("Clock")
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

bg_colour = cor1
root.configure(bg=bg_colour)

time_label = tk.Label(
    master=root,
    text="",
    font=("Comic Sans MS", 48, "italic"),
    foreground=cor2,
)
time_label.pack(expand=True)

date_label = tk.Label(
    master=root,
    text="",
    font=("Comic Sans MS", 32, "bold"),
    foreground=cor2,
)
date_label.pack(expand=True)

root.after(0, update_time())
root.after(0, update_date())
root.mainloop()
