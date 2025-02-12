#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 11 13:24:00 2025

@author: Daryl Lee
"""

import tkinter as tk
from tkinter import filedialog
import cv2
import sys

file_path = ""

def loadImage():
    global file_path
    file_path = filedialog.askopenfilename(
                       initialdir=".", 
                       title="Select a file",
                       filetypes=(
                           ("Image Files", "*.tif"),
                           ("All files", "*.*")))

def startProc():
    global file_path
    img = cv2.imread(file_path)
    print(img.shape)
    cv2.imshow('Original', img)
    img_proc = img.copy()
    cv2.imshow('Processed', img_proc)
    
def stopProc():
    cv2.destroyWindow('Processed')
    cv2.destroyWindow('Original')
    sys.exit(0)

def update():
    pass
    # zoom_factor = zoom.get()
    #  = pixelBits.get()
    # img_proc = img / 2
    
def quantize():
    root = tk.Tk()
    root.title('Quantize Demo')
       
    # Data linkages to controls
    lbl1_txt = tk.StringVar()
    lbl1_txt.set('Zoom Factor')
    lbl2_txt = tk.StringVar()
    lbl2_txt.set('Number of Bits')
    zoom = tk.DoubleVar()
    zoom.trace_add("write", update)
    zoom.set(1.0)
    pixelBits = tk.IntVar()
    pixelBits.set(8)
    pixelBits.trace_add("write", update)
    
    # Controls
    tk.Spinbox(root,
               from_=1.0, to=2.0, increment=0.1,
               textvariable=zoom).grid(row = 0,  column = 0)
    tk.Label(root, textvariable = lbl1_txt).grid(row = 0, column = 1)
    tk.Spinbox(root,
               from_=1, to=8, increment=1,
               textvariable = pixelBits).grid(row = 1, column = 0)
    tk.Label(root, textvariable=lbl2_txt).grid(row = 1, column = 1)
    
    tk.Button(root, text = "Read Image", 
              command = loadImage).grid(row = 2, column = 0)
    tk.Button(root, text = "Start", 
              command = startProc).grid(row = 3, column = 0)
    tk.Button(root, text = "Stop", 
              command = stopProc).grid(row = 4, column = 0)
    root.mainloop()
    
    
if __name__ == "__main__":
    # print(f'Using OpenCV Version {cv2.__version__}\n')
    quantize()
    
    