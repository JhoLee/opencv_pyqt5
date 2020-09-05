import datetime
import os
import sys
from pathlib import Path

import cv2
import filetype
import numpy as np
import qimage2ndarray as q2n
from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QPalette, QPixmap, QKeySequence, QImage
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QMainWindow, QScrollArea, QVBoxLayout, \
    QWidget, QGridLayout, QFileDialog, QShortcut

from image_editor.inference import InferenceModel
from main.utils import print_log

ROOT_DIR = os.path.realpath(os.getcwd())
print(ROOT_DIR)
RESOURCE_DIR = os.path.join(ROOT_DIR, 'resources')
IMG_DIR = os.path.join(RESOURCE_DIR, 'img')

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

        self.show_image(os.path.join(IMG_DIR, "sample2.jpg"))

        self.set_status("HI")

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
        self.btnGroup.addWidget(self.detectBtn, 0, 1)
        self.btnGroup.addWidget(self.compareBtn, 0, 2)
        self.btnGroup.addWidget(self.viewWideBtn, 0, 3)
        self.btnGroup.addWidget(self.saveBtn, 0, 4)

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
        self.set_status("Select image...")
        fname = QFileDialog.getOpenFileName(self, 'Open image', str(Path.home()),
                                            "Image files (*.jpg *.jpeg *.gif *.png)")

        if fname[0]:
            print_log("File path is '{}'".format(fname[0]))
            try:
                kind = filetype.guess(fname[0])
                print_log("Mime type: '{}'".format(kind.mime))
                if kind.mime.split("/")[0] == "image":
                    self.show_image(fname[0])
                    self.set_status("Opened.")
                else:
                    print_log("Not Supported File")
                    self.set_status("Not Supported file..")
            except FileNotFoundError as e:
                print_log("File Not Found!")
                self.set_status("File not found!")
        else:
            print_log("File path is not defined.")
            self.set_status("File not selected.")
        print_log("Finish")

    @pyqtSlot()
    def detect_image(self):
        print_log("Start")
        self.set_status("Detecting...")
        if self.image is None:
            print_log("Image not loaded!", "warn")
            self.set_status("You must load an image.")
        self.set_status("Detecting finished.")
        print_log("End")

    def show_image(self, img):
        print_log("Start")
        qimage = None
        if isinstance(img, str):
            qimage = QImage(img)
        elif isinstance(img, np.ndarray):
            qimage = q2n.array2qimage(img, normalize=False)

        pixmap = QPixmap.fromImage(qimage)
        im_w, im_h = pixmap.size().width(), pixmap.size().height()
        if im_w > im_h:
            pixmap = pixmap.scaledToWidth(self.label_min)
        else:
            pixmap = pixmap.scaledToHeight(self.label_min)

        self.imageLabel.setPixmap(pixmap)
        self.imageLabel.setAlignment(Qt.AlignCenter)
        self.image = cv2.imread(img)
        cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB)
        print_log("End")

    def set_status(self, msg: str):
        msg = "({timestamp}) {msg}".format(
            timestamp=datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            msg=msg,
        )
        self.statusBar().showMessage(msg)


def main():
    app = QApplication(sys.argv)

    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == "__main__":
    main()
