
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Feb 12 2025
As part of ECE533
@author: Daryl Lee


Some (most?) of the OOP GUI ideas come from 
      
Moore, Alan D.. Python GUI # Programming with Tkinter: Design and build functional and user-friendly GUI applications, 2nd Edition (p. 97). (Function). Kindle Edition. 

The occasonal comments like "# [Moore] pg NN" are
page references to that text.
'''

import tkinter as tk
from tkinter import filedialog
import cv2
import sys
import numpy as np

'''
# [Moore] pg 94ff
class LabelInput(tk.Frame):
  """A label and input combined together"""
    def __init__(self, parent, label, inp_cls, inp_args, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = tk.Label(self, text=label, anchor='w')
        self.input = inp_cls(self, **inp_args)
        self.columnconfigure(1, weight=1)
        self.label.grid(sticky=tk.E + tk.W)
        self.input.grid(row=0, column=1, sticky=tk.E + tk.W)
'''

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started = False
        self.title('Quantize Demo')
           
        # Data linkages to controls
        self.lbl1_txt = tk.StringVar()
        self.lbl1_txt.set('Zoom Factor')
        self.zf = tk.DoubleVar()
        self.zf.set(1.0)
        self.zf.trace_add("write", self.updateSize)
    
        self.lbl2_txt = tk.StringVar()
        self.lbl2_txt.set('Number of Bits')
        self.pb = tk.IntVar()
        self.pb.set(8)
        self.pb.trace_add("write", self.updateBits)
        
       # Controls
        tk.Spinbox(self,
                   from_=1.0, to=2.0, increment=0.1,
                   textvariable=self.zf).grid(row = 0,  column = 0)
        tk.Label(self, textvariable = self.lbl1_txt).grid(row = 0, column = 1)
        tk.Spinbox(self,
                   from_=1, to=8, increment=1,
                   textvariable = self.pb).grid(row = 1, column = 0)
        tk.Label(self, textvariable=self.lbl2_txt).grid(row = 1, column = 1)
        
        tk.Button(self, text = "Read Image", 
                  command = self.loadImage).grid(row = 2, column = 0)
        tk.Button(self, text = "Start", 
                  command = self.startProc).grid(row = 3, column = 0)
        tk.Button(self, text = "Stop", 
                  command = self.stopProc).grid(row = 4, column = 0)
      
        
    def loadImage(self):
        file_path = filedialog.askopenfilename(
                           initialdir=".", 
                           title="Select a file",
                           filetypes=(
                               ("Image Files", "*.tif"),
                               ("All files", "*.*")))
        self.img = cv2.imread(file_path)
        self.img_proc = self.img.copy()
 
    
    def startProc(self): 
        self.started = True
        cv2.imshow('Original', self.img)
        cv2.imshow('Processed', self.img_proc)
    
        
    def stopProc(self):
        cv2.destroyWindow('Processed')
        cv2.destroyWindow('Original')
        sys.exit(0)

    def updateSize(self, name, index, mode):
        if not self.started:
            return
        
        zoom_factor =self.zf.get()
        h,w = self.img.shape[:2]
        new_size = (int(zoom_factor * h), int(zoom_factor * w))
        print(f'Zoom Factor = {zoom_factor}; new size = {new_size}\n')
        self.img = cv2.resize( self.img, new_size )
     
        self.img_proc = cv2.resize( self.img_proc, new_size )
        cv2.imshow('Processed', self.img_proc)
        
        self.img = cv2.resize( self.img, new_size )
        cv2.imshow('Original', self.img)


    def updateBits(self, name, index, mode):
        if not self.started:
            return
        
        # Reference: Google('opencv grayscale quantize')
        pb = self.pb.get()
        num_levels = 2 ** pb
        levels = np.arange(0, 256, 256 // num_levels)
        levels = np.append(levels, 255)
        print('levels = ', levels)
        bins = np.digitize(self.img, levels, right=False)
        self.img_proc = (levels[bins]).astype(np.uint8)
        
        cv2.imshow('Processed',self.img_proc)
    
    
if __name__ == "__main__":
     app = Application()
     app.mainloop()
    
    
