import sys

# sys.path.append("../vrpy/")
sys.path.append("../")
from vrpy.main import VehicleRoutingProblem
from vrpy.schedule import Schedule

import logging

logger = logging.getLogger(__name__)

if __name__ == "__main__":
    import networkx as nx

    G = nx.DiGraph()
    for v in [1, 2, 3, 4, 5]:
        G.add_edge("Source", v, cost=10, time=10)
        G.add_edge(v, "Sink", cost=10, time=10)
        G.nodes[v]["demand"] = 5
        G.nodes[v]["upper"] = 100
        G.nodes[v]["lower"] = 5
        G.nodes[v]["service_time"] = 0
    G.nodes[2]["upper"] = 20
    G.nodes[2]["frequency"] = 2
    G.nodes["Sink"]["upper"] = 110
    G.nodes["Source"]["upper"] = 100
    G.add_edge(1, 2, cost=10, time=10)
    G.add_edge(2, 3, cost=10, time=10)
    G.add_edge(3, 4, cost=15, time=15)
    G.add_edge(4, 5, cost=10, time=10)

    G.nodes[1]["collect"] = 12
    G.nodes[4]["collect"] = 1

    G.nodes["Source"]["demand"] = 4

    prob = VehicleRoutingProblem(
        G,
        # num_stops=3,
        # load_capacity=10,
        duration=39,
        # time_windows=True,
        # distribution_collection=True,
        # fixed_cost=[10, 0],
        # drop_penalty=100,
        # periodic=2,
        num_vehicles=3,
        # mixed_fleet=True,
        # minimize_global_span=True,
    )
    prob.solve(
        # cspy=False,
        # solver="cplex",
        # pricing_strategy="Stops"
        # preassignments=[[2, 3]],
        # time_limit=2,
        max_iter=10
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
    print("schedule", prob.schedule)
