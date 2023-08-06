from ordered_set import OrderedSet


class DAESystem:
    def __init__(self):
        self._variables = OrderedSet()

    def add_variable(self):
        variable = object()
        self._variables.add(variable)
        return variable

    def get_variable_position(self, variable):
        return self._variables.index(variable)
