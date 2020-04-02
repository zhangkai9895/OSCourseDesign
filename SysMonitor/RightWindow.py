from PyQt5.QtWidgets import *

'''
右边窗口容器
布局为QvBoxLayout纵向布局
'''


class RightWindow(QWidget):

    def showWindow(self):
        self.layout.setContentsMargins(0,0,0,0)
        self.layout.setSpacing(0)
        self.textBrowser1.setText("测试用右边板块")
        self.textBrowser2.setText("测试用右边板块")
        self.textBrowser3.setText("测试用右边板块")
        self.textBrowser4.setText("测试用右边板块")
        self.layout.addWidget(self.textBrowser1)
        self.layout.addWidget(self.textBrowser2)
        self.layout.addWidget(self.textBrowser3)
        self.layout.addWidget(self.textBrowser4)
        self.textBrowser1.setStyleSheet("background-color:blue")
        self.textBrowser2.setStyleSheet("background-color:red")
        self.textBrowser3.setStyleSheet("background-color:blue")
        self.textBrowser4.setStyleSheet("background-color:red")
        # self.textBrowser1.setFrameShape()
        # self.textBrowser1.setFixedSize(200, 200)
        # self.textBrowser2.setFixedSize(200, 200)
        # self.textBrowser3.setFixedSize(200, 200)
        # self.textBrowser4.setFixedSize(200, 200)
        # self.layout.setMargin(0)
        print(self.layout.getContentsMargins())

        # testLabel1 = QTextBrowser()
        # testLabel1.setText("测试用右边板块")
        # testLabel2 = QLabel("测试用右边板块")
        # testLabel3 = QLabel("测试用右边板块")
        # testLabel4 = QLabel("测试用右边板块")
        # self.layout.addWidget(testLabel1)
        # self.layout.addWidget(testLabel2)
        # self.layout.addWidget(testLabel3)
        # self.layout.addWidget(testLabel4)
        # testLabel1.setStyleSheet("background-color:blue")
        # testLabel2.setStyleSheet("background-color:red")
        # testLabel3.setStyleSheet("background-color:blue")
        # testLabel4.setStyleSheet("background-color:red")

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.textBrowser1 = QTextBrowser()
        self.textBrowser2 = QTextBrowser()
        self.textBrowser3 = QTextBrowser()
        self.textBrowser4 = QTextBrowser()
        self.showWindow()
