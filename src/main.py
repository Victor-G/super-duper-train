# -*- coding: utf-8 -*-

from elements import *
from matplotlib import pyplot as plt

class RunMain:

    A = Node(name="Paris", xy=[2.35222,48.85661])
    B = Node(name="Lyon", xy=[4.83565,45.76404])
    C = Node(name="Berlin", xy=[13.40495,52.52000])
    D = Node(name="Marseille", xy=[5.36977,43.29648])
    E = Node(name="Pragues", xy=[14.43780,50.07553])
    F = Node(name="Vienne",xy=[16.37381,48.20817])

    group = NodesGroup([A, A, B, C, D, E])
    # print(group)
    # print(F in group)
    group += A
    group += F
    print(group)

    path = travelling_salesman_problem(group, [A, B])
    plt.figure(1)
    plt.subplot(211)
    plt.title("Cost of the path: " + str(path.cost()))
    x = list()
    y = list()
    for i in path.path:
        x.append(path.group_of_nodes.nodes[i].xy[0])
        y.append(path.group_of_nodes.nodes[i].xy[1])
        plt.text(x=group.nodes[i].xy[0], y=group.nodes[i].xy[1],
                 s=group.nodes[i].name)
    plt.plot(x,y)

    path = travelling_salesman_problem(group, [A, B, D])
    plt.subplot(212)
    plt.title("Cost of the path: " + str(path.cost()))
    x = list()
    y = list()
    for i in path.path:
        x.append(path.group_of_nodes.nodes[i].xy[0])
        y.append(path.group_of_nodes.nodes[i].xy[1])
        plt.text(x=group.nodes[i].xy[0], y=group.nodes[i].xy[1],
                 s=group.nodes[i].name)
    plt.plot(x, y)
    plt.show()

    path = travelling_salesman_problem(group, [A])
    print(path)
    print(path.cost())

    group -= C
    print(group)
    path = travelling_salesman_problem(group, [A, B])
    print(path)
    print(path.cost())

RunMain()
