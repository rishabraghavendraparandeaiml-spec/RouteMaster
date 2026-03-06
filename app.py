from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import heapq
from itertools import permutations
from time import perf_counter

app = FastAPI()

# Enable CORS so the browser doesn't block requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- MODELS ---
class WarehouseInput(BaseModel):
    grid: List[List[int]]
    start: List[int]
    targets: List[List[int]]


def validate_input(data: WarehouseInput):
    if not data.grid or not data.grid[0]:
        raise HTTPException(400, "Grid cannot be empty")

    rows, cols = len(data.grid), len(data.grid[0])

    for row in data.grid:
        if len(row) != cols:
            raise HTTPException(400, "Grid rows must all have equal length")

    def in_bounds(point):
        return 0 <= point[0] < rows and 0 <= point[1] < cols

    if len(data.start) != 2 or not in_bounds(data.start):
        raise HTTPException(400, "Invalid start position")

    for target in data.targets:
        if len(target) != 2 or not in_bounds(target):
            raise HTTPException(400, "Invalid target position")

    if data.grid[data.start[0]][data.start[1]] == 1:
        raise HTTPException(400, "Start is on an obstacle")

    for target in data.targets:
        if data.grid[target[0]][target[1]] == 1:
            raise HTTPException(400, "Target is on an obstacle")


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def reconstruct_path(came_from, current):
    path = [list(current)]
    while current in came_from:
        current = came_from[current]
        path.append(list(current))
    path.reverse()
    return path

# --- ALGORITHM: A* ---
def a_star(grid, start, goal):
    start, goal = tuple(start), tuple(goal)
    rows, cols = len(grid), len(grid[0])
    open_set = [(manhattan(start, goal), 0, start)]
    g_score = {start: 0}
    came_from = {}

    while open_set:
        _, current_g, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        if current_g > g_score.get(current, float("inf")):
            continue

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = current[0] + dx, current[1] + dy
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] != 1:
                neighbor = (r, c)
                tentative_g = current_g + 1
                if tentative_g < g_score.get(neighbor, float("inf")):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score = tentative_g + manhattan(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g, neighbor))

    return None


def dijkstra(grid, start, goal):
    start, goal = tuple(start), tuple(goal)
    rows, cols = len(grid), len(grid[0])
    queue = [(0, start)]
    dist = {start: 0}
    came_from = {}

    while queue:
        current_dist, current = heapq.heappop(queue)

        if current == goal:
            return reconstruct_path(came_from, current)

        if current_dist > dist.get(current, float("inf")):
            continue

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            r, c = current[0] + dx, current[1] + dy
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] != 1:
                neighbor = (r, c)
                next_dist = current_dist + 1
                if next_dist < dist.get(neighbor, float("inf")):
                    dist[neighbor] = next_dist
                    came_from[neighbor] = current
                    heapq.heappush(queue, (next_dist, neighbor))

    return None


def build_adj_matrix(grid, nodes, pathfinder):
    adj_matrix = {}
    for i in range(len(nodes)):
        for j in range(len(nodes)):
            if i == j:
                continue
            path = pathfinder(grid, nodes[i], nodes[j])
            if not path:
                raise HTTPException(400, "Unreachable target")
            adj_matrix[(nodes[i], nodes[j])] = path
    return adj_matrix


def path_from_order(adj_matrix, start_node, order):
    curr_path = []
    curr_steps = 0
    curr_node = start_node

    for target in order:
        segment = adj_matrix[(curr_node, target)]
        curr_path += segment if not curr_path else segment[1:]
        curr_steps += len(segment) - 1
        curr_node = target

    return curr_path, curr_steps


def optimal_order_route(adj_matrix, start_node, targets):
    best_path = []
    min_steps = float("inf")
    best_order = []

    for order in permutations(targets):
        curr_path, curr_steps = path_from_order(adj_matrix, start_node, order)
        if curr_steps < min_steps:
            min_steps = curr_steps
            best_path = curr_path
            best_order = list(order)

    if min_steps == float("inf"):
        raise HTTPException(400, "No valid route found")

    return best_path, int(min_steps), best_order


def greedy_order_route(adj_matrix, start_node, targets):
    remaining = set(targets)
    order = []
    curr = start_node

    while remaining:
        next_target = min(remaining, key=lambda t: len(adj_matrix[(curr, t)]) - 1)
        order.append(next_target)
        remaining.remove(next_target)
        curr = next_target

    path, steps = path_from_order(adj_matrix, start_node, order)
    return path, int(steps), order


# --- API ENDPOINT ---
@app.post("/route")
async def route(data: WarehouseInput):
    """
    Simplified endpoint matching exact JSON specification:
    - Input: grid with 0=walkable, 1=obstacle, 2=target, start position, targets array (optional)
    - Output: total_steps, path, target_reached, execution_time_ms
    """
    # Extract targets from grid (cells marked with 2) if not provided
    targets_from_grid = []
    for r in range(len(data.grid)):
        for c in range(len(data.grid[r])):
            if data.grid[r][c] == 2:
                targets_from_grid.append([r, c])
    
    # Use targets from grid if available, otherwise use targets from input
    targets_to_use = targets_from_grid if targets_from_grid else data.targets
    
    if len(targets_to_use) == 0:
        raise HTTPException(400, "At least one target is required")
    
    start_node = tuple(data.start)
    target_node = tuple(targets_to_use[0])  # Use first target
    
    started = perf_counter()
    path = a_star(data.grid, start_node, target_node)
    elapsed_ms = round((perf_counter() - started) * 1000, 2)
    
    if path is None:
        return {
            "total_steps": 0,
            "path": [],
            "target_reached": False,
            "execution_time_ms": elapsed_ms,
        }
    
    return {
        "total_steps": len(path) - 1,  # Steps = path length - 1
        "path": path,
        "target_reached": True,
        "execution_time_ms": elapsed_ms,
    }


@app.post("/calculate-route")
async def calculate_route(data: WarehouseInput):
    # Extract targets from grid (cells marked with 2) if not provided
    targets_from_grid = []
    for r in range(len(data.grid)):
        for c in range(len(data.grid[r])):
            if data.grid[r][c] == 2:
                targets_from_grid.append([r, c])
    
    # Use targets from grid if available, otherwise use targets from input
    targets_list = targets_from_grid if targets_from_grid else data.targets
    
    validate_input(data)
    start_node = tuple(data.start)
    targets = [tuple(t) for t in targets_list]
    nodes = [start_node] + targets

    started = perf_counter()
    adj_matrix = build_adj_matrix(data.grid, nodes, a_star)
    best_path, min_steps, best_order = optimal_order_route(adj_matrix, start_node, targets)
    elapsed_ms = round((perf_counter() - started) * 1000, 2)

    direct_order = targets
    _, direct_steps = path_from_order(adj_matrix, start_node, direct_order)
    improvement = 0
    if direct_steps > 0:
        improvement = round(((direct_steps - min_steps) / direct_steps) * 100, 2)

    return {
        "total_steps": min_steps,
        "path": best_path,
        "target_reached": len(targets) > 0,
        "targets_collected": len(targets),
        "best_order": [list(point) for point in best_order],
        "baseline_steps": int(direct_steps),
        "improvement_percent": improvement,
        "execution_time_ms": elapsed_ms,
        "compute_time_ms": elapsed_ms,
    }


@app.post("/compare-algorithms")
async def compare_algorithms(data: WarehouseInput):
    # Extract targets from grid (cells marked with 2) if not provided
    targets_from_grid = []
    for r in range(len(data.grid)):
        for c in range(len(data.grid[r])):
            if data.grid[r][c] == 2:
                targets_from_grid.append([r, c])
    
    # Use targets from grid if available, otherwise use targets from input
    targets_list = targets_from_grid if targets_from_grid else data.targets
    
    validate_input(data)
    start_node = tuple(data.start)
    targets = [tuple(t) for t in targets_list]
    nodes = [start_node] + targets

    a_started = perf_counter()
    a_adj = build_adj_matrix(data.grid, nodes, a_star)
    a_path, a_steps, a_order = optimal_order_route(a_adj, start_node, targets)
    a_time = round((perf_counter() - a_started) * 1000, 2)

    d_started = perf_counter()
    d_adj = build_adj_matrix(data.grid, nodes, dijkstra)
    d_path, d_steps, d_order = optimal_order_route(d_adj, start_node, targets)
    d_time = round((perf_counter() - d_started) * 1000, 2)

    g_started = perf_counter()
    g_path, g_steps, g_order = greedy_order_route(a_adj, start_node, targets)
    g_time = round((perf_counter() - g_started) * 1000, 2)

    fastest = min(a_time, d_time, g_time)
    best_steps = min(a_steps, d_steps, g_steps)

    return {
        "results": [
            {
                "name": "A* + Optimal Order",
                "steps": a_steps,
                "compute_time_ms": a_time,
                "order": [list(point) for point in a_order],
                "path": a_path,
                "is_shortest": a_steps == best_steps,
                "is_fastest": a_time == fastest,
            },
            {
                "name": "Dijkstra + Optimal Order",
                "steps": d_steps,
                "compute_time_ms": d_time,
                "order": [list(point) for point in d_order],
                "path": d_path,
                "is_shortest": d_steps == best_steps,
                "is_fastest": d_time == fastest,
            },
            {
                "name": "A* + Greedy Order",
                "steps": g_steps,
                "compute_time_ms": g_time,
                "order": [list(point) for point in g_order],
                "path": g_path,
                "is_shortest": g_steps == best_steps,
                "is_fastest": g_time == fastest,
            },
        ]
    }


@app.post("/verify-accuracy")
async def verify_accuracy(data: WarehouseInput):
    """
    Analyzes algorithm performance and explains why the chosen algorithm is optimal.
    Returns accuracy percentage and reasoning.
    """
    # Extract targets from grid
    targets_from_grid = []
    for r in range(len(data.grid)):
        for c in range(len(data.grid[r])):
            if data.grid[r][c] == 2:
                targets_from_grid.append([r, c])
    
    targets_list = targets_from_grid if targets_from_grid else data.targets
    
    if len(targets_list) == 0:
        raise HTTPException(400, "At least one target is required")
    
    validate_input(data)
    start_node = tuple(data.start)
    targets = [tuple(t) for t in targets_list]
    nodes = [start_node] + targets
    
    # Test all algorithms
    # A* Algorithm
    a_start = perf_counter()
    a_adj = build_adj_matrix(data.grid, nodes, a_star)
    a_path, a_steps, a_order = optimal_order_route(a_adj, start_node, targets)
    a_time = round((perf_counter() - a_start) * 1000, 2)
    
    # Dijkstra Algorithm
    d_start = perf_counter()
    d_adj = build_adj_matrix(data.grid, nodes, dijkstra)
    d_path, d_steps, d_order = optimal_order_route(d_adj, start_node, targets)
    d_time = round((perf_counter() - d_start) * 1000, 2)
    
    # Greedy Algorithm
    g_start = perf_counter()
    g_path, g_steps, g_order = greedy_order_route(a_adj, start_node, targets)
    g_time = round((perf_counter() - g_start) * 1000, 2)
    
    # Calculate theoretical minimum (Manhattan distance)
    theoretical_min = 0
    current = start_node
    for target in a_order:
        theoretical_min += manhattan(current, target)
        current = target
    
    # Determine best algorithm
    best_steps = min(a_steps, d_steps, g_steps)
    fastest_time = min(a_time, d_time, g_time)
    
    # Calculate accuracy for each algorithm
    a_accuracy = round((theoretical_min / a_steps) * 100, 2) if a_steps > 0 else 100
    d_accuracy = round((theoretical_min / d_steps) * 100, 2) if d_steps > 0 else 100
    g_accuracy = round((theoretical_min / g_steps) * 100, 2) if g_steps > 0 else 100
    
    # Determine chosen algorithm (A* is default)
    chosen_algorithm = "A* Algorithm"
    chosen_steps = a_steps
    chosen_time = a_time
    chosen_accuracy = a_accuracy
    
    # Reasoning for choosing A*
    reasons = []
    if a_steps == best_steps:
        reasons.append("Produces optimal path length")
    if a_time == fastest_time:
        reasons.append("Fastest computation time")
    reasons.append("Uses Manhattan heuristic for efficient pathfinding")
    reasons.append("Guarantees shortest path in grid-based navigation")
    reasons.append("Balances optimality with computational efficiency")
    
    # Performance comparison
    performance_vs_dijkstra = round(((d_time - a_time) / d_time * 100), 2) if d_time > 0 else 0
    performance_vs_greedy = round(((a_steps - g_steps) / a_steps * 100), 2) if a_steps > 0 else 0
    
    return {
        "chosen_algorithm": chosen_algorithm,
        "accuracy_percentage": chosen_accuracy,
        "path_optimality": "Perfect" if chosen_accuracy == 100 else "Near-Optimal" if chosen_accuracy >= 95 else "Good" if chosen_accuracy >= 85 else "Fair",
        "total_steps": chosen_steps,
        "theoretical_minimum": theoretical_min,
        "computation_time_ms": chosen_time,
        "reasoning": {
            "why_chosen": reasons,
            "key_advantage": "A* combines Dijkstra's optimality guarantee with heuristic-guided search, making it ideal for warehouse routing where both path quality and speed matter.",
            "vs_dijkstra": f"A* is {abs(performance_vs_dijkstra)}% {'faster' if performance_vs_dijkstra > 0 else 'comparable'} than Dijkstra",
            "vs_greedy": f"A* produces {abs(performance_vs_greedy)}% {'better' if a_steps < g_steps else 'similar'} path quality than Greedy approach"
        },
        "algorithm_comparison": [
            {
                "name": "A* (Chosen)",
                "steps": a_steps,
                "time_ms": a_time,
                "accuracy": a_accuracy,
                "is_best": a_steps == best_steps
            },
            {
                "name": "Dijkstra",
                "steps": d_steps,
                "time_ms": d_time,
                "accuracy": d_accuracy,
                "is_best": d_steps == best_steps
            },
            {
                "name": "Greedy",
                "steps": g_steps,
                "time_ms": g_time,
                "accuracy": g_accuracy,
                "is_best": g_steps == best_steps
            }
        ]
    }


# --- SERVE THE FRONTEND ---
@app.get("/", response_class=HTMLResponse)
async def serve_ui():
    try:
        with open("index.html", "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        raise HTTPException(404, "Frontend file not found")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
