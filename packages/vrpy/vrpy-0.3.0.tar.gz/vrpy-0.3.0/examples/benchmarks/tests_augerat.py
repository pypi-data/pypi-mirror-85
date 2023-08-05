import time
import os
from pandas import DataFrame
import sys

sys.path.append("../../")
sys.path.append("../../examples/")

from cvrp_augerat import DataSet
from vrpy.clarke_wright import ClarkeWright
from vrpy import VehicleRoutingProblem

initial_routes = [
    ["Source", 21, 31, 19, 17, 13, 7, 26, "Sink"],
    ["Source", 12, 1, 16, 30, "Sink"],
    ["Source", 27, 24, "Sink"],
    ["Source", 29, 18, 8, 9, 22, 15, 10, 25, 5, 20, "Sink"],
    ["Source", 14, 28, 11, 4, 23, 3, 2, 6, "Sink"],
]
initial_routes = None

if __name__ == "__main__":

    TIME = 10
    keys = [
        "instance",
        "nodes",
        "algorithm",
        "res",
        "best known solution",
        "gap",
        "time (s)",
        "vrp",
        "time limit (s)",
    ]
    instance = []
    nodes = []
    alg = []
    res = []
    best_known_solution = []
    gap = []
    run_time = []
    vrp = []
    time_limit = []
    for file_name in os.listdir("./data/"):
        if file_name[-3:] == "vrp" and file_name == "A-n36-k5.vrp":
            for cspy in [True]:
                data = DataSet(path="./data/", instance_name=file_name)
                if len(data.G.nodes()) < 105:
                    print(file_name)
                    print("lower bound =", data.best_known_solution)
                    instance.append(file_name)
                    nodes.append(len(data.G.nodes()) - 1)
                    best_known_solution.append(data.best_known_solution)
                    vrp.append("cvrp")
                    time_limit.append(TIME)

                    start = time.time()
                    prob = VehicleRoutingProblem(data.G, load_capacity=data.max_load)
                    prob.solve(
                        cspy=cspy, solver="cplex", time_limit=TIME,
                    )
                    res.append(prob.best_value)
                    gap.append(
                        (prob.best_value - data.best_known_solution)
                        / data.best_known_solution
                        * 100
                    )

                    run_time.append(float(time.time() - start))
                    if cspy:
                        alg.append("vrpy")
                    else:
                        # alg.append("lp cplex %s" % TIME)
                        alg.append("CW improved")

                    values = [
                        instance,
                        nodes,
                        alg,
                        res,
                        best_known_solution,
                        gap,
                        run_time,
                        vrp,
                        time_limit,
                    ]
                    compar = dict(zip(keys, values))
                    df = DataFrame(compar, columns=keys)
                    # df.to_csv("augerat_vrpy.csv", sep=";", index=False)
