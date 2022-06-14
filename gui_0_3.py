import cv2
import sys
import pickle
from PIL import Image
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import QThread, QTimer
from PyQt5.QtWidgets import QLabel, QWidget, QPushButton, QVBoxLayout, QApplication, QHBoxLayout, QMessageBox

face_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_frontalface_alt2.xml') #cascade for face detection
eye_cascade = cv2.CascadeClassifier('cascades/data/haarcascade_eye.xml')
#initialise model + dataset
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read("trainner.yml")
labels = {"person_name": 1}
with open("labels.pickle", 'rb') as f:
    og_labels = pickle.load(f)
    labels = {v:k for k,v in og_labels.items()}


class Camera:

    def __init__(self, camera):
        self.camera = camera
        self.cap = None
        self.image_recog = "s"

    def openCamera(self):
        #print('openCamera class')
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, 640)  # set width webcam
        self.cap.set(4, 480)  # set height webcam
        #print('OpenCamera after cap.set')
        if not self.cap.isOpened():
            print('failure')
            msgBox = QMessageBox()
            msgBox.setText("Failed to open camera.")
            msgBox.exec_()
            return -2 # error of webcam

    def initialize(self):
        self.cap = cv2.VideoCapture(self.camera)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow, camera = None):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1500, 1000)
        MainWindow.setStyleSheet("background-color: rgb(17, 143, 202);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.Button_1 = QtWidgets.QPushButton(self.centralwidget)
        self.Button_1.setGeometry(QtCore.QRect(910, 670, 171, 61))
        self.Button_1.setStyleSheet("background-color: rgb(0, 255, 127);")
        #self.Button_1.setObjectName("Button_1")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1100, 670, 171, 61))
        self.pushButton.setStyleSheet("background-color: rgb(170, 0, 0);")
        #self.pushButton.setObjectName("pushButton")

        self.pushButton_face = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_face.setGeometry(QtCore.QRect(130, 730, 171, 61))
        self.pushButton_face.setStyleSheet("background-color: rgb(170, 40, 30);")

        MainWindow.setCentralWidget(self.centralwidget)
        #self.menubar = QtWidgets.QMenuBar(MainWindow)
        #self.menubar.setGeometry(QtCore.QRect(0, 0, 1500, 21))
        #self.menubar.setObjectName("menubar")
        #MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        #self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Add a label for video
        self.label = QtWidgets.QLabel(self.centralwidget)
        #self.label = QLabel()
        self.label.setGeometry(QtCore.QRect(830, 180, 640, 480))
        #self.label.setFixedSize(640, 480)
        #MainWindow.addWidget(self.label)

        # Add the label for shoplifters (recognised)
        self.label_recog = QtWidgets.QLabel(self.centralwidget)
        self.label_recog.setGeometry(QtCore.QRect(100,70, 200,200))


        self.camera = camera
        self.timer = QTimer()
        self.timer.timeout.connect(self.nextFrameSlot)
        #self.timer.timeout.connect(self.show_pic)

        self.add_functions()

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Биометрическая система идентификации посетитиелей магазина"))
        self.Button_1.setText(_translate("MainWindow", "Просмотр камеры"))
        self.pushButton.setText(_translate("MainWindow", "Прекратить запись"))
        self.pushButton_face.setText(_translate("MainWindow", "Показать лица"))

    def add_functions(self):
        self.Button_1.clicked.connect(self.start_video)
        self.pushButton.clicked.connect(self.end_video)
        self.pushButton_face.clicked.connect(self.show_pic)

    def show_pic(self):
        #print(camera.image_recog)
        if camera.image_recog != "s":
            print(camera.image_recog)
            pixmap_2 = QPixmap(camera.image_recog)
            print(pixmap_2)
            self.label_recog.setPixmap(pixmap_2)
    def start_video(self):
        print('start video')
        camera.openCamera()
        print('camera was opened')
        self.timer.start(1000. / 24)

    def nextFrameSlot(self):
        #print('nextframeslot')
        #print('face cascade was loaded\n')
        ret, frame = camera.cap.read()
        #print('ret,frame = cap.read')
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #print('grayscale was made')
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=5)
        #print('face cascade function')
        for (x, y, w, h) in faces:
            #print(x, y, h, w)

            roi_gray = gray[y:y + h, x:x + w]
            roi_color = frame[y:y + h, x:x + w]
            id_, conf = recognizer.predict(roi_gray)
            #img_save = "images/" + (labels[id_]) + "/1.png"
            #cv2.imwrite(img_save, roi_gray)
            # lvl of identification (100 max) - sensebility
            if conf >= 45 and conf <= 85:
                #print(id_)
                #print(labels[id_])
                img_save = "images/" + (labels[id_]) + "/today.png"
                cv2.imwrite(img_save, roi_gray)
                font = cv2.FONT_HERSHEY_SIMPLEX
                name = labels[id_]
                color = (255, 0, 0)
                stroke = 2
                cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)

                camera.image_recog = "images/" + (labels[id_]) + "/1.png"

            color = (255, 0, 0)  # BlueGreenRed - BGR (why??)
            stroke = 2
            width = x + w
            height = y + h
            cv2.rectangle(frame, (x, y), (width, height), color, stroke)
            eyes = eye_cascade.detectMultiScale(roi_gray)
            for (xe, ye, we, he) in eyes:
                cv2.rectangle(roi_color, (xe,ye), (xe+we, ye+he), (0,255,0), 2)
        #print('Blue border was made')
        image = QImage(frame, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
        #print('QImage?')
        pixmap = QPixmap.fromImage(image)
        #print('QPixmap?')
        self.label.setPixmap(pixmap)
        #print('setpixmap?')


    def end_video(self):
        #if cv2.waitKey(20) & 0xFF == ord('q'):
            #return 0
        #camera.cap.release(0)
        self.timer.stop()
        self.label.clear()
        #cv2.destroyAllWindows()

camera = Camera(0)

app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
MainWindow.show()
#sys.exit(app.exec_())
app.exit(app.exec_())