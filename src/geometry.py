# -*- coding: utf-8 -*-

import math
from numpy import sort
from scipy.sparse import coo_matrix
from theano.gradient import np


class Node:
    """Geographical point. Attributes:

        index(int):
            index of the node.

        xy([double,double]):
            coordinates (abscissa and ordinate).

        name(str):
            name of the point.
    """

    def __init__(self, index = 0, name="Node", xy=(0,0)):
        # Initialize the node
        self.index = index
        self.name = name
        self.xy = xy

    def __str__(self):
        # Stringify the node
        return "{}: x = {} y = {}".format(self.name, self.xy[0],self.xy[1])


class NodesGroup:
    """Group of geographical points. Attributes:

        name(str):
            name of the group.

        nodes(list[Node]):
            list of the nodes.

    """

    def __init__(self, name="", nodes=[]):
        # Initialize the group of nodes
        # If just one node: transform into a list
        if not isinstance(nodes, list):
            nodes = [nodes]
        # Eliminate the duplicate nodes
        nodes = list(set(nodes))
        # Create the group of nodes
        self.name = name
        self.nodes = nodes
        # Sort the nodes according to the indexes
        self.sort_nodes()

    def __contains__(self, node):
        # Verify if a node is contained in the group
        if node in self.nodes:
            return True
        else:
            return False

    def __getitem__(self, item):
        # Extract a node of the group with the command group[item]
        if not isinstance(item,list):
            item = [item]
        nodes = list()
        for i in item:
            try:
                position = self.get_indexes().index(i)
                nodes.append(self.nodes[position])
            except ValueError:
                print("GETITEM: The node with the index {} is not in the "
                      "group".format(i))
                return []
        if len(nodes) == 1:
            nodes = nodes[0]
        return nodes

    def __delitem__(self, key):
        # Remove a node from the group with the command del group[item]
        if not isinstance(key,list):
            key = [key]
        for i in key:
            if i in self.get_indexes():
                self.nodes.remove(self[i])
                self.sort_nodes()
            else:
                print("DELITEM: The node with the index {} is not in the "
                      "group".format(i))

    def __add__(self, nodes):
        # Add a node to the group
        if isinstance(nodes,NodesGroup):
            nodes = nodes.nodes
        else:
            # If just one node: transform into a list
            if not isinstance(nodes,list):
                nodes = [nodes]
        new_group = NodesGroup(name=self.name,nodes=self.nodes)
        for node in nodes:
            if node in new_group.nodes:
                print("ADD: The node {} is already in the list.".format(
                    node.name))
            else:
                # Addition of the new node(s)
                new_group.nodes.append(node)
        new_group.sort_nodes()
        return new_group

    def __sub__(self, nodes):
        # Remove a node of the group
        if isinstance(nodes,NodesGroup):
            nodes = nodes.nodes
        else:
            # If just one node: transform into a list
            if not isinstance(nodes,list):
                nodes = [nodes]
        new_group = NodesGroup(name=self.name,nodes=self.nodes)
        for node in nodes:
            if node not in new_group.nodes:
                print("SUB: The node {} is not in the group.".format(
                    node.name))
            else:
                new_group.nodes.remove(node)
        new_group.sort_nodes()
        return new_group

    def __str__(self):
        # Stringify the group of nodes
        message = "Group {}: {} node(s):".format(self.name,str(len(self.nodes)))
        i = 0
        while i < len(self.nodes):
            message += "\n - [" + str(self.nodes[i].index) + "] "\
                       + self.nodes[i].__str__()
            i += 1
        return message

    def __len__(self):
        # Return the number of nodes in the group
        return len(self.nodes)

    def sort_nodes(self):
        # Sort the list of nodes in the group according to the index
        indexes = sort(self.get_indexes())
        nodes = list()
        for i in indexes:
            nodes.append(self[i])
        self.nodes = nodes

    def get_names(self):
        # Extract the list of nodes' names
        names = list()
        for node in self.nodes:
            names.append(node.name)
        return names

    def get_indexes(self):
        indexes = list()
        for node in self.nodes:
            indexes.append(node.index)
        return indexes


class CostMatrix:
    """Cost of the paths between each couple of a group of nodes. The costs
    correspond to the geometrical distance between points. They are indexed
    according to the index of each point. Attributes:

        row(np.array):
            rows of the sparse matrix of the costs.

        col(np.array):
            col of the sparse matrix of the costs.

        data(np.array):
            data of the sparse matrix of the costs.

    """

    def __init__(self, group_of_nodes):
        # Initialisation
        row = list()
        col = list()
        data = list()
        for i in group_of_nodes.get_indexes():
            index_j = group_of_nodes.get_indexes()
            index_j.remove(i)
            for j in index_j:
                row.append(i)
                col.append(j)
                data.append(math.sqrt(
                            math.pow(group_of_nodes[i].xy[0] -
                                     group_of_nodes[j].xy[0], 2) +
                            math.pow(group_of_nodes[i].xy[1] -
                                     group_of_nodes[j].xy[1], 2)))
        self.row = np.array(row)
        self.col = np.array(col)
        self.data = np.array(data)

    def value(self,i,j):
        # Calculate the cost of the path between nodes i and j
        if i == j:
            return 0
        else:
            rows = np.where(self.row == i)[0]
            column = rows[np.where(self.col[rows] == j)[0]]
            return self.data[column]


def travelling_salesman_problem(group_of_nodes, costmatrix, init, ax = None):
    """ Calculate the shortest path containing a set of geographical nodes,
    with a, initial solution.

    :param group_of_nodes:
        set of geographical nodes that have to be connected.

    :param costmatrix:
        matrix containing the cost of the path for each pair of nodes.

    :param init:
        initial solution which necessitates at least two nodes or more.

    :return:
        the shortest path and its cost.

    """

    # Verify the input
    try:
        assert len(init) >= 2
    except AssertionError:
        print("The travelling salesman problem needs at least two points for "
              "the initial solution. The returned path is not optimized!")
        return group_of_nodes.nodes, float("Inf")
    for i in range(0,len(init)):
        if isinstance(init[i], Node):
            # The input is a Node object
            if init[i] not in group_of_nodes:
                print("A node of the path is not in the group of nodes."
                      "The returned path is not optimized!")
                return group_of_nodes.nodes, float("Inf")
            init[i] = Node.index
        if isinstance(init[i], str):
            # The input is the name of the node
            position = group_of_nodes.get_names().index(init[i])
            init[i] = group_of_nodes.nodes[position].index
        elif isinstance(init[i], float):
            # The input is the index of the node, but a float
            init[i] = int([init[i]])

    # Set the points to connect and the initial solution
    path = init[:]
    xprim = init[:]
    pts = group_of_nodes.get_indexes()

    # Algorithm of Christofides
    while list(set(pts) - set(xprim)):
        xent = list(set(pts) - set(xprim))
        dminimal = np.zeros(len(xent))
        idminimal = np.zeros(len(xent))
        iaminimal = np.zeros(len(xent))
        d = np.zeros(len(xprim))
        for i in range(0,len(xent)):
            for j in range(0,len(xprim)):
                d[j] = costmatrix.value(xent[i],xprim[j])
            dminimal[i] = min(d)
            position = list(d).index(dminimal[i])
            idminimal[i] = xent[i]
            iaminimal[i] = xprim[position]
        position = list(dminimal).index(max(dminimal))
        n = [int(iaminimal[position]), int(idminimal[position])]
        dmin = float("Inf")
        for i in range(0,len(path)-1):
            new_d = costmatrix.value(path[i],n[1]) + \
                    costmatrix.value(n[1],path[i+1]) - \
                    costmatrix.value(path[i],path[i+1])
            if new_d < dmin:
                dmin = new_d
                order = i
        path = path[:order+1] + [n[1]] + path[order+1:]
        xprim.append(n[1])

    # Cost of the path
    cost = 0
    for i in range(0, len(path) - 1):
        cost += costmatrix.value(path[i], path[i + 1])

    # Display the result
    if ax is not None:
        ax.set_title("Path " + group_of_nodes[init[0]].name
                     + " -> " + group_of_nodes[init[1]].name + " - Cost = "
                     + str(cost))
        x = list()
        y = list()
        for i in path:
            x.append(group_of_nodes[i].xy[0])
            y.append(group_of_nodes[i].xy[1])
            ax.text(x=group_of_nodes[i].xy[0],
                    y=group_of_nodes[i].xy[1],
                    s=group_of_nodes[i].name)
        ax.plot(x, y)

    # Create and return of the optimized path
    return path, cost
