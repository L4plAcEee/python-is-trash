import sys

from PyQt5.QtWidgets import QApplication

from resouces.练习 import UI

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = UI.MainWindow()
    sys.exit(app.exec_())