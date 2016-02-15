import cv2
import numpy as np
import os
from random import randint

#set par_"transformation" for transformations needed
par_skew = 0
par_rotate = 0
par_zoom = 0
par_translate = 1

#set values of paths (labels, original, depth)
path1="../GT/"
path2="../RGB/left/"
path3="../RGB/depth/spsstereo/depth_norm_hist/"

def skew (rows,cols):

	deg_a=randint(-5,5)
	deg_b=randint(-5,5)

	a,b=np.tan(np.deg2rad([deg_a,deg_b]))
	delta_x, delta_y = ([-a*rows/2, -b*cols/2])

	M_skew = np.float32([[1,a,delta_x],[b,1,delta_y],[0, 0, 1]])
	return M_skew

def rotate (rows,cols):
	
	deg = randint(-5,5)
	M_rot2d = cv2.getRotationMatrix2D((cols/2,rows/2),deg,1)
	last_row = np.array([0, 0, 1])

	M_rotate = np.vstack((M_rot2d, last_row))
	return M_rotate

def zoom (rows,cols):
	scale_factor = randint(90,110)/100.

	delta_x=(cols-scale_factor*cols)/2
	delta_y=(rows-scale_factor*rows)/2

	M_zoom = np.float32([[scale_factor,0,delta_x],[0,scale_factor,delta_y],[0, 0, 1]])
	return M_zoom

def translate(rows,cols):
	delta_x = (randint(-5,5)/100.)*cols 
	delta_y = (randint(-5,5)/100.)*rows

	M_translate = np.float32([[1,0,delta_x],[0,1,delta_y],[0, 0, 1]])
	return M_translate

def transform (img1, img2, img3):
	M = np.float32([[1,0,0],[0,1,0],[0,0,1]])
	rows = img1.shape[0]
	cols = img1.shape[1]

	#pictures should have same or similar shape

	if par_skew:
		M = np.dot(M, skew(rows,cols))
	if par_rotate:
		M = np.dot(M, rotate(rows,cols))
	if par_zoom:
		M = np.dot(M, zoom(rows,cols))
	if par_translate:
		M = np.dot(M, translate(rows,cols))

	res1 = cv2.warpPerspective(img1,M,(cols,rows),flags=cv2.INTER_NEAREST)
	res2 = cv2.warpPerspective(img2,M,(cols,rows),flags=cv2.INTER_NEAREST)
	res3 = cv2.warpPerspective(img3,M,(cols,rows),flags=cv2.INTER_NEAREST)
	return [res1,res2,res3]

def main():
	
	image_list = os.listdir(path1)

	for image in image_list:
		img1 = cv2.imread(path1+image)
		img2 = cv2.imread(path2+image)
		img3 = cv2.imread(path3+image)
		res1,res2,res3 = transform(img1,img2,img3)
		print "transform image: "+ image
		

		cv2.imwrite(path1+"NEW_", res1)
		cv2.imwrite(path2+"NEW_", res2)
		cv2.imwrite(path3+"NEW_", res3)


if __name__ == "__main__":
	main()
