import cv2 as cv

img = cv.imread("../pictures/AI.jpeg")
x, y, h, w = 150, 150, 150, 150
cv.rectangle(img, (x, y, x+w, y+h), color=(0, 255, 255),thickness=6)
x, y ,r = 300, 300, 150
cv.circle(img, (x, y), radius=r, color=(0, 0, 255),thickness=2)
cv.imshow("new_img",img)
cv.waitKey(0)
cv.destroyAllWindows()
