"""
Knapsack - Step 4: Compare Brute Force vs Dynamic Programming vs QAOA
"""
import json
import matplotlib.pyplot as plt

with open('/home/claude/project/code/_knapsack_bruteforce_result.json') as f:
    bf = json.load(f)
with open('/home/claude/project/code/_knapsack_dp_result.json') as f:
    dp = json.load(f)
with open('/home/claude/project/code/_knapsack_qaoa_result.json') as f:
    qa = json.load(f)

print("=" * 80)
print("KNAPSACK — FINAL COMPARISON  (capacity = 8 kg)")
print("=" * 80)
print(f"{'Method':<22}{'Value (Rs.)':<14}{'Weight (kg)':<14}{'Time (ms)':<14}{'Optimal?'}")
print("-" * 80)
print(f"{'Brute Force':<22}{bf['value']:<14}{bf['weight']:<14}{bf['time_ms']:<14.4f}{'Yes'}")
print(f"{'Dynamic Programming':<22}{dp['value']:<14}{dp['weight']:<14}{dp['time_ms']:<14.4f}{'Yes'}")
print(f"{'QAOA (quantum)':<22}{qa['qaoa_value']:<14}{qa['qaoa_weight']:<14}{qa['qaoa_time_ms']:<14.4f}{'Yes' if qa['qaoa_valid'] else 'No'}")
print("=" * 80)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))

methods = ['Brute\nForce', 'Dynamic\nProgramming', 'QAOA\n(Quantum)']
times = [bf['time_ms'], dp['time_ms'], qa['qaoa_time_ms']]
values = [bf['value'], dp['value'], qa['qaoa_value']]
colors = ['#4C72B0', '#55A868', '#CC7A00']

axes[0].bar(methods, times, color=colors, edgecolor='black')
axes[0].set_yscale('log')
axes[0].set_ylabel('Execution time (ms, log scale)')
axes[0].set_title('Knapsack: Execution Time Comparison')
for i, t in enumerate(times):
    axes[0].text(i, t * 1.15, f"{t:.2f}", ha='center', fontsize=9)

axes[1].bar(methods, values, color=colors, edgecolor='black')
axes[1].set_ylabel('Value achieved (Rs.)')
axes[1].set_title('Knapsack: Solution Quality Comparison')
axes[1].set_ylim(0, max(values) * 1.2)
for i, v in enumerate(values):
    axes[1].text(i, v + 100, f"Rs.{v}", ha='center', fontsize=9)

plt.tight_layout()
plt.savefig('/home/claude/project/images/05_knapsack_comparison.png', dpi=150)
print("\nSaved: 05_knapsack_comparison.png")
