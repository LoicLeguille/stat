import math
import random
import subprocess
import sys
from os import path
from tkinter import *
import statistics
import numpy as np
from tqdm import trange
from matplotlib import pyplot as plt
from PIL import Image
from PIL import ImageTk

class Hist():
    def __init__(self):
        self.parent = Tk()
        self.description = Toplevel(self.parent)
        self.SW = self.parent.winfo_screenwidth()
        self.SH = self.parent.winfo_screenheight()
        self.parent.resizable(0, 0)
        self.description.resizable(0, 0)
        self.parent.overrideredirect(True)
        self.description.overrideredirect(True)
        content, content1= f'+{int(100 / 2048 * self.SW)}+{int(400 / 1152 * self.SH)}', f'+{int(800 / 2048 * self.SW)}+{int(400 / 1152 * self.SH)}'
        self.parent.geometry(content)
        self.description.geometry(content1)
        self.load_data()
        self.canvas()
        self.parent.bind('<Return>', self.enter)
        self.parent.mainloop()
        self.description.mainloop()
        T1_list, T3_list, T4_list = self.calculation()
        self.plot(T1_list, T3_list, T4_list)

    def load_data(self):
        if getattr(sys, 'frozen', False):
            dir = path.dirname(sys.executable)
        elif __file__:
            dir = path.dirname(__file__)
        with open(path.join(dir, 'description.txt'), 'r', encoding='utf8') as f:
            self.description_txt = f.read()
        Bg = PhotoImage(file = path.join(dir, 'image', 'Bg.png'))
        self.Bg = Bg
        Exit = Image.open(path.join(dir, 'image', 'Exit.png'))
        Exit = Exit.resize((int(50 / 2048 * self.SW), int(48 / 1152 * self.SH)), Image.ANTIALIAS)
        self.Exit = ImageTk.PhotoImage(Exit)

    def canvas(self):
        canvas = Canvas(self.parent, width = int(500 / 2048 * self.SW), height = int(300 / 1152 * self.SH), highlightthickness = 0)
        canvas.pack()
        canvas.create_image(0, 0, image = self.Bg, anchor = NW)
        canvas.create_text(10 / 2052 * self.SW, 30 / 1152 * self.SH, text = 'Projet Stat', anchor = 'w', font = ('Japanese Robot', round(20 / 2048 * self.SW)), fill = 'white')
        canvas.create_text(100 / 2052 * self.SW, 130 / 1152 * self.SH, text = 'nb de tests =', anchor = 'w', font = ('Korean Calligraphy', round(20 / 2048 * self.SW)), fill = 'white')
        canvas.create_text(100 / 2052 * self.SW, 210 / 1152 * self.SH, text = 'theta =', anchor = 'w', font = ('Korean Calligraphy', round(20 / 2048 * self.SW)), fill = 'white')
        exit_btn = Button(self.parent, image = self.Exit, bd = 0, command = sys.exit)
        exit_btn.place(x = 500 / 2048 * self.SW, y = 0, anchor = NE)

        self.entryA = Entry(self.parent, width = 8)
        self.entryA.place(x = 300 / 2048 * self.SW, y = 130 / 1152 * self.SH, anchor = 'w')
        self.entryB = Entry(self.parent, width = 8)
        self.entryB.place(x = 300 / 2048 * self.SW, y = 210 / 1152 * self.SH, anchor = 'w')

        canvas1 = Canvas(self.description, width = int(1050 / 2048 * self.SW), height = int(300 / 1152 * self.SH), highlightthickness = 0)
        canvas1.pack()
        canvas1.create_image(0, 0, image = self.Bg, anchor = NW)
        canvas1.create_text(10 / 2052 * self.SW, 30 / 1152 * self.SH, text = 'Projet Stat', anchor = 'w', font = ('Japanese Robot', round(20 / 2048 * self.SW)), fill = 'white')
        canvas1.create_text(30 / 2052 * self.SW, 200 / 1152 * self.SH, text = self.description_txt, anchor = 'w', font = round(16 / 2048 * self.SW), fill = 'white')

    def enter(self, event):
        try:
            self.nb_test = int(self.entryA.get())
            self.theta = float(self.entryB.get())
        except:
            return
        if self.nb_test < 0 or self.theta <= 0:
            return
        self.parent.destroy()

    def calculation(self):
        T1_size, T3_size, T4_size = 0, 0, 0
        sample_size = 100
        population_size = 1000
        test = 0

        for test in trange(self.nb_test):

            T1, T3, T4 = 0, 0, 0
            T1_list, T3_list, T4_list = [], [], []
            population = [[- self.theta * math.log(random.random()) for i in range(sample_size)] for i in range(population_size)]

            for m in range(len(population)):
                T1_list.append(statistics.mean(population[m]))
                T3_list.append((sum(i ** 2 for i in population[m]) * (1 / (2 * sample_size))) ** .5)
                T4_list.append(statistics.pstdev(population[m]))

            for m in range(len(T1_list)):
                T1 += (T1_list[m] - self.theta) ** 2
                T3 += (T3_list[m] - self.theta) ** 2
                T4 += (T4_list[m] - self.theta) ** 2

            T1 /= population_size
            T3 /= population_size
            T4 /= population_size

            if T1 == min(T1, T3, T4):
                T1_size += 1
            if T3 == min(T1, T3, T4):
                T3_size += 1
            if T4 == min(T1, T3, T4):
                T4_size += 1

            test += 1

        return T1_list, T3_list, T4_list

    def plot(self, T1_list, T3_list, T4_list):
        T1_list.sort()
        T3_list.sort()
        T4_list.sort()
        T1_axis = [m for m in T1_list]
        T3_axis = [m for m in T3_list]
        T4_axis = [m for m in T4_list]
        median_T1 = statistics.median(T1_axis)
        median_T3 = statistics.median(T3_axis)
        median_T4 = statistics.median(T4_axis)

        plt.figure().canvas.set_window_title('Projet stat')
        plt.hist(T4_axis, bins = 'sturges', label = 'T4')
        plt.hist(T3_axis, bins = 'sturges', label = "T3'")
        plt.hist(T1_axis, bins = 'sturges', label = 'T1')

        plt.axvline(median_T1, color = 'red', label = 'T1 mediane')
        plt.axvline(median_T3, color = 'black', label = "T3' mediane")
        plt.axvline(median_T4, color = 'purple', label = 'T4 mediane')

        plt.title(f'theta = {self.theta}')
        plt.xlabel('Valeur des estimateurs')
        plt.ylabel("Nombre d'estimateurs")
        plt.legend()
        plt.show()
