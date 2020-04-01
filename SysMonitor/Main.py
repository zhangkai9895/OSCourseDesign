from time import sleep
from typing import List
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPaintEvent
from CPU import CpuCanvas, CpuShowWin, CpuCanvasHeight, CpuCanvasWidth
from LeftWindow import LeftWindow
from RightWindow import RightWindow
import DISK
import Memory
import SYSTEM
import wmi
import threading
import sys
from PyQt5.QtWidgets import *
import random
import matplotlib.pyplot as plt

'''
main中调用其他py文件中的数据
并且执行绘图操作
'''
WinHeight = 800
winWidth = 800

'''
关于要用获取到参数都在这个地方做了声明
'''
listOfCpuUtilization = [0 for i in range(50)]  # 线程安全的
listOfMemoryUtilization = [0 for i in range(50)]  # 初始化所有时刻的占用率为0


class DetectCpu(QThread):
    Change = pyqtSignal(list)  # 注册信号，当改变数组元素改变的时候刷新

    def run(self):
        while True:
            # 模拟cpu的改变
            listOfCpuUtilization.pop(0)
            listOfCpuUtilization.append(random.randint(0, 100))
            self.Change.emit(listOfCpuUtilization)  # 这里是发射信号，参数为跟新之后的cpu占用率
            sleep(0.5)


class ApplicationWindow(QWidget):
    SharedCanvas = None  # 初始化为空，在创建leftWindow之后赋值给他

    def initWindows(self):
        self.resize(winWidth, WinHeight)
        self.setWindowTitle("SysMonitor")
        # 全局的布局方式
        hBox = QHBoxLayout()
        leftWindow = LeftWindow(None, 600, 800, 100)
        ApplicationWindow.SharedCanvas = leftWindow.SharedCanvas
        rightWindow = RightWindow()
        hBox.addWidget(leftWindow)
        hBox.addWidget(rightWindow)
        self.setLayout(hBox)
        self.show()

    def __init__(self):
        super().__init__()
        self.initWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 注册全局application
    window = ApplicationWindow()
    CpuCanvas = CpuCanvas(ApplicationWindow.SharedCanvas)
    Cputhread: DetectCpu = DetectCpu()
    print(Cputhread.Change.connect(lambda list: CpuCanvas.drawCurve(list)))  # 更加高效的调用 选择lambda
    # CpuCanvas.drawCurve(listOfCpuUtilization)
    # 画布刷新
    Cputhread.start()
    # print(window)
    sys.exit(app.exec_())
