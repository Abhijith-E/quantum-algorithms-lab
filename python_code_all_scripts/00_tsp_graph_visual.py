"""
TSP - Step 1: Visualize the problem as a graph
Amazon delivery truck must visit 5 Karnataka cities exactly once and return home.
"""
import networkx as nx
import matplotlib.pyplot as plt

cities = ['Bangalore', 'Mysore', 'Mangalore', 'Hubli', 'Belgaum']

# Approximate road distances (km) between city pairs
distance = {
    ('Bangalore', 'Mysore'): 145,
    ('Bangalore', 'Mangalore'): 352,
    ('Bangalore', 'Hubli'): 410,
    ('Bangalore', 'Belgaum'): 502,
    ('Mysore', 'Mangalore'): 252,
    ('Mysore', 'Hubli'): 372,
    ('Mysore', 'Belgaum'): 462,
    ('Mangalore', 'Hubli'): 235,
    ('Mangalore', 'Belgaum'): 315,
    ('Hubli', 'Belgaum'): 100,
}

G = nx.Graph()
G.add_nodes_from(cities)
for (a, b), d in distance.items():
    G.add_edge(a, b, weight=d)

pos = {
    'Bangalore': (2.0, 0.0),
    'Mysore': (1.2, -0.8),
    'Mangalore': (0.0, -0.4),
    'Hubli': (0.3, 1.3),
    'Belgaum': (1.4, 1.7),
}

plt.figure(figsize=(8, 6))
nx.draw_networkx_nodes(G, pos, node_size=2600, node_color='#FF9933', edgecolors='black', linewidths=1.5)
nx.draw_networkx_labels(G, pos, font_size=10, font_weight='bold')
nx.draw_networkx_edges(G, pos, width=1.5, edge_color='gray', alpha=0.7)
edge_labels = {(a, b): f"{d} km" for (a, b), d in distance.items()}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)

plt.title("Travelling Salesman Problem\nAmazon delivery truck – 5 Karnataka cities (complete graph, K5)", fontsize=12)
plt.axis('off')
plt.tight_layout()
plt.savefig('/home/claude/project/images/01_tsp_graph.png', dpi=150)
print("Saved: 01_tsp_graph.png")

n = len(cities)
import math
total_routes = math.factorial(n - 1) // 2  # fixing start city, routes undirected
print(f"\nNumber of cities: {n}")
print(f"Total possible distinct routes (undirected, fixed start): {total_routes}")
print(f"Total permutations before removing symmetry: {math.factorial(n)}")
