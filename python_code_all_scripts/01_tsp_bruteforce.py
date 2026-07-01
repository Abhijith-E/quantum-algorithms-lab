"""
TSP - Step 2: Brute Force Solution
Generate EVERY possible route -> calculate distance -> choose minimum.
"""
import itertools
import time

cities = ['Bangalore', 'Mysore', 'Mangalore', 'Hubli', 'Belgaum']

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

def get_distance(a, b):
    if a == b:
        return 0
    return distance.get((a, b), distance.get((b, a)))

def brute_force_tsp(cities):
    start = cities[0]
    remaining = cities[1:]

    best_route = None
    best_cost = float("inf")
    routes_checked = 0

    for perm in itertools.permutations(remaining):
        route = (start,) + perm
        total = 0
        for i in range(len(route) - 1):
            total += get_distance(route[i], route[i + 1])
        total += get_distance(route[-1], route[0])  # return to start
        routes_checked += 1

        if total < best_cost:
            best_cost = total
            best_route = route

    return best_route, best_cost, routes_checked

t0 = time.perf_counter()
best_route, best_cost, routes_checked = brute_force_tsp(cities)
t1 = time.perf_counter()

print("=== BRUTE FORCE TSP RESULT ===")
print(f"Routes evaluated : {routes_checked}")
print(f"Best route       : {' -> '.join(best_route)} -> {best_route[0]}")
print(f"Best distance    : {best_cost} km")
print(f"Time taken       : {(t1 - t0)*1000:.4f} ms")

# Scaling illustration (why brute force breaks down)
import math
print("\n=== WHY BRUTE FORCE DOESN'T SCALE ===")
for n in [4, 6, 8, 10, 12, 15, 20]:
    routes = math.factorial(n - 1) // 2
    print(f"{n:2d} cities -> {routes:,} distinct routes to check")

# Save results for later comparison
import json
with open('/home/claude/project/code/_tsp_bruteforce_result.json', 'w') as f:
    json.dump({
        "route": list(best_route),
        "cost": best_cost,
        "time_ms": (t1 - t0) * 1000,
        "routes_checked": routes_checked
    }, f, indent=2)
