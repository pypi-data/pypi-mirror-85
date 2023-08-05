from networkx import (
    from_numpy_matrix,
    set_node_attributes,
    relabel_nodes,
    DiGraph,
    compose,
)
from numpy import matrix

from data import (
    # DISTANCES,
    TRAVEL_TIMES,
    TIME_WINDOWS_LOWER,
    TIME_WINDOWS_UPPER,
    # DEMANDS,
)
import sys

sys.path.append("../../")
from vrpy import VehicleRoutingProblem

import pickle

with open("distance_matrix.pkl", "rb") as f:
    DISTANCES = pickle.load(f)

with open("frequency.pkl", "rb") as f:
    service_levels = pickle.load(f)

with open("demands.pkl", "rb") as f:
    DEMANDS = pickle.load(f)

A = matrix(DISTANCES, dtype=[("cost", int)])
G_d = from_numpy_matrix(A, create_using=DiGraph())

# Transform time matrix into DiGraph
# Average speed of vehicle is assumed to be 50 km/hr
# Time unit is in minutes, distance unit is in km
TRAVEL_TIMES = [[round(60 * float(j) / 50, 0) for j in i] for i in DISTANCES]

A = matrix(TRAVEL_TIMES, dtype=[("time", int)])
G_t = from_numpy_matrix(A, create_using=DiGraph())

# Merge
G = compose(G_d, G_t)

###Adding frequencies and making the problem periodic in nature
##Setting the frequency for each node
set_node_attributes(G, values=service_levels, name="frequency")

# The demands are stored as node attributes
set_node_attributes(G, values=DEMANDS, name="demand")

# The depot is relabeled as Source and Sink
G = relabel_nodes(G, {0: "Source", len(DISTANCES) - 1: "Sink"})


if __name__ == "__main__":
    # print(DISTANCES)
    # print(list(G.successors("Source")))
    prob = VehicleRoutingProblem(G, load_capacity=15, duration=900, periodic=24)
    prob.solve(cspy=False, solver="cplex", time_limit=3)
    print(prob.best_value)
    print(prob.best_routes)
    print(prob.best_routes_duration)
