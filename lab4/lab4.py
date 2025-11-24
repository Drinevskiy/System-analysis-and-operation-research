class Graph:
    def __init__(self):
        self.adj = {} 
        self.reverse_adj = {}
        self.nodes = set()

    def add_edge(self, u, v, weight):
        if u not in self.adj: self.adj[u] = []
        if v not in self.adj: self.adj[v] = []
        if u not in self.reverse_adj: self.reverse_adj[u] = []
        if v not in self.reverse_adj: self.reverse_adj[v] = []
        
        self.adj[u].append((v, weight))
        self.reverse_adj[v].append((u, weight))
        self.nodes.add(u)
        self.nodes.add(v)

    def topological_sort(self):
        visited = set()
        stack = []

        def dfs(node):
            visited.add(node)
            if node in self.adj:
                for neighbor, _ in self.adj[node]:
                    if neighbor not in visited:
                        dfs(neighbor)
            stack.append(node)

        for v in self.nodes:
            if v not in visited:
                dfs(v)
        
        return stack[::-1]

    def find_longest_path(self, s, t):
        topo_order = self.topological_sort()
        if s not in self.nodes or t not in self.nodes:
            return "Ошибка: одна из вершин отсутствует в графе."

        topo_indices = {node: i for i, node in enumerate(topo_order)}
        
        k = topo_indices[s]
        l = topo_indices[t]

        print(f"Топологический порядок: {topo_order}")
        print(f"Индекс s='{s}': {k}, Индекс t='{t}': {l}")

        if k > l:
            return f"Вершина '{t}' недостижима из '{s}' (s находится после t в топологическом порядке)."

        opt = {node: float('-inf') for node in self.nodes}
        x = {node: None for node in self.nodes}
        opt[s] = 0

        for i in range(k + 1, l + 1):
            v_i = topo_order[i]
            if v_i in self.reverse_adj:
                max_value = float('-inf')
                best_node = None
                for v_prev, weight in self.reverse_adj[v_i]:
                    if opt[v_prev] != float('-inf'):
                        current_val = opt[v_prev] + weight
                        if current_val > max_value:
                            max_value = current_val
                            best_node = v_prev
                
                if max_value != float('-inf'):
                    opt[v_i] = max_value
                    x[v_i] = best_node

        if opt[t] == float('-inf'):
             return f"Вершина '{t}' недостижима из '{s}' (нет связного пути)."
        else:
            print("\nopt: ", opt)
            print("x: ", x, "\n")
            path = []
            curr = t
            while curr is not None:
                path.append(curr)
                curr = x[curr]
            
            path.reverse()
            return {
                "length": opt[t],
                "path": path
            }

if __name__ == "__main__":
    g = Graph()
    s_node = "s"
    t_node = "t"

    g.add_edge(s_node, "a", 3)
    g.add_edge(s_node, "c", 2)
    g.add_edge("c", "a", 2)
    g.add_edge("a", "b", 4)
    g.add_edge("c", "d", 2)
    g.add_edge("b", "d", 1)
    g.add_edge("b", t_node, 2)
    g.add_edge("d", t_node, 1)

    result = g.find_longest_path(s_node, t_node)

    if isinstance(result, dict):
        print(f"Максимальная длина пути: {result['length']}")
        print(f"Путь: {' -> '.join(result['path'])}")
    else:
        print(result)

    print()
    print(g.find_longest_path("b", "c"))