import sys
sys.path.append('/Users/akhilupadhyaya/Library/Python/3.11/lib/python/site-packages')

import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import ttk
import time
from time import strftime
import math
from datetime import datetime
from zoneinfo import ZoneInfo

cor1 = "#0B123B" # Midnight Blue
cor2 = "#EAA221" # Marigold
cor3 = "#F2F2F2" # White Smoke
cor4 = "#1E1E1E" # Jet
cor5 = "#FF6B6B" # Coral Red
cor6 = "#4ECDC4" # Turquoise

Themes = {
    "Marigold Night": {"bg": cor1, "face": cor4, "accent": cor2, "text": cor3, "muted": cor2},
    "Minimal White":  {"bg": cor3, "face": cor3, "accent": cor4, "text": cor1, "muted": cor4},
    "Neon Coral":     {"bg": cor4, "face": cor1, "accent": cor5, "text": cor3, "muted": cor6},

}

Timezones = {
    "Local Time": "Local",
    "New York": "America/New_York",
    "Tokyo": "Asia/Tokyo",
    "London": "Europe/London"
}

window_width = 1280
window_height = 720

active_clocks = []
max_clocks = 5
current_theme = "Marigold Night"

class ClockWidget:

    def __init__(self, parent_container):
        colors = Themes[current_theme]
        # This builds the individual visual box container for a single clock instance
        self.container = tk.Frame(
            parent_container, 
            bg=colors["bg"], 
            highlightbackground=colors["accent"], 
            highlightthickness=1, 
            bd=0
        )
        self.container.pack(fill="x", padx=15, pady=10, ipady=5)
        
        # Track individual settings states inside this specific instance
        self.current_tz_name = "Local Time"
        self.current_view = "Digital"

        self.left_panel = tk.Frame(self.container, bg=colors["bg"])
        self.left_panel.pack(side = "left", padx = 20, expand = True, fill = "both")

        self.tz_dropdown = ttk.Combobox(self.left_panel, values=list(Timezones.keys()), state="readonly", width=20)
        self.tz_dropdown.set(self.current_tz_name)
        self.tz_dropdown.bind("<<ComboboxSelected>>", self.on_tz_change)
        self.tz_dropdown.pack(anchor="w", pady=(5, 0))

        # Text label placeholders for clock box instance
        self.digital_frame = tk.Frame(self.left_panel, bg=colors["bg"])
        self.digital_frame.pack(anchor="w", pady=(5, 0))

        self.time_label = tk.Label(self.container, font=(".AppleSystemUIFont", 28, "bold"), bg=colors["bg"], fg=colors["text"])
        self.time_label.pack(anchor="w", padx=15, pady=(5, 0))
        
        self.date_label = tk.Label(self.container, font=(".AppleSystemUIFont", 12, "normal"), bg=colors["bg"], fg=colors["text"])
        self.date_label.pack(anchor="w", padx=15, pady=(0, 5))

        self.toggle_btn = tk.Button(
            self.left_panel,
            text="Switch to Analogue",
            command=self.toggle_view,
            highlightbackground=colors["accent"],
            font=(".AppleSystemUIFont", 24, "bold"),
        )
        self.toggle_btn.pack(anchor="w", pady=(5, 0))

        self.right_panel = tk.Frame(self.container, bg=colors["bg"])
        self.right_panel.pack(side = "right", padx = 20, pady=5)

        self.dial_canvas = tk.Canvas(self.right_panel, width=120, height=120, bg=colors["bg"], highlightthickness=0)

    def draw_hand(self, angle, length, width, color):
        """Processes trigonometric calculations to project directional line arrays."""
        cx, cy = 60, 60  # Establishes dead-center focal coordinate point inside 120x120 bounds
        x = cx + length * math.sin(math.radians(angle))
        y = cy - length * math.cos(math.radians(angle))
        return self.dial_canvas.create_line(cx, cy, x, y, width=width, fill=color, capstyle=tk.ROUND)

    def refresh_time(self):
        """Extracts database metrics to update display strings and canvas models."""
        tz_key = Timezones[self.current_tz_name]
        colors = Themes[current_theme]
        
        # Pull datetime strings natively accounting for regional variations
        if tz_key == "Local":
            now = datetime.now()
        else:
            now = datetime.now(ZoneInfo(tz_key))

        hours = now.hour
        minutes = now.minute
        seconds = now.second

        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%A, %B %d, %Y")

        self.time_label.config(text=time_str)
        self.date_label.config(text=date_str)

        if self.current_view == "Analogue":
            self.dial_canvas.delete("all")
            self.dial_canvas.create_oval(5, 5, 115, 115, fill=colors["face"])

            sec_angle = seconds * 6
            min_angle = minutes * 6 + seconds * 0.1
            hour_angle = hours * 30 + minutes * 0.5

            self.draw_hand(hour_angle, 32, 4, colors["text"])
            self.draw_hand(min_angle, 45, 2.5, colors["text"])
            self.draw_hand(sec_angle, 50, 1, colors["accent"])

            self.dial_canvas.create_oval(56, 56, 64, 64, fill=colors["accent"], outline=colors["text"])
        
    def toggle_view(self):
        """Switches between digital and analogue display modes."""
        if self.current_view == "Digital":
            self.current_view = "Analogue"
            self.digital_frame.pack_forget()
            self.dial_canvas.pack(side="right", padx=10, pady=5)
            self.toggle_btn.config(text="Switch to Digital")
        else:
            self.current_view = "Digital"
            self.dial_canvas.pack_forget()
            self.time_label.pack(anchor="w", pady=(5, 0))
            self.toggle_btn.config(text="Switch to Analogue")
        self.refresh_time()


    def on_tz_change(self, event):
        self.current_tz_name = self.tz_dropdown.get()
        self.refresh_time()

    def update_widget_colors(self):
        colors = Themes[current_theme]
        self.container.configure(bg=colors["bg"], highlightbackground=colors["accent"])
        self.left_panel.configure(bg=colors["bg"])
        self.digital_frame.configure(bg=colors["bg"])
        self.right_panel.configure(bg=colors["bg"])
        self.time_label.configure(bg=colors["bg"], fg=colors["accent"])
        self.date_label.configure(bg=colors["bg"], fg=colors["text"])
        self.dial_canvas.configure(bg=colors["bg"])
        self.toggle_btn.configure(highlightbackground=colors["bg"])

def master_ticker():
    for clock in active_clocks:
        clock.refresh_time,
        root.after(1000, master_ticker)

def add_new_clock():
    if len(active_clocks) >= max_clocks:
        print("How many clocks do you need?!")
        return
    
    new_clock = ClockWidget(scroll_frame)
    active_clocks.append(new_clock)
    new_clock.refresh_time()

    canvas_container.configure(scrollregion=canvas_container.bbox("all"))
    
root = tk.Tk()
root.title("World Clock")
root.geometry(f"{window_width}x{window_height}")
root.resizable(False, False)

initial_colors = Themes[current_theme]
root.configure(bg=initial_colors["bg"])

canvas_container = tk.Canvas(root, bg=initial_colors["bg"], highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas_container.yview)
scroll_frame = tk.Frame(canvas_container, bg=cor1)

scroll_frame.bind(
    "<Configure>",
    lambda e: canvas_container.configure(scrollregion=canvas_container.bbox("all"))
)

def apply_global_theme(theme_name):
    global current_theme
    current_theme = theme_name
    colors = Themes[theme_name]

    root.configure(bg=colors["bg"])
    top_action_bar.configure(bg=colors["bg"])
    canvas_container.configure(bg=colors["bg"])
    scroll_frame.configure(bg=colors["bg"])
    title_label.configure(bg=colors["bg"], fg=colors["text"])

    for clock in active_clocks:
        clock.update_widget_colors()

top_action_bar = tk.Frame(root, bg=initial_colors["bg"])
top_action_bar.pack(fill="x", side="top", padx=20, pady=15)

title_label = tk.Label(top_action_bar, text="World Clock", font=("AppleSystemUIFont", 24, "bold"), bg=initial_colors["bg"], fg=initial_colors["text"])
title_label.pack(side="left")

add_clock_button = tk.Button(
    master=top_action_bar,
    text="Add Clock",
    command=add_new_clock,
    font=("Comic Sans MS", 16, "bold"),
    bg=cor1,
    fg=cor2,
)

add_clock_button.pack(side="right")

for name in Themes.keys():
    theme_btn = tk.Button(
    master=top_action_bar,
    text=name.split()[0],
    command=lambda n=name: apply_global_theme(n),
    highlightbackground=initial_colors["bg"],
    font=("Comic Sans MS", 12)
    )
theme_btn.pack(side="right", padx=2)

canvas_container.create_window((0, 0), window=scroll_frame, anchor="nw", width=1200)
canvas_container.configure(yscrollcommand=scrollbar.set)

canvas_container.pack(side="left", fill="both", expand=True, padx=[20,0])
scrollbar.pack(side="right", fill="y")

add_new_clock()
master_ticker()
root.mainloop()