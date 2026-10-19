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
cor3 = "#F2F2F2" # White Smoke
cor4 = "#1E1E1E" # Jet
cor5 = "#FF6B6B" # Coral Red
cor6 = "#4ECDC4" # Turquoise

window_width = 1280
window_height = 720

root = tk.Tk()
root.title("World Clock")
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

canvas_container = tk.Canvas(root, bg=cor1, highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas_container.yview)
scroll_frame = tk.Frame(canvas_container, bg=cor1)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas_container.configure(scrollregion=canvas_container.bbox("all"))
)
canvas_container.create_window((0, 0), window=scroll_frame, anchor="nw", width=400)
canvas_container.configure(yscrollcommand=scrollbar.set)

canvas_container.pack(side="left", fill="both", expand=True)
scrollbar.pack(side="right", fill="y")

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

#This section is going to be used for the next feature, the ability to add other clocks.

class ClockWidget:
    """The master template blueprint for creating independent clock units."""
    
    def __init__(self, parent_container):
        # This builds the individual visual box container for a single clock instance
        self.container = tk.Frame(
            parent_container, 
            bg=cor1, 
            highlightbackground=cor2, 
            highlightthickness=1, 
            bd=0
        )
        self.container.pack(fill="x", padx=10, pady=8, ipady=5)
        
        # Track individual settings states inside this specific instance
        self.current_tz_name = "Local Time"
        self.current_view = "Digital"
        
        # Create text label placeholders for this clock box instance
        self.time_label = tk.Label(self.container, font=(".AppleSystemUIFont", 28, "bold"), bg=cor1, fg=cor2)
        self.time_label.pack(anchor="w", padx=15, pady=(5, 0))
        
        self.date_label = tk.Label(self.container, font=(".AppleSystemUIFont", 12, "normal"), bg=cor1, fg=cor2)
        self.date_label.pack(anchor="w", padx=15, pady=(0, 5))

active_clocks = []

max_clocks = 10

def master_ticker():
    for clock in active_clocks:
        clock.refresh_time()
        root.after(1000, master_ticker)

def add_new_clock():
    if len(active_clocks) >= max_clocks:
        print("How many clocks do you need?!")
        return
    
new_clock = ClockWidget(scroll_frame)
active_clocks.append(new_clock)
new_clock.refresh_time()

canvas_container.configure(scrollregion=canvas_container.bbox("all"))

top_action_bar = tk.Frame(root, bg=cor1)
top_action_bar.pack(fill="x", side="top", padx=10, pady=10)

add_clock_button = tk.Button(
    master=top_action_bar,
    text="Add Clock",
    command=add_new_clock,
    font=("Comic Sans MS", 16, "bold"),
    bg=cor1,
    fg=cor2,
)

add_clock_button.pack(side="right")

from datetime import datetime
from zoneinfo import ZoneInfo

# We are going to have 3 main timezones, but we can add more later. 
ny_time = datetime.now(ZoneInfo("America/New_York"))
tokyo_time = datetime.now(ZoneInfo("Asia/Tokyo"))
london_time = datetime.now(ZoneInfo("Europe/London"))



