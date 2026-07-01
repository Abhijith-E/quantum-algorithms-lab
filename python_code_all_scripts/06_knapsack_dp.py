"""
Knapsack - Step 2: Dynamic Programming Solution (Better Classical Algorithm)
Builds a table of best achievable value for every (item, weight) combination.
Much faster than brute force: O(n * capacity) instead of O(2^n).
"""
import time
import json

items = [
    ("Laptop", 4, 3000),
    ("Phone", 2, 2000),
    ("Camera", 3, 2500),
    ("Book", 5, 500),
    ("Headphones", 2, 1000),
]
capacity = 8

def dp_knapsack(items, capacity):
    n = len(items)
    # dp[i][w] = best value using first i items with capacity w
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]

    for i in range(1, n + 1):
        name, weight, value = items[i - 1]
        for w in range(capacity + 1):
            if weight <= w:
                dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weight] + value)
            else:
                dp[i][w] = dp[i - 1][w]

    # Backtrack to find which items were chosen
    chosen = []
    w = capacity
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            name, weight, value = items[i - 1]
            chosen.append(name)
            w -= weight

    chosen.reverse()
    return chosen, dp[n][capacity], dp

t0 = time.perf_counter()
chosen_items, best_value, dp_table = dp_knapsack(items, capacity)
t1 = time.perf_counter()

print("=== DYNAMIC PROGRAMMING KNAPSACK RESULT ===")
print(f"Capacity        : {capacity} kg")
print(f"Chosen items    : {chosen_items}")
weight_used = sum(w for n_, w, v in items if n_ in chosen_items)
print(f"Total weight    : {weight_used} kg")
print(f"Total value     : Rs. {best_value}")
print(f"Time taken      : {(t1 - t0)*1000:.4f} ms")
print(f"Table cells computed : {(len(items)+1) * (capacity+1)}  (vs {2**len(items)-1} subsets for brute force)")

with open('/home/claude/project/code/_knapsack_bruteforce_result.json') as f:
    bf = json.load(f)

print("\n=== COMPARISON: BRUTE FORCE vs DYNAMIC PROGRAMMING ===")
print(f"{'Method':<20}{'Value (Rs.)':<14}{'Time (ms)':<12}{'Work Done'}")
print(f"{'Brute Force':<20}{bf['value']:<14}{bf['time_ms']:<12.4f}{bf['subsets_checked']} subsets")
print(f"{'Dynamic Programming':<20}{best_value:<14}{(t1-t0)*1000:<12.4f}{(len(items)+1)*(capacity+1)} table cells")

with open('/home/claude/project/code/_knapsack_dp_result.json', 'w') as f:
    json.dump({
        "items": chosen_items,
        "weight": weight_used,
        "value": best_value,
        "time_ms": (t1 - t0) * 1000
    }, f, indent=2)
