import cv2 as cv

# 加载训练好的 LBPH 人脸识别器
recognizer = cv.face.LBPHFaceRecognizer_create()
recognizer.read("./trainer/trainer.yml")

# 加载人脸检测器
face_detector = cv.CascadeClassifier("../../.venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

# 读取图片
# img = cv.imread("pictures/9.jpg")
img = cv.imread("../pictures/(16).jpg")
gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

# 检测人脸
faces = face_detector.detectMultiScale(gray)

# 遍历每个检测到的人脸
for (x, y, w, h) in faces:
    # 提取人脸区域
    face_roi = gray[y:y + h, x:x + w]

    # 识别人脸并获取置信度得分
    label, confidence = recognizer.predict(face_roi)

    # 在图片上绘制人脸框
    cv.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # 在人脸框上方显示置信度得分和模型ID
    cv.putText(img, f"ID: {label}, Confidence: {confidence:.2f}",
               (x, y - 10), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
    print(f"ID: {label}, Confidence: {confidence:.2f}")

# 显示图片
cv.imshow("Faces", img)
cv.waitKey(0)
cv.destroyAllWindows()
