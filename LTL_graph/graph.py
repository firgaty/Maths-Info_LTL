from graphviz import Digraph
from ast import *


class BaseGraph(object):

    def __init__(self, graph_dict=None):
        """ initializes a graph object 
            If no dictionary or None is given, 
            an empty dictionary will be used
        """
        if graph_dict == None:
            graph_dict = {}
        self._graph_dict = graph_dict

    def vertices(self):
        """ returns the vertices of a graph """
        return list(self._graph_dict.keys())

    def edges(self):
        """ returns the edges of a graph """
        return self._generate_edges()

    def add_vertex(self, vertex):
        """ If the vertex "vertex" is not in 
            self._graph_dict, a key "vertex" with an empty
            list as a value is added to the dictionary. 
            Otherwise nothing has to be done. 
        """
        if vertex not in self._graph_dict:
            self._graph_dict[vertex] = []

    def add_edge(self, edge):
        """ assumes that edge is of type set, tuple or list; 
            between two vertices can be multiple edges! 
        """
        # edge = set(edge)
        # (vertex1, vertex2) = tuple(edge)
        vertex1, vertex2 = edge[0], edge[1]
        if vertex1 in self._graph_dict:
            self._graph_dict[vertex1].append(vertex2)
        else:
            self._graph_dict[vertex1] = [vertex2]

    def _generate_edges(self):
        """ A static method generating the edges of the 
            graph "graph". Edges are represented as sets 
            with one (a loop back to the vertex) or two 
            vertices 
        """
        edges = []
        for vertex in self._graph_dict:
            for neighbour in self._graph_dict[vertex]:
                if [neighbour, vertex] not in edges:
                    edges.append([vertex, neighbour])
        return edges

    def __str__(self):
        res = "vertices: "
        for k in self._graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self._generate_edges():
            res += str(edge) + " "
        return res


class Buchi(BaseGraph):
    def __init__(self, graph_dict=None):
        super(Buchi, self).__init__(graph_dict)
        self.init_states = []
        self.repeated_states = []

    def add_init(self, vertex):
        self.init_states.append(vertex)

    def add_repeated(self, vertex):
        self.repeated_states.append(vertex)

    def __str__(self):
        res = "vertices: "
        for k in self._graph_dict:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self._generate_edges():
            res += str(edge) + " "
        res += "\ninit: "
        for i in self.init_states:
            res += str(i) + " "
        res += "\nrepeated: "
        for i in self.repeated_states:
            res += str(i) + " "
        return res

    def make_dot(self, atoms=None):
        g = Digraph('buchi', filename='buchi.png')
        g.attr('node', style='filled')

        for e in self._graph_dict:
            g.attr('node', shape='oval')
            g.attr('node', fillcolor='white')

            label = ''

            if atoms is None:
                label = str(e)
            else:
                for i in atoms[e]:
                    if (type(i) is not Not):
                        label += " " + i.to_string() + " |"

                if len(label) >= 2:
                    label = list(label)
                    label.pop()
                    label.pop()
                    label = ''.join(label)
                else:
                    label = "⊥"
            if e in self.init_states:
                g.attr('node', fillcolor='grey')
            if e in self.repeated_states:
                g.attr('node', shape='octagon')
            
            g.node(str(e), label=label)

            

        for e in self._generate_edges():
            g.edge(str(e[0]), str(e[1]))

        g.render()

        print("Les états à fond gris sont les états initiaux et acceptants, ceux à fond blanc les états ne reconnaissant pas la formule.\nLes états octogonaux sont les états qui doivent être infiniement répétés afin de vérifier la formule.")

        g.view()

        input("\n\nAppuyez sur une touche pour continuer...\n")
