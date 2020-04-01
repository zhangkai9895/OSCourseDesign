import sys
from PyQt5.QtWidgets import QApplication, QWidget, QHBoxLayout, QVBoxLayout, \
                            QGridLayout, QFormLayout, QPushButton

class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('嵌套布局')

        # 全局布局：水平
        wlayout = QHBoxLayout()
        # 局部布局：水平，垂直，网格，表单
        hlayout = QHBoxLayout()
        # vlayout = QVBoxLayout()
        # glayout = QGridLayout()
        # flayout = QFormLayout()

        # 为局部布局添加控件
        hlayout.addWidget(QPushButton(str(1)))
        hlayout.addWidget(QPushButton(str(2)))
        # vlayout.addWidget(QPushButton(str(3)))
        # vlayout.addWidget(QPushButton(str(4)))
        # glayout.addWidget(QPushButton(str(5)), 0, 0)
        # glayout.addWidget(QPushButton(str(6)), 0, 1)
        # glayout.addWidget(QPushButton(str(7)), 1, 0)
        # glayout.addWidget(QPushButton(str(8)), 1, 1)
        # flayout.addWidget(QPushButton(str(9)))
        # flayout.addWidget(QPushButton(str(10)))
        # flayout.addWidget(QPushButton(str(11)))
        # flayout.addWidget(QPushButton(str(12)))

        # 准备4个控件
        hwg = QWidget()
        # vwg = QWidget()
        # gwg = QWidget()
        # fwg = QWidget()

        # 使用4个控件设置局部布局
        hwg.setLayout(hlayout)
        # vwg.setLayout(vlayout)
        # gwg.setLayout(glayout)
        # fwg.setLayout(flayout)

        # 将4个控件添加到全局布局中
        wlayout.addWidget(hwg)
        # wlayout.addWidget(vwg)
        # wlayout.addWidget(gwg)
        # wlayout.addWidget(fwg)

        self.setLayout(wlayout)
        self.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = Window()
    sys.exit(app.exec_())