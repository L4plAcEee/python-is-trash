import cv2 as cv


img = cv.imread("../pictures/AI.jpeg")
cv.imshow("AI.jpeg", img)
cv.waitKey(0)
cv.destroyWindow("AI.jpeg")
