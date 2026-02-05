import tkinter as tk
import finn_made_uno

root = tk.Tk()
root.title("Finn Made Uno")
root.geometry("800x600")

mini_icon = "C:/Users/Fengl/OneDrive/documents/Github Projects/Finn-Made-Uno/src/finn_made_uno/assets/uno_icon_32.png"
icon_image_small = tk.PhotoImage(file=mini_icon)
root.iconphoto(False, icon_image_small)

title = tk.Label(root, text="===== Finn Made Uno =====", font=("Arial", 30))
title.pack(expand=True)

player_amount_text = tk.Label(root, text="Enter total amount of players (2-6): ", font=("Arial", 15))
player_amount_text.pack(expand=True)


def return_pressed(event):
    label.config(text=event.widget.get())

entry = tk.Entry(root)
entry.insert(0, "Enter your text")
entry.bind("<Return>", return_pressed)
entry.pack(padx=5, pady=5, fill="x")

label = tk.Label(root, text="Entry demo!")
label.pack(padx=5, pady=5, fill="x")

root.mainloop()