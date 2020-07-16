import cv2
import numpy as np

#frameWidth = 640
#frameHeight = 480
cap = cv2.VideoCapture(1)
cap.set(3, 640)
cap.set(4, 480)
cap.set(10, 130)

# h_min, s_min, v_min, h_max, s_max,v_max
myColors = [[26, 82, 119, 179, 255, 255],  # hot pink
            [28, 78, 0, 138, 255, 255],    # green
            [226, 90, 0, 132, 255, 255],   # yellow
            [22, 115, 0, 179, 255, 255],   # blue
            [35, 70, 66, 157, 255, 255],   # purple
            [0, 181, 234, 33, 255, 255]]   # orange

myColorValues = [[153, 51, 255],   # hot pink          #BGR in HSV
                 [0, 255, 0],      # green
                 [102, 255, 255],  # yellow
                 [255, 0, 0],      # blue
                 [255, 0, 127 ],   # purple
                 [0, 128, 255]]    # orange


myPoints = [] #[x, y, colorId]

def findColors(img, myColors, myColorValues):
    imgHSV = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    count = 0
    newPoints = []
    for color in myColors: # gives us 3 diff windows
        lower = np.array(color[0:3])
        upper = np.array(color[3:6])
        mask = cv2.inRange(imgHSV,lower,upper)
        getContours(mask)
        x, y = getContours(mask)
        cv2.circle(imgResult, (x, y), 10, myColorValues[count], cv2.FILLED)
        if x!=0 and y!=0:
            newPoints.append([x, y, count])
        count +=1
        #cv2.imshow(str(color[0]),mask)
    return newPoints

# we need to get our contours, so that we can find the location of the object in img/vid
def getContours(img):
    contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    x, y, w, h = 0, 0, 0, 0
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area>500:
            #cv2.drawContours(imgResult, cnt, -1, (255, 0, 0), 3)
            peri = cv2.arcLength(cnt, True)
            approx = cv2.approxPolyDP(cnt, 0.02*peri, True)
            x, y, w, h = cv2.boundingRect(approx)
    return x+w//2, y  # top of bounding box

def drawOnCanvas(myPoints, myColorValues):
    for point in myPoints:
        cv2.circle(imgResult, (point[0], point[1]), 10, myColorValues[point[2]], cv2.FILLED)

while True:
    success, img = cap.read()
    imgResult = img.copy()
    newPoints = findColors(img, myColors, myColorValues)
    if len(newPoints) != 0:
        for newP in newPoints:
            myPoints.append(newP) # appendin since newpoints is a list
    if len(myPoints) != 0:
        drawOnCanvas(myPoints, myColorValues)

    cv2.imshow('Result', imgResult)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break