import cv2 as cv

img = cv.imread("../pictures/AI.jpeg")
cv.imshow("AI_img", img)
gray_img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
cv.imshow("AI_img_gray", gray_img)
cv.imwrite("../pictures/gray_AI_img.jpeg", gray_img)
cv.waitKey()
cv.destroyAllWindows()
