# -*- coding: utf-8 -*-

import math
from elements import *


class RunMain:

    A = Node(name="A", x=0, y=0)
    B = Node(name="B", x=1, y=2)
    C = Node(name="C", x=3, y=4)
    D = Node(name="D", x=5, y=6)
    E = Node(name="E", x=7, y=8)

    print(A)

    group = NodeGroup([A, B, C, D, E])
    print(group)

    sorted_group = group.travelling_salesman_problem()
    print(sorted_group)

RunMain()
