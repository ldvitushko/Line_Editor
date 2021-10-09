from tkinter import ttk

import matplotlib.pyplot as plt
import numpy as np
from greenlet.tests.test_generator_nested import ax
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.spatial.qhull import ConvexHull
import tkinter as tk


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, start_point, finish_point):
        self.start_point = start_point
        self.finish_point = finish_point


def last(list):
    return list[-1]


def Plot(x, y, color):
    pts1 = [[int(x) - 0.5, int(y) - 0.5], [int(x) - 0.5, int(y) + 0.5], [int(x) + 0.5, int(y) + 0.5],
            [int(x) + 0.5, int(y) - 0.5]]
    pts = np.array(pts1)
    hull = ConvexHull(pts)
    ax.fill(pts[hull.vertices, 0], pts[hull.vertices, 1], color)
    line.draw()


def dda(line, debug):
    tree["displaycolumns"] = ("#1", "#3", "#4", "#6")
    start_point = line.start_point
    finish_point = line.finish_point
    line_len = max(abs(finish_point.x - start_point.x), abs(finish_point.y - start_point.y))
    dx = (finish_point.x - start_point.x) / line_len
    dy = (finish_point.y - start_point.y) / line_len
    x = start_point.x + 0.5 * np.sign(dx)
    y = start_point.y + 0.5 * np.sign(dy)
    i = 0
    if debug == 1:
        results.append((f'{i}', 0, f'{x}', f'{y}', 0, f'({int(x)};{int(y)})', 0, 0, 0))
        for res in results:
            tree.insert('', tk.END, values=res)
        tree.grid(row=0, column=0, sticky='we')
    Plot(x, y, 'black')
    if debug == 1:
        next_step_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    while i < line_len:
        if debug == 1:
            next_step_button.wait_variable(waitVar)
        x = x + dx
        y = y + dy
        i = i + 1
        Plot(x, y, 'black')
        if debug == 1:
            results.append((f'{i}', 0, f'{x}', f'{y}', 0, f'({int(x)};{int(y)})', 0, 0, 0))
            tree.insert('', tk.END, values=last(results))
    next_step_button.grid_forget()
    results.clear()
    ax.plot([start_point.x, finish_point.x], [start_point.y, finish_point.y], 'c')


def bresenham(line, debug):
    tree["displaycolumns"] = ("#1", "#2", "#3", "#4", "#5", "#6")
    start_point = line.start_point
    finish_point = line.finish_point
    x = start_point.x
    y = start_point.y
    dx = abs(finish_point.x - start_point.x)
    dy = abs(finish_point.y - start_point.y)
    i = 0
    e = 0
    e_next = 2 * min(dy, dx) - max(dx, dy)
    if debug == 1:
        results.append((f'{i}', f'{e}', f'{x}', f'{y}', f'{e_next}', f'({int(x)};{int(y)})', 0, 0, 0))
        for res in results:
            tree.insert('', tk.END, values=res)
        tree.grid(row=0, column=0, sticky='we')
    Plot(x, y, 'black')
    e = e_next
    if debug == 1:
        next_step_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
    while i < max(dx, dy):
        e_start = e
        if debug == 1:
            next_step_button.wait_variable(waitVar)
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
        if debug == 1:
            results.append((f'{i}', f'{e_start}', f'{x}', f'{y}', f'{e_next}', f'({int(x)};{int(y)})', 0, 0, 0))
            tree.insert('', tk.END, values=last(results))
        e = e_next
    next_step_button.grid_forget()
    results.clear()
    ax.plot([start_point.x, finish_point.x], [start_point.y, finish_point.y], 'c')


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
        bresenham(line, debug)
    else:
        tree["displaycolumns"] = ("#1", "#2", "#3", "#4", "#5", "#6", "#7", "#8", "#9")
        x = start_point.x
        y = start_point.y
        dx = abs(finish_point.x - start_point.x)
        dy = abs(finish_point.y - start_point.y)
        i = 0
        e = 0
        e_next = 2 * min(dy, dx) - max(dx, dy)
        if debug == 1:
            results.append((f'{i}', f'{e}', f'{x}', f'{y}', f'{e_next}', f'({start_point.x};{start_point.y})', f'100%', f'None', f'None'))
            for res in results:
                tree.insert('', tk.END, values=res)
            tree.grid(row=0, column=0, sticky='we')
        e = e_next
        Plot(x, y, 'black')
        if debug == 1:
            next_step_button.grid(row=7, column=0, columnspan=2, padx=5, pady=5)
        while i < max(dx, dy):
            e_start = e
            if debug == 1:
                next_step_button.wait_variable(waitVar)
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
            if debug == 1:
                results.append((f'{i}', f'{e_start}', f'{x}', f'{y}', f'{e_next}', f'({point1.x};{point1.y})', f'{(100 - float(str(color2)) * 100)}%', f'({point2.x};{point2.y})', f'{(100 - float(str(color1)) * 100)}%'))
                tree.insert('', tk.END, values=last(results))
            e = e_next
        next_step_button.grid_forget()
        results.clear()
        ax.plot([start_point.x, finish_point.x], [start_point.y, finish_point.y], 'c')


def draw_button_action():
    ax.clear()
    results.clear()
    tree.delete(*tree.get_children())
    tree.grid_forget()
    if comboAlgorithms.current() == 0:
        dda(Line(Point(start_point_x.get(), start_point_y.get()), Point(finish_point_x.get(), finish_point_y.get())),
            debug=is_debug_mode.get())
    elif comboAlgorithms.current() == 1:
        bresenham(
            Line(Point(start_point_x.get(), start_point_y.get()), Point(finish_point_x.get(), finish_point_y.get())),
            debug=is_debug_mode.get())
    elif comboAlgorithms.current() == 2:
        woo(Line(Point(start_point_x.get(), start_point_y.get()), Point(finish_point_x.get(), finish_point_y.get())),
            debug=is_debug_mode.get())
    line.draw()


if __name__ == "__main__":
    results = []
    root = tk.Tk()
    root.geometry('940x650')
    root.title("Графический редактор для построения отрезков")
    left_frame = tk.Frame(root)
    left_frame.place(relx=0.03, rely=0.05, relwidth=0.25, relheight=0.55)
    right_frame = tk.Frame(root, bg='#C0C0C0', bd=1.5)
    right_frame.place(relx=0.3, rely=0.05, relwidth=0.65, relheight=0.55)
    bottom_frame = tk.Frame(root, bd=3)
    bottom_frame.place(relx=0.03, rely=0.6, relwidth=0.94, relheight=0.4)
    bottom_frame.grid_rowconfigure(0, weight=1)
    bottom_frame.grid_columnconfigure(0, weight=1)
    RH = 0.19

    start_point_x = tk.IntVar()
    start_point_y = tk.IntVar()
    finish_point_x = tk.IntVar()
    finish_point_y = tk.IntVar()

    start_point_x_label = tk.Label(left_frame, text="x1:")
    start_point_y_label = tk.Label(left_frame, text="y1:")

    start_point_x_label.grid(row=0, column=0, sticky="w")
    start_point_y_label.grid(row=1, column=0, sticky="w")

    start_point_x_entry = tk.Entry(left_frame, textvariable=start_point_x)
    start_point_y_entry = tk.Entry(left_frame, textvariable=start_point_y)

    start_point_x_entry.grid(row=0, column=1, padx=5, pady=5)
    start_point_y_entry.grid(row=1, column=1, padx=5, pady=5)

    finish_point_x_label = tk.Label(left_frame, text="x2:")
    finish_point_y_label = tk.Label(left_frame, text="y2:")

    finish_point_x_label.grid(row=2, column=0, sticky="w")
    finish_point_y_label.grid(row=3, column=0, sticky="w")

    finish_point_x_entry = tk.Entry(left_frame, textvariable=finish_point_x)
    finish_point_y_entry = tk.Entry(left_frame, textvariable=finish_point_y)

    finish_point_x_entry.grid(row=2, column=1, padx=5, pady=5)
    finish_point_y_entry.grid(row=3, column=1, padx=5, pady=5)

    comboAlgorithms = ttk.Combobox(left_frame,
                                   values=[
                                       "Цифровой дифференциальный анализатор",
                                       "Алгоритм Брезенхема",
                                       "Алгоритм Ву"])
    comboAlgorithms.current(0)
    comboAlgorithms.grid(row=4, column=0, columnspan=2, padx=5, pady=5)

    is_debug_mode = tk.BooleanVar()
    is_debug_mode.set(0)
    checkDebugButton = tk.Checkbutton(left_frame, text="Режим дебага",
                                      variable=is_debug_mode,
                                      onvalue=1, offvalue=0)
    checkDebugButton.grid(row=5, column=0, columnspan=2, padx=5, pady=5)

    draw_button = tk.Button(left_frame, text="Отрисовать", command=draw_button_action)
    draw_button.grid(row=6, column=0, columnspan=2, padx=5, pady=5)

    next_step_button = tk.Button(left_frame, text="Следующий шаг", command=lambda: waitVar.set(1))

    columns = ('#1', '#2', '#3', '#4', '#5', '#6', '#7', '#8', '#9')

    tree = ttk.Treeview(bottom_frame, columns=columns, show='headings')
    tree.heading('#1', text='Шаг')
    tree.heading('#2', text='Ошибка e')
    tree.heading('#3', text='х')
    tree.heading('#4', text='у')
    tree.heading('#5', text='Скорректированное значение ошибки e*')
    tree.heading('#6', text='Отображаемые координаты')
    tree.heading('#7', text='Интенсивность первого пикселя')
    tree.heading('#8', text='Координаты второго пикселя')
    tree.heading('#9', text='Интенсивность второго пикселя')

    figure = plt.Figure(dpi=100)
    ax = figure.add_subplot(111, aspect='equal')
    line = FigureCanvasTkAgg(figure, right_frame)
    line.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)

    waitVar = tk.IntVar()

    root.mainloop()
