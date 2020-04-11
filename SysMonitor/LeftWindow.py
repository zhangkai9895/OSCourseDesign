import matplotlib
from PyQt5.QtWidgets import *

from GlobalConst import *

matplotlib.use("Qt5Agg")
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

import matplotlib.pyplot as plt

'''
定义全局的Canvas
所有的绘图都是在这张画布上面进行绘画的
'''


class SharedCanvas(FigureCanvas):
    def __init__(self, parent, width, height, dpi):
        self.figure = plt.figure(figsize=(width, height), dpi=dpi)
        FigureCanvas.__init__(self, self.figure)  # 调用父类的构造函数
        self.setParent(parent)


"""
这个是左边窗口的容器
在这个容器内应该有一个Canvas，用供给其他的模块进行绘画
"""


class LeftWindow(QWidget):

    def initWindow(self):
        # 设置布局中的各个控件之间的距离为0
        self.verBoxLayout.setContentsMargins(0, 0, 10, 0)
        self.verBoxLayout.setSpacing(0)

        self.verBoxLayout.addWidget(self.titleText)
        self.verBoxLayout.addWidget(self.SharedCanvas)
        self.verBoxLayout.addWidget(self.detailText)

        # 测试用样式
        self.titleText.setStyleSheet("background-color:blue")
        self.titleText.setFixedSize(600, 100)
        self.detailText.setFixedSize(600, 300)
        self.detailText.setStyleSheet("background-color:red")
        pass

    def __init__(self, parent, width, height, dpi, ApplicationWindow):
        super().__init__()
        self.verBoxLayout = QVBoxLayout()
        self.titleText = QTextBrowser()  # 定义一个TextBrowser用来显示该硬件的名称版本等等
        self.SharedCanvas = SharedCanvas(parent, width, height, dpi)
        self.detailText = QTextBrowser()  # 这个Label用来显示具体的参数
        self.setLayout(self.verBoxLayout)

        # 为了在其他的类中能够正常的访问整个界面，
        # 并且避免全局变量在不同的文件中调用出错的问题，采用了这种传递参数的方式
        self.ApplicationWindow = ApplicationWindow
        self.currentPage = self.ApplicationWindow.rightWindow.textBrowser1.__hash__()  # 默认进入cpu界面
        self.initWindow()

    def drawLeftWindow(self, hashcode):
        """
        传入page编号，方便识别现在要绘制哪一个page，然后再去调用响应的绘制函数
        这个函数作为点击事件的槽函数
        :param hashcode:
        :return:
        """

        print("信号绑定成功")
        print(hashcode)
        if hashcode is None:
            return
        if hashcode == abs(self.ApplicationWindow.rightWindow.textBrowser1.__hash__()) % 100000:
            self.ApplicationWindow.CpuShow.drawAllCpuAbout()
        if hashcode == abs(self.ApplicationWindow.rightWindow.textBrowser2.__hash__()) % 100000:
            pass
        if hashcode == abs(self.ApplicationWindow.rightWindow.textBrowser3.__hash__()) % 100000:
            pass
        if hashcode == abs(self.ApplicationWindow.rightWindow.textBrowser4.__hash__()) % 100000:
            pass

    pass
