import tkinter as tk

root = tk.Tk()
root.title("Finn Made Uno")
root.geometry("800x600")

mini_icon = "C:/Users/Fengl/OneDrive/documents/Github Projects/Finn-Made-Uno/src/finn_made_uno/assets/uno_icon_32.png"
icon_image_small = tk.PhotoImage(file=mini_icon)
root.iconphoto(False, icon_image_small)

root.mainloop()