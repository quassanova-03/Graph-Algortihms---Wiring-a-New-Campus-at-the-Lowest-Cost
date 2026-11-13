
import csv
import math
import os

# --------------------------------
# 1. Read building coordinates
# --------------------------------

buildings = []

with open("data/buildings.csv", "r", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)

    for row in reader:
        buildings.append((
            row["building"].strip(),
            float(row["latitude"]),
            float(row["longitude"])
        ))

n = len(buildings)


# --------------------------------
# 2. Set network constraints
# --------------------------------

# These are example constraints.
# Change them to the building names required for your project.

mandatory_edge = (buildings[0][0], buildings[1][0])
forbidden_edge = (buildings[0][0], buildings[2][0])

MAX_DEGREE = 3


# --------------------------------
# 3. Calculate geographical distance
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

    return 6371000 * 2 * math.atan2(
        math.sqrt(x), math.sqrt(1 - x)
    )


# --------------------------------
# 4. Build weighted graph
# --------------------------------

edges = []

for i in range(n):
    for j in range(i + 1, n):

        weight = distance(buildings[i], buildings[j])
        edges.append((weight, i, j))


# --------------------------------
# 5. Find the normal MST for comparison
# --------------------------------

def find_mst(edges, n):

    parent = list(range(n))
    rank = [0] * n

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(a, b):

        root_a = find(a)
        root_b = find(b)

        if root_a == root_b:
            return False

        if rank[root_a] < rank[root_b]:
            parent[root_a] = root_b

        elif rank[root_a] > rank[root_b]:
            parent[root_b] = root_a

        else:
            parent[root_b] = root_a
            rank[root_a] += 1

        return True

    total = 0

    for weight, u, v in sorted(edges):

        if union(u, v):
            total += weight

    return total


normal_cost = find_mst(edges, n)


# --------------------------------
# 6. Create constrained MST
# --------------------------------

parent = list(range(n))
rank = [0] * n
degree = [0] * n

def find(x):

    if parent[x] != x:
        parent[x] = find(parent[x])

    return parent[x]


def union(a, b):

    root_a = find(a)
    root_b = find(b)

    if root_a == root_b:
        return False

    if rank[root_a] < rank[root_b]:
        parent[root_a] = root_b

    elif rank[root_a] > rank[root_b]:
        parent[root_b] = root_a

    else:
        parent[root_b] = root_a
        rank[root_a] += 1

    return True


# Find the indices of the mandatory and forbidden buildings

name_to_index = {
    building[0]: i for i, building in enumerate(buildings)
}

if mandatory_edge[0] not in name_to_index or mandatory_edge[1] not in name_to_index:
    raise ValueError("Mandatory edge contains an unknown building.")

if forbidden_edge[0] not in name_to_index or forbidden_edge[1] not in name_to_index:
    raise ValueError("Forbidden edge contains an unknown building.")

mandatory = (
    name_to_index[mandatory_edge[0]],
    name_to_index[mandatory_edge[1]]
)

forbidden = (
    name_to_index[forbidden_edge[0]],
    name_to_index[forbidden_edge[1]]
)

if set(mandatory) == set(forbidden):
    raise ValueError("An edge cannot be both mandatory and forbidden.")


# Add the mandatory edge first

u, v = mandatory

mandatory_weight = distance(buildings[u], buildings[v])

if not union(u, v):
    raise ValueError("Mandatory edge creates a cycle.")

mst = [(u, v, mandatory_weight)]
total_cost = mandatory_weight

degree[u] += 1
degree[v] += 1


# Consider the remaining edges in increasing order

for weight, u, v in sorted(edges):

    if len(mst) == n - 1:
        break

    # Skip the forbidden edge
    if set((u, v)) == set(forbidden):
        continue

    # Skip buildings that have reached the degree limit
    if degree[u] >= MAX_DEGREE or degree[v] >= MAX_DEGREE:
        continue

    # Add the edge only if it does not create a cycle
    if union(u, v):

        mst.append((u, v, weight))
        total_cost += weight

        degree[u] += 1
        degree[v] += 1


# --------------------------------
# 7. Check whether a spanning tree was formed
# --------------------------------

if len(mst) != n - 1:
    raise ValueError(
        "Could not form a spanning tree with these constraints. "
        "Try different mandatory or forbidden edges."
    )


# --------------------------------
# 8. Display results
# --------------------------------

additional_cost = total_cost - normal_cost

print("\nTASK 3: CONSTRAINED NETWORK")
print("---------------------------")

print("Number of buildings:", n)
print("Number of cables:", len(mst))

print("Mandatory edge:", mandatory_edge)
print("Forbidden edge:", forbidden_edge)
print("Maximum degree:", MAX_DEGREE)

print("\nNormal MST cost:", round(normal_cost, 2), "metres")
print("Constrained MST cost:", round(total_cost, 2), "metres")
print("Additional cost:", round(additional_cost, 2), "metres")

print("\nBuilding connections:")

for i, building in enumerate(buildings):
    print(building[0], ":", degree[i], "connections")


# --------------------------------
# 9. Save results
# --------------------------------

os.makedirs("outputs", exist_ok=True)

with open("outputs/task3_constrained_edges.csv", "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "source_building",
        "destination_building",
        "distance_m"
    ])

    for u, v, weight in mst:

        writer.writerow([
            buildings[u][0],
            buildings[v][0],
            round(weight, 2)
        ])


with open("outputs/task3_summary.txt", "w") as file:

    file.write("TASK 3: CONSTRAINED NETWORK\n")
    file.write("---------------------------\n")

    file.write(f"Number of buildings: {n}\n")
    file.write(f"Number of cables: {len(mst)}\n")

    file.write(f"Mandatory edge: {mandatory_edge}\n")
    file.write(f"Forbidden edge: {forbidden_edge}\n")
    file.write(f"Maximum degree: {MAX_DEGREE}\n")

    file.write(f"Normal MST cost: {normal_cost:.2f} metres\n")
    file.write(f"Constrained MST cost: {total_cost:.2f} metres\n")
    file.write(f"Additional cost: {additional_cost:.2f} metres\n")

print("\nTASK 3 COMPLETED!")
print("Results saved in the outputs folder.")
