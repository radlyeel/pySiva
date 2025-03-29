import tkinter as tk
def double_click_function(event):
    print("Double click detected!")



window = tk.Tk()
window.bind("<Double-Button-1>", double_click_function)
window.mainloop()