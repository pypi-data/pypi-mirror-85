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

for v in range(len(G.nodes())):
    G.add_node("dummy_%s" % v, demand=0)

if __name__ == "__main__":

    prob = cp.Problem()
    positions = 7
    prob.addVariables(["P_%s" % k for k in range(positions)], list(G.nodes()))
    # prob.addVariables(["L_%s" % k for k in range(positions)], range(36))

    prob.addConstraint(
        lambda first_node: first_node == "Source", "P_0",
    )
    prob.addConstraint(cp.SomeInSetConstraint(["Sink"]))

    prob.addConstraint(cp.AllDifferentConstraint())

    prob.addConstraint(cp.SomeInSetConstraint([2]))
    prob.addConstraint(cp.SomeInSetConstraint([3]))

    def start_at_source(first_position):
        if first_position == "Source":
            return True

    prob.addConstraint(start_at_source, ["P_0"])

    def finish_at_sink(last_position):
        if last_position == "Sink":
            return True

    prob.addConstraint(finish_at_sink, ["P_4"])

    """
    def initial_load(depot_load):
        if depot_load == 0:
            return True

    prob.addConstraint(initial_load, ["L_0"])

    def capacity_constraint(new_load, current_load, current_node):
        demand = G.nodes[current_node]["demand"]
        if new_load == current_load + demand:
            return True

    for k in [1, 2, 3, 4, 5]:  # range(positions - 2):
        prob.addConstraint(
            capacity_constraint, ["L_%s" % (k + 1), "L_%s" % k, "P_%s" % k]
        )
    """

    def finish(node, next_node):
        if node != "Sink" or (
            next_node == "dummy_1"
            or next_node == "dummy_2"
            or next_node == "dummy_3"
            or next_node == "dummy_4"
            or next_node == "dummy_5"
        ):
            return True

    for k in [1, 2, 3, 4, 5]:
        prob.addConstraint(finish, ["P_%s" % k, "P_%s" % (k + 1)])

    def f(node, next_node):
        if node != "dummy_1" or (
            next_node == "dummy_2"
            or next_node == "dummy_3"
            or next_node == "dummy_4"
            or next_node == "dummy_5"
        ):
            return True

    for k in [1, 2, 3, 4, 5]:
        prob.addConstraint(f, ["P_%s" % k, "P_%s" % (k + 1)])

    def g(node, next_node):
        if node != "dummy_5" or (
            next_node == "dummy_2"
            or next_node == "dummy_3"
            or next_node == "dummy_4"
            or next_node == "dummy_1"
        ):
            return True

    for k in [1, 2, 3, 4, 5]:
        prob.addConstraint(g, ["P_%s" % k, "P_%s" % (k + 1)])

    def h(node, next_node):
        if node != "dummy_6" or (
            next_node == "dummy_2"
            or next_node == "dummy_3"
            or next_node == "dummy_4"
            or next_node == "dummy_5"
        ):
            return True

    for k in [1, 2, 3, 4, 5]:
        prob.addConstraint(h, ["P_%s" % k, "P_%s" % (k + 1)])

    def i(node, next_node):
        if node != "dummy_4" or (
            next_node == "dummy_2"
            or next_node == "dummy_3"
            or next_node == "dummy_1"
            or next_node == "dummy_5"
        ):
            return True

    for k in [1, 2, 3, 4, 5]:
        prob.addConstraint(i, ["P_%s" % k, "P_%s" % (k + 1)])

    solution = prob.getSolution()
    for x in sorted(solution.keys()):
        if "P" in x:
            print(x, solution[x])
    print()
    for x in sorted(solution.keys()):
        if "L" in x:
            print(x, solution[x])
