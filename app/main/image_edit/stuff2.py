import numpy as np
import cv2

image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20201214\lock.JPG'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20201225\notebooks.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\20210107\dm2.jpg'
image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\tedi.jpg.png'
# image_path = r'C:\Users\shossein\Downloads\Telegram Desktop\2021\dm.jpg'
# read image


def order_points(pts):
    rect = np.zeros((4, 2), dtype = "float32")
    s = pts.sum(axis = 1)
    rect[0] = pts[np.argmin(s)]
    rect[2] = pts[np.argmax(s)]
    diff = np.diff(pts, axis = 1)
    rect[1] = pts[np.argmin(diff)]
    rect[3] = pts[np.argmax(diff)]
    return rect

def four_point_transform(image, pts):
    (tl, tr, br, bl) = pts
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype = "float32")
    M = cv2.getPerspectiveTransform(pts, dst)
    warped = cv2.warpPerspective(image, M, (maxWidth, maxHeight))
    return warped

def intersection(line1, line2):
    """Finds the intersection of two lines given in Hesse normal form.
    Returns closest integer pixel locations.
    See https://stackoverflow.com/a/383527/5087436
    """
    rho1, theta1 = line1
    rho2, theta2 = line2
    A = np.array([
        [np.cos(theta1), np.sin(theta1)],
        [np.cos(theta2), np.sin(theta2)]
    ])
    b = np.array([[rho1], [rho2]])
    x0, y0 = np.linalg.solve(A, b)
    x0, y0 = int(np.round(x0)), int(np.round(y0))
    return [[x0, y0]]

def resize(image, width=None, height=None, inter=cv2.INTER_AREA):
    dim = None
    (h, w) = image.shape[:2]
    if width is None and height is None:
        return image
    if width is None:
        r = height / float(h)
        dim = (int(w * r), height)
    else:
        r = width / float(w)
        dim = (width, int(h * r))
    resized = cv2.resize(image, dim, interpolation=inter)
    return resized

def draw_lines(image, lines):
    for line in lines:
        rho, theta = line
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a*rho
        y0 = b*rho
        x1 = int(x0 + 1000*(-b))
        y1 = int(y0 + 1000*(a))
        x2 = int(x0 - 1000*(-b))
        y2 = int(y0 - 1000*(a))
        cv2.line(image, (x1, y1), (x2, y2), (0,0,255), 2)

image = cv2.imread(image_path)
orig = image.copy()
draw = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.bitwise_not(gray)
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (45, 45)) # Increased kernel size
gray = cv2.morphologyEx(gray, cv2.MORPH_CLOSE, sqKernel)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

# Find the right most point of the content by finding contours.
# This is required as the content doesn't have extreme right edge line
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]

origH, origW = gray.shape[:2]
xMIN = origW
yMIN = origH
xwMAX = 0
yhMAX = 0

for c in cnts:
    (x, y, w, h) = cv2.boundingRect(c)
    if x > 5 and y > 5 and x + w < origW - 5 and y + h < origH - 5:
        if xMIN > x: xMIN = x
        if yMIN > y: yMIN = y
        if xwMAX < x + w: xwMAX = x + w
        if yhMAX < y + h: yhMAX = y + h

# Edge detection and houghlines transform for finding edge lines
edges = cv2.Canny(image, 50, 200)
cv2.imshow("Input", resize(image, height = 650))

lines = cv2.HoughLines(edges, 1, np.pi/180, 100)

# Filter out irrelevant lines from houghlines transform
strong_lines = np.zeros([12, 1, 2]) # Increased number of considered strong_lines
n2 = 0
for n1 in range(0,len(lines)):
    for rho,theta in lines[n1]:
        theta_diff = np.abs(np.abs(theta) - np.abs(strong_lines[0, 0, 1])) * 180 / np.pi
        if theta_diff > 90:
            theta_diff -= 90
        if rho < 0:
           rho*=-1
           theta-=np.pi
        if n1 == 0:
            strong_lines[n2] = rho, theta
            n2 = n2 + 1
        elif n2 < 12 and not np.isclose(theta_diff, 45, atol=15):
            closeness_rho = np.isclose(rho,strong_lines[0:n2,0,0],atol = max(image.shape) / 10) # One-tenth of the image width/height
            closeness_theta = np.isclose(theta,strong_lines[0:n2,0,1],atol = np.pi/36)
            closeness = np.all([closeness_rho,closeness_theta],axis=0)
            if not any(closeness):
                strong_lines[n2] = rho, theta
                n2 = n2 + 1

# Removing the blank strong_lines entries
if n2 < strong_lines.shape[0]:
    strong_lines.resize(n2, 1, 2)

# Grouping the filtered lines in horizontal and vertical categories
vert_ind = np.abs(strong_lines[:, :, 1] - 1.5) > 0.5
vert_lines = strong_lines[vert_ind]
hori_lines = strong_lines[np.logical_not(vert_ind), :]

test = np.argsort(np.abs(vert_lines[:, 0]))
vert_lines = vert_lines[test]

test = np.argsort(np.abs(hori_lines[:, 0]))
hori_lines = hori_lines[test]

# Extra vert_line to cater the right side where no houghlines will be detected
# After checking if the right most line is already there
far_point1 = intersection(vert_lines[0], hori_lines[0])
far_point2 = intersection(vert_lines[-1], hori_lines[-1])
if not np.isclose(far_point1[0][0], xwMAX, atol=10) and not np.isclose(far_point2[0][0], xwMAX, atol=10):
    vert_lines = np.append(vert_lines, [[xwMAX, vert_lines[0][1]]], 0)

# Finding the intersection points of the lines
points = []
num_vert_lines = vert_lines.shape[0]
num_hori_lines = hori_lines.shape[0]
for i in range(num_vert_lines):
    for j in range(num_hori_lines):
        point = intersection(vert_lines[i], hori_lines[j])
        points.append(point)

# Drawing the lines and points
draw_lines(draw, vert_lines)
draw_lines(draw, hori_lines)
[cv2.circle(draw, (p[0][0], p[0][1]), 5, 255, 2) for p in points]

# Finding the four corner points and ordering them
pts = np.asarray(points)
four_vertices = order_points(pts.reshape(pts.shape[0], pts.shape[2]))

# Giving a 5 pixels margin for better readability
four_vertices[0] = four_vertices[0][0] - 5, four_vertices[0][1] - 5
four_vertices[1] = four_vertices[1][0] + 5, four_vertices[1][1] - 5
four_vertices[2] = four_vertices[2][0] + 5, four_vertices[2][1] + 5
four_vertices[3] = four_vertices[3][0] - 5, four_vertices[3][1] + 5

# Perspective transform to get the warped image
warped = four_point_transform(orig, four_vertices)

# Displaying the results
cv2.imshow("Input", resize(image, height = 650))
cv2.imshow("Marks", resize(draw, height = 650))
cv2.imshow("Warped", resize(warped, height = 650))
cv2.waitKey(0)