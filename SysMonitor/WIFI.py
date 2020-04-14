import win32com
import wmi
import platform
import time

class WIFI:
    '''
    设置需要获取在工作的WiFi相关属性作为WIFI类的属性
    '''
    def __init__(self):
        self.WMI = wmi.WMI()
        self.net_list = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=1)
        self.netname = self.getName()
        self.model = self.getModel()
        self.macaddress = self.getMacaddress()
        self.ipaddress = self.getIpaddress()
        self.netmask = self.getNetmask()
        self.sentflow = self.getSentflow()
        self.recflow = self.getRecflow()
    '''
    定义数据具体的获取函数
    '''

    def getName(self) -> str:
        for nic in self.net_list:
            return nic.ServiceName
        pass

    def getModel(self) ->str:
        for nic in self.net_list:
            return nic.Caption
        pass

    def getMacaddress(self) ->str:
        for nic in self.net_list:
            return nic.MACAddress
        pass

    def getIpaddress(self) ->str:
        for nic in self.net_list:
            if nic.IPAddress is not None:
                return nic.IPAddress[0]
            else:
                ip = ""
                return ip
        pass

    def getNetmask(self) ->str:
        for nic in self.net_list:
            if nic.IPAddress is not None:
                return nic.netmask
            else:
                netmask = ""
                return  netmask
        pass

    def getSentflow(self) ->str:
        for interfacePerTcp in self.WMI.Win32_PerfRawData_Tcpip_TCPv4():
            sentflow = float(interfacePerTcp.SegmentsSentPersec)
        time.sleep(1)
        for interfacePerTcp in self.WMI.Win32_PerfRawData_Tcpip_TCPv4():
            pre_sentflow = float(interfacePerTcp.SegmentsSentPersec)
        sent_network_flow = (sentflow - pre_sentflow)/1024
        return "%.2f"%sent_network_flow  
        

    def getRecflow(self) ->str:
        for interfacePerTcp in self.WMI.Win32_PerfRawData_Tcpip_TCPv4():
            receivedflow = float(interfacePerTcp.SegmentsReceivedPersec)
        time.sleep(1)
        for interfacePerTcp in self.WMI.Win32_PerfRawData_Tcpip_TCPv4():
            pre_recflow = float(interfacePerTcp.SegmentsReceivedPersec)
        rec_network_flow = (receivedflow - pre_recflow)/1024
        return "%.2f"%rec_network_flow 
        

    def update(self):
        '''
        更新数据
        '''
        self.WMI = wmi.WMI()
        self.net_list = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=1)
        self.netname = self.getName()
        self.model = self.getModel()
        self.macaddress = self.getMacaddress()
        self.ipaddress = self.getIpaddress()
        self.netmask = self.getNetmask()
        self.sentflow = self.getSentflow()
        self.recflow = self.getRecflow()
        pass

