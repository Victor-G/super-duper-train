# -*- coding: utf-8 -*-

import pandas as pd
from geometry import *


def import_data(data_name):
    with open(data_name,'rb') as file:
        data = pd.read_csv(file)
        nodes = list()
        for index,name,x,y in data.values:
            nodes.append(Node(index=index, name=name, xy=[x,y]))
        return NodesGroup(nodes)