#!/usr/bin/env python
'''
===============================================================================
Interactive Image Segmentation using GrabCut algorithm.

This sample shows interactive image segmentation using grabcut algorithm.

USAGE :
    python grabcut.py <filename>

README FIRST:
    Two windows will show up, one for input and one for output.

    At first, in input window, draw a rectangle around the object using
mouse right button. Then press 'n' to segment the object (once or a few times)
For any finer touch-ups, you can press any of the keys below and draw lines on
the areas you want. Then again press 'n' for updating the output.

Key '0' - To select areas of sure background
Key '1' - To select areas of sure foreground
Key '2' - To select areas of probable background
Key '3' - To select areas of probable foreground

Key 'n' - To update the segmentation
Key 'r' - To reset the setup
Key 's' - To save the results
===============================================================================
'''

import numpy as np
import cv2
import sys
import os

BLUE = [255,0,0]        # rectangle color
RED = [0,0,255]         # PR BG
GREEN = [0,255,0]       # PR FG
BLACK = [0,0,0]         # sure BG
WHITE = [255,255,255]   # sure FG

DRAW_BG = {'color' : BLACK, 'val' : 0}
DRAW_FG = {'color' : WHITE, 'val' : 1}
DRAW_PR_FG = {'color' : GREEN, 'val' : 3}
DRAW_PR_BG = {'color' : RED, 'val' : 2}

# setting up flags
rect = (0,0,1,1)
drawing = False         # flag for drawing curves
rectangle = False       # flag for drawing rect
rect_over = False       # flag to check if rect drawn
rect_or_mask = 100      # flag for selecting rect or mask mode
value = DRAW_FG         # drawing initialized to FG
thickness = 3           # brush thickness
def gene_imgnames(datapath, fix):
    # '*.png' files in the folder
    imglist = []
    count = 0
    for tmpfile in os.listdir(datapath):
        if tmpfile.endswith(fix):
            imglist.append(tmpfile)
            count += 1
    return imglist

def onmouse(event,x,y,flags,param):
    global img,img2,drawing,value,mask,rectangle,rect,rect_or_mask,ix,iy,rect_over, all_mask

    # Draw Rectangle
    if event == cv2.EVENT_RBUTTONDOWN:
        rectangle = True
        ix,iy = x,y

    elif event == cv2.EVENT_MOUSEMOVE:
        if rectangle == True:
            img = img2.copy()
            cv2.rectangle(img,(ix,iy),(x,y),BLUE,2)
            rect = (ix,iy,abs(ix-x),abs(iy-y))
            rect_or_mask = 0

    elif event == cv2.EVENT_RBUTTONUP:
        rectangle = False
        rect_over = True
        cv2.rectangle(img,(ix,iy),(x,y),BLUE,2)
        rect = (ix,iy,abs(ix-x),abs(iy-y))
        rect_or_mask = 0
        print " Now press the key 'z' a few times until no further change \n"

    # draw touchup curves

    if event == cv2.EVENT_LBUTTONDOWN:
        if rect_over == False:
            print "first draw rectangle \n"
        else:
            drawing = True
            cv2.circle(img,(x,y),thickness,value['color'],-1)
            cv2.circle(mask,(x,y),thickness,value['val'],-1)

    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing == True:
            cv2.circle(img,(x,y),thickness,value['color'],-1)
            cv2.circle(mask,(x,y),thickness,value['val'],-1)

    elif event == cv2.EVENT_LBUTTONUP:
        if drawing == True:
            drawing = False
            cv2.circle(img,(x,y),thickness,value['color'],-1)
            cv2.circle(mask,(x,y),thickness,value['val'],-1)

# print documentation
print __doc__

# Loading images
if len(sys.argv) == 3:
    datapath = sys.argv[1]
    dataname = sys.argv[2]


elif len(sys.argv) == 2:
    datapath = sys.argv[1]
    dataname = []
else:
    print "No input image given, so loading default image, 1.png \n"
    print "Correct Usage : python grab_add.py <pathname> \n"
    datapath = './test/'
    dataname = []

imgnames = gene_imgnames(datapath, ".png")

if len(dataname) == 0:
    global begin_id
    begin_id = 0
    filename = datapath + imgnames[begin_id]
    print('initial image is: ', filename)
else:
    global begin_id
    begin_id = imgnames.index(dataname)
    filename = datapath + imgnames[begin_id]
    print('initial image is: ', filename)

save_path = datapath + '/' + 'grab/'
if os.path.isdir(save_path):
    print('save label results in: ', save_path)
else:
    os.mkdir(save_path)


img = cv2.imread(filename)
img2 = img.copy()                               # a copy of original image
mask = np.zeros(img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
all_mask = np.zeros(img.shape[:2],dtype = np.uint8)
output = np.zeros(img.shape,np.uint8)           # output image to be shown

# input and output windows
cv2.namedWindow('output')
cv2.namedWindow('input')
cv2.setMouseCallback('input',onmouse)
cv2.moveWindow('input',img.shape[1]+10,90)

print " Instructions : \n"
print " Draw a rectangle around the object using right mouse button \n"

while(1):

    cv2.imshow('output',output)
    cv2.imshow('input',img)
    k = 0xFF & cv2.waitKey(1)

    # key bindings
    if k == 27:         # esc to exit
        break
    elif k == ord('0'): # BG drawing
        print " mark background regions with left mouse button \n"
        value = DRAW_BG
    elif k == ord('1'): # FG drawing
        print " mark foreground regions with left mouse button \n"
        value = DRAW_FG
    elif k == ord('2'): # PR_BG drawing
        value = DRAW_PR_BG
    elif k == ord('3'): # PR_FG drawing
        value = DRAW_PR_FG
    elif k == ord('s'): # save image
        bar = np.zeros((img.shape[0],5,3),np.uint8)
        res = np.hstack((img2,bar,img,bar,output))
        print(save_path + imgnames[begin_id][:-4])
        cv2.imwrite(save_path + imgnames[begin_id], all_mask)
        print " Result saved as image \n"
    elif k == ord('r'): # reset everything
        print "resetting \n"
        rect = (0,0,1,1)
        drawing = False
        rectangle = False
        rect_or_mask = 100
        rect_over = False
        value = DRAW_FG
        img = img2.copy()
        mask = np.zeros(img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
        output = np.zeros(img.shape,np.uint8)           # output image to be shown
        all_mask = np.zeros(img.shape[:2],dtype = np.uint8)

    elif k == ord('a'):
        all_mask = np.where((mask==1) + (mask==3) + (all_mask!=0),255,0).astype('uint8')
        output = cv2.bitwise_and(img2,img2,mask=all_mask)

    elif k == ord('z'): # segment the image
        print """ For finer touchups, mark foreground and background after pressing keys 0-3
        and again press 'z' \n"""
        if (rect_or_mask == 0):         # grabcut with rect
            bgdmodel = np.zeros((1,65),np.float64)
            fgdmodel = np.zeros((1,65),np.float64)
            cv2.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv2.GC_INIT_WITH_RECT)
            rect_or_mask = 1
        elif rect_or_mask == 1:         # grabcut with mask
            bgdmodel = np.zeros((1,65),np.float64)
            fgdmodel = np.zeros((1,65),np.float64)
            cv2.grabCut(img2,mask,rect,bgdmodel,fgdmodel,1,cv2.GC_INIT_WITH_MASK)

    elif k == ord('j'):
        begin_id -= 1
        begin_id = np.mod(begin_id, len(imgnames))
        filename = datapath + imgnames[begin_id]
        img = cv2.imread(filename)
        img2 = img.copy()                               # a copy of original image
        mask = np.zeros(img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
        all_mask = np.zeros(img.shape[:2],dtype = np.uint8)
        output = np.zeros(img.shape,np.uint8)           # output image to be shown

    elif k == ord('k'):
        begin_id += 1
        begin_id = np.mod(begin_id, len(imgnames))
        filename = datapath + imgnames[begin_id]
        img = cv2.imread(filename)
        img2 = img.copy()                               # a copy of original image
        mask = np.zeros(img.shape[:2],dtype = np.uint8) # mask initialized to PR_BG
        all_mask = np.zeros(img.shape[:2],dtype = np.uint8)
        output = np.zeros(img.shape,np.uint8)           # output image to be shown

    mask2 = np.where((mask==1) + (mask==3),255,0).astype('uint8')
    mask2 = np.where((mask2!=0) + (all_mask!=0),255,0).astype('uint8')
    output = cv2.bitwise_and(img2,img2,mask=mask2)
    cv2.imshow('all_mask', all_mask)

cv2.destroyAllWindows()
