import sys
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt, QPoint, QTimer
from main import TaskifyApp  # Import TaskifyApp from main.py

class SplashScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.oldPos = self.pos()
        self.initUI()

    def initUI(self):
        self.setGeometry(100, 100, 800, 600)  # Set the same size as the app screen
        self.setStyleSheet("background-color: #3498db; color: #ffffff;")  # Button background color
        self.setWindowFlags(Qt.FramelessWindowHint)
        layout = QVBoxLayout()
        self.title_label = QLabel("Taskify")
        font = QFont()
        font.setPointSize(64)
        font.setBold(True)
        self.title_label.setFont(font)
        self.title_label.setAlignment(Qt.AlignCenter)
        layout.addStretch()
        layout.addWidget(self.title_label)
        layout.addStretch()
        self.setLayout(layout)

    def mousePressEvent(self, event):
        self.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self.oldPos)
        self.move(self.x() + delta.x(), self.y() + delta.y())
        self.oldPos = event.globalPos()

def main():
    app = QApplication(sys.argv)
    splash = SplashScreen()
    splash.show()

    def load_main_window():
        splash.close()
        taskify_app = TaskifyApp()
        taskify_app.show()

    QTimer.singleShot(3000, load_main_window)  # Wait for 3 seconds
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()