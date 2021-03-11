import numpy as np
import cv2
from app.main.image_edit import draw_contours, PaperEdgeDetector

# image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20201214\lock.JPG'
# image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20201225\notebooks.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20210107\dm3.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\tedi.jpg'
# image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\2021\dm.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\2021\mostafa2.jpg'

image = cv2.imread(image_path)

edges = PaperEdgeDetector(image=image).get_image_edges()
# print(edges, edges.shape)
draw_contours(image, np.array(edges), include_points=False)
# cv2.waitKey(0)
