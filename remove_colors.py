import cv2
import numpy as np
import os
import sys


path = sys.argv[1]+'/'
pathOut = sys.argv[2]+'/'

print path
print pathOut

image_list = os.listdir(path)

#RGB value of color you want to keep
#sign 
red, green, blue = [192, 128, 128]

#if we want threshold for color, set value t
t=0
lower_color = np.array([blue-t,green-t,red-t], dtype=np.uint8)
upper_color = np.array([blue+t,green+t,red+t], dtype=np.uint8)

for image in image_list:
	img = cv2.imread(path+image)
	mask = cv2.inRange(img, lower_color, upper_color)
	output = cv2.bitwise_and(img, img, mask = mask)
	#set shift (if other color should not be black)
	shift = 200
	output = (shift-output)

	#cv2.imshow ("output", output)
	#cv2.waitKey()
	print "image "+ image
	cv2.imwrite(pathOut+image, output)


print "end"
