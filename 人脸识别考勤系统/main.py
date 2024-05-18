import sys
import time
import cv2
import pyttsx3
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QVBoxLayout
from PyQt5.QtCore import QThread, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from resouces import MySqlTool


class VideoThread(QThread):
    change_pixmap_signal = pyqtSignal(QImage)
    result_signal = pyqtSignal(str)

    def __init__(self, parent=None):
        super(VideoThread, self).__init__(parent)
        self._run_flag = True
        self.name_list = {
            1: "雷军"
        }
        self.face_detector = cv2.CascadeClassifier(
            "../.venv/Lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")
        self.recognizer = cv2.face.LBPHFaceRecognizer_create()
        self.recognizer.read("./trainer/trainer.yml")
        self.cap = cv2.VideoCapture(0)
        MySqlTool.ConnectSql()

    def run(self):
        while self._run_flag:
            ref, frame = self.cap.read()
            if not ref:
                break

            label, confidence = self.face_recognition(frame)
            self.display_image(frame)

            if label > 0 and confidence < 50:
                currentTime = time.strftime(f"%Y-%m-%d %H:%M:%S", time.localtime())
                MySqlTool.ExecuteData(
                    "insert into attendance(name,time)values('%s', '%s')" % (f"{self.name_list[label]}", currentTime))
                result_text = f"{self.name_list[label]}签到成功！当前时间为：{currentTime}"
                self.result_signal.emit(result_text)
                text = pyttsx3.init()
                text.say(result_text)
                text.runAndWait()

                break

    def display_image(self, img):
        qformat = QImage.Format_RGB888
        out_image = QImage(img, img.shape[1], img.shape[0], img.strides[0], qformat)
        out_image = out_image.rgbSwapped()
        self.change_pixmap_signal.emit(out_image)

    def face_recognition(self, img):
        try:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            faces = self.face_detector.detectMultiScale(gray)
            label = 0
            confidence = 200
            for (x, y, w, h) in faces:
                face_roi = gray[y:y + h, x:x + w]
                label, confidence = self.recognizer.predict(face_roi)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
            return label, confidence
        except cv2.error as e:
            print(f"OpenCV 错误：{e}")
        except Exception as e:
            print(f"其他错误：{e}")
        return 0, 200

    def stop(self):
        self._run_flag = False
        self.cap.release()
        MySqlTool.CloseMySql()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("人脸识别签到系统")

        self.image_label = QLabel(self)
        self.image_label.setFixedSize(640, 480)
        self.image_label.setStyleSheet("background-color: black; color: black;")

        self.result_label = QLabel('点击“签到”按钮以捕捉和识别人脸', self)

        self.button = QPushButton('签到', self)
        self.button.clicked.connect(self.signin)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.image_label)
        self.layout.addWidget(self.button)
        self.layout.addWidget(self.result_label)
        self.setLayout(self.layout)

        self.thread = VideoThread()
        self.thread.change_pixmap_signal.connect(self.update_image)
        self.thread.result_signal.connect(self.update_result)

    def update_image(self, cv_img):
        self.image_label.setPixmap(QPixmap.fromImage(cv_img))

    def update_result(self, text):
        self.result_label.setText(text)
        self.thread.stop()

    def signin(self):
        self.result_label.setText('正在捕捉...')
        self.thread.start()

    def closeEvent(self, event):
        self.thread.stop()
        event.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = MainWindow()
    main_win.show()
    sys.exit(app.exec_())
