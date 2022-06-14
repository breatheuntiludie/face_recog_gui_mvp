import cv2
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPixmap, QImage

class Camera:

    def __init__(self, camera):
        self.camera = camera
        self.cap = None

    def openCamera(self):
        self.vc = cv2.VideoCapture(0)
        # vc.set(5, 30)  #set FPS
        self.vc.set(3, 640)  # set width
        self.vc.set(4, 480)  # set height

        if not self.vc.isOpened():
            print('failure')
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return

    # https://stackoverflow.com/questions/41103148/capture-webcam-video-using-pyqt
    def initialize(self):
        self.cap = cv2.VideoCapture(self.camera)



from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox
#from models import Camera

class UI_Window(QWidget):

    def __init__(self, camera = None):
        super().__init__()
        self.camera = camera
        print('UI')
        # Create a timer.
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)

        # Create a layout.
        layout = QVBoxLayout()

        # Add a button
        button_layout = QHBoxLayout()

        btnCamera = QPushButton("Open camera")
        btnCamera.clicked.connect(self.start)
        button_layout.addWidget(btnCamera)
        layout.addLayout(button_layout)

        # Add a label
        self.label = QLabel()
        self.label.setFixedSize(640, 640)

        layout.addWidget(self.label)

        # Set the layout
        self.setLayout(layout)
        self.setWindowTitle("First GUI with QT")
        self.setFixedSize(800, 800)

    def start(self):
        camera.openCamera()
        self.timer.start(1000. / 24)

    def nextFrameSlot(self):
        face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml')
        ret, frame = camera.vc.read()
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        for (x, y, w, h) in faces:
            print(x, y, h, w)
            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            # img_save = "my_image.png"
            # cv2.imwrite(img_save, roi_gray)
            color = (255, 0, 0)  # BlueGreenRed - BGR (why??)but RGB in pyqt
            stroke = 2
            width = x + w
            height = y + h
            cv2.rectangle(frame, (x, y), (width, height), color, stroke)
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(image)
        self.label.setPixmap(pixmap)


    # https://stackoverflow.com/questions/1414781/prompt-on-exit-in-pyqt-application

class MovieThread(QThread):
    def __init__(self, camera):
        super().__init__()
        self.camera = camera

    def run(self):
        self.camera.acquire_movie(200)

#if __name__ == '__main__':
#    app = QApplication([])
#    window = UI_Window()
#    window.show()

#start.py

from PyQt5.QtWidgets import QApplication

#from models import Camera
#from views import UI_Window

camera = Camera(0)
#camera.initialize()
print('test')
app = QApplication([])
start_window = UI_Window(camera)
start_window.show()
app.exit(app.exec_())