import cv2
from app.main.image_edit import draw_contours, PaperEdgeDetector

# image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20201214\lock.JPG'
# image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20201225\notebooks.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20210107\dm3.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\tedi.jpg'
# image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\2021\dm.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\2021\real.jpg'

image = cv2.imread(image_path)

edges = PaperEdgeDetector(image=image).get_image_edges()

draw_contours(image, edges, include_points=False)
cv2.waitKey(0)
