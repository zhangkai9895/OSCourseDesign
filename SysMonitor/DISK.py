import matplotlib
from PyQt5.QtWidgets import *
from matplotlib import pyplot
from matplotlib.axes import SubplotBase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

matplotlib.use("Qt5Agg")


class DISK:

    def __init__(self):
        pass

    pass


class DiskCanvas(FigureCanvas):
    def __init__(self, SharedCanvas):
        self.canvas = SharedCanvas
        self.figure = SharedCanvas.figure  # 定义一个子图
        print(self.figure)
        self.axes = self.figure.add_subplot(111)

    def drawCurve(self, SpeedUtilization):
        print("磁盘的传输速度绘制正常")
        y = SpeedUtilization
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
