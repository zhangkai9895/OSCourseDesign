#-*- coding: utf-8 -*

import random
from time import sleep
import wmi
import matplotlib
from PyQt5 import QtCore
from PyQt5.QtCore import QThread, pyqtSignal, QMutex
from PyQt5.QtWidgets import *
from matplotlib import pyplot
from matplotlib.axes import SubplotBase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
from GlobalConst import *

matplotlib.use("Qt5Agg")
mutex = QMutex()


class DISK:

    def __init__(self):
        self.diskDrive_list = wmi.WMI().Win32_DiskDrive()
        self.diskLogical_list = wmi.WMI().Win32_LogicalDisk()
        self.diskInfo_list = wmi.WMI().Win32_PerfFormattedData_PerfDisk_LogicalDisk()
        self.name = self.getDiskName()#磁盘 C
        self.model = self.getModel()#磁盘信息 SSD 或者固态磁盘
        self.readSpeed = self.getReadSpeed()#磁盘读取速率
        self.writeSpeed = self.getWriteSpeed()#磁盘写入速率
        self.runTime = self.getRunTime()#
        self.capacity = self.getCapacity()#磁盘容量
        self.isSysDisk = self.isSysDisk()#
        pass

    def getDiskName(self) -> str:
        return self.diskLogical_list[1].DeviceID
        pass

    def getReadSpeed(self) -> int:
        return int(self.diskInfo_list[0].DiskReadBytesPerSec)/1024
        pass

    def getWriteSpeed(self) -> int:
        return int(self.diskInfo_list[0].DiskWriteBytesPerSec)/1024
        pass

    def getRunTime(self) -> int:
        #未找到具体方法
        pass

    def getCapacity(self) -> int:
        return int(int(self.diskDrive_list[1].Size)/(1024*1024*1024))#C盘容量
        pass

    def isSysDisk(self) -> bool:
        #有待商定 如果只做C盘？？？
        pass

    def getModel(self)->str:
        return self.diskDrive_list[1].Model #SSD应为 KXG5AZNV256G TOSHIBA

    pass


    def  UpdateDiskStatus(self):
        self.diskDrive_list = wmi.WMI().Win32_DiskDrive()
        self.diskLogical_list = wmi.WMI().Win32_LogicalDisk()
        self.diskInfo_list = wmi.WMI().Win32_PerfFormattedData_PerfDisk_LogicalDisk()
        self.readSpeed = self.getReadSpeed()  # 磁盘读取速率
        self.writeSpeed = self.getWriteSpeed()  # 磁盘写入速率
        self.runTime = self.getRunTime()
#测试用
if __name__ =="__main__":
    disk = DISK()
    while True:
        disk.UpdateDiskStatus()
        print(disk.readSpeed)
        print(disk.writeSpeed)