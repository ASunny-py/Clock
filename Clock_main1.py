import customtkinter as ctk
import time

# Basic theme
cor1 = "#191970" # Midnight Blue
cor2 = "#EAA221" # Marigold

window_width = 550
window_height = 330

root = ctk.CTk()
root.title("Clock")
root.geometry(f"{window_width}x{window_height}")
root.configure(fg= cor2, bg= cor1)

label = ctk.CTkLabel(root, text="", font=("Comic Sans MS", 48), fg_color=cor2, text_color=cor1)

def update_time():
    label.configure(text=time.strftime("%H:%M:%S"))
    root.after(1000, update_time)

update_time()
root.mainloop()