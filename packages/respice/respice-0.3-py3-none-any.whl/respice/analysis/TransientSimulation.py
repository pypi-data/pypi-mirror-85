from threading import Event, RLock
from typing import Hashable, Union, Iterable, Collection, Optional, List

import numpy as np

from respice.collections import OneToManyInvertibleMapping
from respice.components import Component, Branch, SwitchBranch


class TransientSimulation:
    class _LockedOperationsInterface:
        def __init__(self, parent):
            self._parent = parent

        @property
        def ts(self):
            return self._parent._ts

        @property
        def node_potentials(self):
            return self._parent._node_potentials

        @property
        def branch_voltages(self):
            return self._parent._branch_voltages

        @property
        def branch_currents(self):
            return self._parent._branch_currents

        @property
        def component_states(self):
            return self._parent._component_states

        @property
        def switch_states(self):
            return self._parent._switch_states

        def extend_from_simulation(self, simulation):
            self.ts.extend(simulation.get_timesteps())
            for node in self._parent._nodes:
                self.node_potentials[node].extend(simulation.get_potentials(node))
            for branch in self._parent._components_to_branches.reverse:
                self.branch_voltages[branch].extend(simulation.get_voltages(branch))
                self.branch_currents[branch].extend(simulation.get_currents(branch))
                if isinstance(branch, SwitchBranch):
                    self.switch_states[branch].extend(simulation.get_switch_states(branch))
            for component in self._parent._components_to_branches:
                self.component_states[component].extend(simulation.get_states(component))

    def __init__(self,
                 ts1: float,
                 ts2: float,
                 components_to_branches: OneToManyInvertibleMapping,
                 nodes: Iterable[Hashable]):

        self._ts1 = ts1
        self._ts2 = ts2

        self._components_to_branches = OneToManyInvertibleMapping(components_to_branches)
        self._nodes = list(nodes)
        self._ts = []
        self._node_potentials = {node: [] for node in self._nodes}
        self._branch_voltages = {branch: [] for branch in components_to_branches.reverse}
        self._branch_currents = {branch: [] for branch in components_to_branches.reverse}
        self._component_states = {component: [] for component in components_to_branches}
        self._switch_states = {branch: []
                               for branch in components_to_branches.reverse
                               if isinstance(branch, SwitchBranch)}

        self._modification_lock = RLock()
        self._finished = Event()
        self._cancelled = Event()
        self._aborted = Event()
        self._exception = None

    def __enter__(self) -> _LockedOperationsInterface:
        """
        Acquire the *modification lock*.

        :return:
            A view into the object data allowing direct, thread-safe modifications.
        """
        self._modification_lock.acquire()
        if self._finished.is_set():
            self._modification_lock.release()
            raise RuntimeError('modifications after the simulation has finished are prohibited')
        return self._LockedOperationsInterface(self)

    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Releases the modification lock.
        """
        self._modification_lock.release()

    def finish(self):
        """
        Signals the simulation to be finished.

        This function shouldn't be used from user perspective but is intended to be used from inside the simulation
        implementations.
        """
        with self._modification_lock:
            # Optimize inner fields for performance (e.g. convert lists to numpy arrays).
            self._ts = np.fromiter(self._ts, dtype=float)
            self._node_potentials = {node: np.fromiter(data, dtype=float) for node, data in self._node_potentials.items()}
            self._branch_voltages = {branch: np.fromiter(data, dtype=float) for branch, data in self._branch_voltages.items()}
            self._branch_currents = {branch: np.fromiter(data, dtype=float) for branch, data in self._branch_currents.items()}
            self._switch_states = {switch: np.fromiter(data, dtype=bool) for switch, data in self._switch_states.items()}

            self._finished.set()

    def cancel(self):
        """
        Cancels an ongoing simulation.

        If the simulation has finished or is about to be finished, this function has no effect except still
        setting `is_cancelled` to `True`.
        """
        self._cancelled.set()
        self._finished.set()

    @property
    def is_cancelled(self) -> bool:
        """
        Determines whether the simulation was cancelled.
        """
        return self._cancelled.is_set()

    def abort(self, ex: Exception):
        """
        Aborts the simulation due to an error.

        This function shouldn't be used from user perspective but is intended to be used from inside the simulation
        implementations.

        :param ex:
            Exception that occurred causing the simulatino to abort.
        """
        self._exception = ex
        self._aborted.set()
        self._finished.set()

    @property
    def is_aborted(self) -> bool:
        """
        Determines whether the simulation was aborted due to an error.
        """
        return self._aborted.is_set()

    def wait(self, timeout: Optional[float] = None) -> bool:
        """
        Wait for the simulation to finish.

        :param timeout:
            Timeout to wait. If `None`, blocks infinitely until result is ready.
        :return:
            `True` if the result is ready, `False` if not. Only meaningful when a timeout is given.
        """
        finished = self._finished.wait(timeout)
        if self._aborted.is_set():
            raise self._exception
        return finished

    def get_timesteps(self) -> np.ndarray:
        """
        Returns all discrete time steps simulated.
        """
        with self._modification_lock:
            return np.array(self._ts)

    t = get_timesteps  # Shorthand function

    def get_potentials(self, node: Hashable) -> np.ndarray:
        """
        Returns the calculated potentials at the given node.

        :param node:
            The node.
        """
        return np.array(self._node_potentials[node])

    def get_voltages(self, entity: Union[Component, Branch, Hashable], target_node: Hashable = None) -> np.ndarray:
        """
        Returns the solved voltages over a given entity.

        :param entity:
            Can be either:
            * a component (where `default_branch` must be set and not return `None` - e.g. two-terminal-components).
            * a branch.
            * a node.
        :param target_node:
            If `entity` is a (source) node, this parameter denotes the target node to get the voltages from in between.
        :return:
            The solved voltages measured in Volts in form of an `np.ndarray`.
        """
        if target_node is None:
            # Lookup by single component or branch.
            branch = entity.default_branch if isinstance(entity, Component) else entity

            with self._modification_lock:
                return np.array(self._branch_voltages[branch])
        else:
            # Lookup between nodes.
            with self._modification_lock:
                return self._node_potentials[target_node] - self._node_potentials[entity]

    v = get_voltages  # Shorthand function

    def get_currents(self, entity: Union[Component, Branch]) -> np.ndarray:
        """
        Returns the solved currents over a given entity.

        :param entity:
            Can be either:
            * a component (where `default_branch` must be set and not return `None` - e.g. two-terminal-components).
            * a branch.
        :return:
            The solved currents measured in Amperes in form of an `np.ndarray`.
        """
        branch = entity.default_branch if isinstance(entity, Component) else entity

        with self._modification_lock:
            return np.array(self._branch_currents[branch])

    i = get_currents  # Shorthand function

    def get_power(self, *entities: Union[Component, Branch]) -> np.ndarray:
        """
        Calculates power consumption over multiple components or branches.

        :param entities:
            (Multiple) entities to calculate power for. If a component is given, its default branch is taken.
        :return:
            The power measured in Watts.
        """
        with self._modification_lock:
            return sum(self.get_voltages(entity) * self.get_currents(entity)
                       for entity in entities)

    p = get_power  # Shorthand function

    def get_states(self, component: Component) -> List[np.ndarray]:
        """
        Returns the computed states of the component.

        :param component:
            The component.
        :return:
            The state vectors. Refer to each component type individually which entry means what state.
        """
        with self._modification_lock:
            return list(self._component_states[component])

    s = get_states  # Shorthand function

    def get_switch_states(self, switch: SwitchBranch) -> np.ndarray:
        """
        Returns the computed switch states during simulation.

        :param switch:
            The switch.
        :return:
            The switch states, an array with `bool`s.
        """
        with self._modification_lock:
            return np.array(self._switch_states[switch])

    def plot(self, *entities: Union[Component, Branch], features: Collection[str] = 'vip'):
        """
        Plots the result.

        Plotting waits until the full simulation is finished. Live-plotting is right now not supported.

        Uses Plotly to present graphs in your browser. Make sure to have it installed.

        :param entities:
            Optional specific entities to plot. If none are specified, all available are plotted.
            Branches as well as components can be specified. In case the component defines a valid `default_branch`,
            this branch's data will be plotted. If `default_branch` returns `None`, all associated branches of this
            component will be plotted.

            Duplicate branches are filtered properly and won't be plotted twice.
        :param features:
            What kind of plots to make. Must be an iterable made out of following values:
            * v: voltage plot
            * i: current plot
            * p: power plot
        """
        if not features:
            raise ValueError('no features specified')

        self.wait()

        # Determine necessary components and respective branches to plot.
        if entities:
            plotset = {}
            for entity in entities:
                if isinstance(entity, Component):
                    component = entity
                    plotset[component] = (self._components_to_branches[component]
                                          if component.default_branch is None else
                                          {component.default_branch})
                else:
                    branch = entity
                    plotset[self._components_to_branches.reverse[branch]] = branch
        else:
            plotset = self._components_to_branches

        from itertools import cycle

        try:
            from plotly.subplots import make_subplots
            from plotly.graph_objects import Scatter
            from plotly.express import colors
        except ImportError:
            raise RuntimeError('plotly not found! Please install before using this function.')

        fig = make_subplots(rows=len(features), cols=1, shared_xaxes=True)

        colorcycle = cycle(colors.qualitative.Plotly)

        for component, branches in plotset.items():
            color = next(colorcycle)
            for branch in branches:
                showlegend = True
                for i, feature in enumerate(features, start=1):
                    if feature == 'v':
                        get_solutions = self.get_voltages
                    elif feature == 'i':
                        get_solutions = self.get_currents
                    elif feature == 'p':
                        get_solutions = self.get_power
                    else:
                        raise ValueError(f'invalid feature: {feature}')

                    fig.append_trace(
                        Scatter(
                            x=self._ts,
                            y=get_solutions(branch),
                            legendgroup=str(component),
                            name=str(branch),
                            mode='lines',
                            line={'color': color},
                            showlegend=showlegend,
                        ),
                        row=i,
                        col=1,
                    )

                    showlegend = False

        # Update xaxis properties
        for i, feature in enumerate(features, start=1):
            if feature == 'v':
                title_text = 'voltage V [V]'
            elif feature == 'i':
                title_text = 'current I [A]'
            else:  # --> feature == 'p'
                title_text = 'power P [W]'

            fig.update_yaxes(row=i, col=1, title_text=title_text)

        fig.update_xaxes(row=len(features), col=1, title_text="time t [s]")
        fig.update_layout(title="Transient Simulation Results")

        fig.show()

    def save(self, filename: str):
        """
        Stores quickly simulation data inside the given circuit to CSV-format.

        This functions waits until the simulation is finished completely.

        :param filename:
            The filename to store the data in.
        """
        self.wait()

        data = [('t', self._ts)]

        # Additionally iterating over components sorts branches by component,
        # thus makes it easier for humans to read.
        for component in self._components_to_branches:
            for branch in self._components_to_branches[component]:
                data.append((f'v({str(branch)})', self.get_voltages(branch)))
                data.append((f'i({str(branch)})', self.get_currents(branch)))
                if isinstance(branch, SwitchBranch):
                    data.append((f'switchstate({str(branch)})',
                                 ['on' if ss else 'off' for ss in self.get_switch_states(branch)]))

            for i, state in enumerate(zip(*self.get_states(component)), start=1):
                data.append((f'state({str(component)})[{i}]', state))

        import csv
        with open(filename, 'w', newline='') as fl:
            w = csv.writer(fl)
            w.writerow(name for name, _ in data)
            w.writerows(zip(*(d for _, d in data)))

    def print_progress(self):
        try:
            import rich.progress
        except ImportError:
            raise RuntimeError('rich not found! Please install before using this function.')

        progress = rich.progress.Progress(
            '[progress.description]{task.description}',
            rich.progress.BarColumn(),
            '[progress.percentage]{task.percentage:>3.1f}% ({task.completed}s/{task.total}s)',
            '•',
            'ETC',
            rich.progress.TimeRemainingColumn(),
            refresh_per_second=2,
        )

        total = self._ts2 - self._ts1
        with progress:
            task = progress.add_task(
                'simulate',
                total=total,
                completed=self._ts[-1] - self._ts1 if len(self._ts) > 0 else 0.0,
            )

            while not self._finished.wait(0.5):
                progress.update(task, completed=self._ts[-1] - self._ts1 if len(self._ts) > 0 else 0.0)

            progress.update(task, completed=total)
