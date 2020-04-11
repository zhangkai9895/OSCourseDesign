from time import sleep
from typing import List
from PyQt5.QtCore import QThread, pyqtSignal, QObject
from PyQt5.QtGui import QPainter, QPaintEvent
from CPU import CpuCanvas, CPU, CpuShow
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
from GlobalConst import *

'''
main中调用其他py文件中的数据
并且执行绘图操作
'''


class DetectMemory(QThread):
    def run(self) -> None:
        pass


class DetectDisk(QThread):
    def run(self) -> None:
        pass


class DetectWifi(QThread):
    def run(self) -> None:
        pass


class ApplicationWindow(QWidget):
    """
    ******全局变量在此声明**********************
    通过Application.**调用，在调用之前找地方初始化
    *******************************************
    """
    leftWindow = None
    rightWindow = None
    SharedCanvas = None  # 初始化为空，在创建leftWindow之后赋值给他
    CpuShow = None
    MemoryShow = None
    DISKShow = None
    WIFIShow = None
    '''
    '''

    def initHardWares(self):
        ApplicationWindow.CpuShow = CpuShow(ApplicationWindow.SharedCanvas, self)
        pass

    def initWindows(self):
        self.resize(winWidth, WinHeight)
        self.setWindowTitle("SysMonitor")
        # 全局的布局方式
        hBox = QHBoxLayout()
        hBox.setSpacing(0)
        hBox.setContentsMargins(0, 0, 0, 0)
        # 这里生成左右窗口的顺序不能够改变，应为在生成左侧左边窗口的时候会调用右边窗口对象中的内容
        ApplicationWindow.rightWindow = RightWindow(self)
        ApplicationWindow.leftWindow = LeftWindow(None, 600, 800, 100, self)
        ApplicationWindow.SharedCanvas = ApplicationWindow.leftWindow.SharedCanvas

        hBox.addWidget(ApplicationWindow.leftWindow)
        hBox.addWidget(ApplicationWindow.rightWindow)
        # 只有当两个左右窗体都生成了才能够为其中的信号绑定槽函数
        ApplicationWindow.rightWindow.textBrowser1.doubleClicked.connect(
            lambda hashcode:
            ApplicationWindow.leftWindow.drawLeftWindow(hashcode))
        ApplicationWindow.rightWindow.textBrowser2.doubleClicked.connect(
            lambda hashcode: ApplicationWindow.leftWindow.drawLeftWindow(hashcode))
        ApplicationWindow.rightWindow.textBrowser3.doubleClicked.connect(
            lambda hashcode: ApplicationWindow.leftWindow.drawLeftWindow(hashcode))
        ApplicationWindow.rightWindow.textBrowser4.doubleClicked.connect(
            lambda hashcode: ApplicationWindow.leftWindow.drawLeftWindow(hashcode))

        self.setLayout(hBox)
        self.show()

    def __init__(self):
        super().__init__()
        self.initWindows()
        '''初始化硬件对象'''
        self.initHardWares()


if __name__ == '__main__':
    app = QApplication(sys.argv)  # 注册全局application
    window = ApplicationWindow()
    sys.exit(app.exec_())
