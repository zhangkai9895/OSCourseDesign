from time import sleep
from typing import List
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPaintEvent
from CPU import CpuCanvas, CpuShowWin, CpuCanvasHeight, CpuCanvasWidth
import DISK
import Memory
import SYSTEM
import wmi
import threading
import sys
from PyQt5.QtWidgets import *
import random

'''
main中调用其他py文件中的数据
并且执行绘图操作
'''
WinHeight = 800
winWidth = 600

listOfCpuUtilization = [0 for i in range(50)]  # 线程安全的
cpuCanvas = CpuCanvas(None, CpuCanvasWidth / 100, CpuCanvasHeight / 100, 100)


class DetectCpu(QThread):
    Change = pyqtSignal(list)  # 注册信号，当改变数组元素改变的时候刷新

    def run(self):
        while True:
            # 模拟cpu的改变
            listOfCpuUtilization.pop(0)
            listOfCpuUtilization.append(random.randint(0, 100))
            self.Change.emit(listOfCpuUtilization)
            sleep(0.5)


class ApplicationWindow(QWidget):

    def initWindows(self):
        self.resize(winWidth, WinHeight)
        self.setWindowTitle("SysMonitor")
        # 全局的布局方式
        vBox = QVBoxLayout()
        vBox.addWidget(CpuShowWin(cpuCanvas))
        vBox.addWidget(QPushButton("12345"))
        self.setLayout(vBox)
        self.show()

    def drawPoints(self, list):
        print(list)
        self.update()

    def __init__(self):
        super().__init__()
        self.initWindows()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 注册全局application
    window = ApplicationWindow()
    Cputhread: DetectCpu = DetectCpu()
    Cputhread.Change.connect(cpuCanvas.drawCurve)
    Cputhread.start()
    print(window)
    sys.exit(app.exec_())
