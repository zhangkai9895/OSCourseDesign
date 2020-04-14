import random
from time import sleep

import matplotlib
from PyQt5.QtCore import QThread, pyqtSignal

from PyQt5.QtWidgets import *
from matplotlib.axes import SubplotBase
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import wmi

from GlobalConst import listOfMemoryUtilization

matplotlib.use("Qt5Agg")


class Memory:

    def __init__(self):
        self.WMI = wmi.WMI()
        self.memory_list = wmi.WMI().Win32_PhysicalMemory()
        self.cs_list = wmi.WMI().Win32_ComputerSystem()
        self.os_list = wmi.WMI().Win32_OperatingSystem()
        self.pfu_list = wmi.WMI().Win32_PageFileUsage()
        self.TotalMemory = self.getTotalMemory()
        self.FreeMemory = self.getFreeMemory()
        self.UsedMemory = self.getUsedMemory()
        self.Speed = self.getSpped()
        self.TotalSwap = self.getTotalSwap()
        self.FreeSwap =self.getFreeSwap()
        self.utilization = self.getUtilization()



    def getTotalMemory(self) -> int:
        for cs in self.cs_list:
            return int(int(cs.TotalPhysicalMemory)/1024/1024/1024+0.5)

    def getFreeMemory(self)->float:
        for os in self.os_list:
            return int(os.FreePhysicalMemory)/1024/1024

    def getUsedMemory(self)->float:
        return self.TotalMemory-self.FreeMemory

    def getUtilization(self)->float:
        return self.UsedMemory/self.TotalMemory

    def getTotalSwap(self)->int:
        pass

    def getSpeed(self)->int:
        for memory in self.memory_list:
            return memory.Speed


    def UpdateMemoryStatus(self):
        self.cs_list = wmi.WMI().Win32_ComputerSystem()
        self.os_list = wmi.WMI().Win32_OperatingSystem()
        self.pfu_list = wmi.WMI().Win32_PageFileUsage()
        self.TotalMemory = self.getTotalMemory()
        self.FreeMemory = self.getFreeMemory()
        self.UsedMemory = self.getUsedMemory()
        self.utilization = self.getUtilization()








