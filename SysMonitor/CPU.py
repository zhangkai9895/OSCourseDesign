import random
from time import sleep

import matplotlib
import pythoncom
from PyQt5 import QtCore

from PyQt5.QtCore import QThread, pyqtSignal, QMutex
import wmi
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import *
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from GlobalConst import listOfCpuUtilization

matplotlib.use("Qt5Agg")

CpuCanvasWidth = 800
CpuCanvasHeight = 200
CpuGraphViewWidth = 800
CpuGraphViewHeight = 200

mutex = QMutex()


class CPU:
    '''
    设置需要获取的cpu的相关属性作为cpu类的属性
    '''

    def __init__(self):
        self.WMI = wmi.WMI()
        self.cpu_list = wmi.WMI().Win32_Processor()
        self.CpuID = self.getCpuID()
        self.utilization = self.getUtilization()
        self.speed = self.getSpeed()
        self.processNum = self.getProcessNum()
        self.threadNum = self.getThreadNum()  # 目前来看这一步非常耗时，是不能接受的那种
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
        for cpu in self.cpu_list:
            return cpu.Name
        pass

    def getUtilization(self) -> int:
        for cpu in self.cpu_list:
            return cpu.LoadPercentage
        pass

    def getSpeed(self) -> float:
        for cpu in self.cpu_list:
            return cpu.CurrentClockSpeed
            #return cpu.ExtClock
        pass

    def getProcessNum(self) -> int:
        return (wmi.WMI().Win32_OperatingSystem())[0].NumberOfProcesses
        # return len(self.WMI.Win32_Process())
        pass

    def getThreadNum(self) -> int:
        # 这样操作耗时太长了
        # listThread = self.WMI.Win32_Thread()
        # return len(list)
        pass

    def getHandleNum(self) -> int:
        # count = 0
        # for process in wmi.WMI().Win32_Process():
        #     count += process.HandleCount
        # return count
        pass

    def getRunTime(self) -> str:
        pass

    def getStandardSpeed(self) -> float:
        pass

    def getSlot(self) -> int:
        # return self.cpu_list[0].UpgradeMethod
        pass

    def getKernel(self) -> int:
        return self.cpu_list[0].NumberOfEnabledCore
        pass

    def getLogicalProcessors(self) -> int:
        return self.cpu_list[0].NumberOfLogicalProcessors
        pass

    def getVirtual(self) -> bool:
        return self.cpu_list[0].VirtualizationFirmwareEnabled
        pass

    def getL1Cache(self) -> float:
        # return self.cpu_list[0].L1CacheSize
        pass

    def getL2Cache(self) -> float:
        return self.cpu_list[0].L2CacheSize
        pass

    def getL3Cache(self) -> float:
        return self.cpu_list[0].L3CacheSize
        pass

    '''
    ********此函数比较关键，用来供给实时监测的线程使用，用来不断刷新cpu的状态（cpu对象中的需要跟新的数据）
    '''

    def UpdateCpuStatus(self):
        """
        根性需要根性的数据的函数
        :return: void
        """
        pythoncom.CoInitialize()
        self.cpu_list = wmi.WMI().Win32_Processor()
        self.utilization = self.getUtilization()
        self.speed = self.getSpeed()
        self.processNum = self.getProcessNum()
        self.threadNum = self.getThreadNum()
        self.handleNum = self.getHandleNum()
        self.runTime = self.getRunTime()
        # 等等其他的信息
        pythoncom.CoInitialize()

    pass


class DetectCpu(QThread):
    """
    单独的一个线程实时刷新cpu的相关的数据，
    并且通过信号机制通知绘图函数进行图形绘制
    """
    UtilizationChange = pyqtSignal(list)  # 注册信号，当改变数组元素改变的时候刷新
    OthersChange = pyqtSignal()

    def run(self):
        print("这里正常")
        while self.ApplicationWindow.leftWindow.currentPage == abs(
                self.ApplicationWindow.rightWindow.textBrowser1.__hash__()) % 100000:
            # 模拟cpu的改变
            self.cpu.UpdateCpuStatus()
            mutex.lock()
            listOfCpuUtilization.pop(0)
            listOfCpuUtilization.append(self.cpu.utilization)
            self.UtilizationChange.emit(listOfCpuUtilization)  # 这里是发射信号，参数为跟新之后的cpu占用率
            self.OthersChange.emit()
            mutex.unlock()
            sleep(0.2)

    def __init__(self, ApplicationWindow, cpu: CPU):
        super().__init__()
        self.ApplicationWindow = ApplicationWindow
        self.cpu = cpu


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
        translate = QtCore.QCoreApplication.translate
        thread = DetectCpu(self.ApplicationWindow, self.cpu)
        thread.UtilizationChange.connect(lambda CpuUtilization: self.cpuCanvas.drawCurve(CpuUtilization))
        thread.OthersChange.connect(lambda: self.drawDetailBrowser())
        thread.start()
        self.leftWindow.titleText.setText(self.cpu.CpuID)
        '''
        *******************************这里的html是不应该随便变动的，否则会更改页面的布局************
        '''
        self.leftWindow.titleText.setHtml(translate("LeftWindow",
                                                    "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                                    "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n "
                                                    "<html><head><meta name=\"qrichtext\" content=\"1\" /><style "
                                                    "type=\"text/css\">\n "
                                                    "p, li { white-space: pre-wrap; }\n"
                                                    "</style></head><body style=\" font-family:'SimSun'; "
                                                    "font-size:9pt; font-weight:400; font-style:normal;\">\n "
                                                    "<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; "
                                                    "margin-left:0px; margin-right:0px; -qt-block-indent:0; "
                                                    "text-indent:0px;\"><span style=\" font-size:15pt; "
                                                    "font-weight:600;\">" + self.cpu.CpuID +
                                                    "</span></p></body></html>"))
        self.drawDetailBrowser()

    def drawDetailBrowser(self):
        translate = QtCore.QCoreApplication.translate
        '''
        *******************html部分是是不可以随便便改动的，否则会更改布局****************
        '''
        self.leftWindow.detailText.setHtml(translate("LeftWindow",
                                                     "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" "
                                                     "\"http://www.w3.org/TR/REC-html40/strict.dtd\">\n "
                                                     "<html><head><meta name=\"qrichtext\" content=\"1\" /><style "
                                                     "type=\"text/css\">\n "
                                                     "p, li { white-space: pre-wrap; }\n"
                                                     "</style></head><body style=\" font-family:'Consolas'; "
                                                     "font-size:9pt; font-weight:400; font-style:normal;\">\n "
                                                     "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                                     "margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span "
                                                     "style=\" font-size:14pt; "
                                                     "font-weight:600;\">Utilization:</span><span style=\" "
                                                     "font-size:14pt;\">" + str(self.cpu.utilization) + "%</span><span "
                                                                                                        "style=\" "
                                                                                                        "font-size:14pt; "
                                                                                                        "font-weight:600;\">         Vitual:</span><span style=\" "
                                                                                                        "font-size:14pt;\">" + str(
                                                         self.cpu.virtual) + "</span></p>\n "
                                                                             "<p style=\"-qt-paragraph-type:empty; margin-top:0px; "
                                                                             "margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                                                             "-qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br "
                                                                             "/></p>\n "
                                                                             "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                                                             "margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span "
                                                                             "style=\" font-size:14pt; font- "
                                                                             "weight:600;\">LogicalProcessors:</span><span style=\" "
                                                                             "font-size:14pt;\">" + str(
                                                         self.cpu.logicalProcess) + "    </span"
                                                                                    "><span "
                                                                                    "style=\" "
                                                                                    "font-size:14pt; "
                                                                                    "font-weight:600;\">Speed:</span><span style=\" "
                                                                                    "font-size:14pt;\">" + str(
                                                         self.cpu.speed) + "MHz</span></p>\n "
                                                                           "<p style=\"-qt-paragraph-type:empty; margin-top:0px; "
                                                                           "margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                                                           "-qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br "
                                                                           "/></p>\n "
                                                                           "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                                                           "margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span "
                                                                           "style=\" font-size:14pt; "
                                                                           "font-weight:600;\">KernelNum:</span><span style=\" "
                                                                           "font-size:14pt;\">" + str(
                                                         self.cpu.kernel) + "</span><span style=\" font-size:14pt; "
                                                                            "font-weight:600;\">            ProcessNum:</span><span style=\" "
                                                                            "font-size:14pt;\">" + str(
                                                         self.cpu.processNum) + "</span></p>\n "
                                                                                "<p style=\"-qt-paragraph-type:empty; margin-top:0px; "
                                                                                "margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                                                                "-qt-block-indent:0; text-indent:0px; font-size:14pt;\"><br "
                                                                                "/></p>\n "
                                                                                "<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; "
                                                                                "margin-right:0px; -qt-block-indent:0; text-in "
                                                                                "dent:0px;\"><span style=\" font-size:14pt; "
                                                                                "font-weight:600;\">L2Cache:</span><span style=\" "
                                                                                "font-size:14pt;\">" + str(
                                                         self.cpu.L2Cache) + "Kb</span><span style=\" font-size:14pt; "
                                                                             "font-weight:600;\">         L3Cache:</span><span style=\" "
                                                                             "font-size:14pt;\">" + str(
                                                         self.cpu.L3Cache) + "Kb</span></p>\n "
                                                                             "<p style=\"-qt-paragraph-type:empty; margin-top:0px; "
                                                                             "margin-bottom:0px; margin-left:0px; margin-right:0px; "
                                                                             "-qt-block-indent:0; text-indent:0px;\"><br "
                                                                             "/></p></body></html>"))
        pass

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

    def drawCurve(self, CpuUtilization):
        mutex.lock()
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
        mutex.unlock()
        # 用于画布的刷新
        # 传入一个list用来读取20个前状态的cpu占用率
