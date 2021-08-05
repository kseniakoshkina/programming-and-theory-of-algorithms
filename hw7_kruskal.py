class Edge:

    def __init__(self, vertex1, vertex2, weight):
        self.vertex1 = vertex1
        self.vertex2 = vertex2
        self.weight = weight

    def getEdgeDetails(self):
        return '{}{}{}'.format(self.vertex1, self.weight, self.vertex2)


class Graph:
    def __init__(self, edges=None):
        self.vertices = {}
        self.edges = []
        if edges is not None:
            for edge in edges:
                self.addingEdge(edge)

    def addingEdge(self, edge, isDirected=False):

        if edge.vertex1 not in self.vertices:
            self.vertices[edge.vertex1] = []

        if edge.vertex2 not in self.vertices:
            self.vertices[edge.vertex2] = []

        self.vertices[edge.vertex1].append((edge.vertex2))

        if not isDirected:
            self.vertices[edge.vertex2].append((edge.vertex1))

    def removeEdge(self, edge, isDirected=False):
        self.edges.remove(edge)
        self.vertices[edge.vertex1].remove(edge.vertex2)

        if not isDirected:
            self.vertices[edge.vertex2].remove(edge.vertex1)

    def printingGraph(self):
        print('Количество вершин', len(self.vertices))
        keys = self.vertices.keys()
        for key in keys:
            print(key, ':', end=' ')
            print(self.vertices[key], end=' ')
            print()

    def printingEdges(self):
        for edge in self.edges:
            print(edge.getEdgedetails())

    def sortingEdges(self):
        edgeList = self.edges[:]
        from operator import attrgetter
        edgeList.sort(key=attrgetter('weight'), reverse=False)
        return edgeList

    def kruskal(self):
        main = Graph()
        edgeList = self.sortingEdges()
        for edge in edgeList:
            print('Добавление ребра', edge.getEdgeDetails())

            set1 = set(mst.vertices[edge.vertex1])
            set2 = set(mst.vertices[edge.vertex2])
            set3 = set1.intersection(set2)
            print(set1, set2)
            print(set3)

            if len(set3) != 0:
                main.removeEdge(edge)
                print(edge.getEdgeDetails())

            print()
        return main


edge0 = Edge(0, 1, 9)
edge1 = Edge(0, 2, 75)
edge2 = Edge(1, 2, 95)
edge3 = Edge(1, 3, 19)
edge4 = Edge(1, 4, 42)
edge5 = Edge(2, 3, 51)
edge6 = Edge(3, 4, 31)
edges = [edge0, edge1, edge2, edge3, edge4, edge5, edge6]

graph = Graph(edges)
graph.printingGraph()
graph.printingEdges()
main = graph.kruskal()
main.printingGraph()
main.printingEdges()
