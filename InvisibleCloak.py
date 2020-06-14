# -*- coding: utf-8 -*-
"""
Created on Sat Jun 13 15:30:26 2020

@author: Arushi
"""
'''
The technique works as follows: 
1. Capture and store the background frame
2. Detect the defined color using color detection and segmentation algorithm
3. Segment out the defined colored part by generating a mask
4. Replace the defined color with the mask image in each frame
5. Display the final output 

'''

#Install cv2 using : pip install opevcv-python

import cv2
import time
import numpy as np

## Preparation for writing the ouput video
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('output.avi',fourcc,20.0, (640,480))

##reading from the webcam 
video_record = cv2.VideoCapture(0)

## Allow the system to sleep for 5 seconds before the webcam starts
time.sleep(5)
count = 0
background = 0

#HSV - Hue, saturation, value. The code converts RGB value to HSV and captures red color. 
## Capture the background in range of 60 (HSV of red color)
for i in range(60):
    ret,background = video_record.read()
background = np.flip(background,axis=1)


## Read every frame from the webcam, until the camera is open
while(video_record.isOpened()):
    ret, img = video_record.read()
    if not ret:
        break
    count+=1
    img = np.flip(img,axis=1)
    
    ## Convert the color space from BGR to HSV
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    ## Generat masks to detect red color
    lower_red = np.array([0,120,50])
    upper_red = np.array([10,255,255])
    mask1 = cv2.inRange(hsv,lower_red,upper_red)

    lower_red = np.array([170,120,70])
    upper_red = np.array([180,255,255])
    mask2 = cv2.inRange(hsv,lower_red,upper_red)

    mask1 = mask1+mask2

    ## Open and Dilate the mask image
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_OPEN, np.ones((3,3),np.uint8))
    mask1 = cv2.morphologyEx(mask1, cv2.MORPH_DILATE, np.ones((3,3),np.uint8))
 
 
    ## Create an inverted mask to segment out the red color from the frame
    mask2 = cv2.bitwise_not(mask1)
 
 
    ## Segment the red color part out of the frame using bitwise and with the inverted mask
    res1 = cv2.bitwise_and(img,img,mask=mask2)

    ## Create image showing static background frame pixels only for the masked region
    res2 = cv2.bitwise_and(background, background, mask = mask1)
 
 
    ## Generating the final output and writing
    finalOutput = cv2.addWeighted(res1,1,res2,1,0)
    out.write(finalOutput)
    cv2.imshow("magic",finalOutput)
    cv2.waitKey(1)

video_record.release()
out.release()
cv2.destroyAllWindows()