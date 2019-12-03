# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'vehicle_ui.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#

import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import *
import proceed


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 650)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(280, 25, 140, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton.setFont(font)
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(440, 25, 140, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setObjectName("pushButton_2")

        self.pushButton_3 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_3.setGeometry(QtCore.QRect(600, 25, 140, 40))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.pushButton_3.setFont(font)
        self.pushButton_3.setObjectName("pushButton_3")

        self.graphicsView = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView.setGeometry(QtCore.QRect(40, 120, 500, 400))
        self.graphicsView.setObjectName("graphicsView")
        self.graphicsView_2 = QtWidgets.QGraphicsView(self.centralwidget)
        self.graphicsView_2.setGeometry(QtCore.QRect(600, 120, 500, 400))
        self.graphicsView_2.setObjectName("graphicsView_2")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(20, 30, 231, 31))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setTextFormat(QtCore.Qt.RichText)
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(600, 510, 550, 90))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(14)
        self.label_2.setFont(font)
        # self.label_2.setTextFormat(QtCore.Qt.RichText)
        self.label_2.setObjectName("label_2")

        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        # self.setWindowTitle("Vehicle Detection");

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.setWindowIcon(QIcon('vehicle_icon64.ico'))
        self.pushButton.setText(_translate("MainWindow", "加载图片"))
        self.pushButton_2.setText(_translate("MainWindow", "开始识别"))
        self.pushButton_3.setText(_translate("MainWindow", "关于"))
        self.label.setText(_translate("MainWindow",
                                      "<html><head/><body><p><span style=\" font-size:14pt; font-weight:600;\">车辆型号检测识别</span></p></body></html>"))
        # self.label_2.setText("Results")
        # 按钮点击事件
        self.pushButton.clicked.connect(self.buttonAction1)
        self.pushButton_2.clicked.connect(self.buttonAction2)
        self.pushButton_3.clicked.connect(self.buttonAction3)

    # 按钮1 响应
    def buttonAction1(self):
        self.image = QPixmap()

        file_path = QFileDialog.getOpenFileName(self, '选择文件', '', '(*.png);(*.jpg)')[0]
        # print(file_path)
        self.image.load(file_path)

        global global_path
        global_path = file_path

        scaled_img = self.image.scaled(500, 400, QtCore.Qt.IgnoreAspectRatio)
        self.graphicsView.scene = QGraphicsScene()
        raw_img = QGraphicsPixmapItem(scaled_img)
        self.graphicsView.scene.addItem(raw_img)
        self.graphicsView.setScene(self.graphicsView.scene)
        # print("image loaded")

    # 按钮2 响应
    def buttonAction2(self):
        # print("button 2 click")
        caption, process_time = proceed.start_proceed(img_path=global_path)

        self.image = QPixmap()
        self.image.load('output.jpg')
        scaled_img = self.image.scaled(500, 400, QtCore.Qt.IgnoreAspectRatio)
        self.graphicsView_2.scene = QGraphicsScene()
        raw_img = QGraphicsPixmapItem(scaled_img)
        self.graphicsView_2.scene.addItem(raw_img)
        self.graphicsView_2.setScene(self.graphicsView_2.scene)

        self.label_2.setText("识别结果: " + str(caption) + " \n" + "耗时: " + str(round(process_time, 3)) + ' 秒')

        # global global_caption
        # global_caption=caption
        # print(caption)

    def buttonAction3(self):
        QMessageBox.about(self, "关于", "精细化车辆型号检测识别\nAuthored by: github/Joey66666")


# QPixmap scaled_img = image.scaled(img_object->size(), Qt::KeepAspectRatio);
class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.setupUi(self)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.setWindowTitle("Vehicle-Classify");
    myWin.show()
    sys.exit(app.exec_())
