# -*- coding: utf-8 -*-
"""
Spyder Editor

Verification of OpenCV installation
"""

import numpy as np
import sys
import cv2
#sys.path.append('C:/python27/Lib/site-packages/')
sys.path.append('C:/Users/Igor/Anaconda2/Lib/site-packages')

print np.__version__
#set working directory
"""
wrkDir = "D:/sandbox/python/img/"

imgname1 = "shunt1.jpg" 

# reading an image from a file
# Load an color image in grayscale
img1 = wrkDir+imgname1
print "Reading from ", img1 
img = cv2.imread(img1,0)

cv2.imshow('image',img)
cv2.waitKey(0)
cv2.destroyAllWindows()

"""
print 'Done!'