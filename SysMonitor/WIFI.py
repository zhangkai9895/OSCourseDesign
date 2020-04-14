import win32com
import wmi
import platform
import time
import psutil

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
        self.sentflow,self.recflow = self.getspeed()
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

    def update(self):
        '''
        更新数据
        '''
        self.recflow,self.sentflow = self.getspeed()
        pass
    
    def get_key(self):

        key_info = psutil.net_io_counters(pernic=True).keys()

        recv = {}
        sent = {}

        for key in key_info:
            recv.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_recv)
            sent.setdefault(key, psutil.net_io_counters(pernic=True).get(key).bytes_sent)
        return key_info,recv,sent
    
    def get_rate(self):
        key_info,old_recv,old_sent = self.get_key()

        time.sleep(0.1)

        key_info,now_recv,now_sent = self.get_key()

        net_in = {}
        net_out = {}

        for key in key_info:
            net_in.setdefault(key, float('%.2f' %((now_recv.get(key) - old_recv.get(key)) / 102.4)))
            net_out.setdefault(key, float('%.2f' %((now_sent.get(key) - old_sent.get(key)) / 102.4)))

        return key_info,net_in,net_out
    
    def getspeed(self):
        key_info,net_in,net_out = self.get_rate()
        for key in key_info:
            if key == '以太网':
                return net_in.get(key),net_out.get(key)
            else:
                pass    
            
    
    
    
