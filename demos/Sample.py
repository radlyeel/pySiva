
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
As partial fulfillment of the requirements for ECE533 at 
University of New Mexico, Spring semester 2025
@author: Daryl Lee


Some (most?) of the OOP GUI ideas come from 
      
Moore, Alan D.. Python GUI # Programming with Tkinter: Design and build functional and user-friendly GUI applications, 2nd Edition (p. 97). (Function). Kindle Edition. 

The occasional comments like "# [Moore] pg NN" are
page references to that text.
'''
# TODO Add type hints to function defs

import tkinter as tk
from tkinter import filedialog
import cv2
import sys
import os
import numpy as np

# [Moore] pg 94ff
class LabelInput(tk.Frame):
    # Note that the space after "together" is important
    """A label and input combined together"""
    def __init__(self, parent, label, inp_cls, inp_args, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.label = tk.Label(self, text=label, anchor='w')
        self.input = inp_cls(self, **inp_args)
        self.columnconfigure(1, weight=1)
        self.label.grid(sticky=tk.E + tk.W)
        self.input.grid(row=0, column=1, sticky=tk.E + tk.W)

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started = False
        self.img = None
        self.title('Sample Demo')
           
        # Data linkages to controls
        self.lbl1_txt = tk.StringVar()
        self.lbl1_txt.set('Zoom Factor')
        self.zf = tk.DoubleVar()
        self.zf.set(1.0)
        self.zf.trace_add("write", self.updateSize)
    
        self.lbl2_txt = tk.StringVar()
        self.lbl2_txt.set('Image')

        self.samples = tk.StringVar(value = '256x256')
        self.samples.trace_add("write", self.updateSamples)
        
       # Controls
        tk.Spinbox(self,
                   from_=1.0, to=2.0, increment=0.1,
                   textvariable=self.zf).grid(row = 0,  column = 0, sticky = 'nwes')
        tk.Label(self, textvariable = 
                              self.lbl1_txt).grid(row = 0, column = 1)
        value_strings = ['256x256', '128x128', '64x64', '32x32']
        tk.Spinbox(self,
                   values = value_strings,
                   textvariable = 
                      self.samples).grid(row = 1, column = 0, sticky = 'nwes')
        tk.Label(self, textvariable=self.lbl2_txt).grid(row = 1, column = 1)
        
        tk.Button(self, text = "Read Image", 
                  command = 
                      self.loadImage).grid(row = 2, column = 0, sticky = 'nwes')
        tk.Button(self, text = "Start", 
                  command = 
                      self.startProc).grid(row = 3, column = 0, sticky = 'nwes')
        tk.Button(self, text = "Stop", 
                  command = 
                      self.stopProc).grid(row = 4, column = 0, sticky = 'nwes')
      
        
    def loadImage(self):
        images_at = os.getenv("SIVA_IMAGES_PATH", default=".")
        file_path = filedialog.askopenfilename(
                           initialdir=images_at, 
                           title="Select a file",
                           filetypes=(
                               ("Image Files", "*.tif"),
                               ("All files", "*.*")))
        self.img_orig = cv2.imread(file_path)
        if self.img_orig is not None:
            self.img_proc = self.img_orig.clone()
 
    
    def startProc(self):
        if self.img_orig is not None:
            self.started = True
            cv2.imshow('Original', self.img_orig)
            cv2.imshow('Processed', self.img_proc)
    
        
    def stopProc(self):
        if self.started:
            cv2.destroyAllWindows()
            sys.exit(0) 

    def updateSize(self, name, index, mode):
        if not self.started:
            return
        
        zoom_factor =self.zf.get()
        h,w = self.img_orig.shape[:2]
        new_size = (int(zoom_factor * h), int(zoom_factor * w))
        print(f'Zoom Factor = {zoom_factor}; new size = {new_size}\n')
        self.img = cv2.resize( self.img, new_size )
     
        self.img_proc = cv2.resize( self.img_proc, new_size )
        cv2.imshow('Processed', self.img_proc)
        
        self.img = cv2.resize( self.img, new_size )
        cv2.imshow('Original', self.img)

    def resample(img_orig, new_dims):
      
        times =
        old_shape = img_orig.shape  
        old_rows = old_shape[0]
        new_rows = old_shape[0]
        new_rows = new_dims[0]
        new_cols = new_dims[1]

        mask = np.ones(new_dims[0], new_dims[1]) * (1 / (new_dims[0] * new_dims[1]))



    def updateSamples(self, name, index, mode):
        if not self.started:
            return
        
        str = self.samples.get()
        # parse the substring AFTER the 'x'
        ndx = 1 + str.find('x')
        samples = int(str[ndx:])
        self.img_proc = self.img_orig.clone()
        print(f'{samples}x{samples}')
        self.img_proc = resample(self.img_orig, (samples, samples))
        cv2.imshow('Processed',self.img_proc)
    
    
if __name__ == "__main__":
     app = Application()
     app.mainloop()
    
    
