VRPy
====

VRPy is a python framework for solving Vehicle Routing Problems (VRP) including:

-   the Capacitated VRP (CVRP),
-   the CVRP with resource constraints,
-   the CVRP with time windows (CVRPTW),
-   the CVRP with simultaneous distribution and collection (CVRPSDC),
-   the CVRP with heterogeneous fleet (HFCVRP).

Check out the docs_ to find more variants and options.

.. _docs : https://vrpy.readthedocs.io/en/latest/

Simple example
--------------

.. code:: python

	>>> from networkx import DiGraph
	>>> from vrpy import VehicleRoutingProblem

	# Define the network
	>>> G = DiGraph()
	>>> G.add_edge("Source",1,cost=1,time=2)
	>>> G.add_edge("Source",2,cost=2,time=1)
	>>> G.add_edge(1,"Sink",cost=0,time=2)
	>>> G.add_edge(2,"Sink",cost=2,time=3)
	>>> G.add_edge(1,2,cost=1,time=1)
	>>> G.add_edge(2,1,cost=1,time=1)

	# Define the customers demands
	>>> G.nodes[1]["demand"] = 5
	>>> G.nodes[2]["demand"] = 4

	# Define the Vehicle Routing Problem
	>>> prob = VehicleRoutingProblem(G, load_capacity=10, duration=5)

	# Solve and display solution value
	>>> prob.solve()
	>>> print(prob.best_value)
	3
	>>> print(prob.best_routes)
	{1: ["Source",2,1,"Sink"]}

Install
-------

.. code:: sh

	pip install vrpy


Requirements
------------

	cspy_

	NetworkX_

	numpy_

	PuLP_

.. _cspy : https://pypi.org/project/cspy/
.. _NetworkX : https://pypi.org/project/networkx/
.. _numpy : https://pypi.org/project/numpy/
.. _PuLP : https://pypi.org/project/PuLP/

Documentation
-------------

Documentation is found here_.

.. _here : https://vrpy.readthedocs.io/en/latest/

Running the tests
-----------------

Unit Tests
~~~~~~~~~~

.. code:: sh

	cd tests
	pytest unittests/


Bugs
----

Please report any bugs that you find in the issues_ section. Or, even better, fork the repository on GitHub_ and create a pull request. Any contributions are welcome.

.. _issues : https://github.com/Kuifje02/vrpy/issues
.. _GitHub : https://github.com/Kuifje02/vrpy 