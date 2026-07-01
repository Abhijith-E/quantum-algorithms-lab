"""
TSP - Step 4: Quantum Formulation with QAOA (Qiskit)

Pipeline:  TSP -> Graph -> QUBO -> Ising Hamiltonian -> QAOA -> Optimal Route

QAOA is a hybrid quantum-classical algorithm:
  - The quantum computer prepares candidate solutions using a parameterized circuit.
  - A classical optimizer updates the circuit parameters to minimize the cost Hamiltonian.

NOTE: Because QAOA is simulated on a classical computer here (no real QPU access),
this is a full noiseless simulation useful for teaching the workflow. Even 4-5 city
TSP already needs many qubits (n^2 qubits for n cities using this encoding), so we
use a SMALL 4-city sub-problem for the live QAOA demo, and clearly explain why.
"""
import time
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt

from qiskit_optimization.applications import Tsp
from qiskit_optimization.converters import QuadraticProgramToQubo
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals
from qiskit.primitives import StatevectorSampler as Sampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer

algorithm_globals.random_seed = 42
np.random.seed(42)

# ---- Use a 4-city subset for the live QAOA demo -----------------------------
# n cities -> n^2 qubits under the standard QUBO encoding.
# 4 cities = 16 qubits (already heavy for a laptop-simulated statevector demo).
cities = ['Bangalore', 'Mysore', 'Mangalore', 'Hubli']
distance = {
    ('Bangalore', 'Mysore'): 145,
    ('Bangalore', 'Mangalore'): 352,
    ('Bangalore', 'Hubli'): 410,
    ('Mysore', 'Mangalore'): 252,
    ('Mysore', 'Hubli'): 372,
    ('Mangalore', 'Hubli'): 235,
}
n = len(cities)
idx = {c: i for i, c in enumerate(cities)}
dist_matrix = np.zeros((n, n))
for (a, b), d in distance.items():
    dist_matrix[idx[a]][idx[b]] = d
    dist_matrix[idx[b]][idx[a]] = d

print(f"Using {n} cities for the live QAOA demo -> {n*n} qubits under standard TSP QUBO encoding")
print("(Full 5-city problem is used for classical brute force / nearest neighbor;")
print(" QAOA demo is scaled down to keep the quantum simulation fast in-class.)\n")

# ---- Build the TSP application and convert to QUBO / Ising ------------------
tsp = Tsp(nx.from_numpy_array(dist_matrix))
qp = tsp.to_quadratic_program()

qubo_converter = QuadraticProgramToQubo()
qubo = qubo_converter.convert(qp)
qubitOp, offset = qubo.to_ising()

print(f"QUBO variables (qubits required): {qubo.get_num_binary_vars()}")
print(f"Ising Hamiltonian terms: {len(qubitOp)}")

# ---- Classical exact solver for ground truth (small enough to brute force) --
t0 = time.perf_counter()
exact = MinimumEigenOptimizer(NumPyMinimumEigensolver())
exact_result = exact.solve(qp)
t1 = time.perf_counter()
exact_route = tsp.interpret(exact_result)
exact_route_names = [cities[i] for i in exact_route]
exact_cost = tsp.tsp_value(exact_route, dist_matrix)
print("\n=== EXACT (classical eigensolver, ground truth) ===")
print(f"Route: {' -> '.join(exact_route_names)} -> {exact_route_names[0]}")
print(f"Cost : {exact_cost} km")
print(f"Time : {(t1-t0)*1000:.2f} ms")

# ---- QAOA (quantum hybrid solver) -------------------------------------------
sampler = Sampler()
optimizer = COBYLA(maxiter=500)
qaoa_mes = QAOA(sampler=sampler, optimizer=optimizer, reps=3)
qaoa = MinimumEigenOptimizer(qaoa_mes)

t2 = time.perf_counter()
qaoa_result = qaoa.solve(qp)
t3 = time.perf_counter()

try:
    qaoa_route = tsp.interpret(qaoa_result)
    qaoa_route_names = [cities[i] for i in qaoa_route]
    qaoa_cost = tsp.tsp_value(qaoa_route, dist_matrix)
    valid = True
except Exception as e:
    valid = False
    qaoa_route_names = None
    qaoa_cost = None

print("\n=== QAOA (quantum-hybrid solver) ===")
print(f"Raw objective value : {qaoa_result.fval}")
if valid:
    print(f"Route  : {' -> '.join(qaoa_route_names)} -> {qaoa_route_names[0]}")
    print(f"Cost   : {qaoa_cost} km")
else:
    print("QAOA returned an INVALID tour on this run (a common outcome with few reps/")
    print("iterations — this is exactly why QAOA result quality depends on circuit")
    print("depth (reps) and optimizer budget, and is an active research area.)")
print(f"Time   : {(t3-t2)*1000:.2f} ms")

# ---- Save comparison data -----------------------------------------------
import json
with open('/home/claude/project/code/_tsp_qaoa_result.json', 'w') as f:
    json.dump({
        "cities": cities,
        "exact_route": exact_route_names,
        "exact_cost": float(exact_cost),
        "exact_time_ms": (t1 - t0) * 1000,
        "qaoa_valid": valid,
        "qaoa_route": qaoa_route_names,
        "qaoa_cost": float(qaoa_cost) if valid else None,
        "qaoa_time_ms": (t3 - t2) * 1000,
        "num_qubits": qubo.get_num_binary_vars(),
    }, f, indent=2)

# ---- Visualize: exact route (left) + QAOA output analysis (right) ----------
pos = nx.spring_layout(nx.from_numpy_array(dist_matrix), seed=7)
fig, axes = plt.subplots(1, 2, figsize=(13, 5))

G_plot = nx.from_numpy_array(dist_matrix)
labels = {i: cities[i] for i in range(n)}

# Left panel: exact (ground-truth) route
ax = axes[0]
nx.draw_networkx_nodes(G_plot, pos, ax=ax, node_size=1800, node_color='#FFD580', edgecolors='black')
nx.draw_networkx_labels(G_plot, pos, labels, ax=ax, font_size=9, font_weight='bold')
nx.draw_networkx_edges(G_plot, pos, ax=ax, edge_color='lightgray', width=1)
route_edges = [(exact_route[i], exact_route[(i + 1) % len(exact_route)]) for i in range(len(exact_route))]
nx.draw_networkx_edges(G_plot, pos, edgelist=route_edges, ax=ax, edge_color="#2E8B57", width=3)
ax.set_title(f"Exact classical solution\n{' -> '.join(exact_route_names)}\nCost = {exact_cost} km", fontsize=10)
ax.axis('off')

# Right panel: QAOA outcome
ax = axes[1]
if valid:
    nx.draw_networkx_nodes(G_plot, pos, ax=ax, node_size=1800, node_color='#FFD580', edgecolors='black')
    nx.draw_networkx_labels(G_plot, pos, labels, ax=ax, font_size=9, font_weight='bold')
    nx.draw_networkx_edges(G_plot, pos, ax=ax, edge_color='lightgray', width=1)
    qaoa_edges = [(qaoa_route[i], qaoa_route[(i + 1) % len(qaoa_route)]) for i in range(len(qaoa_route))]
    nx.draw_networkx_edges(G_plot, pos, edgelist=qaoa_edges, ax=ax, edge_color="#CC5500", width=3)
    ax.set_title(f"QAOA solution\n{' -> '.join(qaoa_route_names)}\nCost = {qaoa_cost} km", fontsize=10)
    ax.axis('off')
else:
    ax.axis('off')
    ax.text(0.5, 0.60,
            "QAOA did not converge to a valid tour\non this run (16-qubit permutation encoding).",
            ha='center', va='center', fontsize=10, wrap=True)
    ax.text(0.5, 0.30,
            "Expected with few QAOA layers (reps) and a\nmodest optimizer budget on 16 qubits — the\nsearch often lands on an infeasible bitstring.\nDeeper circuits, more iterations, or real hardware\nimprove this. This is exactly why NISQ-era\noptimization is still an active research area.",
            ha='center', va='center', fontsize=9, color='#444444', wrap=True)
    ax.set_title("QAOA outcome (this run): infeasible tour", fontsize=10)

plt.suptitle("TSP (4-city subset): Exact classical solver vs QAOA quantum-hybrid solver", fontsize=12)
plt.tight_layout()
plt.savefig('/home/claude/project/images/02_tsp_qaoa_routes.png', dpi=150)
print("\nSaved: 02_tsp_qaoa_routes.png")
