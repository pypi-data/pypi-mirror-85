from dataclasses import dataclass
from math import exp, log

from .TwoTerminalCurrentComponent import TwoTerminalCurrentComponent


@dataclass(eq=False)
class LinearizedShockleyDiode(TwoTerminalCurrentComponent):
    """
    Describes an ideal Shockley Diode, linearized after a certain voltage `V_L`.

    Additionally to https://en.wikipedia.org/wiki/Diode_modelling#Shockley_diode_model, for better convergence this
    linearized diode model exists. Exponential terms grow too big too fast and often prevent convergence of the
    solution. A very accurate approximation can be made by linearizing the equations after a certain linearization
    threshold voltage where the curve only grows linearly. So if you encounter convergence problems because you
    have used diodes that are caused by overflow errors, this linearized model might want you want to use.

    For the pure ideal model, see `respice.components.ShockleyDiode`.

    i_s:
        Reverse bias saturation current (also known as leakage current).
        Depending on the material used, common values are
        * silicon diodes: usually between 10^-12 A and 10^-10 A (1uA to 100uA).
        * germanium diodes: about 10^-4 A (0.1mA)
    v_t:
        Thermal voltage V_T. For approximate room temperate 300K this value
        is 25.85mV (0.02585V). This is default.
    n:
        Ideality factor (also known as quality factor). By default 1.
    dv_l:
        The gradient at which the voltage is linearized.
    """
    i_s: float = 1e-12
    v_t: float = 0.02585
    n: float = 1.0
    dv_l: float = 10000.0

    @property
    def v_l(self):
        return log(self.dv_l * self.v_t / self.i_s) * self.v_t

    def get_current(self, v: float, t1: float, t2: float) -> float:
        return (self.i_s * (exp(v / (self.n * self.v_t)) - 1)
                if v <= self.v_l else
                self.get_current(self.v_l, t1, t2) + (v - self.v_l) * self.dv_l)

    def get_jacobian(self, v: float, t1: float, t2: float) -> float:
        return (self.i_s / (self.n * self.v_t) * exp(v / (self.n * self.v_t))
                if v <= self.v_l else
                self.dv_l)
