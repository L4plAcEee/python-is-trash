import cv2 as cv


def face_detect_demo():
    gray = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
    face_detector = cv.CascadeClassifier("../../.venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
    faces = face_detector.detectMultiScale(gray)
    for x, y, h, w in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
    cv.imshow("result_img", img)


img = cv.imread("../pictures/face1.jpeg")
face_detect_demo()
cv.waitKey()
cv.destroyAllWindows()
