import time
import os
from pandas import DataFrame, read_csv
import sys
import numpy as np

sys.path.append("../../")
sys.path.append("../../examples/")

# sys.path.append("../../../cspy")
from benchmarks.cvrptw_solomon import DataSet
from vrpy import VehicleRoutingProblem


def read_best():
    best = {}
    df = read_csv("solomon_best.csv", engine="python", sep=";")
    df["Problem"] = df["Problem"].str.rstrip()
    for line in df.itertuples():
        best[line[1]] = np.float64(line[3]).item()
    return best


"""
routes = [
    ["Source", 5, 3, 7, 8, 10, 11, 9, 6, 4, 2, 1, "Sink"],
    ["Source", 13, 17, 18, 19, 15, 16, 14, 12, "Sink"],
    ["Source", 20, 24, 23, 22, 21, "Sink"],
]
"""
routes = [
    ["Source", 21, 22, 6, 2, 20, 24, 10, 4, 8, 12, 11, "Sink"],
    ["Source", 23, 18, 3, 17, 14, 16, 13, 15, 5, 1, "Sink"],
    ["Source", 9, 19, 7, "Sink"],
]
if __name__ == "__main__":

    TIME = 60 * 30
    best = read_best()
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
        if file_name[-3:] == "txt" and file_name == "c101.txt":
            for cspy in [False]:
                for strat in ["BestEdges1"]:
                    data = DataSet(
                        path="./data/", instance_name=file_name, n_vertices=25
                    )
                    if len(data.G.nodes()) < 30:
                        print(file_name)
                        instance.append(file_name[:-3] + "25")
                        nodes.append(len(data.G.nodes()))
                        best_known = best[file_name[:-3] + "25"]
                        best_known_solution.append(best_known)
                        vrp.append("cvrptw")
                        time_limit.append(TIME)

                        start = time.time()
                        prob = VehicleRoutingProblem(
                            data.G,
                            load_capacity=data.max_load,
                            time_windows=True,
                            # num_stops=4,
                        )
                        prob.solve(
                            cspy=cspy,
                            solver="cplex",
                            pricing_strategy=strat,
                            time_limit=TIME,
                            preassignments=routes,
                        )
                        print(prob.best_value)
                        print(prob.best_routes)
                        res.append(prob.best_value)
                        gap.append((prob.best_value - best_known) / best_known * 100)
                        run_time.append(float(time.time() - start))
                        if cspy:
                            alg.append("cspy %s" % strat)
                        else:
                            alg.append("lp cplex %s %s" % (strat, TIME))

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
                        df.to_csv("cplex_30.csv", sep=";", index=False)
