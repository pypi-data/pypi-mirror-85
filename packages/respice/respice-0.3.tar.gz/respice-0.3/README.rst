respice
=======

Flexible and easy to use non-linear transient electric circuit simulator.

Install
-------

.. code:: bash

   pip3 install respice

Usage
-----

Create your circuit and simulate it!

.. code:: python

   from respice.analysis import Circuit
   from respice.components import CurrentSourceDC, R, C

   # Define components for our circuit.
   R1 = R(100)
   R2 = R(200)
   C3 = C(10e-6)
   R4 = R(200)
   R5 = R(100)
   Isrc = CurrentSourceDC(0.1)

   # Construct the circuit. All circuits are just
   # Digraphs allowing multiple edges. On each edge
   # one component.
   wheatstone_bridge = Circuit()
   wheatstone_bridge.add(R1, 0, 1)
   wheatstone_bridge.add(R2, 0, 2)
   wheatstone_bridge.add(C3, 1, 2)
   wheatstone_bridge.add(R4, 1, 3)
   wheatstone_bridge.add(R5, 2, 3)
   wheatstone_bridge.add(Isrc, 3, 0)

   # Simulate! From t1 = 0ms to t2 = 5ms with 100 steps.
   simulation = wheatstone_bridge.simulate(0, 0.005, 100)

The results are stored in the returned object and can be easily accessed
via ``simulation.v(component)``, ``simulation.i(component)`` or ``simulation.p(component)``.
Those contain the voltages, currents and powers respectively for each time step
as a list. The time steps can be accessed with ``simulation.t()``.

All simulations are asynchronous. Accessing results early may only give partial
results. Use ``simulation.wait()`` to wait until the result is ready.

Circuits are graphs (like mentioned in the snippet). More precisely, a
Digraph allowing multiple edges from and to the same nodes. Each edge
represents a single two-terminal component (like a resistor). Those are
connected to nodes, which are simple joints that can be arbitrarly named
or identified (for example numbers like in the example above, but
strings, or even other objects are possible if necessary).

Example Plotting
----------------

Results can be immediately plotted.
For plotting, ``plotly`` is required.

.. code:: python

   from respice.examples import RC

   # Define an example RC circuit. The package respice.examples
   # contains a few!
   rc = RC(100, 100e-6, 10)  # 100Ohm, 100uF, 10V
   simulation = rc.simulate(0, 0.1, 100)
   simulation.plot()

The plot function will wait automatically until the result is finished. Live-plotting
is not supported yet.

Supports
--------

- **MNA - Modified Nodal Analysis**

  This is the algorithm employed by this software. So it’s easily
  possible to handle voltages as well as currents.

- **Transient steady-state analysis**

  Find quickly periodic steady-state solutions of a circuit that appear
  when the circuit transients have settled.

- **Multi-terminal components**

  Components with more than just two terminals can be handled easily.
  Whether each sub-branch of them is a current- or voltage-branch, or
  whether they are current- or voltage-driven.

- **Mutual coupling**

  Usually required by multi-terminal components, mutual coupling is
  easily implementable. Each sub-branch in a component is automatically
  receiving the voltages and currents of all other branches comprising
  the component.

The Future
----------

- **Incorporating interfaces for heat-dynamics**

  Components are often depending on operation temperature. This can
  highly change behaviour of the whole circuit. Implementing new simulation variables like
  current component temperature could allow to simulate temperature influence. This
  is especially useful for safety analysis and estimating the maximum critical
  operation point.

  This might even serve as a general concept to introduce even more parameters
  besides heat that influence component performance and behaviour.

- **Enhancing components (maybe heat-dynamics coupled) to simulate breakage**

  Components can break. Either due to age, or because currents where to high. Consecutively
  extending components to contain "breakage-states" (so state variables that
  tell you if the element is destroyed or not) could improve analysis for circuits
  operating near critical operation points.
