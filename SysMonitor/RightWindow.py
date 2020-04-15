from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import *

'''
右边窗口容器
布局为QvBoxLayout纵向布局
'''


class MyTextBrowser(QTextBrowser):
    # 用来处理点击事件的函数
    doubleClicked = pyqtSignal(int)  # 定义双击之后的信号

    def mouseDoubleClickEvent(self, *args, **kwargs):
        """
        双击之后应该响应一事件
        :param args:
        :param kwargs:
        :return:
        """

        """
        由于emit函数的底层实现是c++，python的int与c++的取值范围有不同，
        所以在这里对hashcode做一定的处理，保证能够正确的传递参数
        """
        print(hash(self))
        selfHash = abs( hash(self))%100000
        self.doubleClicked.emit(selfHash)
        # 基本想法是调用


class RightWindow(QWidget):

    def showWindow(self):
        self.layout.setContentsMargins(0, 0, 0, 0)
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

    def __init__(self, ApplicationWindow):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.textBrowser1 = MyTextBrowser()
        self.textBrowser2 = MyTextBrowser()
        self.textBrowser3 = MyTextBrowser()
        self.textBrowser4 = MyTextBrowser()
        # 为了在这里访问整个程序的变量，传参的方式将ApplicationWidow对象传递过来
        self.ApplicationWindow = ApplicationWindow
        # print(self.ApplicationWindow) 检验发现传递正确
        '''
        ********************下面为每一个textBrowser的双击信号绑定槽函数********************
        '''
        # self.textBrowser1.doubleClicked.connect(
        #     lambda hashcode: self.ApplicationWindow.leftWindow.drawLeftWindow(hashcode))
        # self.textBrowser2.doubleClicked.connect(
        #     lambda hashcode: self.ApplicationWindow.leftWindow.drawLeftWindow(hashcode))
        # self.textBrowser3.doubleClicked.connect(
        #     lambda hashcode: self.ApplicationWindow.leftWindow.drawLeftWindow(hashcode))
        # self.textBrowser4.doubleClicked.connect(
        #     lambda hashcode: self.ApplicationWindow.leftWindow.drawLeftWindow(hashcode))
        self.showWindow()
