
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

class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        '''Set up GUI interface'''
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

        value_strings = ['32x32', '64x64', '128x128', '256x256']
        tk.Spinbox(self,
                   values = value_strings,
                   textvariable = 
                      self.samples).grid(row = 1, column = 0, sticky = 'nwes')
        self.samples.set('256x256')
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
        '''Load imafe using system file selector starting at SIVA_IMAGES_PATH,
           if it is defined, current directory if it is not defined.'''
        images_at = os.getenv("SIVA_IMAGES_PATH", default=".")
        file_path = filedialog.askopenfilename(
                           initialdir=images_at, 
                           title="Select a file",
                           filetypes=(
                               ("Image Files", "*.tif"),
                               ("All files", "*.*")))
        self.img_orig = cv2.imread(file_path)
        if self.img_orig is not None:
            self.img_proc = self.img_orig.copy()
 
    
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
        '''Resize original image by requested scale factor'''
        if not self.started:
            return
        
        zoom_factor =self.zf.get()
        h,w = self.img_orig.shape[:2]
        new_size = (int(zoom_factor * h), int(zoom_factor * w))
        self.img = cv2.resize( self.img, new_size )
     
        self.img_proc = cv2.resize( self.img_proc, new_size )
        cv2.imshow('Processed', self.img_proc)
        
        self.img = cv2.resize( self.img, new_size )
        cv2.imshow('Original', self.img)


    def updateSamples(self, name, index, mode):
        '''Resize image to requested dimensions'''
        if not self.started:
            return
        
        sstr = self.samples.get()
        # parse the substrings before and after the 'x'
        ndx = sstr.find('x')
        new_height = int(sstr[:ndx])
        new_width = int(sstr[ndx + 1:])
        
        self.img_proc = cv2.resize(self.img_orig, 
                                   (new_width, new_height), 
                                   interpolation=cv2.INTER_AREA)

        cv2.imshow('Processed',self.img_proc)
    
    
if __name__ == "__main__":
     app = Application()
     app.mainloop()
    
    
