import os

os.environ['TK_SILENCE_DEPRECATION'] = '1'

import customtkinter as ctk
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
cor1 = "#191970" # Midnight Blue
cor2 = "#EAA221" # Marigold

ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('blue')

window_width = 550
window_height = 330

root = ctk.CTk()
root.title("Clock")
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

time_label = ctk.CTkLabel(
    master=root,
    text="",
    font=("Comic Sans MS", 48, "italic"),
    text_color=cor2,
)
time_label.pack(expand=True)

date_label = ctk.CTkLabel(
    master=root,
    text="",
    font=("Comic Sans MS", 60, "bold"),
    text_color=cor2,
)
date_label.pack(expand=True)

root.after(0, update_time())
root.after(0, update_date())
root.mainloop()