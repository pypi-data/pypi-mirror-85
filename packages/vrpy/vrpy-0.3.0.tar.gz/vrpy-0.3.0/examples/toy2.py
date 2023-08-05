import sys

# sys.path.append("../vrpy/")
sys.path.append("../")
from vrpy.vrp import VehicleRoutingProblem

import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import networkx as nx

    G = nx.DiGraph()
    for v in [1, 2, 3, 4, 5]:
        G.add_edge("Source", v, cost=[10, 11], time=20)
        G.add_edge(v, "Sink", cost=[10, 11], time=20)
        G.nodes[v]["demand"] = 2
    G.add_edge(1, 2, cost=[10, 11], time=20)
    G.add_edge(2, 3, cost=[10, 11], time=20)
    G.add_edge(3, 4, cost=[15, 16], time=20)
    G.add_edge(4, 5, cost=[10, 11], time=25)

    prob = VehicleRoutingProblem(
        G,
        # num_stops=4,
        load_capacity=[5, 1],
        # duration=64,
        # time_windows=True,
        # distribution_collection=True,
        fixed_cost=[0, 5],
        # drop_penalty=100,
        # periodic=True,
        num_vehicles=[5, 1],
        mixed_fleet=True,
    )

    prob.solve(
        cspy=False,
        solver="cplex",
        # pricing_strategy="Stops"
        # preassignments=[[2, 3]],
        # time_limit=2,
    )
    print("routes", prob.best_routes)
    print("cost", prob.best_routes_cost)
    print("type", prob.best_routes_type)
    print("best value", prob.best_value)
    print("load", prob.best_routes_load)
    print("time", prob.best_routes_duration)
    print("arrival time", prob.arrival_time)
    print("departure time", prob.departure_time)
    print("node load", prob.node_load)
