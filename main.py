import tkinter as tk

# set up of the window
window = tk.Tk()
window.geometry("500x500")
window.title("user interface database")

# set up the text in the window
titleLabel = tk.Label(window, text="Enter new data into database here:", font="bold")
titleLabel.pack()

# opens the window
window.mainloop()