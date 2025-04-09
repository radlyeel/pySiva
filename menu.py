import tkinter as tk
from tkinter import ttk
import subprocess
import os

'''
Reference:
https://pythonassets.com/posts/treeview-in-tk-tkinter/
'''

# As topics and demos are developed, add them here
topics = ['Mod1-Introduction',
          'Mod2-Binary Image Processing',
          'Mod3-Histogram and Point Operations',
          # 'Mod4-Discrete FourierTransform, Sampling Theory',
          # 'Mod5-Linear Filtering, Enhancement, and Restoration',
         ]
# For example, the first entry refers to demos/Quantize.py.
# Note that the demos directory is NOT divided into mods.
mod1_names = ['Quantize', 'Sample']
mod2_names = ['Complement', 'Histogram','Skeleton', 'Threshold']
mod3_names = ['Histoshape', 'ImageDifference', 'Interpolate', 'LinearPoint']
mod_names  = [mod1_names, mod2_names, mod3_names]

# There should be no routine reason to modify anything below here
# Create the main window
root = tk.Tk()
root.title('Essential Guide to Image Processing')
treeview = ttk.Treeview()

# Set up topics
mods = []
for topic in topics:
    mods.append(treeview.insert("", tk.END, text=topic))
 
# Add demos.
for i in range(len(mods)):
    mod = mods[i]
    for demo_name in mod_names[i]:
        treeview.insert(mod, tk.END, text=demo_name)
treeview.pack()

# Handle menu selection
def handleMenu(event):
    print('cwd = ' + os.getcwd())
    
    item = event.widget.selection()
    txt = treeview.item(item, "text")
    if not txt.startswith('Mod'):
        path = 'demos/' + txt + '.py'
        exec = [ 'python', path ]
        subprocess.Popen(exec)
        print(path) 
treeview.bind("<Double-Button-1>", handleMenu)


# Run the main loop
root.mainloop()
