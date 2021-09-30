import matplotlib.pyplot as plt
import numpy as np
from PyQt5.QtWidgets import QAction
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QMenu
from scipy.spatial.qhull import ConvexHull
from sqlalchemy import false, true


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


def dda(line, debug):
    start_point = line.start_point
    finish_point = line.finish_point
    line_len = max(abs(finish_point.x - start_point.x), abs(finish_point.y - start_point.y))
    dx = (finish_point.x - start_point.x) / line_len
    dy = (finish_point.y - start_point.y) / line_len
    x = start_point.x + 0.5 * np.sign(dx)
    y = start_point.y + 0.5 * np.sign(dy)
    i = 0
    if debug is true:
        print('Шаг %s; x = %f; y = %f\n'
              'Принимаем решение, что надо отразить пиксель (%s,%s)' % (i, x, y, int(x), int(y)))
    Plot(x, y, 'black')
    result = 0
    if debug is true:
        print('Введите 1, чтобы выполнить следующий шаг')
        result = input()
    if (debug is false) or (debug is true and int(result) == 1):
        while i < line_len:
            x = x + dx
            y = y + dy
            i = i + 1
            Plot(x, y, 'black')
            if debug is true and i < line_len and int(result) == 1:
                print('Шаг %s; x = %f; y = %f\n'
                      'Принимаем решение, что надо отразить пиксель (%s,%s)' % (i, x, y, int(x), int(y)))
                print('Введите 1, чтобы выполнить следующий шаг')
                result = input()
            elif debug is true and line_len >= 1 and int(result) == 1:
                print('Шаг %s; x = %f; y = %f\n'
                      'Принимаем решение, что надо отразить пиксель (%s,%s)' % (i, x, y, int(x), int(y)))
            elif debug is true and result != 1:
                print('Вы прервали построение')
                break;
    else:
        print('Вы прервали построение')
    plt.plot([start_point.x, finish_point.x], [start_point.y, finish_point.y], 'c')
    plt.gca().set_aspect('equal')
    plt.show()


def bresenham(line, debug):
    start_point = line.start_point
    finish_point = line.finish_point
    x = start_point.x
    y = start_point.y
    dx = abs(finish_point.x - start_point.x)
    dy = abs(finish_point.y - start_point.y)
    i = 0
    e = None
    e_next = 2 * min(dy, dx) - max(dx, dy)
    if debug is true:
        print('Шаг %s; e = %s; x = %f; y = %f; Скорректированное значение ошибки e* = %s\n'
              'Принимаем решение, что надо отразить пиксель (%s,%s)' % (i, e, x, y, e_next, int(x), int(y)))
    Plot(x, y, 'black')
    e = e_next
    result = 0
    if debug is true:
        print('Введите 1, чтобы выполнить следующий шаг')
        result = input()
    if (debug is false) or (debug is true and int(result) == 1):
        while i < max(dx, dy):
            if e >= 0:
                if dx > dy:
                    y = y + 1 * np.sign(finish_point.y - start_point.y)
                else:
                    x = x + 1 * np.sign(finish_point.x - start_point.x)
                e = e - 2 * max(dx, dy)
            if dx > dy:
                x = x + 1 * np.sign(finish_point.x - start_point.x)
            else:
                y = y + 1 * np.sign(finish_point.y - start_point.y)
            e_next = e + 2 * min(dy, dx)
            i = i + 1
            Plot(x, y, 'black')
            if debug is true and i < max(dx, dy) and int(result) == 1:
                print('Шаг %s; e = %s; x = %f; y = %f; Скорректированное значение ошибки e* = %s\n'
                      'Принимаем решение, что надо отразить пиксель (%s,%s)' % (i, e, x, y, e_next, int(x), int(y)))
                print('Введите 1, чтобы выполнить следующий шаг')
                result = input()
            elif debug is true and max(dx, dy) >= 1 and int(result) == 1:
                print('Шаг %s; e = %s; x = %f; y = %f; Скорректированное значение ошибки e* = %s\n'
                      'Принимаем решение, что надо отразить пиксель (%s,%s)' % (i, e, x, y, e_next, int(x), int(y)))
            elif debug is true and result != 1:
                print('Вы прервали построение')
                break
            e = e_next
    else:
        print('Вы прервали построение')
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


def woo(line, debug):
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
        i = 0
        e = None
        e_next = 2 * min(dy, dx) - max(dx, dy)
        if debug is true:
            print('Шаг %s; e = %s; x = %f; y = %f; Скорректированное значение ошибки e* = %s\n'
                  'Принимаем решение, что надо отразить пиксель (%s,%s) интенсивностью 100%%' % (
                      i, e, x, y, e_next, int(x), int(y)))
        e = e_next
        Plot(x, y, 'black')
        result = 0
        if debug is true:
            print('Введите 1, чтобы выполнить следующий шаг')
            result = input()
        if (debug is false) or (debug is true and int(result) == 1):
            while i < max(dx, dy):
                if dx > dy:
                    point1 = Point(x + 1 * np.sign(finish_point.x - start_point.x), y)
                    point2 = Point(x + 1 * np.sign(finish_point.x - start_point.x),
                                   y + 1 * np.sign(finish_point.y - start_point.y))
                else:
                    point1 = Point(x, y + 1 * np.sign(finish_point.y - start_point.y))
                    point2 = Point(x + 1 * np.sign(finish_point.x - start_point.x),
                                   y + 1 * np.sign(finish_point.y - start_point.y))
                len1 = get_len(point1, line)
                len2 = get_len(point2, line)
                len = len1 + len2
                color2 = round(len1 / len, 1)
                color1 = round(1 - color2, 1)
                Plot(point1.x, point1.y, str(color2))
                Plot(point2.x, point2.y, str(color1))
                if e >= 0:
                    if dx > dy:
                        y = y + 1 * np.sign(finish_point.y - start_point.y)
                    else:
                        x = x + 1 * np.sign(finish_point.x - start_point.x)
                    e = e - 2 * max(dx, dy)
                if dx > dy:
                    x = x + 1 * np.sign(finish_point.x - start_point.x)
                else:
                    y = y + 1 * np.sign(finish_point.y - start_point.y)
                e_next = e + 2 * min(dy, dx)
                i = i + 1
                if debug is true and i < max(dx, dy) and int(result) == 1:
                    print('Шаг %s; e = %s; x = %f; y = %f; Скорректированное значение ошибки e* = %s\n'
                          'Принимаем решение, что надо отразить пиксель (%s,%s) интенсивностью %s%% и пиксель (%s,'
                          '%s) интенсивностью %s%%' % (
                              i, e, x, y, e_next, point1.x, point1.y, (100 - float(str(color2))*100), point2.x, point2.y,
                              (100 - float(str(color1))*100)))
                    print('Введите 1, чтобы выполнить следующий шаг')
                    result = input()
                elif debug is true and max(dx, dy) >= 1 and int(result) == 1:
                    print('Шаг %s; e = %s; x = %f; y = %f; Скорректированное значение ошибки e* = %s\n'
                          'Принимаем решение, что надо отразить пиксель (%s,%s) интенсивностью %s%% и пиксель (%s,'
                          '%s) интенсивностью %s%%' % (
                              i, e, x, y, e_next, point1.x, point1.y, (100 - float(str(color2))*100), point2.x, point2.y,
                              (100 - float(str(color1))*100)))
                elif debug is true and int(result) != 1:
                    print('Вы прервали построение')
                    break
                e = e_next
        else:
            print('Вы прервали построение')
        plt.plot([start_point.x, finish_point.x], [start_point.y, finish_point.y], 'c')
        plt.gca().set_aspect('equal')
        plt.show()


def print_menu():
    print('\n--------------Меню---------------\n'
          '1. Построить отрезки\n'
          '2. Отладочный режим\n'
          '0. Выход')


def algorithm_menu(debug):
    print('\n1. Цифровой дифференциальный анализатор\n'
          '2. Алгоритм Брезенхема\n'
          '3. Алгоритм Ву\n'
          '0. Выход в главное меню')
    choice = int(input())
    if choice == 1:
        print('Введите координаты стартовой точки отрезка x и y через пробел')
        x1, y1 = map(int, input().split())
        print('Введите координаты конечной точки отрезка x и y через пробел')
        x2, y2 = map(int, input().split())
        dda(Line(Point(x1, y1), Point(x2, y2)), debug)
    elif choice == 2:
        print('Введите координаты стартовой точки отрезка x и y через пробел')
        x1, y1 = map(int, input().split())
        print('Введите координаты конечной точки отрезка x и y через пробел')
        x2, y2 = map(int, input().split())
        bresenham(Line(Point(x1, y1), Point(x2, y2)), debug)
    elif choice == 3:
        print('Введите координаты стартовой точки отрезка x и y через пробел')
        x1, y1 = map(int, input().split())
        print('Введите координаты конечной точки отрезка x и y через пробел')
        x2, y2 = map(int, input().split())
        woo(Line(Point(x1, y1), Point(x2, y2)), debug)
    elif choice == 0:
        menu()


def menu():
    x = 1
    while x:
        print_menu()
        x = int(input())
        if x == 1:
            algorithm_menu(debug=false)
        elif x == 2:
            algorithm_menu(debug=true)
        elif x == 0:
            break;


if __name__ == "__main__":
    '''app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())'''
    menu()
