"""
Knapsack - Step 3: Quantum Formulation with QAOA (Qiskit)

Pipeline:  Knapsack -> Binary Variables -> QUBO -> QAOA -> Solution

Each item gets one binary decision variable x_i (0 = leave out, 1 = take).
The weight constraint is folded into the objective as a penalty term, turning
the constrained problem into an unconstrained QUBO that QAOA can optimize.
"""
import time
import json
import numpy as np
import matplotlib.pyplot as plt

from qiskit_optimization.applications import Knapsack
from qiskit_algorithms import QAOA, NumPyMinimumEigensolver
from qiskit_algorithms.optimizers import COBYLA
from qiskit_algorithms.utils import algorithm_globals
from qiskit.primitives import StatevectorSampler as Sampler
from qiskit_optimization.algorithms import MinimumEigenOptimizer

algorithm_globals.random_seed = 42
np.random.seed(42)

items = [
    ("Laptop", 4, 3000),
    ("Phone", 2, 2000),
    ("Camera", 3, 2500),
    ("Book", 5, 500),
    ("Headphones", 2, 1000),
]
capacity = 8

names = [i[0] for i in items]
weights = [i[1] for i in items]
values = [i[2] for i in items]

knapsack = Knapsack(values=values, weights=weights, max_weight=capacity)
qp = knapsack.to_quadratic_program()
print("=== QUADRATIC PROGRAM (QUBO formulation) ===")
print(qp.prettyprint())

# ---- Exact solver (ground truth via eigensolver, same result DP gives) -----
t0 = time.perf_counter()
exact = MinimumEigenOptimizer(NumPyMinimumEigensolver())
exact_result = exact.solve(qp)
t1 = time.perf_counter()
exact_items = [names[i] for i in knapsack.interpret(exact_result)]
exact_value = sum(values[names.index(x)] for x in exact_items)
exact_weight = sum(weights[names.index(x)] for x in exact_items)
print("\n=== EXACT (classical eigensolver, ground truth) ===")
print(f"Items  : {exact_items}")
print(f"Weight : {exact_weight} kg  |  Value : Rs. {exact_value}")
print(f"Time   : {(t1-t0)*1000:.2f} ms")

# ---- QAOA (quantum-hybrid solver) -------------------------------------------
sampler = Sampler()
optimizer = COBYLA(maxiter=300)
qaoa_mes = QAOA(sampler=sampler, optimizer=optimizer, reps=3)
qaoa = MinimumEigenOptimizer(qaoa_mes)

t2 = time.perf_counter()
qaoa_result = qaoa.solve(qp)
t3 = time.perf_counter()

qaoa_items = [names[i] for i in knapsack.interpret(qaoa_result)]
qaoa_weight = sum(weights[names.index(x)] for x in qaoa_items)
qaoa_value = sum(values[names.index(x)] for x in qaoa_items)
qaoa_valid = qaoa_weight <= capacity

print("\n=== QAOA (quantum-hybrid solver) ===")
print(f"Items  : {qaoa_items}")
print(f"Weight : {qaoa_weight} kg  |  Value : Rs. {qaoa_value}")
print(f"Within capacity? : {'Yes' if qaoa_valid else 'No -> INFEASIBLE'}")
print(f"Time   : {(t3-t2)*1000:.2f} ms")

with open('/home/claude/project/code/_knapsack_qaoa_result.json', 'w') as f:
    json.dump({
        "exact_items": exact_items, "exact_value": exact_value, "exact_weight": exact_weight,
        "exact_time_ms": (t1 - t0) * 1000,
        "qaoa_items": qaoa_items, "qaoa_value": qaoa_value, "qaoa_weight": qaoa_weight,
        "qaoa_valid": qaoa_valid, "qaoa_time_ms": (t3 - t2) * 1000,
        "num_qubits": qp.get_num_binary_vars(),
    }, f, indent=2)

# ---- Visualization: items chosen by each method -----------------------------
fig, axes = plt.subplots(1, 3, figsize=(15, 5))

with open('/home/claude/project/code/_knapsack_bruteforce_result.json') as f:
    bf = json.load(f)
with open('/home/claude/project/code/_knapsack_dp_result.json') as f:
    dp = json.load(f)

datasets = [
    (bf['items'], bf['weight'], bf['value'], "Brute Force", "#4C72B0"),
    (dp['items'], dp['weight'], dp['value'], "Dynamic Programming", "#55A868"),
    (qaoa_items, qaoa_weight, qaoa_value, "QAOA (Quantum)", "#C44E52" if not qaoa_valid else "#CC7A00"),
]

for ax, (chosen, w, v, title, color) in zip(axes, datasets):
    all_items = names
    bar_colors = [color if item in chosen else '#DDDDDD' for item in all_items]
    ax.bar(all_items, [values[names.index(i)] for i in all_items], color=bar_colors, edgecolor='black')
    ax.set_title(f"{title}\nWeight={w}kg  Value=Rs.{v}" + ("" if title != "QAOA (Quantum)" or qaoa_valid else "  [INFEASIBLE]"))
    ax.set_ylabel("Item value (Rs.)")
    ax.tick_params(axis='x', rotation=30)

plt.suptitle(f"Knapsack (capacity = {capacity} kg): items selected by each method (highlighted = selected)", fontsize=12)
plt.tight_layout()
plt.savefig('/home/claude/project/images/04_knapsack_selection.png', dpi=150)
print("\nSaved: 04_knapsack_selection.png")
