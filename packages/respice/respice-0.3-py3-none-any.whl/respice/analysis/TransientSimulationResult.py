import numpy as np

from respice.collections import OneToManyInvertibleMapping
from respice.components import Component


class TransientSimulationResult:
    def __init__(self,
                 components_to_branches,
                 mna_equation,
                 ts,
                 raw_solutions,
                 branch_solutions_v,
                 branch_solutions_i,
                 state_solutions):
        self._components_to_branches = OneToManyInvertibleMapping(components_to_branches)
        self._mna_equation = mna_equation
        self._ts = ts
        self._raw_solutions = raw_solutions
        self._branch_solutions_v = branch_solutions_v
        self._branch_solutions_i = branch_solutions_i
        self._state_solutions = state_solutions

    @classmethod
    def init_from(cls, sim):
        return cls(
            sim._components_to_branches,
            sim._mna_equation,
            sim._ts,
            sim._raw_solutions,
            sim._branch_solutions_v,
            sim._branch_solutions_i,
            sim._state_solutions,
        )

    def get_timesteps(self):
        return np.array(self._ts)

    t = get_timesteps  # Shorthand function

    def get_voltages(self, entity, target_node=None):
        """
        Returns the solved currents over a given entity.

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

            return np.array(self._branch_solutions_v[branch])
        else:
            # Lookup between nodes.
            return np.fromiter(
                (self._mna_equation.get_voltage_between_nodes(result, entity, target_node)
                 for result in self._raw_solutions),
                dtype=float,
            )

    v = get_voltages  # Shorthand function

    def get_currents(self, entity):
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

        return np.array(self._branch_solutions_i[branch])

    i = get_currents  # Shorthand function

    def get_power(self, *entities):
        return sum(self.get_voltages(entity) * self.get_currents(entity)
                   for entity in entities)

    p = get_power  # Shorthand function

    def get_states(self, component):
        return self._state_solutions[component]

    s = get_states  # Shorthand function

    def plot(self, *entities, features='vip', backend='matplotlib'):
        """
        Plots with a given backend package. Make sure to have the respective package installed.

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
        :param backend:
            A string denoting which backend/package to use for plotting. Available are:
            * matplotlib (default)
            * plotly
        """
        if not features:
            raise ValueError('no features specified')

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

        if backend == 'matplotlib':
            try:
                import matplotlib.pyplot as plot
            except ImportError:
                raise RuntimeError('matplotlib not found!')

            plot.figure('Transient Simulation Results')

            ref_axis = plot.subplot(len(features), 1, 1)
            for i, feature in enumerate(features, start=1):
                plot.subplot(len(features), 1, i, sharex=ref_axis)

                if feature == 'v':
                    plot.ylabel('voltage $V$ [V]')
                    get_solutions = self.get_voltages
                elif feature == 'i':
                    plot.ylabel('current $I$ [A]')
                    get_solutions = self.get_currents
                elif feature == 'p':
                    plot.ylabel('power $P$ [W]')
                    get_solutions = self.get_power
                else:
                    raise ValueError(f'invalid feature: {feature}')

                for component, branches in plotset.items():
                    for branch in branches:
                        plot.plot(self._ts, get_solutions(branch), label=str(branch))

                plot.grid()

            plot.xlabel('time $t$ [s]')
            plot.legend()

            plot.show()

        elif backend == 'plotly':
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

        else:
            raise ValueError(f'unsupported backend: {backend}')

    def save(self, filename):
        """
        Stores quickly simulation data inside the given circuit to CSV-format.

        :param filename:
            The filename to store the data in.
        """
        data = [('t', self._ts)]

        # Additionally iterating over components sorts branches by component,
        # thus makes it easier for humans to read.
        for component in self._components_to_branches:
            for branch in self._components_to_branches[component]:
                data.append((f'v({str(branch)})', self.get_voltages(branch)))
                data.append((f'i({str(branch)})', self.get_currents(branch)))

            for i, state in enumerate(zip(*self.get_states(component)), start=1):
                data.append((f'state({str(component)})[{i}]', state))

        import csv
        with open(filename, 'w', newline='') as fl:
            w = csv.writer(fl)
            w.writerow(name for name, _ in data)
            w.writerows(zip(*(d for _, d in data)))
