import win32com
import wmi
import platform
import time
import psutil

class WIFI:
    '''
    各个属性量
    '''    
    def __init__(self):
        self.WMI = wmi.WMI()
        self.net_list = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=1)
        self.status = wmi.WMI().Win32_NetworkAdapter()[1].NetEnabled #status表示以太网是否被使用
        self.netname = self.getName()                                #netname表示网名 类似‘Netwtw08’
        self.model = self.getModel()                                 #model表示CIM_Setting对象的描述，即大类网卡名称
        self.macaddress = self.getMacaddress()                       #macaddress表示mac地址
        self.ipaddress = self.getIpaddress()                         #ipaddresss表示ip地址
        self.netmask = self.getNetmask()                             #netmask表示伪码类型，即表示地址类别
        self.adaptername,self.recflow,self.sentflow = self.getspeed() #adaptername表示适配器名称，即‘WLAM'或者'以太网'


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
                return nic.IPSubnet
            else:
                netmask = ""
                return  netmask
        pass
        
    def update(self):
        self.WMI = wmi.WMI()
        self.net_list = wmi.WMI().Win32_NetworkAdapterConfiguration(IPEnabled=1)
        self.netname = self.getName()
        self.model = self.getModel()
        self.macaddress = self.getMacaddress()
        self.ipaddress = self.getIpaddress()
        self.netmask = self.getNetmask()
        self.adaptername,self.recflow,self.sentflow = self.getspeed()
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
        if self.status == True:
            for key in key_info:
                if key == '以太网':
                    return key,net_in.get(key),net_out.get(key)
                else:
                    pass
        else:
            for key in key_info:
                if key == 'WLAN':
                    return key,net_in.get(key),net_out.get(key)
                else:
                    pass          
    
    
    
