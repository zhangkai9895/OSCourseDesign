from typing import List

import matplotlib
from PyQt5.QtCore import QObject
from PyQt5.QtWidgets import *
from matplotlib import pyplot
from matplotlib.axes import SubplotBase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

matplotlib.use("Qt5Agg")

CpuCanvasWidth = 800
CpuCanvasHeight = 200
CpuGraphViewWidth = 800
CpuGraphViewHeight = 200


class CPU:
    '''
    设置需要获取的cpu的相关属性作为cpu类的属性
    '''

    def __init__(self):
        self.example = None  # 示例

    def getCpuID(self):
        pass

    def getCpuType(self):
        pass

    def getCpuCurrentUtilization(self):
        pass

    # 等等其他的信息

    pass


# 创建cpu窗口控件
class CpuShowWin(QWidget):
    def initCpuWin(self, cpuCanvas):
        verBoxLayout = QVBoxLayout()

        graphicsView = QGraphicsView()  # 创建一个GraphicsView
        graphicsView.setObjectName("graphicsView")
        '''
        要把画布放在scene，然后把scene放在View中
        '''
        # 在这里我们暂时不绘制，到了更新数据的时候绘制//cpuCanvas.drawsurve
        graphicsScene = QGraphicsScene()  # 创建scene
        graphicsScene.addWidget(cpuCanvas)
        graphicsView.setScene(graphicsScene)
        graphicsView.setFixedSize(802, 202)
        verBoxLayout.addWidget(graphicsView)
        verBoxLayout.addWidget(QPushButton("12321"))
        self.setLayout(verBoxLayout)

        pass

    def __init__(self, cpuCanvas):
        super().__init__()
        self.initCpuWin(cpuCanvas)


# 用来显示实时使用率
class CpuCanvas(FigureCanvas):
    def __init__(self, SharedCanvas):
        self.canvas=SharedCanvas
        self.figure = SharedCanvas.figure  # 定义一个子图
        print(self.figure)
        self.axes = self.figure.add_subplot(111)

    def drawCurve(self, CpuUtilization: list):
        y = CpuUtilization
        x = list(range(50))
        self.axes.remove()
        self.axes = self.figure.add_subplot(111)

        # 规定xy中的数据范围
        plt.xlim(0, 50)
        plt.ylim(0, 100)
        # x，y轴的名称
        plt.xlabel("time")
        plt.ylabel("Utilization")

        # plt.axis("off")
        # 设置x轴不显示任何东西
        plt.xticks([])

        plt.subplots_adjust(top=0.99, bottom=0.1, left=0.07, right=1, hspace=0, wspace=0)
        plt.margins(0, 0)
        self.axes.plot(x, y)  # 绘图
        self.canvas.draw()
        # 用于画布的刷新
        # 传入一个list用来读取20个前状态的cpu占用率
