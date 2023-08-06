from .TransientSimulationResult import TransientSimulationResult


class TransientSteadyStateSimulationResult(TransientSimulationResult):
    def get_steadystate(self, component):
        return self.get_states(component)[0]
