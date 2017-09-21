# -*- coding: utf-8 -*-

from geometry import *
from data import *
from gui import *
from matplotlib import pyplot as plt
import matplotlib
matplotlib.use("TkAgg")


class RunMain:

    # # Importation du fichier de villes
    # group = import_data("villes.csv")
    # group.name = "Test"
    # print(group)
    # group += Node(index=14, name="Barcelone", xy=[2.17340,41.38506])
    # print(group)
    #
    # # Calcul des chemins et réation des figures
    # fig = plt.figure(1)
    # ax1 = fig.add_subplot(311)
    # path1, cost1 = travelling_salesman_problem(group, CostMatrix(group),
    #                                     ["Paris", "Moscou"], ax1)
    #
    # ax2 = fig.add_subplot(312)
    # travelling_salesman_problem(group, CostMatrix(group),
    #                             ["Paris", "Marseille", "Lyon", "Rome",
    #                              "Paris"],ax2)
    #
    # ax3 = fig.add_subplot(313)
    # travelling_salesman_problem(group, CostMatrix(group),
    #                             ["Paris", "Paris"], ax3)

    # plt.show()

    # var_case = IntVar()
    # case = Checkbutton(fenetre, text="Ne plus poser cette question",
    #                    variable=var_case)
    # case.pack()
    # print(var_case.get())
    #
    # var_choix = StringVar()
    # choix_rouge = Radiobutton(fenetre, text="Rouge", variable=var_choix,
    #                           value="rouge")
    # choix_vert = Radiobutton(fenetre, text="Vert", variable=var_choix,
    #                          value="vert")
    # choix_bleu = Radiobutton(fenetre, text="Bleu", variable=var_choix,
    #                          value="bleu")
    # choix_rouge.pack()
    # choix_vert.pack()
    # choix_bleu.pack()
    # print(var_choix.get())
    #
    # liste = Listbox(fenetre)
    # liste.insert(END, "Pierre")
    # liste.insert(END, "Feuille")
    # liste.insert(END, "Ciseau")
    # liste.pack()
    # print(liste.curselection())

    app = MainPage()
    app.mainloop()

RunMain()
