""""
********************这个文件将用来定义全局常量*****************
"""
'''
*****全局常量定义的位置****************
**************************************
'''
WinHeight = 800
winWidth = 800
# 定义cpu的占用率，内存的占用率，磁盘的活动时间，Wifi的吞吐量
listOfCpuUtilization = [0 for i in range(50)]  # 线程安全的,注意这也是个常量，但其中的内容可变
listOfMemoryUtilization = [0 for i in range(50)]  # 初始化所有时刻的占用率为0
listOfDiskRuntime = [0 for i in range(50)]
listOfWiFiThroughoutCapacity = [0 for i in range(50)]

# 定义几个页面的表示符，用来判别左边窗口当前在哪一个页面之中


'''
**************************************
**************************************
'''
