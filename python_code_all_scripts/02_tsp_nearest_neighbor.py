"""
TSP - Step 3: Nearest Neighbor Heuristic (Better Classical Algorithm)
Greedy approach: always go to the closest unvisited city.
Much faster than brute force but not guaranteed to be optimal.
"""
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

def nearest_neighbor_tsp(cities, start=None):
    start = start or cities[0]
    unvisited = set(cities)
    unvisited.remove(start)
    route = [start]
    current = start
    total_cost = 0

    while unvisited:
        nearest_city = min(unvisited, key=lambda city: get_distance(current, city))
        total_cost += get_distance(current, nearest_city)
        route.append(nearest_city)
        unvisited.remove(nearest_city)
        current = nearest_city

    total_cost += get_distance(current, start)  # return to start
    return route, total_cost

t0 = time.perf_counter()
nn_route, nn_cost = nearest_neighbor_tsp(cities)
t1 = time.perf_counter()

print("=== NEAREST NEIGHBOR TSP RESULT ===")
print(f"Route     : {' -> '.join(nn_route)} -> {nn_route[0]}")
print(f"Distance  : {nn_cost} km")
print(f"Time      : {(t1 - t0)*1000:.4f} ms")

# Compare against brute force optimal
import json
with open('/home/claude/project/code/_tsp_bruteforce_result.json') as f:
    bf = json.load(f)

gap = nn_cost - bf['cost']
gap_pct = (gap / bf['cost']) * 100

print("\n=== COMPARISON: BRUTE FORCE (OPTIMAL) vs NEAREST NEIGHBOR (HEURISTIC) ===")
print(f"{'Method':<20}{'Route Cost (km)':<18}{'Time (ms)':<12}")
print(f"{'Brute Force':<20}{bf['cost']:<18}{bf['time_ms']:<12.4f}")
print(f"{'Nearest Neighbor':<20}{nn_cost:<18}{(t1-t0)*1000:<12.4f}")
print(f"\nOptimality gap: {gap} km ({gap_pct:.1f}% worse than optimal)")

with open('/home/claude/project/code/_tsp_nn_result.json', 'w') as f:
    json.dump({"route": nn_route, "cost": nn_cost, "time_ms": (t1 - t0) * 1000}, f, indent=2)
