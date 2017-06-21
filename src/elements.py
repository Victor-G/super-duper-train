# -*- coding: utf-8 -*-

# Classes pour définir des noeuds et des groupes de noeuds, avec les méthodes
# géométriques et de théoriedes graphes correspondante.
# A faire :
# - générer un sous-groupe de noeud à partir d'un groupe

import math
from scipy.sparse import coo_matrix
from theano.gradient import np


class Node:
    """Geographical point. Attributes:

        xy([double,double]):
            coordinates (abscissa and ordinate).

        name(str):
            name of the point.
    """

    def __init__(self, xy, name="Node"):
        self.name = name
        self.xy = xy

    def __str__(self):
        return "Node {} : x = {} y = {}".format(self.name, self.xy[0],
                                                self.xy[1])


class NodesGroup:
    """Group of geographical points. Attributes:

        nodes(list[Node]):
            list of the nodes.

        d(coomatrix):
            sparse matrix of the distance between each couple of nodes (in
            meter).

    """

    def __init__(self, nodes):
        # If just one node: transform into a list
        if not isinstance(nodes, list):
            nodes = [nodes]
        # Eliminate the duplicate nodes
        nodes = list(set(nodes))
        # Create the group of nodes
        self.nodes = nodes
        self.d = distance_calculation(nodes)

    def __contains__(self, node):
        if node in self.nodes:
            return True
        else:
            return False

    def __add__(self, nodes):
        # If just one node: transform into a list
        if not isinstance(nodes,list):
            nodes = [nodes]
        # Verificate if there are not duplicate nodes
        for i in range(0, len(nodes)):
            if nodes[i] in self.nodes:
                print("The node {} is already in the list.".format(
                      nodes[i].name))
                nodes.remove(nodes[i])
        # Addition of the new node(s)
        new_group = self
        for i in range(0,len(nodes)):
            new_group.nodes.append(nodes[i])
        new_group.d = distance_calculation(new_group.nodes)
        return new_group

    def __sub__(self, nodes):
        # If just one node: transform into a list
        if not isinstance(nodes,list):
            nodes = [nodes]
        new_group = self
        for i in range(0,len(nodes)):
            new_group.nodes.remove(nodes[i])
        new_group.d = distance_calculation(new_group.nodes)
        return new_group

    def __str__(self):
        message = "Group of nodes:"
        i = 0
        while i < len(self.nodes):
            message += "\n - " + self.nodes[i].__str__()
            i += 1
        return message

    def __len__(self):
        return len(self.nodes)

    def costs(self,i,j):
        matrix = self.d.toarray()
        return matrix[min([i,j]),max([i,j])]


class Path:
    """Set of geographical points forming a path. Attributes:

        group_of_nodes(NodesGroup):
            group of the geographical points contained in the path.

        path(list[int]):
            list of the index of the geographical points forming the path,
            in order. The index corresponds to the position of the point in
            the group of points. An index can appear several times.

    """

    def __init__(self, group_of_nodes, path):
        self.group_of_nodes = group_of_nodes
        self.path = path

    def __str__(self):
        message = "Path: " + self.group_of_nodes.nodes[self.path[0]].name
        i = 1
        while i < len(self.path):
            message += " -> " + self.group_of_nodes.nodes[self.path[i]].name
            i += 1
        return message

    def cost(self):
        cost = 0
        for i in range(0, len(self.path)-1):
            cost += self.group_of_nodes.costs(self.path[i], self.path[i+1])
        return cost


def distance_calculation(nodes):
    """ Calculate the distance between each pair of a set of nodes.

    :param nodes:
        set of the nodes for the calculation.

    :return:
        sparse matrix of the distance between each couple of nodes (in
            meter).

    """

    row = list()
    col = list()
    data = list()
    for i in range(0, len(nodes) - 1):
        for j in range(i + 1, len(nodes)):
            row.append(i)
            col.append(j)
            data.append(math.sqrt(
                        math.pow(nodes[i].xy[0] - nodes[j].xy[0], 2) +
                        math.pow(nodes[i].xy[1] - nodes[j].xy[1], 2)))
    return coo_matrix((data, (row, col)))


def travelling_salesman_problem(group_of_nodes, init):
    """ Calculate the shortest path containing a set of geographical nodes,
    with a, initial solution.

    :param group_of_nodes:
        set of geographical nodes that have to be connected.

    :param init:
        initial solution which necessitates at least two nodes or more.

    :return:
        the shortest path.

    """

    # Verify the input
    try:
        assert len(init) >= 2
    except AssertionError:
        print("The travelling salesman problem needs at least two points for "
              "the initial solution. The returned path is not optimized !")
        return Path(group_of_nodes, list(range(0, len(group_of_nodes.nodes))))

    # Set the points to connect and the initial solution
    path = list()
    for node in init:
        path.append(group_of_nodes.nodes.index(node))
    xprim = path[:]
    pts = list(range(0, len(group_of_nodes.nodes)))

    # Algorithm of Christofides
    while list(set(pts) - set(xprim)):
        xent = list(set(pts) - set(xprim))
        dminimal = np.zeros(len(xent))
        idminimal = np.zeros(len(xent))
        iaminimal = np.zeros(len(xent))
        d = np.zeros(len(xprim))
        for i in range(0,len(xent)):
            for j in range(0,len(xprim)):
                d[j] = group_of_nodes.costs(xent[i],xprim[j])
            dminimal[i] = min(d)
            position = list(d).index(dminimal[i])
            idminimal[i] = xent[i]
            iaminimal[i] = xprim[position]
        position = list(dminimal).index(max(dminimal))
        n = [int(iaminimal[position]), int(idminimal[position])]
        dmin = float("Inf")
        for i in range(0,len(path)-1):
            if group_of_nodes.costs(path[i],n[1]) + \
                    group_of_nodes.costs(n[1],path[i+1]) - \
                    group_of_nodes.costs(path[i],path[i+1]) < dmin:
                dmin = group_of_nodes.costs(path[i],n[1]) + \
                       group_of_nodes.costs(n[1],path[i+1]) - \
                       group_of_nodes.costs(path[i],path[i+1])
                order = i
        path = path[:order+1] + [n[1]] + path[order+1:]
        xprim.append(n[1])

    # Create and return of the optimized path
    return Path(group_of_nodes, path)
