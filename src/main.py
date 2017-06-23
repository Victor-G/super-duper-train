# -*- coding: utf-8 -*-

from geometry import *
from data import *
from matplotlib import pyplot as plt


class RunMain:

    group = import_data("villes.csv")
    group.name = "Test"
    print(group)
    group += Node(index=14, name="Barcelone", xy=[2.17340,41.38506])
    print(group)

    fig = plt.figure(1)
    ax1 = fig.add_subplot(311)
    path1, cost1 = travelling_salesman_problem(group, CostMatrix(group),
                                        ["Paris", "Moscou"], ax1)

    ax2 = fig.add_subplot(312)
    travelling_salesman_problem(group, CostMatrix(group),
                                ["Paris", "Marseille", "Lyon", "Rome",
                                 "Paris"],ax2)

    ax3 = fig.add_subplot(313)
    travelling_salesman_problem(group, CostMatrix(group),
                                ["Paris", "Paris"], ax3)

    plt.show()

RunMain()
