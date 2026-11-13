import csv
import math
import heapq
import folium

# Read building names and coordinates from the CSV file
buildings = []

with open("data/buildings.csv", "r", newline="", encoding="utf-8-sig") as file:
    reader = csv.DictReader(file)
    for row in reader:
        name = row["building"].strip()
        latitude = float(row["latitude"])
        longitude = float(row["longitude"])
        buildings.append((name, latitude, longitude))

if len(buildings) < 2:
    raise ValueError("Enter at least two buildings in data/buildings.csv.")

# Calculate the distance between two buildings using the Haversine formula
def distance(a, b):
    lat1 = math.radians(a[1])
    lon1 = math.radians(a[2])
    lat2 = math.radians(b[1])
    lon2 = math.radians(b[2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    x = (math.sin(dlat / 2) ** 2
         + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2)

    return 6371000 * 2 * math.atan2(math.sqrt(x), math.sqrt(1 - x))


# Build the weighted graph (distance between every pair of buildings)
n = len(buildings)
graph = [[] for _ in range(n)]

for i in range(n):
    for j in range(i + 1, n):
        w = distance(buildings[i], buildings[j])
        graph[i].append((w, j))
        graph[j].append((w, i))


# Prim's algorithm using a min-heap
visited = [False] * n
visited[0] = True

heap = []
for weight, neighbour in graph[0]:
    heapq.heappush(heap, (weight, 0, neighbour))

mst = []
total_cost = 0

while heap and len(mst) < n - 1:
    weight, u, v = heapq.heappop(heap)

    if visited[v]:
        continue

    visited[v] = True
    mst.append((u, v, weight))
    total_cost += weight

    for next_weight, neighbour in graph[v]:
        if not visited[neighbour]:
            heapq.heappush(heap, (next_weight, v, neighbour))

if len(mst) != n - 1:
    raise ValueError("The graph is disconnected; an MST could not be formed.")


# Save the selected cable connections
with open("outputs/mst_edges.csv", "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["source_building", "destination_building", "distance_m"])

    for u, v, weight in mst:
        writer.writerow([buildings[u][0], buildings[v][0], round(weight, 2)])


# Draw the buildings and MST cable connections on a map
center = [
    sum(b[1] for b in buildings) / n,
    sum(b[2] for b in buildings) / n
]

campus_map = folium.Map(location=center, zoom_start=17)

for u, v, weight in mst:
    a = buildings[u]
    b = buildings[v]

    folium.PolyLine(
        [(a[1], a[2]), (b[1], b[2])],
        color="blue",
        weight=4,
        tooltip=f"{a[0]} to {b[0]}: {weight:.2f} m"
    ).add_to(campus_map)

for name, lat, lon in buildings:
    folium.Marker(
        [lat, lon],
        tooltip=name
    ).add_to(campus_map)

campus_map.save("outputs/campus_mst_map.html")


# Save a short result summary
with open("outputs/mst_summary.txt", "w", encoding="utf-8") as file:
    file.write(f"Number of buildings: {n}\n")
    file.write(f"Number of MST cables: {len(mst)}\n")
    file.write(f"Total cable length: {total_cost:.2f} metres\n")

print("Task 1 completed!")
print("Number of buildings:", n)
print("Number of MST cables:", len(mst))
print(f"Total cable length: {total_cost:.2f} metres")
print("Open outputs/campus_mst_map.html to see the campus network.")
