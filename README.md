# Graph Algorithms Project 06
## Wiring a New Campus at the Lowest Cost

## About the Project

The aim of this project is to find the minimum cost of connecting all the buildings on a campus using a cable network.

We represent the campus as a weighted graph, where each building is a vertex and the possible connections between buildings are edges. The weight of each edge is the geographical distance between the two buildings.

The project is divided into four tasks, each implementing a different graph algorithm or technique.

## Tasks

**Task 1 – Prim's Algorithm**
- Construct a weighted graph using building coordinates.
- Calculate distances using the Haversine formula.
- Implement Prim's algorithm using a min-heap.
- Generate an interactive map showing the Minimum Spanning Tree (MST).

**Task 2 – Kruskal's Algorithm**
- Implement Kruskal's algorithm using Union-Find.
- Compare its MST cost with Prim's algorithm.
- Compare execution times on sparse and dense graphs.

**Task 3 – Network Constraints**
- Include a mandatory edge and exclude a forbidden edge.
- Restrict each building to a maximum of three connections.
- Calculate the additional cost due to these constraints.

**Task 4 – Spanning Tree Enumeration**
- Generate and count spanning trees for graphs with up to 8 vertices.
- Verify the results using Kirchhoff's Matrix-Tree Theorem.

## Technologies Used

- Python
- Folium for map visualization
- heapq for the priority queue
- CSV for input data and storing results

## Project Structure

```text
Graph_Project/
│
├── data/
├── outputs/
├── .venv/
├── .venv-1/
├── .gitignore
├── README.md
├── requirements.txt
├── task1_prim_project.py
├── task2_kruskal.py
├── task3_constraints.py
└── task4_spanning_trees.py
```

## Input Data

The input file is `data/buildings.csv`.

It contains the building names and their latitude and longitude coordinates.

Example:

```csv
building,latitude,longitude
Building A,17.000001,78.000001
Building B,17.000100,78.000100
```

Note: The current demo dataset contains synthetic coordinates. These need to be replaced with actual campus building coordinates before final submission.

## How to Run

First, install the required packages:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Run the individual tasks using:

```bash
./.venv/bin/python task1_prim_project.py
./.venv/bin/python task2_kruskal.py
./.venv/bin/python task3_constraints.py
./.venv/bin/python task4_spanning_trees.py
```

## Output Files

The results of the programs are saved in the `outputs` folder.

- `campus_mst_map.html` – Interactive map showing the campus network.
- `mst_edges.csv` – Edges selected by Prim's algorithm.
- `mst_summary.txt` – MST cost and connection details.
- `kruskal_mst_edges.csv` – MST generated using Kruskal's algorithm.
- `task2_benchmark.csv` – Execution time comparison.
- `task3_constrained_edges.csv` – Network connections after applying constraints.
- `task3_summary.txt` – Summary of Task 3.
- `task4_results.csv` – Spanning tree counts and verification results.

## Results

The programs were tested using the demonstration dataset.

- **Task 1:** Connected 36 buildings using 35 edges, with a total cable length of 3516.87 metres.
- **Task 2:** Prim's and Kruskal's algorithms produced the same MST cost.
- **Task 3:** The constrained network had an additional cost of 425.49 metres compared to the normal MST.
- **Task 4:** The enumeration counts matched the results obtained using Kirchhoff's theorem for all tested graphs.

## Conclusion

Through this project, we implemented and explored different graph algorithms and understood how they can be used to solve a real-world network design problem. We also compared algorithms, applied additional constraints, and verified spanning tree counts using a mathematical theorem.