import os
import os
import sys
from pathlib import Path

import cv2
import filetype
from PyQt5 import uic
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPalette, QPixmap, QKeySequence
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QScrollArea, QVBoxLayout, \
    QWidget, QGridLayout, QFileDialog, QShortcut

from src.utils import print_log

ROOT_DIR = os.path.realpath(os.pardir)
UI_DIR = os.path.join(ROOT_DIR, 'designer')
RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')
IMG_DIR = os.path.join(RESOURCE_DIR, 'img')

form_class = uic.loadUiType(os.path.join(UI_DIR, "mainwindow.ui"))[0]

HEIGHT = 800
WIDTH = 600


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.image = None

        print_log("Start", "debug")
        self.initUI()
        print_log("End", "debug")

    def initUI(self):
        print_log("Start", "debug")
        self.setFixedSize(WIDTH, HEIGHT)
        self.setWindowTitle('Scroll Area Demonstration')

        # Widgets
        self.imageLabel = QLabel("ImageLabel")
        self.imageLabel.setBackgroundRole(QPalette.Dark)

        self.imageLabel = QLabel("ImageLabel")
        label_w, label_h = self.imageLabel.size().width(), self.imageLabel.size().height()
        self.label_min = min(label_w, label_h)

        self.imageLabel.resize(self.label_min, self.label_min)
        print_log("Resize imageLabel")

        self.set_image(os.path.join(IMG_DIR, "sample2.jpg"))

        self.statusBar().showMessage("HI")

        self.openBtn = QPushButton("Open")
        self.openBtn.clicked.connect(self.open_image)

        self.detectBtn = QPushButton("Detect")
        self.detectBtn.clicked.connect(self.detect_image)

        self.compareBtn = QPushButton("Compare")

        self.viewWideBtn = QPushButton("View Wide")

        self.saveBtn = QPushButton("Save")

        self.scrollArea = QScrollArea()

        # Layouts
        self.btnGroup = QGridLayout()
        self.btnGroup.addWidget(self.openBtn, 0, 0)
        self.btnGroup.addWidget(self.saveBtn, 0, 1)
        self.btnGroup.addWidget(self.viewWideBtn, 0, 2)
        self.btnGroup.addWidget(self.compareBtn, 0, 3)

        self.viewLayout = QVBoxLayout()

        self.layout = QVBoxLayout()

        self.layout.addWidget(self.imageLabel)

        self.layout.addLayout(self.btnGroup)

        self.layout.addWidget(self.scrollArea)

        # Shortcuts
        self.openFile = QShortcut(QKeySequence("Ctrl+O"), self)
        self.openFile.activated.connect(self.open_image)

        centralWidget = QWidget()
        centralWidget.setLayout(self.layout)
        self.setCentralWidget(centralWidget)

        print_log("End", "debug")

    @pyqtSlot()
    def open_image(self):
        print_log("Start")
        self.statusBar().showMessage("Select image...")
        fname = QFileDialog.getOpenFileName(self, 'Open image', str(Path.home()),
                                            "Image files (*.jpg *.jpeg *.gif *.png)")
        print_log("File path is '{}'".format(fname[0]))

        if fname[0]:
            try:
                kind = filetype.guess(fname[0])
                print_log("Mime type: '{}'".format(kind.mime))
                if kind.mime.split("/")[0] == "image":
                    self.set_image(fname[0])
                    print_log("Image label setting done.")
                    self.statusBar().showMessage("Opened.")
                else:
                    print_log("Not Supported File")
                    self.statusBar().showMessage("Not Supported file..")
            except FileNotFoundError as e:
                print_log("File Not Found!")
                self.statusBar().showMessage("File not found!")
        print_log("Finish")

    @pyqtSlot()
    def detect_image(self):
        print_log("Start")

    def set_image(self, image_path):
        pixmap = QPixmap(image_path)
        im_w, im_h = pixmap.size().width(), pixmap.size().height()
        if im_w > im_h:
            pixmap = pixmap.scaledToWidth(self.label_min)
        else:
            pixmap = pixmap.scaledToHeight(self.label_min)

        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.image = cv2.imread(image_path)
        cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
