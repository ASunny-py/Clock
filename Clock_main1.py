import os
os.environ['TK_SILENCE_DEPRECATION'] = '1'

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import re
import time
from time import strftime
import math
from datetime import datetime
from zoneinfo import ZoneInfo
import json
from pathlib import Path

cor1 = "#0B123B" # Midnight Blue
cor2 = "#EAA221" # Marigold
cor3 = "#F2F2F2" # White Smoke
cor4 = "#1E1E1E" # Jet
cor5 = "#FF6B6B" # Coral Red
cor6 = "#4ECDC4" # Turquoise

Themes = {
    "Marigold Night": {"bg": cor1, "face": cor4, "accent": cor2, "text": cor3},
    "Minimal White":  {"bg": cor3, "face": cor3, "accent": cor4, "text": cor1},
    "Neon Coral":     {"bg": cor4, "face": cor1, "accent": cor5, "text": cor3}
}

Timezones = {
    "Local Time": "Local",
    "New York": "America/New_York",
    "Los Angeles": "America/Los_Angeles",
    "Chicago": "America/Chicago",
    "London": "Europe/London",
    "Paris": "Europe/Paris",
    "Dubai": "Asia/Dubai",
    "Tokyo": "Asia/Tokyo",
    "Sydney": "Australia/Sydney",
    "Auckland": "Pacific/Auckland"
}

window_width = 1280
window_height = 640

active_clocks = []
max_clocks = 10
current_theme = "Marigold Night"

Custom_Themes_File = Path.home() / ".world_clock_themes.json"
custom_themes = {}

if Custom_Themes_File.exists():
    try:
        custom_themes = json.loads(Custom_Themes_File.read_text())
        if not isinstance(custom_themes, dict):
            raise ValueError("Custom themes file must contain a JSON object.")
        Themes.update(custom_themes)
    except (json.JSONDecodeError, OSError, ValueError) as error:
        print(f"Could not load custom themes: {error}")

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
        self.left_panel.pack(side="left", padx=20, expand=True, fill="both")

        self.tz_dropdown = ttk.Combobox(self.left_panel, values=list(Timezones.keys()), state="readonly", width=20)
        self.tz_dropdown.set(self.current_tz_name)
        self.tz_dropdown.bind("<<ComboboxSelected>>", self.on_tz_change)
        self.tz_dropdown.pack(anchor="w", pady=(5, 0))

        # Text labels for clock box
        self.digital_frame = tk.Frame(self.left_panel, bg=colors["bg"])
        self.digital_frame.pack(anchor="w", pady=(5, 0))

        self.time_label = tk.Label(self.digital_frame, font=("Comic Sans MS", 28, "bold"), bg=colors["bg"], fg=colors["text"])
        self.time_label.pack(anchor="w", padx=15, pady=(5, 0))

        self.date_label = tk.Label(self.left_panel, font=("Comic Sans MS", 12, "normal"), bg=colors["bg"], fg=colors["text"])
        self.date_label.pack(anchor="w", padx=15, pady=(0, 5))

        self.toggle_btn = tk.Button(
            self.left_panel,
            text="Switch to Analogue",
            command=self.toggle_view,
            highlightbackground=colors["accent"],
            font=(".Comci Sans MS", 24, "bold"),
        )
        self.toggle_btn.pack(anchor="w", pady=(5, 0))

        self.remove_btn = tk.Button(
            self.left_panel,
            text="Remove",
            command=self.remove_self,
            bg=colors["accent"],
            fg=colors["bg"],
            highlightbackground=colors["text"],
            font=("Comic Sans MS", 12, "bold"),
        )
        self.remove_btn.pack(anchor="w", pady=(5, 0))

        self.right_panel = tk.Frame(self.container, bg=colors["bg"])
        self.right_panel.pack(side="right", padx=20, pady=5)

        self.dial_canvas = tk.Canvas(self.right_panel, width=120, height=120, bg=colors["bg"], highlightthickness=0)

    def remove_self(self):
        if self in active_clocks:
            active_clocks.remove(self)
        self.container.destroy()
        if canvas_container.winfo_exists():
            canvas_container.configure(scrollregion=canvas_container.bbox("all"))

    def draw_hand(self, angle, length, width, color):
        """Processes trigonometric calculations to project directional line arrays."""
        cx, cy = 60, 60
        x = cx + length * math.sin(math.radians(angle))
        y = cy - length * math.cos(math.radians(angle))
        return self.dial_canvas.create_line(cx, cy, x, y, width=width, fill=color, capstyle=tk.ROUND)

    def draw_clock_face(self, colors):
        self.dial_canvas.delete("all")
        self.dial_canvas.create_oval(7.5, 7.5, 120, 120, fill=colors["face"], outline=colors["text"], width=2)

        for minute in range(60):
            mark_angle = minute * 6
            inner = 45 if minute % 5 else 40
            outer = 52 if minute % 5 else 48
            start_x = 60 + inner * math.sin(math.radians(mark_angle))
            start_y = 60 - inner * math.cos(math.radians(mark_angle))
            end_x = 60 + outer * math.sin(math.radians(mark_angle))
            end_y = 60 - outer * math.cos(math.radians(mark_angle))
            self.dial_canvas.create_line(start_x, start_y, end_x, end_y, fill=colors["text"], width=1 if minute % 5 else 2)

        for hour in range(1, 13):
            angle = hour * 30 - 90
            x = 60 + 36 * math.cos(math.radians(angle))
            y = 60 + 36 * math.sin(math.radians(angle))
            self.dial_canvas.create_text(x, y, text=str(hour), fill=colors["text"], font=("Comic Sans MS", 8, "bold"))

    def refresh_time(self):
        """Extracts database metrics to update display strings and canvas models."""
        tz_key = Timezones.get(self.current_tz_name, 'Local')
        colors = Themes[current_theme]

        # Pull datetime strings. Account for regions.
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
            self.draw_clock_face(colors)

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
            self.digital_frame.pack(anchor="w", pady=(5, 0), before=self.date_label)
            self.toggle_btn.config(text="Switch to Analogue")
        self.refresh_time()

    def on_tz_change(self, event):
        self.current_tz_name = self.tz_dropdown.get()
        self.refresh_time()

def update_widget_colors(self):
    colors = Themes[current_theme]
    self.container.coonfigure(
        bg = colors["bg"],
        highlightbackground=colors["accent"]
    )
    self.left_panel.configure(bg=colors["bg"])
    self.digital_frame.configure(bg=colors["bg"])
    self.right_panel.configure(bg=colors["bg"])
    self.time_label.configure(bg=colors["bg"], fg=colors["text"])
    self.date_label.configure(bg=colors["bg"], fg=colors["text"])
    self.dial_canvas.configure(bg=colors["bg"])
    self.toggle_btn.configure(
        bg=colors["bg"],
        fg=colors["text"],
        highlightbackground=colors["accent"],
    )
    self.remove_btn.configure(
        bg=colors["accent"],
        fg=colors["bg"],
        highlightbackground=colors["text"]
    )

def save_custom_themes():
    try:
        Custom_Themes_File.write_text(json.dumps(custom_themes, indent=2))
    except OSError as error:
        messagebox.showerror("Theme save error", str(error), parent=root)
        return False
    return True


def open_settings():
    settings_window = tk.Toplevel(root)
    settings_window.title("Theme Options")
    settings_window.geometry("440x430")
    settings_window.resizable(False, False)
    settings_window.transient(root)
    settings_window.grab_set()

    tk.Label(settings_window, text="Choose a theme").pack(padx=15, pady=(15, 5))

    theme_choice = tk.StringVar(value=current_theme)
    theme_dropdown = ttk.Combobox(
        settings_window,
        textvariable=theme_choice,
        values=list(Themes.keys()),
        state="readonly",
        width=30,
    )
    theme_dropdown.pack(pady=5)

    def apply_selected_theme():
        apply_global_theme(theme_choice.get())

    ttk.Button(
        settings_window,
        text="Apply Theme",
        command=apply_selected_theme,
    ).pack(padx=15, pady=(5, 15))

    ttk.Separator(settings_window).pack(fill="x", padx=20, pady=5)
    tk.Label(settings_window, text="Create a custom theme").pack(pady=(10, 5))

    name_entry = tk.Entry(settings_window, width=28)
    name_entry.insert(0, "Custom Theme")
    name_entry.pack(pady=5)

    color_entries = {}
    defaults = Themes[current_theme]
    for color_key in ("bg", "face", "accent", "text"):
        row = tk.Frame(settings_window)
        row.pack(fill="x", padx=55, pady=3)
        tk.Label(row, text=color_key.title(), width=10, anchor="w").pack(side="left")

        entry = tk.Entry(row, width=12)
        entry.insert(0, defaults[color_key])
        entry.pack(side="left")
        color_entries[color_key] = entry

    def save_custom_theme():
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror(
                "Invalid theme",
                "Enter a name for the theme.",
                parent=settings_window,
            )
            return
        if name in Themes:
            messagebox.showerror(
                "Invalid theme",
                "A theme with that name already exists.",
                parent=settings_window,
            )
            return

        colors = {key: entry.get().strip() for key, entry in color_entries.items()}
        if any(
            not re.fullmatch(r"#[0-9a-fA-F]{6}", color)
            for color in colors.values()
        ):
            messagebox.showerror(
                "Invalid color",
                "Enter each color as a six-digit hex value, like #1A2B3C.",
                parent=settings_window,
            )
            return

        custom_themes[name] = colors
        if not save_custom_themes():
            del custom_themes[name]
            return

        Themes[name] = colors
        theme_dropdown["values"] = list(Themes.keys())
        theme_choice.set(name)
        apply_global_theme(name)

    ttk.Button(
        settings_window,
        text="Save and Apply Custom Theme",
        command=save_custom_theme,
    ).pack(pady=12)

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

title_label = tk.Label(top_action_bar, text="World Clock", font=("Comic Sans MS", 24, "bold"), bg=initial_colors["bg"], fg=initial_colors["text"])
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

settings_button = tk.Button(
    top_action_bar,
    text="Theme Options",
    command=open_settings ,
    font=("Comic Sans MS", 20),
)
settings_button.pack(side="right", padx=2)

canvas_container.create_window((0, 0), window=scroll_frame, anchor="nw", width=1200)
canvas_container.configure(yscrollcommand=scrollbar.set)

canvas_container.pack(side="left", fill="both", expand=True, padx=[20,0])
scrollbar.pack(side="right", fill="y")

def scroll_wheel(event):
    canvas_container.yview_scroll(-1 if event.delta > 0 else 1, "units")

root.bind_all("<MouseWheel>", scroll_wheel)

add_new_clock()
master_ticker()
root.mainloop()