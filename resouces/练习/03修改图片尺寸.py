import cv2 as cv

img = cv.imread("../pictures/AI.jpeg")
cv.imshow("AI_img", img)
print("原图片形状：", img.shape)
resize_img = cv.resize(img, dsize=(500, 500))
print("修改后图片形状：", resize_img)
cv.imshow("resize_AI_img", resize_img)
cv.waitKey()
cv.destroyAllWindows()
