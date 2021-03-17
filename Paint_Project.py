import cv2
import numpy as np

frame_width = 700
frame_height = 700

cap = cv2.VideoCapture(0)
cap.set(3, frame_width)
cap.set(4, frame_height)
cap.set(10, 150)  # brightness setting

# define colors to detect
# requires min and max saturation values for each color
colors = [[153, 92, 163, 179, 255, 255],  # hot pink
          [64, 143, 101, 99, 255, 255],   # green
          [103, 102, 0, 131, 224, 255],   # purple
          [5, 23, 213, 55, 193, 255]]     # yellow

# list of BGR colors for each HSV color
# so that bounding bx point is same color as color/object detected
color_values = [[211, 73, 244],  # hot pink
                [51, 255, 128],  # green
                [255, 47, 149],  # purple
                [43, 246, 204]]  # yellow

# list of points
points = []


# function for finding colors
def find_color(img, colors, color_values):
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    new_points = []
    for color in colors:
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(img_hsv, lower, upper)  # set limits for mask
        x, y = get_contours(mask)
        cv2.circle(img_result, (x, y), 10, color_values[count], cv2.FILLED)
        if x != 0 and y != 0:
            new_points.append([x, y, count])
        count += 1
        # cv2.imshow(str(color[0]), mask) for testing
    return new_points


# we need to get our contours, so that we can find the location of the object in img/vid
def get_contours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 500:
            # cv2.draw_contours(img_result, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y  # top of bounding box at the tip of marker


def draw_on_screen(points, color_values):
    for point in points:
        cv2.circle(img_result, (point[0], point[1]), 20, color_values[point[2]], cv2.FILLED)


while True:
    success, img = cap.read()
    img_result = img.copy()
    new_points = find_color(img, colors, color_values)
    if len(new_points) != 0:
        for newP in new_points:
            points.append(newP)  # putting a list inside a list, since the points create a list
    if len(points) != 0:
        draw_on_screen(points, color_values)

    cv2.imshow("Result", img_result)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

