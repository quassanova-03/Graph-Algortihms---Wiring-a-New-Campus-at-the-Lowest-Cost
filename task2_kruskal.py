
import csv
import math
import heapq
import random
import time
import os

# --------------------------------
# 1. Read building coordinates
# --------------------------------

buildings = []

with open("data/buildings.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        name = row["building"].strip()
        latitude = float(row["latitude"])
        longitude = float(row["longitude"])
        buildings.append((name, latitude, longitude))


# --------------------------------
# 2. Calculate geographical distance
# --------------------------------

def distance(a, b):
    lat1 = math.radians(a[1])
    lon1 = math.radians(a[2])
    lat2 = math.radians(b[1])
    lon2 = math.radians(b[2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    x = (math.sin(dlat / 2) ** 2
         + math.cos(lat1) * math.cos(lat2)
         * math.sin(dlon / 2) ** 2)

    return 6371000 * 2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))


# --------------------------------
# 3. Build the campus graph
# --------------------------------

n = len(buildings)
edges = []

for i in range(n):
    for j in range(i + 1, n):
        w = distance(buildings[i], buildings[j])
        edges.append((w, i, j))


# --------------------------------
# 4. Disjoint Set Union (Union-Find)
# --------------------------------

class DSU:

    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])

        return self.parent[x]

    def union(self, a, b):
        root_a = self.find(a)
        root_b = self.find(b)

        if root_a == root_b:
            return False

        if self.rank[root_a] < self.rank[root_b]:
            self.parent[root_a] = root_b

        elif self.rank[root_a] > self.rank[root_b]:
            self.parent[root_b] = root_a

        else:
            self.parent[root_b] = root_a
            self.rank[root_a] += 1

        return True


# --------------------------------
# 5. Kruskal's Algorithm
# --------------------------------

def kruskal(vertices, edges):

    sorted_edges = sorted(edges)
    dsu = DSU(vertices)

    mst = []
    total_cost = 0

    for weight, u, v in sorted_edges:

        if dsu.union(u, v):
            mst.append((u, v, weight))
            total_cost += weight

        if len(mst) == vertices - 1:
            break

    if len(mst) != vertices - 1:
        raise ValueError("Graph is disconnected.")

    return mst, total_cost


# --------------------------------
# 6. Prim's Algorithm for comparison
# --------------------------------

def prim(vertices, edges):

    graph = [[] for _ in range(vertices)]

    for weight, u, v in edges:
        graph[u].append((weight, v))
        graph[v].append((weight, u))

    visited = [False] * vertices
    visited[0] = True

    heap = []

    for weight, v in graph[0]:
        heapq.heappush(heap, (weight, 0, v))

    mst = []
    total_cost = 0

    while heap and len(mst) < vertices - 1:

        weight, u, v = heapq.heappop(heap)

        if visited[v]:
            continue

        visited[v] = True
        mst.append((u, v, weight))
        total_cost += weight

        for next_weight, neighbour in graph[v]:
            if not visited[neighbour]:
                heapq.heappush(
                    heap, (next_weight, v, neighbour)
                )

    if len(mst) != vertices - 1:
        raise ValueError("Graph is disconnected.")

    return mst, total_cost


# --------------------------------
# 7. Run both algorithms on campus data
# --------------------------------

kruskal_mst, kruskal_cost = kruskal(n, edges)
prim_mst, prim_cost = prim(n, edges)

print("\nCAMPUS MST RESULTS")
print("---------------------------")
print("Number of buildings:", n)
print("Number of Kruskal edges:", len(kruskal_mst))
print("Kruskal total cost:", round(kruskal_cost, 2), "metres")
print("Prim total cost:", round(prim_cost, 2), "metres")

if math.isclose(kruskal_cost, prim_cost, rel_tol=1e-9):
    print("Verification: Both algorithms give the same MST cost.")
else:
    print("Verification failed!")


# Compare with the saved Task 1 result
if os.path.exists("outputs/mst_edges.csv"):

    with open("outputs/mst_edges.csv", "r") as file:
        reader = csv.DictReader(file)
        task1_cost = sum(float(row["distance_m"]) for row in reader)

    print("Saved Task 1 cost:", round(task1_cost, 2), "metres")
    print("Difference from Task 2:",
          round(abs(task1_cost - kruskal_cost), 2), "metres")


# Save Kruskal MST edges
os.makedirs("outputs", exist_ok=True)

with open("outputs/kruskal_mst_edges.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["source_building", "destination_building", "distance_m"])

    for u, v, weight in kruskal_mst:
        writer.writerow([
            buildings[u][0],
            buildings[v][0],
            round(weight, 2)
        ])


# --------------------------------
# 8. Create sparse and dense graphs
# --------------------------------

def random_graph(vertices, dense=False):

    graph_edges = []
    random.seed(10)

    # First connect all vertices using a chain
    for i in range(vertices - 1):
        weight = random.randint(1, 1000)
        graph_edges.append((weight, i, i + 1))

    if dense:
        # Add all remaining edges
        for i in range(vertices):
            for j in range(i + 1, vertices):
                if j != i + 1:
                    weight = random.randint(1, 1000)
                    graph_edges.append((weight, i, j))

    else:
        # Add extra edges to make the graph sparse
        while len(graph_edges) < 2 * vertices:
            u = random.randint(0, vertices - 1)
            v = random.randint(0, vertices - 1)

            if u != v:
                edge = (min(u, v), max(u, v))

                existing = [(a, b) for w, a, b in graph_edges]

                if edge not in existing:
                    weight = random.randint(1, 1000)
                    graph_edges.append((weight, edge[0], edge[1]))

    return graph_edges


# --------------------------------
# 9. Compare execution times
# --------------------------------

def benchmark(vertices, graph_edges):

    start = time.perf_counter()
    kruskal(vertices, graph_edges)
    kruskal_time = time.perf_counter() - start

    start = time.perf_counter()
    prim(vertices, graph_edges)
    prim_time = time.perf_counter() - start

    return kruskal_time, prim_time


print("\nEXECUTION TIME COMPARISON")
print("---------------------------")

results = []

for graph_type in ["Sparse", "Dense"]:

    is_dense = graph_type == "Dense"
    test_edges = random_graph(100, is_dense)

    k_time, p_time = benchmark(100, test_edges)

    print("\nGraph type:", graph_type)
    print("Number of vertices: 100")
    print("Number of edges:", len(test_edges))
    print("Kruskal time:", round(k_time, 6), "seconds")
    print("Prim time:", round(p_time, 6), "seconds")

    results.append([
        graph_type,
        100,
        len(test_edges),
        k_time,
        p_time
    ])


# --------------------------------
# 10. Save benchmark results
# --------------------------------

with open("outputs/task2_benchmark.csv", "w", newline="") as file:
    writer = csv.writer(file)

    writer.writerow([
        "Graph Type",
        "Vertices",
        "Edges",
        "Kruskal Time (seconds)",
        "Prim Time (seconds)"
    ])

    writer.writerows(results)


print("\nTASK 2 COMPLETED!")
print("Kruskal MST saved in outputs/kruskal_mst_edges.csv")
print("Benchmark saved in outputs/task2_benchmark.csv")
