import collections

class Bipartite:
    def __init__(self, V1, V2, edges):
        self.V1 = V1
        self.V2 = V2
        self.original_edges = edges
        self.graph = {}
        self.s = 's'
        self.t = 't'

    def create_graph(self):
        all_nodes = self.V1 + self.V2 + [self.s, self.t]
        self.graph = {node: set() for node in all_nodes}
        for u, v in self.original_edges:
            if u in self.V1 and v in self.V2:
                self.graph[u].add(v)
            elif v in self.V1 and u in self.V2:
                self.graph[v].add(u)
        for u in self.V1:
            self.graph[self.s].add(u)
        for v in self.V2:
            self.graph[v].add(self.t)

    def find_path(self):
        queue = collections.deque([[self.s]])
        visited = {self.s}
        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == self.t:
                return path
            for neighbor in self.graph.get(node, []):
                if neighbor not in visited:
                    visited.add(neighbor)
                    new_path = list(path)
                    new_path.append(neighbor)
                    queue.append(new_path)
        return None

    def solve(self):
        self.create_graph()
        iteration = 1
        while True:
            path = self.find_path()
            if not path:
                break
            first_node_in_V1 = path[1]
            if first_node_in_V1 in self.graph[self.s]:
                self.graph[self.s].remove(first_node_in_V1)
            last_node_in_V2 = path[-2]
            if self.t in self.graph[last_node_in_V2]:
                self.graph[last_node_in_V2].remove(self.t)
            internal_path = path[1:-1]
            for i in range(len(internal_path) - 1):
                u = internal_path[i]
                v = internal_path[i+1]
                if v in self.graph[u]:
                    self.graph[u].remove(v)
                self.graph[v].add(u)
            iteration += 1
        matching = []
        for v in self.V2:
            for u in self.graph[v]:
                if u in self.V1:
                    matching.append({u, v})
        return matching