from sys import maxsize as inf

temp = 1  # объявляем константы
const = 2


class Vertex:
    def __init__(self, name):
        self.name = name  # название вершины графа


class DirectedWeightedGraph:
    def __init__(self, size=30):
        self.main = [[0 for column in range(size)] for row in range(size)]
        self.start = 0
        self.listvertex = []

    def display(self):
        for i in range(self.start):
            for j in range(self.start):
                print(self.main[i][j], end=' ')

    def Vertices(self):
        return self.name

    def Edges(self):
        start = 0
        for i in range(self.start):
            for j in range(self.start):
                if self.main[i][j] != 0:
                    start += 1
        return start

    def vertices(self):
        return [vertex.name for vertex in self.listvertex]

    def Edges(self):
        edges = []
        for i in range(self.start):
            for j in range(self.start):
                if self.main[i][j] != 0:
                    edges.append(self.listvertex[i].name)
                    edges.append(self.listvertex[j].name)
                    edges.append(self.main[i][j])
        return edges

    def getIndex(self, s):
        index = 0
        for name in (vertex.name for vertex in self.listvertex):
            if s == name:
                return index
            index += 1
        return None

    def insertVertex(self, name):
        if name in (vertex.name for vertex in self.listvertex):
            print('Такая вершина уже существует')
            return

        self.listvertex.append(Vertex(name))
        self.start += 1

    def removeVertex(self, name):
        index0 = self.getIndex(name)
        if index0 is None:
            print('Вершины нет в графе')
            return
        self.main.pop(index0)
        for i in range(self.start):
            self.main[i].pop(index0)
        self.listvertex.pop(index0)
        self.start -= 1

    def insertEdge(self, s1, s2, value):
        s1 = self.getIndex(s1)
        s2 = self.getIndex(s2)
        if s1 is None:
            print('Обозначьте стартовую вершину ')
        if s2 is None:
            print('Обозначьте конечную вершину')
        elif s1 == s2:
            print('Недопустимое ребро')
        elif self.main[s1][s2] != 0:
            print('Ребро уже существует')
        else:
            self.main[s1][s2] = value

    def removeEdge(self, s1, s2):
        s1 = self.getIndex(s1)
        s2 = self.getIndex(s2)
        if s1 is None:
            print('Начальной вершины нет в графе')
        elif s2 is None:
            print('Конечной вершины нет в графе')
        elif self.main[s1][s2] == 0:
            print('Ребра нет в графе')
        else:
            self.main[s1][s2] = 0

    def checkup(self, s1, s2):
        s1 = self.getIndex(s1)
        s2 = self.getIndex(s2)
        if s1 is None:
            print('Начальной вершины нет в графе')
            return False
        elif s2 is None:
            print('Конечной вершины нет в графе')
            return False
        return False if self.main[s1][s1] == 0 else True

    def outdegree(self, index1):
        u = self.getIndex(index1)
        if u is None:
            print('Вершины нет в графе')
            return
        outd = 0
        for v in range(self.start):
            if self.main[u][v] != 0:
                outd += 1
        return outd

    def indegree(self, index1):
        index1 = self.getIndex(index1)
        if index1 is None:
            print('Вершины нет в графе')
            return
        ind = 0

        for v in range(self.start):
            if self.main[u][v] != 0:
                ind += 1
        return ind

    def dijkstra(self, s):
        for i in range(self.start):
            self.listvertex[i].status = temp
            self.listvertex[i].pathLength = inf
            self.listvertex[i].parent = None

        self.listvertex[s].pathLength = 0
        while True:
            temp_vert = self.tempVertex()
            if temp_vert is None:
                return
            self.listvertex[temp_vert].status = const

            for v in range(self.start):
                if self.main[temp_vert][v] != 0 and \
                        self.listvertex[v].status == temp:
                    if self.listvertex[temp_vert].pathLength + \
                            self.main[temp_vert][v] < \
                            self.listvertex[v].pathLength:
                        self.listvertex[v].parent = temp_vert
                        self.listvertex[v].pathLength = \
                            self.listvertex[temp_vert].pathLength + \
                            self.main[temp_vert][v]

    def tempVertex(self):
        minimum = inf
        x = None
        for i in range(self.start):
            if self.listvertex[i].status == \
                    temp and self.listvertex[i].pathLength < minimum:
                minimum = self.listvertex[i].pathLength
                x = i
        return x

    def Paths(self, source):
        index1 = self.getIndex(source)
        if index1 is None:
            print('Вершины нет в графе')
            return

        self.dijkstra(index1)
        print('Исходная вершина:', source)
        for i in range(self.start):
            print('Конечная вершина:', self.listvertex[i].name)
            if self.listvertex[i].pathLength == inf:
                print('Нет пути от', source, 'к', \
                      self.listvertex[i].name, '\n')
            else:
                self.findPaths(index1, i)

    def findPaths(self, index1, value):
        paths = []
        start = 0
        count = 0
        while value != index1:
            count += 1
            paths.append(value)
            value1 = self.listvertex[value].parent
            start += self.main[value1][value]
            value = value1
        paths.append(index1)

        print('Самый короткий путь ', end=' ')
        for k in reversed(paths):
            print(k, end=' ')
        print('\nСамая короткая дистанция ', start, '\n')


graph = DirectedWeightedGraph()
graph.insertVertex('0')
graph.insertVertex('1')
graph.insertVertex('2')
graph.insertVertex('3')
graph.insertVertex('4')
graph.insertVertex('5')

graph.insertEdge('0', '2', 2)
graph.insertEdge('0', '2', 2)
graph.insertEdge('0', '1', 5)
graph.insertEdge('0', '3', 8)
graph.insertEdge('1', '4', 2)
graph.insertEdge('2', '3', 3)
graph.insertEdge('1', '3', 4)
graph.insertEdge('2', '4', 7)

graph.Paths('1')  # ищем пути во все вершины, которые есть
