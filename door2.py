import cv2
from numpy import *

test_imgs = ['day_open.jpg']
#'night_open.jpg', 'night_closed.jpg', 'day_open.jpg', 'day_closed.jpg'

for imgFile in test_imgs:
    img = cv2.imread(imgFile)

    print (img)

    