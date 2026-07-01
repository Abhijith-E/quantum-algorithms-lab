"""
TSP - Step 5: Compare Brute Force vs Nearest Neighbor vs QAOA
"""
import json
import matplotlib.pyplot as plt

with open('/home/claude/project/code/_tsp_bruteforce_result.json') as f:
    bf = json.load(f)
with open('/home/claude/project/code/_tsp_nn_result.json') as f:
    nn = json.load(f)
with open('/home/claude/project/code/_tsp_qaoa_result.json') as f:
    qa = json.load(f)

print("=" * 78)
print("TSP — FINAL COMPARISON")
print("=" * 78)
print(f"{'Method':<20}{'Scope':<22}{'Cost (km)':<14}{'Time (ms)':<14}{'Optimal?'}")
print("-" * 78)
print(f"{'Brute Force':<20}{'5 cities':<22}{bf['cost']:<14}{bf['time_ms']:<14.3f}{'Yes'}")
print(f"{'Nearest Neighbor':<20}{'5 cities':<22}{nn['cost']:<14}{nn['time_ms']:<14.3f}{'No (heuristic)'}")
print(f"{'Exact (eigensolver)':<20}{'4 cities (subset)':<22}{qa['exact_cost']:<14.1f}{qa['exact_time_ms']:<14.3f}{'Yes'}")
qaoa_cost_str = f"{qa['qaoa_cost']:.1f}" if qa['qaoa_valid'] else "N/A (invalid)"
print(f"{'QAOA (quantum)':<20}{'4 cities (subset)':<22}{qaoa_cost_str:<14}{qa['qaoa_time_ms']:<14.3f}{'Approximate'}")
print("=" * 78)

# Bar chart: execution time comparison (log scale, since they differ by orders of magnitude)
fig, axes = plt.subplots(1, 2, figsize=(12, 5))

methods = ['Brute\nForce\n(5 cities)', 'Nearest\nNeighbor\n(5 cities)', 'Exact\nEigensolver\n(4 cities)', 'QAOA\n(4 cities,\n16 qubits)']
times = [bf['time_ms'], nn['time_ms'], qa['exact_time_ms'], qa['qaoa_time_ms']]
colors = ['#4C72B0', '#55A868', '#8172B2', '#C44E52']

axes[0].bar(methods, times, color=colors, edgecolor='black')
axes[0].set_yscale('log')
axes[0].set_ylabel('Execution time (ms, log scale)')
axes[0].set_title('TSP: Execution Time Comparison')
for i, t in enumerate(times):
    axes[0].text(i, t * 1.15, f"{t:.1f}", ha='center', fontsize=9)

# Scaling chart: how brute force explodes vs a heuristic that stays linear-ish
import math
ns = list(range(4, 15))
bf_routes = [math.factorial(k - 1) // 2 for k in ns]
axes[1].plot(ns, bf_routes, marker='o', color='#C44E52', label='Brute Force (routes to check)')
axes[1].set_yscale('log')
axes[1].set_xlabel('Number of cities')
axes[1].set_ylabel('Routes to evaluate (log scale)')
axes[1].set_title('Why Brute Force Doesn\'t Scale')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('/home/claude/project/images/03_tsp_comparison.png', dpi=150)
print("\nSaved: 03_tsp_comparison.png")
