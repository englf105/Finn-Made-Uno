import tkinter as tk

root = tk.Tk()
root.title("Finn Made Uno")
file_path = "C:/Users/englf105/Documents/Github Projects/Finn-Made-Uno/"
file_path += "Finn-Made-Uno/src/finn_made_uno/assets/uno_icon.png"
icon_image = tk.PhotoImage(file=file_path)
root.iconphoto(False, icon_image)

root.mainloop()