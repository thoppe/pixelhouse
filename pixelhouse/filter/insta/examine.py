import cv2
import os
import numpy as np

## AAAHHHH images are not aligned

img_src = cv2.imread("examples/0_nashville-e1448853218475.jpg")
img0 = cv2.imread("examples/1_nashville-e1448853218475.jpg")
img1 = cv2.imread("examples/2_nashville-e1448853218475.jpg")


diff = np.abs(img1[:,:,0] - img0[:,:,0]) < 100
diff = (255*diff).astype(np.uint8)

#cv2.imshow("", diff)
#cv2.waitKey(0)

while True:
    cv2.imshow("", img_src)
    cv2.waitKey(0)
    
    cv2.imshow("",img0)
    cv2.waitKey(0)

'''
import pylab as plt
import seaborn as sns

f, axes = plt.subplots(3, 1)
axes = axes.ravel()

b = img1[:, :, 0].ravel() - img0[:,:,0].ravel()
sns.distplot(b,ax=axes[0],color='b')

g = img1[:, :, 1].ravel() - img0[:,:,1].ravel()
sns.distplot(b,ax=axes[1],color='g')

r = img1[:, :, 2].ravel() - img0[:,:,2].ravel()
sns.distplot(b,ax=axes[2],color='r')

plt.show()
'''
