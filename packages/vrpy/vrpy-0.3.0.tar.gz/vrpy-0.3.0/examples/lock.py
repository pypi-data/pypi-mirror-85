from networkx import (
    from_numpy_matrix,
    set_node_attributes,
    relabel_nodes,
    DiGraph,
    compose,
)
from numpy import array

from data import DISTANCES, TRAVEL_TIMES, TIME_WINDOWS_LOWER, TIME_WINDOWS_UPPER
import sys

sys.path.append("../")
from vrpy import VehicleRoutingProblem

# Transform distance matrix to DiGraph
A = array(DISTANCES, dtype=[("cost", int)])
G_d = from_numpy_matrix(A, create_using=DiGraph())

# Transform time matrix to DiGraph
A = array(TRAVEL_TIMES, dtype=[("time", int)])
G_t = from_numpy_matrix(A, create_using=DiGraph())

# Merge
G = compose(G_d, G_t)

# Set time windows
set_node_attributes(G, values=TIME_WINDOWS_LOWER, name="lower")
set_node_attributes(G, values=TIME_WINDOWS_UPPER, name="upper")

# Relabel depot
G = relabel_nodes(G, {0: "Source", 17: "Sink"})
# G.edges["Source", 5]["cost"] = 100

initial_routes = [
    ["Source", 9, 14, 16, "Sink"],
    ["Source", 7, 1, 4, 3, "Sink"],
    ["Source", 12, 13, 15, 11, "Sink"],
    ["Source", 5, 8, 6, 2, 10, "Sink"],
]

initial_routes = [
    [9, 14, 16,],
    [7, 1, 4, 3,],
    [12, 13, 15, 11,],
    [5, 8, 6, 2, 10,],
]


if __name__ == "__main__":

    prob = VehicleRoutingProblem(G, time_windows=True)
    prob.solve(preassignments=initial_routes)
    print(prob.best_value)
    print(prob.best_routes)
    print("arrivals", prob.arrival_time)
    print("times", prob.best_routes_duration)
    assert prob.best_value == 6528
