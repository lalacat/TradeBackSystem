import sys

import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QApplication, QPushButton, QMainWindow, QVBoxLayout, QWidget
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FC


class QtDraw(QMainWindow):
    flag_btn_start = True

    def __init__(self):
        super(QtDraw, self).__init__()
        self.init_ui()

    def init_ui(self):
        self.resize(800, 600)
        self.setWindowTitle('PyQt5 Draw')

        # TODO:这里是结合的关键
        self.fig = plt.Figure()
        self.canvas = FC(self.fig)
        self.btn_start = QPushButton(self)
        self.btn_start.setText('draw')
        self.btn_start.clicked.connect(self.slot_btn_start)

        widget = QWidget()
        layout = QVBoxLayout()
        layout.addWidget(self.canvas)
        layout.addWidget(self.btn_start)
        widget.setLayout(layout)
        self.setCentralWidget(widget)

    def slot_btn_start(self):
        try:
            ax = self.fig.add_subplot(111)
            x = np.linspace(0, 100, 100)
            y = np.random.random(100)
            ax.cla()  # TODO:删除原图，让画布上只有新的一次的图
            ax.plot(x, y)
            self.canvas.draw()  # TODO:这里开始绘制
        except Exception as e:
            print(e)


def ui_main():
    app = QApplication(sys.argv)
    w = QtDraw()
    w.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    ui_main()
