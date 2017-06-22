# -*- coding: utf-8 -*-

from geometry import *
from data import *
from matplotlib import pyplot as plt


class RunMain:

    group = import_data("villes.csv")
    print(group)
    group += Node(index=7, name="Barcelone", xy=[2.17340,41.38506])
    print(group)

    fig = plt.figure(1)
    ax1 = fig.add_subplot(211)
    path1 = travelling_salesman_problem(group, ["Paris", "Marseille"],ax1)

    del group[5]
    print(group)
    ax2 = fig.add_subplot(212)
    path2 = travelling_salesman_problem(group, [1, 6],ax2)
    plt.show()

RunMain()
