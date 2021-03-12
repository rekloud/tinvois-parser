# import the necessary packages
from rdp import rdp
from .utils import four_point_transform, order_points, clockwise_angle_and_distance
from skimage.filters import threshold_local
import numpy as np
import argparse
import cv2
import imutils
from math import atan2
# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20201214\lock.JPG'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20201225\notebooks.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20210107\dm2.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\tedi.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\2021\mostafa2.jpg'
image = cv2.imread(image_path)
ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height=500)
# convert the image to grayscale, blur it, and find edges
# in the image
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(gray, (5, 5), 0)
edged = cv2.Canny(gray, 30, 200)
# show the original image and the edge detected image
print("STEP 1: Edge Detection")
cv2.imshow("Image", image)
cv2.imshow("Edged", edged)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
nb_edges, output, stats, centroids = cv2.connectedComponentsWithStats(edged.copy(), connectivity=8)
label_of_biggest_component = stats[1:, 4].argmax() + 1
print('output', output.shape)
output[output != label_of_biggest_component] = 0
output[output == label_of_biggest_component] = 100
print('output', output.shape)
print('edged', edged.shape)
# cv2.imshow("nb_edges", nb_edges)
cv2.imshow("output", output.astype(np.uint8))
cv2.imwrite(image_path+'.png', output)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
print('EGES')
print(len(edged))
# cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
# image = cv2.cvtColor(output.copy(), cv2.COLOR_BGR2GRAY)
cnts = cv2.findContours(output.astype(np.uint8), cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
print('cnts')
print(len(cnts))
# cnts = imutils.grab_contours(cnts)
# cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
# loop over the contours
screenCnt = None
cnt = np.array([[[b, a]] for a, b in zip(*np.where(output == 100))])
# for c in cnts:
    # approximate the contour
peri = cv2.arcLength(cnt, True)
# approx = cv2.approxPolyDP(cnt, 0.05 * peri, True)
approx = cv2.convexHull(cnt)
print('approx', len(approx))
# if our approximated contour has four points, then we
# can assume that we have found our screen
print("STEP 2: Find contours of paper")
# cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
for p in approx:
    # print('p', p)
    cv2.drawMarker(image, tuple(p[0]), color=(0,255,0), markerType=cv2.MARKER_CROSS)
cv2.imshow("full Outline", image)
epsilon = 0
for i in range(10):
    approx = order_points(approx.reshape(-1, 2)).reshape(-1, 1, 2).astype(np.int32)
    # approx = np.array(sorted(approx, key=lambda p: clockwiseangle_and_distance(approx[0][0], p[0])))
    print('len(approx)', len(approx))
    if len(approx) > 4:
        approx = rdp(approx, epsilon=epsilon)
        print(i, 'rdp', len(approx))
    else:
        break
    epsilon += .5
# print(approx, approx.shape, approx.dtype)
# cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
for p in approx:
    # print('p', p)
    cv2.drawMarker(image, tuple(p[0]), color=(0,0,255), markerType=cv2.MARKER_DIAMOND)
cv2.drawContours(image, [approx], -1, (0, 255, 0), 2)
# cv2.destroyAllWindows()
cv2.imshow("Outline", image)
# print('screenCnt', screenCnt)
# show the contour (outline) of the piece of paper
cv2.waitKey(0)
# if len(approx) == 5:
#     approx = approx[:-1]


# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, approx.reshape(4, 2) * ratio)
cv2.imwrite(image_path+'.jpg', warped)
# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
# warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# T = threshold_local(warped, 11, offset = 10, method = "gaussian")
# warped = (warped > T).astype("uint8") * 255
# show the original and scanned images
print("STEP 3: Apply perspective transform")
# cv2.imshow("Original", imutils.resize(orig, height = 650))
cv2.imshow("Scanned", imutils.resize(warped, height = 650))
cv2.waitKey(0)