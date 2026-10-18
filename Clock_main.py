from tkinter import *
import time


cor1 = "#191970" # Midnight Blue
cor2 = "#EAA221" # Marigold

root = Tk()
root.title("Home Clock")

root.geometry("550x330")
root.configure(background=cor1)

label = Label(root, text="", font=("Arial", 30), bg=cor1, fg=cor2)
label.pack(expand=True)

def update_time():
    label.config(text=time.strftime("%H: %M: %S"))
    root.after(1000, update_time)

update_time()
root.mainloop()