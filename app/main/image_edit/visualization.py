import cv2
import imutils
import numpy as np


def draw_contours(image, contour, include_points=False, title='Outline'):
    ratio = image.shape[0] / 650.0
    contour = (contour / ratio).astype(np.int32)
    image = imutils.resize(image, height=650)
    if include_points:
        for p in contour:
            cv2.drawMarker(image, tuple(p[0]), color=(0, 0, 255), markerType=cv2.MARKER_DIAMOND)
    cv2.drawContours(image, [contour], -1, (0, 255, 0), 2)
    cv2.imshow(title, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


