import constraint as cp
import networkx as nx

G = nx.DiGraph()
for v in [1, 2, 3, 4, 5]:
    G.add_edge("Source", v, cost=10, time=20)
    G.add_edge(v, "Sink", cost=10, time=20)
    G.nodes[v]["demand"] = 5

G.nodes["Source"]["demand"] = 0
G.nodes["Sink"]["demand"] = 0
G.add_edge(1, 2, cost=10, time=20)
G.add_edge(2, 3, cost=10, time=20)
G.add_edge(3, 4, cost=15, time=20)
G.add_edge(4, 5, cost=10, time=25)

for v in [1, 2, 3, 4, 5]:
    G.add_node("dummy_%s" % v, demand=0)

if __name__ == "__main__":

    print(G.nodes())

    prob = cp.Problem()
    positions = 7
    prob.addVariables(["P_%s" % k for k in range(positions)], list(G.nodes()))
    # prob.addVariables(["L_%s" % k for k in range(positions)], range(36))

    prob.addConstraint(lambda first_node: first_node == "Source", ["P_0"])
    prob.addConstraint(cp.SomeInSetConstraint(["Sink"]))
    prob.addConstraint(cp.AllDifferentConstraint())

    prob.addConstraint(lambda third_node: third_node == "Sink", ["P_2"])

    for v in [3, 4, 5]:  # [1, 2, 3, 4, 5]:
        prob.addConstraint(lambda second_node: second_node != "dummy_%s" % v, ["P_1"])

    # P[k] = dummy => P[k+1] != 1,2,3,4,5,Sink
    # for v in [1, 2, 3, 4, 5, "Sink"]:
    #    prob.addConstraint(
    #        lambda node, next_node: node != "dummy_%s" % i or next_node != v,
    #        ["P_%s" % k, "P_%s" % (k + 1)],
    #    )

    solution = prob.getSolution()
    for x in sorted(solution.keys()):
        if "P" in x:
            print(x, solution[x])
