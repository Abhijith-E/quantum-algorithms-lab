"""
Knapsack - Step 1: Brute Force Solution
Try every subset of items, keep the best one that fits the weight capacity.
"""
import time
from itertools import combinations

items = [
    ("Laptop", 4, 3000),
    ("Phone", 2, 2000),
    ("Camera", 3, 2500),
    ("Book", 5, 500),
    ("Headphones", 2, 1000),
]

capacity = 8  # kg

def brute_force_knapsack(items, capacity):
    best_value = 0
    best_items = []
    subsets_checked = 0

    for r in range(1, len(items) + 1):
        for combo in combinations(items, r):
            subsets_checked += 1
            weight = sum(i[1] for i in combo)
            value = sum(i[2] for i in combo)
            if weight <= capacity and value > best_value:
                best_value = value
                best_items = combo

    return best_items, best_value, subsets_checked

t0 = time.perf_counter()
best_items, best_value, subsets_checked = brute_force_knapsack(items, capacity)
t1 = time.perf_counter()

print("=== BRUTE FORCE KNAPSACK RESULT ===")
print(f"Capacity           : {capacity} kg")
print(f"Subsets evaluated   : {subsets_checked} (2^{len(items)} - 1 = {2**len(items) - 1})")
print(f"Best items          : {[i[0] for i in best_items]}")
print(f"Total weight         : {sum(i[1] for i in best_items)} kg")
print(f"Total value (Rs.)    : {best_value}")
print(f"Time taken           : {(t1 - t0)*1000:.4f} ms")

print("\n=== WHY BRUTE FORCE DOESN'T SCALE ===")
for n in [5, 10, 15, 20, 25, 30, 40]:
    print(f"{n:2d} items -> {2**n - 1:,} subsets to check")

import json
with open('/home/claude/project/code/_knapsack_bruteforce_result.json', 'w') as f:
    json.dump({
        "items": [i[0] for i in best_items],
        "weight": sum(i[1] for i in best_items),
        "value": best_value,
        "time_ms": (t1 - t0) * 1000,
        "subsets_checked": subsets_checked
    }, f, indent=2)
