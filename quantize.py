#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Feb 12 2025
As part of ECE533
@author: Daryl Lee
"""

import tkinter as tk
from tkinter import filedialog
import cv2
import sys
import numpy as np


# A few globals
file_path = ""
img = np.zeros((1,1,1),dtype=np.uint8)
img_proc = np.zeros((1,1,1),dtype=np.uint8)
started = False
variables = dict()  # Thanks Alan Moore , for this solution to globals

def loadImage():
    global file_path
    global img
    file_path = filedialog.askopenfilename(
                       initialdir=".", 
                       title="Select a file",
                       filetypes=(
                           ("Image Files", "*.tif"),
                           ("All files", "*.*")))
    img = cv2.imread(file_path)
 

def startProc(): 
    global started
    started = True
    cv2.imshow('Original', img)
    img_proc = img.copy()
    cv2.imshow('Processed', img_proc)
    
def stopProc():
    cv2.destroyWindow('Processed')
    cv2.destroyWindow('Original')
    sys.exit(0)

def updateSize(name, index, mode):
    global img_proc
    global img
    global started
    if not started:
        return
    zoom_factor = variables['zoom'].get()
    h,w = img.shape[:2]
    new_size = (int(zoom_factor * h), int(zoom_factor * w))
    img = cv2.resize( img, new_size )
 
    img_proc = cv2.resize( img, new_size )
    cv2.imshow('Processed', img_proc)
    
    img = cv2.resize( img, new_size )
    cv2.imshow('Original', img)

def updateBits(name, index, mode):
    global img_proc
    global started
    if not started:
        return
    # Reference: Google('opencv python grayscale quantize')
    pb = variables['pixelBits'].get()
    levels = 2 ** pb
    print(f'Quantizing to {levels} levels\n')
    img_proc = np.floor(img / (256 // levels)) * (256 // levels)
    img_proc = img_proc.astype(np.uint8)
    cv2.imshow('Processed',img_proc)
 
def main():
    root = tk.Tk()
    root.title('Quantize Demo')
       
    # Data linkages to controls
    lbl1_txt = tk.StringVar()
    lbl1_txt.set('Zoom Factor')
    lbl2_txt = tk.StringVar()
    lbl2_txt.set('Number of Bits')
    zf = tk.DoubleVar()
    variables['zoom'] = zf
    variables['zoom'].set(1.0)  # Make sur to set value before trace_add
    zf.trace_add("write", updateSize)
    pb = tk.IntVar()
    variables['pixelBits'] = pb
    pb.set(8)
    pb.trace_add("write", updateBits)
    # Controls
    tk.Spinbox(root,
               from_=1.0, to=2.0, increment=0.1,
               textvariable=variables['zoom']).grid(row = 0,  column = 0)
    tk.Label(root, textvariable = lbl1_txt).grid(row = 0, column = 1)
    tk.Spinbox(root,
               from_=1, to=8, increment=1,
               textvariable = variables['pixelBits']).grid(row = 1, column = 0)
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
    main()
    
    
