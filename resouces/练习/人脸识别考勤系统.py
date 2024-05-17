import sys
import time
import cv2
import pyttsx3
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLabel, QVBoxLayout, QWidget
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap
from resouces import MySqlTool


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        MySqlTool.ConnectSql()
        self.initUI()

        self.cap = cv2.VideoCapture(0)
        # 加载训练好的 LBPH 人脸识别器
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("./trainer/trainer.yml")
        # 加载人脸检测器
        self.face_detector = cv2.CascadeClassifier(
            "../../.venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(30)
        self.name_list = {
            1: "王尼玛"
        }

    def initUI(self):
        self.setWindowTitle('签到系统')

        self.label = QLabel(self)
        self.label.setAlignment(Qt.AlignCenter)
        self.label.resize(640, 480)

        self.btn = QPushButton('签到', self)
        self.btn.clicked.connect(self.signin)

        self.result_label = QLabel(self)
        self.result_label.setAlignment(Qt.AlignCenter)
        self.result_label.resize(640, 30)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.btn)
        layout.addWidget(self.result_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.show()

    def face_detect(self, img):
        gray = cv2.cvtColor(img, cv2.COLOR_BGRA2GRAY)
        # 检测人脸
        faces = self.face_detector.detectMultiScale(gray)
        # 遍历每个检测到的人脸
        for (x, y, w, h) in faces:
            # 提取人脸区域
            face_roi = gray[y:y + h, x:x + w]
            # 识别人脸并获取置信度得分
            label, confidence = self.recognizer.predict(face_roi)
            # 在图片上绘制人脸框
            cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            # 在人脸框上方显示置信度得分和模型ID
            cv2.putText(img, f"ID: {label}, Confidence: {confidence:.2f}",
                        (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    def update_frame(self):
        ret, self.frame = self.cap.read()
        if ret:
            self.face_detect(self.frame)
            self.display_image(self.frame)

    def display_image(self, img):
        qformat = QImage.Format_RGB888
        out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        out_image = out_image.rgbSwapped()
        self.label.setPixmap(QPixmap.fromImage(out_image))

    def signin(self):
        self.recognize_face(self.cap.read()[1])

    def recognize_face(self, img):
        # 我们有一个人脸识别函数 `face_recognition`，这里调用它来进行签到
        label_list, confidence_list = face_recognition(img, self.face_detector, self.recognizer)
        currentTime = time.strftime(f"%Y-%m-%d %H:%M:%S", time.localtime())
        for i in range(0, len(label_list)):
            if confidence_list[i] <= 60:
                # result = MySqlTool.SearchSingle("select *from attendance where name='%s'" % f"{self.name_list[label_list[i]]}")
                # if not result:
                #     MySqlTool.ExecuteData(
                #         "insert into attendance(name,time)values('%s', '%s')" % (f"{self.name_list[label_list[i]]}", currentTime))
                #     self.result_label.setText(f"{self.name_list[label_list[i]]}签到成功！当前时间为：{currentTime}")
                # else:
                #     self.result_label.setText(f"{self.name_list[label_list[i]]}重复签到！当前时间为：{currentTime}")
                MySqlTool.ExecuteData(
                    "insert into attendance(name,time)values('%s', '%s')" % (f"{self.name_list[label_list[i]]}", currentTime))
                self.result_label.setText(f"{self.name_list[label_list[i]]}签到成功！当前时间为：{currentTime}")
            else:
                self.result_label.setText(f"{self.name_list[label_list[i]]}签到失败，请重试")
            try:
                text = pyttsx3.init()
                text.say(self.result_label.text())
                text.runAndWait()
            except Exception as e:
                print("发生错误:", e)

    def closeEvent(self, event):
        MySqlTool.CloseMySql()
        self.cap.release()
        cv2.destroyAllWindows()
        event.accept()


def face_recognition(img, face_detector, recognizer):
    try:

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # 检测人脸
        faces = face_detector.detectMultiScale(gray)
        if len(faces) == 0:
            print("未检测到人脸")

        # 遍历每个检测到的人脸
        label_list = []
        confidence_list = []
        for (x, y, w, h) in faces:
            # 提取人脸区域
            face_roi = gray[y:y + h, x:x + w]

            # 识别人脸并获取置信度得分
            label, confidence = recognizer.predict(face_roi)
            label_list.append(label)
            confidence_list.append(confidence)

        return label_list, confidence_list

    except cv2.error as e:
        print(f"OpenCV 错误：{e}")
    except Exception as e:
        print(f"其他错误：{e}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
