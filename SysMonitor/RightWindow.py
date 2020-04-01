from PyQt5.QtWidgets import *

'''
右边窗口容器
布局为QvBoxLayout纵向布局
'''


class RightWindow(QWidget):
    def showWindow(self):
        testLabel1 = QLabel("测试用右边板块")
        testLabel2 = QLabel("测试用右边板块")
        testLabel3 = QLabel("测试用右边板块")
        testLabel4 = QLabel("测试用右边板块")
        self.layout.addWidget(testLabel1)
        self.layout.addWidget(testLabel2)
        self.layout.addWidget(testLabel3)
        self.layout.addWidget(testLabel4)
        testLabel1.setStyleSheet("background-color:blue")
        testLabel2.setStyleSheet("background-color:red")
        testLabel3.setStyleSheet("background-color:blue")
        testLabel4.setStyleSheet("background-color:red")


    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.showWindow()
