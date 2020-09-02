import os
import sys

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QSizePolicy, QScrollArea, QVBoxLayout, \
    QGroupBox, QFormLayout, QWidget, QHBoxLayout, QGridLayout
from PyQt5 import uic

ROOT_DIR = os.path.realpath(os.pardir)
UI_DIR = os.path.join(ROOT_DIR, 'designer')
RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')
IMG_DIR = os.path.join(RESOURCE_DIR, 'img')

form_class = uic.loadUiType(os.path.join(UI_DIR, "mainwindow.ui"))[0]


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        # self.setGeometry(600, 100, 600, 800)
        self.setFixedSize(600, 800)
        self.setWindowTitle('Scroll Area Demonstration')

        self.imageLabel = QLabel("ImageLabel")
        self.imageLabel.setBackgroundRole(QPalette.Dark)
        pixmap = QPixmap(os.path.join(IMG_DIR, "sample2.jpg"))

        im_w, im_h = pixmap.size().width(), pixmap.size().height()
        label_w, label_h = self.imageLabel.size().width(), self.imageLabel.size().height()
        label_min = min(label_w, label_h)

        self.imageLabel.resize(label_min, label_min)

        if im_w > im_h:
            pixmap = pixmap.scaledToWidth(label_min)
        else:
            pixmap = pixmap.scaledToHeight(label_min)

        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setScaledContents(True)

        self.openBtn = QPushButton("Open")

        self.saveBtn = QPushButton("Save")

        self.viewWideBtn = QPushButton("View Wide")

        self.compareBtn = QPushButton("Compare")

        self.scrollArea = QScrollArea()

        self.btnGroup = QGridLayout()
        self.btnGroup.addWidget(self.openBtn, 0, 0)
        self.btnGroup.addWidget(self.saveBtn, 0, 1)
        self.btnGroup.addWidget(self.viewWideBtn, 0, 2)
        self.btnGroup.addWidget(self.compareBtn, 0, 3)

        self.viewLayout = QVBoxLayout()

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.imageLabel)
        # todo: Align widgets in layout

        self.layout.addLayout(self.btnGroup)

        self.layout.addWidget(self.scrollArea)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
