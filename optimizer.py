import networkx as nx
import matplotlib.pyplot as plt
from scipy.optimize import linear_sum_assignment
import numpy as np

# ============================================================
# PART 1 — BUILD THE SUPPLY CHAIN GRAPH
# ============================================================

def build_graph():
    """
    Creates the main supply chain graph.
    Nodes: 'S' = Supplier, 'W' = Warehouse, 'H' = Hub, 'D' = Distribution Center, 'R' = Store
    """
    G = nx.DiGraph()  # Directed graph

    # Add nodes with a 'type' attribute - EXPANDED NETWORK
    [G.add_node(f"S{i}", type='supplier') for i in range(1, 7)]  # 6 suppliers
    [G.add_node(f"W{i}", type='warehouse') for i in range(1, 6)]  # 5 warehouses
    [G.add_node(f"D{i}", type='distribution') for i in range(1, 5)]  # 4 distribution centers
    [G.add_node(f"H{i}", type='hub') for i in range(1, 5)]  # 4 hubs
    [G.add_node(f"R{i}", type='store') for i in range(1, 11)]  # 10 stores

    # Add weighted edges (costs)
    # ===== Suppliers → Warehouses =====
    edges_s_w = [
        ("S1", "W1", 10), ("S1", "W2", 15), ("S1", "W3", 20),
        ("S2", "W1", 12), ("S2", "W2", 18), ("S2", "W3", 14), ("S2", "W4", 22),
        ("S3", "W2", 13), ("S3", "W3", 17), ("S3", "W4", 16), ("S3", "W5", 19),
        ("S4", "W1", 16), ("S4", "W3", 15), ("S4", "W5", 14),
        ("S5", "W2", 11), ("S5", "W4", 13), ("S5", "W5", 17),
        ("S6", "W1", 18), ("S6", "W3", 12), ("S6", "W4", 15), ("S6", "W5", 20)
    ]
    for s, w, cost in edges_s_w:
        G.add_edge(s, w, weight=cost)

    # ===== Warehouses → Distribution Centers =====
    edges_w_d = [
        ("W1", "D1", 5), ("W1", "D2", 7),
        ("W2", "D1", 6), ("W2", "D2", 5), ("W2", "D3", 8),
        ("W3", "D2", 6), ("W3", "D3", 5), ("W3", "D4", 7),
        ("W4", "D3", 6), ("W4", "D4", 5),
        ("W5", "D2", 9), ("W5", "D4", 6)
    ]
    for w, d, cost in edges_w_d:
        G.add_edge(w, d, weight=cost)

    # ===== Distribution Centers → Hubs =====
    edges_d_h = [
        ("D1", "H1", 4), ("D1", "H2", 6),
        ("D2", "H1", 5), ("D2", "H2", 4), ("D2", "H3", 7),
        ("D3", "H2", 5), ("D3", "H3", 4), ("D3", "H4", 6),
        ("D4", "H3", 5), ("D4", "H4", 4)
    ]
    for d, h, cost in edges_d_h:
        G.add_edge(d, h, weight=cost)

    # ===== Hubs → Stores =====
    edges_h_r = [
        ("H1", "R1", 8), ("H1", "R2", 6), ("H1", "R3", 10),
        ("H2", "R2", 7), ("H2", "R3", 5), ("H2", "R4", 9), ("H2", "R5", 11),
        ("H3", "R4", 6), ("H3", "R5", 8), ("H3", "R6", 7), ("H3", "R7", 10),
        ("H4", "R6", 9), ("H4", "R7", 7), ("H4", "R8", 8), ("H4", "R9", 11), ("H4", "R10", 12)
    ]
    for h, r, cost in edges_h_r:
        G.add_edge(h, r, weight=cost)

    # ===== Some direct routes for redundancy =====
    direct_routes = [
        ("W1", "H1", 15), ("W2", "H2", 18),
        ("D1", "R1", 20), ("D2", "R3", 22),
        ("W3", "R5", 28), ("W5", "H4", 16)
    ]
    for start, end, cost in direct_routes:
        G.add_edge(start, end, weight=cost)

    # ===== Cross-connections for redundancy =====
    cross_connections = [
        ("W1", "D3", 12), ("W4", "D1", 11),
        ("D1", "H3", 9), ("D4", "H1", 10),
        ("H1", "R5", 15), ("H2", "R7", 14), ("H3", "R2", 13)
    ]
    for start, end, cost in cross_connections:
        G.add_edge(start, end, weight=cost)

    return G


# ============================================================
# PART 2 — OPTIMAL SUPPLIER–WAREHOUSE ASSIGNMENT
# ============================================================

def find_optimal_assignment(G):
    """
    Uses the Hungarian algorithm to find the min-cost assignment
    of suppliers to warehouses.
    """
    suppliers = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'supplier'])
    warehouses = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'warehouse'])

    # Build cost matrix
    cost_matrix = np.zeros((len(suppliers), len(warehouses)))
    for i, s in enumerate(suppliers):
        for j, w in enumerate(warehouses):
            if G.has_edge(s, w):
                cost_matrix[i, j] = G[s][w]['weight']
            else:
                cost_matrix[i, j] = 999  # Large penalty if no direct path

    # Solve with Hungarian Algorithm
    row_ind, col_ind = linear_sum_assignment(cost_matrix)
    total_cost = cost_matrix[row_ind, col_ind].sum()
    assignments = [(suppliers[i], warehouses[j]) for i, j in zip(row_ind, col_ind)]

    return assignments, total_cost


# ============================================================
# PART 3 — SHORTEST PATH & REROUTING
# ============================================================

def find_shortest_path(G, start_node, end_node):
    """Finds the shortest path and cost using Dijkstra's algorithm."""
    try:
        path = nx.dijkstra_path(G, source=start_node, target=end_node, weight='weight')
        cost = nx.dijkstra_path_length(G, source=start_node, target=end_node, weight='weight')
        return path, cost
    except nx.NetworkXNoPath:
        return None, None


# ============================================================
# PART 4 — COLORING & LAYOUT FUNCTIONS
# ============================================================

def get_node_colors(G, path=None):
    """Returns node colors depending on node type and path."""
    if path is None:
        path = []
    colors = []
    for node in G.nodes():
        if node in path:
            colors.append('#ff6b6b')  # Path highlight - red
        elif G.nodes[node]['type'] == 'supplier':
            colors.append('#51cf66')  # Green
        elif G.nodes[node]['type'] == 'warehouse':
            colors.append('#4dabf7')  # Blue
        elif G.nodes[node]['type'] == 'distribution':
            colors.append('#ff922b')  # Orange
        elif G.nodes[node]['type'] == 'store':
            colors.append('#ffd43b')  # Yellow
        else:
            colors.append('#cc5de8')  # Hub = Purple
    return colors


def compute_semantic_positions(G):
    """
    Creates a layered layout:
    Suppliers → Warehouses → Distribution Centers → Hubs → Stores
    Prevents overlap and keeps visualization clean.
    """
    pos = {}
    suppliers = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'supplier'])
    warehouses = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'warehouse'])
    distributions = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'distribution'])
    hubs = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'hub'])
    stores = sorted([n for n, d in G.nodes(data=True) if d['type'] == 'store'])

    def spread(nodes, x_pos, y_gap=1.8):
        """Spread nodes vertically with enough spacing"""
        n = len(nodes)
        for i, node in enumerate(nodes):
            y = (i - (n - 1) / 2) * y_gap
            pos[node] = (x_pos, y)

    # Layer positions with good horizontal spacing
    spread(suppliers, x_pos=0, y_gap=2.0)
    spread(warehouses, x_pos=4, y_gap=2.2)
    spread(distributions, x_pos=8, y_gap=2.3)
    spread(hubs, x_pos=12, y_gap=2.5)
    spread(stores, x_pos=16, y_gap=1.6)

    return pos


def compute_label_positions(pos):
    """Offsets node labels slightly to avoid overlap with nodes."""
    label_pos = {node: (x, y + 0.35) for node, (x, y) in pos.items()}
    return label_pos


# ============================================================
# PART 5 — MAIN EXECUTION (TESTING)
# ============================================================

if __name__ == "__main__":
    G = build_graph()

    print("\n=== COMPLEX SUPPLY CHAIN NETWORK ===")
    print(f"Total Nodes: {G.number_of_nodes()}")
    print(f"Total Edges: {G.number_of_edges()}")
    
    suppliers = [n for n, d in G.nodes(data=True) if d['type'] == 'supplier']
    warehouses = [n for n, d in G.nodes(data=True) if d['type'] == 'warehouse']
    distributions = [n for n, d in G.nodes(data=True) if d['type'] == 'distribution']
    hubs = [n for n, d in G.nodes(data=True) if d['type'] == 'hub']
    stores = [n for n, d in G.nodes(data=True) if d['type'] == 'store']
    
    print(f"Suppliers: {len(suppliers)}, Warehouses: {len(warehouses)}, Distribution Centers: {len(distributions)}")
    print(f"Hubs: {len(hubs)}, Stores: {len(stores)}\n")

    print("--- Part 2: Optimal Assignment (Hungarian) ---")
    assignments, cost = find_optimal_assignment(G)
    print(f"Optimal Assignments: {assignments}")
    print(f"Total Assignment Cost: ${cost}\n")

    print("--- Part 3: Shortest Path (Dijkstra) ---")
    start, end = "S1", "R10"
    path, cost = find_shortest_path(G, start, end)
    if path:
        print(f"Shortest path from {start} to {end}: {' -> '.join(path)}")
        print(f"Cost: ${cost}\n")
    else:
        print(f"No path found from {start} to {end}\n")

    print("--- Part 4: Dynamic Rerouting ---")
    broken_node = "D2"
    print(f"Simulating failure of node: {broken_node}")

    G_broken = G.copy()
    G_broken.remove_node(broken_node)
    path_new, cost_new = find_shortest_path(G_broken, start, end)
    if path_new:
        print(f"New shortest path: {' -> '.join(path_new)} (Cost: ${cost_new})")
    else:
        print(f"No path found after failure of {broken_node}.")

    # ========================================================
    # Visualization (Non-overlapping version)
    # ========================================================

    pos = compute_semantic_positions(G)
    label_pos = compute_label_positions(pos)
    colors = get_node_colors(G, path)

    plt.figure(figsize=(18, 10))
    nx.draw(
        G, pos,
        with_labels=False,
        node_color=colors,
        node_size=1200,
        arrows=True,
        arrowsize=12,
        arrowstyle='->',
        connectionstyle="arc3,rad=0.08",
        edge_color='#888888',
        width=1.5,
        alpha=0.7
    )
    nx.draw_networkx_labels(G, label_pos, font_size=9, font_weight='bold')
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7)

    plt.title("Complex Supply Chain Network", fontsize=16, pad=20)
    plt.axis('off')
    plt.tight_layout()
    plt.show()