
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Feb 12 2025
As part of ECE533 @ UNM Spring Semester 2025
@author: Daryl Lee

'''

import tkinter as tk
from tkinter import filedialog
import cv2
import sys
import os
import numpy as np


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.started = False
        self.img = None
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
                   textvariable=self.zf).grid(row = 0,  column = 0, sticky = 'nwes')
        tk.Label(self, textvariable = 
                              self.lbl1_txt).grid(row = 0, column = 1)
        tk.Spinbox(self,
                   from_=1, to=8, increment=1,
                   textvariable = self.pb).grid(row = 1, column = 0, sticky = 'nwes')
        tk.Label(self, textvariable=self.lbl2_txt).grid(row = 1, column = 1)
        
        tk.Button(self, text = "Read Image", 
                  command = self.loadImage).grid(row = 2, column = 0, sticky = 'nwes')
        tk.Button(self, text = "Start", 
                  command = self.startProc).grid(row = 3, column = 0, sticky = 'nwes')
        tk.Button(self, text = "Stop", 
                  command = self.stopProc).grid(row = 4, column = 0, sticky = 'nwes')
      
        
    def loadImage(self):
        # Use environment variable SIVA_IMAGES_PATH if it exists, else default to '.'
        images_at = os.getenv("SIVA_IMAGES_PATH", default=".")
        file_path = filedialog.askopenfilename(
                           initialdir=images_at, 
                           title="Select a file",
                           filetypes=(
                               ("Image Files", "*.tif"),
                               ("All files", "*.*")))
        self.img = cv2.imread(file_path)
        if self.img is not None:
            self.img_proc = self.img.copy()
 
    
    def startProc(self):
        if self.img is not None:
            self.started = True
            cv2.imshow('Original', self.img)
            cv2.imshow('Processed', self.img_proc)
    
        
    def stopProc(self):
        if self.started:
            cv2.destroyAllWindows()
            sys.exit(0) 

    def updateSize(self, name, index, mode):
        if not self.started:
            return
        
        zoom_factor =self.zf.get()
        h,w = self.img.shape[:2]
        new_size = (int(zoom_factor * h), int(zoom_factor * w))
        # print(f'Zoom Factor = {zoom_factor}; new size = {new_size}\n')
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
        bins = np.digitize(self.img, levels, right=False)
        self.img_proc = (levels[bins]).astype(np.uint8)
        
        cv2.imshow('Processed',self.img_proc)
    
    
if __name__ == "__main__":
     app = Application()
     app.mainloop()
    
    
