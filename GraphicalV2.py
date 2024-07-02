import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QSizePolicy, QWidget, QMainWindow, QMenu, QVBoxLayout, QSpinBox, QScrollBar
from PyQt5.QtCore import Qt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MyMplCanvas(FigureCanvas):
    def __init__(self, parent=None, width=10, height=7, dpi=200):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        FigureCanvas.__init__(self, fig)
        self.setParent(parent)
        self.axes.plot()
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


class MyDynamicMplCanvas(MyMplCanvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.t = np.arange(0.0, 3.0, 0.01)

    def update_figure(self, value):
        self.axes.cla()
        s = np.sin(value * np.pi * self.t)
        self.axes.plot(self.t, s)
        self.draw()


class ApplicationWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setStyleSheet('font-size: 35px;')
        self.file_menu = QMenu('&File', self)
        self.file_menu.addAction('&Quit', self.close, Qt.CTRL + Qt.Key_Q)
        self.menuBar().addMenu(self.file_menu)

        self.main_widget = QWidget()
        layout = QVBoxLayout(self.main_widget)

        self.spinbox = QSpinBox(minimum=1, maximum=10, singleStep=1, value=1)
        self.scrollbar = QScrollBar(Qt.Horizontal)
        self.scrollbar.setMinimum(1)
        self.scrollbar.setMaximum(10)
        self.scrollbar.setValue(1)

        sc = MyDynamicMplCanvas(self.main_widget)

        self.spinbox.valueChanged.connect(sc.update_figure)
        self.scrollbar.valueChanged.connect(sc.update_figure)

        sc.update_figure(self.spinbox.value())

        layout.addWidget(self.spinbox)
        layout.addWidget(self.scrollbar)
        layout.addWidget(sc)

        self.main_widget.setFocus()
        self.setCentralWidget(self.main_widget)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = ApplicationWindow()
    win.setWindowTitle("PyQt5 Matplotlib App Demo")
    win.show()
    sys.exit(app.exec_())
