# -*- coding: utf-8 -*-

from data import *
from geometry import *
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, \
    NavigationToolbar2TkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
LARGE_FONT = ("Verdana", 12)

# Variables globales
global group
group = import_data("villes.csv")
group.name = "Test"


class MainPage(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, "Travelling salesman problem")

        # Définition des frames
        self.commandes = tk.Frame(self)
        self.commandes.grid(row=0, column=0, sticky=W+E+N+S)
        self.affichage = tk.Frame(self)
        self.affichage.grid(row=2, column=0, sticky=W+E)
        self.fig = plt.figure(1)
        canvas = FigureCanvasTkAgg(self.fig, self.affichage)
        canvas.get_tk_widget().pack(side="top", fill=BOTH, expand=True)
        toolbar = NavigationToolbar2TkAgg(canvas, self.affichage)
        toolbar.update()
        canvas._tkcanvas.pack(side="top", fill=BOTH, expand=True)

        # Commandes
        button = ttk.Button(self.commandes, text="Charger groupe",
                            command=lambda: self.charger())
        button.grid(row=0, column=0)
        button2 = ttk.Button(self.commandes, text="Ajouter noeud",
                             command=lambda: self.ajouter_noeud())
        button2.grid(row=0, column=1)
        button3 = ttk.Button(self.commandes, text="Calcul",
                             command=lambda: self.calcul(group))
        button3.grid(row=0, column=2)

        # Nouveau noeud
        nv_noeud = tk.Frame(self)
        nv_noeud.grid(row=1, column=0, sticky=W+E)
        Label(nv_noeud, text="Nom du noeud :").grid(row=1, column=0)
        self.nv_noeud_nom = Entry(nv_noeud, textvariable=StringVar())
        self.nv_noeud_nom.grid(row=1, column=1)
        Label(nv_noeud, text="Index :").grid(row=1, column=2)
        self.nv_noeud_index = Entry(nv_noeud, textvariable=StringVar())
        self.nv_noeud_index.grid(row=1, column=3)
        Label(nv_noeud, text="X = ").grid(row=1, column=4)
        self.nv_noeud_X = Entry(nv_noeud, textvariable=StringVar())
        self.nv_noeud_X.grid(row=1, column=5)
        Label(nv_noeud, text="Y = ").grid(row=1, column=6)
        self.nv_noeud_Y = Entry(nv_noeud, textvariable=StringVar())
        self.nv_noeud_Y.grid(row=1, column=7)

    def charger(self):
        global group
        filename = filedialog.askopenfilename()
        group = import_data(filename)
        group.name = filename
        print("Chargement du fichier {}".format(filename))
        print(group)
        return group

    def ajouter_noeud(self):
        global group
        # group += Node(index=14, name="Barcelone", xy=[2.17340,41.38506])
        group += Node(index=int(self.nv_noeud_index.get()),
                      name=self.nv_noeud_nom.get(),
                      xy=[float(self.nv_noeud_X.get()),
                          float(self.nv_noeud_Y.get())])
        print(group)
        return group

    def calcul(self, group):
        self.fig.clear()
        self.fig.add_axes([0.1, 0.1, 0.8, 0.8])
        path1, cost1 = travelling_salesman_problem(group, CostMatrix(group),
                                                   ["Paris", "Moscou"],
                                                   self.fig.axes[0])
        self.fig.canvas.draw()
