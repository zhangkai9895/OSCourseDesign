import random
from time import sleep

import matplotlib
from PyQt5.QtCore import QThread, pyqtSignal

from PyQt5.QtWidgets import *
from matplotlib.axes import SubplotBase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from GlobalConst import listOfCpuUtilization

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
        self.CpuID = self.getCpuID()
        self.utilization = self.getUtilization()
        self.speed = self.getSpeed()
        self.processNum = self.getProcessNum()
        self.threadNum = self.getThreadNum()
        self.handleNum = self.getHandleNum()
        self.runTime = self.getRunTime()
        self.standardSpeed = self.getStandardSpeed()
        self.slot = self.getSlot()
        self.kernel = self.getKernel()
        self.logicalProcess = self.getLogicalProcessors()
        self.virtual = self.getVirtual()
        self.L1Cache = self.getL1Cache()
        self.L2Cache = self.getL2Cache()
        self.L3Cache = self.getL3Cache()
        self.UpdateCpuStatus()
        # self.example = None  # 示例

    """
    ********定义数据具体的获取函数
    """

    def getCpuID(self) -> str:
        pass

    def getUtilization(self) -> int:
        pass

    def getSpeed(self) -> float:
        pass

    def getProcessNum(self) -> int:
        pass

    def getThreadNum(self) -> int:
        pass

    def getHandleNum(self) -> int:
        pass

    def getRunTime(self) -> str:
        pass

    def getStandardSpeed(self) -> float:
        pass

    def getSlot(self) -> int:
        pass

    def getKernel(self) -> int:
        pass

    def getLogicalProcessors(self) -> int:
        pass

    def getVirtual(self) -> bool:
        pass

    def getL1Cache(self) -> float:
        pass

    def getL2Cache(self) -> float:
        pass

    def getL3Cache(self) -> float:
        pass

    '''
    ********此函数比较关键，用来供给实时监测的线程使用，用来不断刷新cpu的状态（cpu对象中的需要跟新的数据）
    '''

    def UpdateCpuStatus(self):
        """
        根性需要根性的数据的函数
        :return: void
        """
        self.utilization = self.getUtilization()
        self.speed = self.getSpeed()
        self.processNum = self.getProcessNum()
        self.threadNum = self.getThreadNum()
        self.handleNum = self.getHandleNum()
        self.runTime = self.getRunTime()
        # 等等其他的信息

    pass


class DetectCpu(QThread):
    """
    单独的一个线程实时刷新cpu的相关的数据，
    并且通过信号机制通知绘图函数进行图形绘制
    """
    Change = pyqtSignal(list)  # 注册信号，当改变数组元素改变的时候刷新

    def run(self):
        while self.ApplicationWindow.leftWindow.currentPage == self.ApplicationWindow.rightWindow.textBrowser1.__hash__():
            # 模拟cpu的改变
            listOfCpuUtilization.pop(0)
            listOfCpuUtilization.append(random.randint(0,100))
            self.Change.emit(listOfCpuUtilization)  # 这里是发射信号，参数为跟新之后的cpu占用率
            sleep(0.5)

    def __init__(self, ApplicationWindow):
        super().__init__()
        self.ApplicationWindow = ApplicationWindow


class CpuShow:
    """
    这个类提供中间服务，是介于显示层和数据控制层的中间层，
    从CPU类中获取CPU的相关硬件信息，并且把这些信息发送到相关的视图控件中
    并且实时控制视图层的更新活动
    """

    def drawAllCpuAbout(self):
        """
        :param cpu:
        :return:
        """
        thread = DetectCpu(self.ApplicationWindow)
        thread.Change.connect(lambda CpuUtilization: self.cpuCanvas.drawCurve(CpuUtilization))
        thread.start()
        self.leftWindow.titleText.setText("这里是cpu")
        self.leftWindow.detailText.setText("cpu详细信息")

    def __init__(self, SharedCanvas, ApplicationWindow):
        self.cpuCanvas = CpuCanvas(SharedCanvas)
        self.cpu = CPU()
        self.ApplicationWindow = ApplicationWindow
        self.leftWindow = ApplicationWindow.leftWindow


"""

这个类用来向左侧窗口中央画板绘制cpu实时占用率动态统计图
得到调用的是drawCurve
没有定义自己的Figure 用的是SharedCanvas提供的Figure画板，
具体做的工作是清除SharedCanvas的Figure中的内容，然后将自己的子图（subplot）添加其中
"""


class CpuCanvas(FigureCanvas):
    def __init__(self, SharedCanvas):
        self.canvas = SharedCanvas
        self.figure = SharedCanvas.figure  # 定义一个子图
        print(self.figure)
        self.axes = self.figure.add_subplot(111)

    def drawCurve(self, CpuUtilization: list):
        print("cpu图表绘制正常")
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
