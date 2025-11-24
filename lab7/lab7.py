import numpy as np
import collections
from Bipartite import Bipartite

class HungarianSolver:
    def __init__(self, matrix):
        self.C = np.array(matrix, dtype=float)
        self.n = self.C.shape[0]
        self.alpha = np.zeros(self.n)
        self.beta = np.min(self.C, axis=0)
        self.iteration_count = 0

    def get_equality_graph_edges(self):
        edges = []
        epsilon = 1e-9
        for i in range(self.n):
            for j in range(self.n):
                if abs(self.alpha[i] + self.beta[j] - self.C[i][j]) < epsilon:
                    u_node = f"u_{i}"
                    v_node = f"v_{j}"
                    edges.append((u_node, v_node))
        return edges

    def parse_matching(self, matching_sets):
        matching_pairs = []
        for pair_set in matching_sets:
            pair = list(pair_set)
            u, v = None, None
            for node in pair:
                if node.startswith("u_"):
                    u = int(node.split("_")[1])
                elif node.startswith("v_"):
                    v = int(node.split("_")[1])
            if u is not None and v is not None:
                matching_pairs.append((u, v))
        return matching_pairs

    def find_reachable_sets(self, M_pairs, equality_edges_str):
        J_eq = []
        for u_str, v_str in equality_edges_str:
            u = int(u_str.split("_")[1])
            v = int(v_str.split("_")[1])
            J_eq.append((u, v))

        M_set = set(M_pairs)
        adj = collections.defaultdict(list)
        for u, v in J_eq:
            if (u, v) in M_set:
                adj[self.n + v].append(u)
            else:
                adj[u].append(self.n + v)

        covered_rows = {r for r, c in M_pairs}
        start_nodes = [r for r in range(self.n) if r not in covered_rows]

        visited = set(start_nodes)
        queue = collections.deque(start_nodes)
        while queue:
            curr = queue.popleft()
            for neighbor in adj[curr]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        I_star = {x for x in visited if x < self.n}
        J_star = {x - self.n for x in visited if x >= self.n}
        return I_star, J_star

    def solve(self):
        print("Матрица стоимостей C:")
        print(self.C)
        print()
        while True:
            self.iteration_count += 1
            print(f"\nИТЕРАЦИЯ {self.iteration_count}")
            print(f"Alpha: {self.alpha}")
            print(f"Beta:  {self.beta}")
            eq_edges = self.get_equality_graph_edges()
            V1_labels = [f"u_{i}" for i in range(self.n)]
            V2_labels = [f"v_{j}" for j in range(self.n)]
            matching_sets = Bipartite(V1_labels, V2_labels, eq_edges).solve()
            M = self.parse_matching(matching_sets)
            print(f"Найдено паросочетание (размер {len(M)}): {sorted(M)}")
            if len(M) == self.n:
                print("\nРЕШЕНИЕ НАЙДЕНО")
                total_cost = 0
                res_matrix = np.zeros_like(self.C, dtype=int)
                
                print("Выбранные элементы:")
                for i, j in M:
                    res_matrix[i][j] = 1
                    val = self.C[i][j]
                    total_cost += val
                    print(f"Строка {i+1}, Столбец {j+1} (стоимость {val})")
                print(res_matrix)
                print(f"\nМинимальная сумма: {total_cost}")
                return M, total_cost

            I_star, J_star = self.find_reachable_sets(M, eq_edges)
            
            print(f"I* (строки): {[i for i in sorted(list(I_star))]}")
            print(f"J* (столбцы): {[j for j in sorted(list(J_star))]}")

            min_theta = float('inf')
            for i in range(self.n):
                for j in range(self.n):
                    if (i in I_star) and (j not in J_star):
                        val = (self.C[i][j] - self.alpha[i] - self.beta[j]) / 2.0
                        if val < min_theta:
                            min_theta = val
            print(f"Theta = {min_theta}")

            for i in range(self.n):
                if i in I_star:
                    self.alpha[i] += min_theta
                else:
                    self.alpha[i] -= min_theta
            for j in range(self.n):
                if j in J_star:
                    self.beta[j] -= min_theta
                else:
                    self.beta[j] += min_theta

if __name__ == "__main__":
    matrix = [
        [7, 2, 1, 9, 4],
        [9, 6, 9, 5, 5],
        [3, 8, 3, 1, 8],
        [7, 9, 4, 2, 2],
        [8, 4, 7, 4, 8]
    ]

    HungarianSolver(matrix).solve()