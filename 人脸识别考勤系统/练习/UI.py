from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QObject, pyqtSignal, QThread, pyqtSlot
from PyQt5.QtWidgets import QApplication, QMainWindow


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(640, 615)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(0, 0, 640, 480))
        self.label.setMinimumSize(QtCore.QSize(640, 480))
        self.label.setText("")
        self.label.setObjectName("label")

        self.result_label = QtWidgets.QLabel(self.centralwidget)
        self.result_label.setGeometry(QtCore.QRect(0, 530, 640, 60))
        self.result_label.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.result_label.setObjectName("label_2")
        self.result_label.setAlignment(QtCore.Qt.AlignCenter)

        self.btn = QtWidgets.QPushButton(self.centralwidget)
        self.btn.setGeometry(QtCore.QRect(280, 490, 75, 23))
        self.btn.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.btn.setObjectName("pushButton")
        self.btn.clicked.connect(self.signin)

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.result_label.setText(_translate("MainWindow", ""))
        self.btn.setText(_translate("MainWindow", "签到"))

    def signin(self):
        pass


class CameraThread(QObject):
    finished = pyqtSignal()  # 完成信号

    @pyqtSlot()
    def run(self):

        self.finished.emit()  # 发送完成信号


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.thread = QThread()
        self.worker = CameraThread()
        self.worker.moveToThread(self.thread)
        self.worker.finished.connect(self.task_finished)

        self.thread.started.connect(self.worker.run)
        self.setupUi(self)
        self.retranslateUi(self)
        self.show()

    def signin(self):
        self.btn.setEnabled(False)
        self.thread.start()