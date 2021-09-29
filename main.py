import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from scipy.spatial.qhull import ConvexHull


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Графический редактор для построения отрезков")
        self.resize(800, 400)
        # self.centralWidget = QLabel("Hello, World")
        # self.centralWidget.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        # self.setCentralWidget(self.centralWidget)
        self._createActions()
        self._createMenuBar()

    def _createMenuBar(self):
        menuBar = self.menuBar()
        # File menu
        lineMenu = QMenu("Отрезки", self)
        menuBar.addMenu(lineMenu)
        lineMenu.addAction(self.ddaAction)
        lineMenu.addAction(self.bresenhamAction)
        lineMenu.addAction(self.wooAction)
        # Edit menu
        editMenu = menuBar.addMenu("Отладочный режим")
        menuBar.addMenu(editMenu)

    # Действие для QAction
    '''def _f(self):
        win.setCentralWidget(QLabel("EEEEEEE"))'''

    def _createActions(self):
        self.ddaAction = QAction("Алгоритм ЦДА", self)
        # Добавляем функцию которая отработает при нажатии
        # self.ddaAction.triggered.connect(self._f)
        # ---------------------------------------------
        self.bresenhamAction = QAction("Целочисленный алгоритм Брезенхема", self)
        self.wooAction = QAction("Алгоритм Ву", self)


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start_point, finish_point):
        self.start_point = start_point
        self.finish_point = finish_point


def Plot(x, y, color):
    pts1 = [[int(x) - 0.5, int(y) - 0.5], [int(x) - 0.5, int(y) + 0.5], [int(x) + 0.5, int(y) + 0.5],
            [int(x) + 0.5, int(y) - 0.5]]
    pts = np.array(pts1)
    hull = ConvexHull(pts)
    plt.fill(pts[hull.vertices, 0], pts[hull.vertices, 1], color)


def dda(line):
    start_point = line.start_point
    finish_point = line.finish_point
    line_len = max(abs(finish_point.x - start_point.x), abs(finish_point.y - start_point.y))
    dx = (finish_point.x - start_point.x) / line_len
    dy = (finish_point.y - start_point.y) / line_len
    x = start_point.x + 0.5 * np.sign(dx)
    y = start_point.y + 0.5 * np.sign(dy)
    i = 0
    print(i, x, y, int(x), int(y))
    Plot(x, y, 'black')
    while i < line_len:
        x = x + dx
        y = y + dy
        i = i + 1
        print(i, x, y, int(x), int(y))
        Plot(x, y, 'black')
    plt.plot([start_point.x, finish_point.x], [start_point.y, finish_point.y], 'c')
    plt.gca().set_aspect('equal')
    plt.show()


def bresenham(line):
    start_point = line.start_point
    finish_point = line.finish_point
    x = start_point.x
    y = start_point.y
    dx = abs(finish_point.x - start_point.x)
    dy = abs(finish_point.y - start_point.y)
    e = 2 * dy - dx
    i = 0
    Plot(x, y, 'black')
    print(i, e, x, y)
    while i < dx:
        if e >= 0:
            y = y + 1*np.sign(finish_point.y - start_point.y)
            e = e - 2 * dx
        x = x + 1*np.sign(finish_point.x - start_point.x)
        e = e + 2 * dy
        i = i + 1
        Plot(x, y, 'black')
        print(i, e, x, y)
    plt.plot([start_point.x, finish_point.x], [start_point.y, finish_point.y], 'c')
    plt.gca().set_aspect('equal')
    plt.show()


def get_len(point, line):
    x1 = line.start_point.x
    y1 = line.start_point.y
    x2 = line.finish_point.x
    y2 = line.finish_point.y
    x3 = point.x
    y3 = point.y
    k = ((y2 - y1) * (x3 - x1) - (x2 - x1) * (y3 - y1)) / ((y2 - y1) ^ 2 + (x2 - x1) ^ 2)
    x4 = x3 - k * (y2 - y1)
    y4 = y3 + k * (x2 - x1)
    dist = np.sqrt((x4 - x3) ** 2 + (y4 - y3) ** 2)
    return dist


def woo(line):
    start_point = line.start_point
    finish_point = line.finish_point
    if start_point.x == finish_point.x or start_point.y == finish_point.y or abs(finish_point.y - start_point.y) == abs(
            finish_point.x - start_point.x):
        bresenham(line)
    else:
        x = start_point.x
        y = start_point.y
        dx = abs(finish_point.x - start_point.x)
        dy = abs(finish_point.y - start_point.y)
        e = 2 * dy - dx
        i = 0
        Plot(x, y, 'black')
        while i < dx:
            point1 = Point(x+1 * np.sign(finish_point.x - start_point.x), y)
            point2 = Point(x+1 * np.sign(finish_point.x - start_point.x), y + 1 * np.sign(finish_point.y - start_point.y))
            len1 = get_len(point1, line)
            len2 = get_len(point2, line)
            len = len1 + len2
            color2 = round(len1/len, 1)
            color1 = round(1 - color2, 1)
            Plot(point1.x, point1.y, str(color2))
            Plot(point2.x, point2.y, str(color1))
            print(point1.x, point1.y, str(color2))
            print(point2.x, point2.y, str(color1))
            if e >= 0:
                y = y + 1 * np.sign(finish_point.y - start_point.y)
                e = e - 2 * dx
            x = x + 1 * np.sign(finish_point.x - start_point.x)
            e = e + 2 * dy
            i = i + 1
        plt.plot([start_point.x, finish_point.x], [start_point.y, finish_point.y], 'c')
        plt.gca().set_aspect('equal')
        plt.show()


if __name__ == "__main__":
    '''app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())'''
    line = Line(Point(0, 0), Point(8, 2))
    woo(line)
