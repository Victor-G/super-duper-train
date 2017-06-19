# -*- coding: utf-8 -*-


class Node:

    def __init__(self, x, y, name="Node"):
        self.name = name
        self.x = x
        self.y = y

    def __str__(self):
        return "Node {} : x = {} y = {}".format(self.name, self.x, self.y)


class NodeGroup:

    def __init__(self, nodes):
        self.nodes = nodes

    def __str__(self):
        message = "Group of nodes:"
        i = 0
        while i < len(self.nodes):
            message += "\n - " + self.nodes[0].__str__()
            i += 1
        return message

    def travelling_salesman_problem(self):
        return self

        # function[mco, mch] = voyageur_de_commerce(pts, costs, mch)
        #
        # Xprim = unique(mch);
        #
        # while ~isempty(setdiff(pts, Xprim)),
        #
        # Xent = setdiff(pts, Xprim);
        # dminimal = zeros(length(Xent), 1);
        # idminimal = zeros(length(Xent), 1);
        # iaminimal = zeros(length(Xent), 1);
        # d = zeros(length(Xprim), 1);
        # for j = 1:length(Xent),
        # for k = 1:length(Xprim),
        # d(k) = costs(Xprim(k), Xent(j));
        # end
        # [valeur, position] = min(d);
        # dminimal(j) = valeur;
        # idminimal(j) = Xent(j);
        # iaminimal(j) = Xprim(position);
        # end
        # [~, position] = max(dminimal);
        # N = [iaminimal(position) idminimal(position)];
        # dmin = Inf;
        # for k = 1:length(mch) - 1
        # if costs(mch(k), N(2)) + costs(N(2), mch(k + 1)) - ...
        #     costs(mch(k), mch(k + 1)) < dmin,
        # dmin = costs(mch(k), N(2)) + costs(N(2), mch(k + 1)) - ...
        # costs(mch(k), mch(k + 1));
        # ordre = k;
        # end
        # end
        # mch = [mch(1:ordre) N(2)
        # mch(ordre + 1: end)];
        # Xprim = [Xprim N(2)];
        #
        # end
        #
        # mco = 0;
        # for k = 1:length(mch) - 1,
        # mco = mco + costs(mch(k), mch(k + 1));
        # end
        # mch = mch
        # ';
