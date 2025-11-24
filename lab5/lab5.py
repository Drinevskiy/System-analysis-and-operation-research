import collections

class Edge:
    def __init__(self, u, v, capacity):
        self.u = u
        self.v = v
        self.capacity = capacity
        self.flow = 0

    def __repr__(self):
        return f"{self.u}->{self.v} ({self.flow}/{self.capacity})"

class Graph:
    def __init__(self):
        self.edges = {}
        self.adj = collections.defaultdict(list)

    def add_edge(self, u, v, capacity):
        edge = Edge(u, v, capacity)
        self.edges[(u, v)] = edge
        self.adj[u].append(edge)

    def get_flow_value(self, s):
        sum_flow = 0
        for edge in self.adj[s]:
            sum_flow += edge.flow
        return sum_flow

class FordFulkerson:
    def __init__(self, graph, s, t):
        self.graph = graph
        self.s = s
        self.t = t


    def get_auxiliary_network(self):
        G_f = collections.defaultdict(dict)
        edges = set()
        for (u, v) in self.graph.edges:
            edges.add((u, v))
            edges.add((v, u))
        
        for u, v in edges:
            edge_direct = self.graph.edges.get((u, v))
            if edge_direct:
                c_a = edge_direct.capacity
                f_a = edge_direct.flow
            else:
                c_a = 0
                f_a = 0
            edge_reverse = self.graph.edges.get((v, u))
            if edge_reverse:
                f_a_reverse = edge_reverse.flow
            else:
                f_a_reverse = 0
            cf_a = c_a - f_a + f_a_reverse
            if cf_a > 0:
                G_f[u][v] = cf_a
        return G_f

    def method_of_labels(self, G_f):
        queue = collections.deque([self.s])
        parent = {self.s: None}
        marked_X = {self.s}
        while queue:
            u = queue.popleft()
            for v in G_f.get(u, {}):
                if v not in marked_X:
                    marked_X.add(v)
                    parent[v] = u
                    queue.append(v)
                    if v == self.t:
                        path = []
                        curr = self.t
                        while curr is not None:
                            path.append(curr)
                            curr = parent[curr]
                        return path[::-1], marked_X
        return None, marked_X

    def solve(self):
        print(f"Исток: {self.s}, Сток: {self.t}")
        iteration = 1
        while True:
            print(f"\n=== Итерация {iteration} ===")
            G_f = self.get_auxiliary_network()
            path, marked_X = self.method_of_labels(G_f)
            if path is None:
                print("В сети G_f нет пути из s в t.")
                print(f"Множество помеченных вершин X: {marked_X}")
                print("Текущий поток является максимальным.")
                break
            
            print(f"Найден путь P: {' -> '.join(path)}")
            
            theta = float('inf')
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                theta = min(theta, G_f[u][v])
            print(f"theta = {theta}")
            
            for i in range(len(path) - 1):
                u, v = path[i], path[i+1]
                if (u, v) in self.graph.edges:
                    self.graph.edges[(u, v)].flow += theta
                elif (v, u) in self.graph.edges:
                    self.graph.edges[(v, u)].flow -= theta
                else:
                    raise Exception(f"Ошибка: дуга {u}->{v} отсутствует в G")
            iteration += 1

        max_flow = self.graph.get_flow_value(self.s)
        print(f"Максимальный поток: {max_flow}")
        print("Распределение потоков по дугам:")
        for key, edge in self.graph.edges.items():
            print(f"  {edge}")

if __name__ == "__main__":
    g = Graph()
    s_node = 's'
    t_node = 't'

    g.add_edge(s_node, 'a', 3)
    g.add_edge('a', s_node, 0)
    g.add_edge(s_node, 'b', 2)
    g.add_edge('b', s_node, 0)
    g.add_edge('a', 'b', 2)
    g.add_edge('b', 'a', 0)
    g.add_edge('a', t_node, 1)
    g.add_edge(t_node, 'a', 0)
    g.add_edge('b', t_node, 2)
    g.add_edge(t_node, 'b', 0)

    solver = FordFulkerson(g, s_node, t_node)
    solver.solve()