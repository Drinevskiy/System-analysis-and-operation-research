from typing import List, Tuple

def bag_solver(
    items: List[Tuple[int, int]], 
    capacity: int
) -> Tuple[int, List[Tuple[int, Tuple[int, int]]], List[List[int]], List[List[int]]]:
    n = len(items)
    opt = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]
    x = [[0 for _ in range(capacity + 1)] for _ in range(n + 1)]

    for k in range(1, n + 1):
        volume, value = items[k - 1]
        for b in range(1, capacity + 1):
            opt[k][b] = opt[k - 1][b]
            x[k][b] = 0
            if volume <= b:
                picked_value = opt[k - 1][b - volume] + value
                if picked_value > opt[k - 1][b]:
                    opt[k][b] = picked_value
                    x[k][b] = 1

    max_value = opt[n][capacity]

    selected_items = []
    rest_capacity = capacity
    for k in range(n, 0, -1):
        if x[k][rest_capacity] == 1:
            item_data = items[k - 1]
            selected_items.append((k - 1, item_data))
            rest_capacity -= item_data[0]
    
    selected_items.reverse()

    return max_value, selected_items, opt, x

def print_matrix(matrix: List[List[int]], name: str):
    print(f"\n{name}:")
    header = "k\\b  " + " ".join(f"{i: >3}" for i in range(len(matrix[0])))
    print(header)
    print("-" * len(header))
    for i, row in enumerate(matrix):
        print(f"{i: >2} | " + " ".join(f"{cell: >3}" for cell in row))

if __name__ == "__main__":
    items_to_pack = [
        (1, 2),  
        (2, 2),   
        (3, 1),  
        (3, 2), 
    ]
    backpack_capacity = 6

    total_value, packed_items, opt_matrix, x_matrix = bag_solver(items_to_pack, backpack_capacity)
    
    print_matrix(opt_matrix, "Матрица OPT")
    print_matrix(x_matrix, "Матрица X")

    print(f"\nМаксимальная суммарная ценность: {total_value}")
    print("Предметы, которые нужно положить в рюкзак:")
    for index, item_data in packed_items:
        print(f"  - Предмет {index + 1}: {item_data}")