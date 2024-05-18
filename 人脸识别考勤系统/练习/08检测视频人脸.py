import cv2 as cv


def face_detect_demo(img):
    gray = cv.cvtColor(img, cv.COLOR_BGRA2GRAY)
    face_detector = cv.CascadeClassifier("../../.venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
    faces = face_detector.detectMultiScale(gray)
    for x, y, h, w in faces:
        cv.rectangle(img, (x, y), (x + w, y + h), color=(0, 255, 0), thickness=2)
    cv.imshow("result", img)


cap = cv.VideoCapture("../video/video.mp4")

while True:
    flag, frame = cap.read()
    if not flag:
        break
    face_detect_demo(frame)
    if ord("q") == cv.waitKey(1):
        break
cv.destroyAllWindows()
cap.release()