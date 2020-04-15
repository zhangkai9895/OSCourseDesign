#-*- coding: utf-8 -*

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
        self.memoryArray_list = wmi.WMI().Win32_PhysicalMemoryArray()

        self.Name = self.getName()#获取内存名称
        self.PartNumber =self.getPartNumber()#内存卡序列号
        self.MemoryDevices =self.getMemoryDevices() #获取插槽信息
        self.Speed = self.getSpeed()  # 获取运行速度

        self.TotalMemory = self.getTotalMemory()#获取总内存
        self.FreeMemory = self.getFreeMemory()#获取空闲内存
        self.UsedMemory = self.getUsedMemory()#获取已经使用内存

        #self.TotalSwap = self.getTotalSwap()
        #self.FreeSwap =self.getFreeSwap()
        self.utilization = self.getUtilization()#获取内存使用百分比



    def getTotalMemory(self) -> int:
        for cs in self.cs_list:
            return int(int(cs.TotalPhysicalMemory)/1024/1024/1024+0.5)

    def getFreeMemory(self)->float:
        for os in self.os_list:
            return round(int(os.FreePhysicalMemory)/1024/1024,1)#内存使用量保留一位小数

    def getUsedMemory(self)->float:
        return self.TotalMemory-self.FreeMemory

    def getUtilization(self)->float:
        return self.UsedMemory/self.TotalMemory

    def getTotalSwap(self)->int:
        pass

    def getSpeed(self)->int:
        for memory in self.memory_list:
            return memory.Speed

    def getName(self)->str:
        for memory in self.memory_list:
            return memory.caption

    def getPartNumber(self)->str:
        for memory in self.memory_list:
            return memory.PartNumber

    def getMemoryDevices(self)->str:
        for memory in self.memoryArray_list:
            return memory.MemoryDevices


    def UpdateMemoryStatus(self):
        self.cs_list = wmi.WMI().Win32_ComputerSystem()
        self.os_list = wmi.WMI().Win32_OperatingSystem()
        self.pfu_list = wmi.WMI().Win32_PageFileUsage()
        self.TotalMemory = self.getTotalMemory()
        self.FreeMemory = self.getFreeMemory()
        self.UsedMemory = self.getUsedMemory()
        self.utilization = self.getUtilization()

#测试Memory.py用
if __name__ =="__main__":
    memory = Memory()
    while True:
        memory.UpdateMemoryStatus()
        print(memory.UsedMemory)





