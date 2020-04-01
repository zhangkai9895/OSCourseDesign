import matplotlib
from PyQt5.QtWidgets import *
from matplotlib import pyplot
from matplotlib.axes import SubplotBase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

matplotlib.use("Qt5Agg")

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
        self.verBoxLayout.addWidget(self.titleLabel)
        self.verBoxLayout.addWidget(self.SharedCanvas)
        self.verBoxLayout.addWidget(self.detailLabel)

        # 测试用样式
        self.titleLabel.setStyleSheet("background-color:blue")
        self.titleLabel.setFixedSize(600,100)
        self.detailLabel.setFixedSize(600,300)
        self.detailLabel.setStyleSheet("background-color:red")
        pass

    def __init__(self, parent, width, height, dpi):
        super().__init__()
        self.verBoxLayout = QVBoxLayout()
        self.titleLabel = QLabel("测试的板块")  # 定义一个Label用来显示该硬件的名称版本等等
        self.SharedCanvas = SharedCanvas(parent, width, height, dpi)
        self.detailLabel = QLabel("测试用的板块")  # 这个Label用来显示具体的参数
        self.setLayout(self.verBoxLayout)
        self.initWindow()

    pass
