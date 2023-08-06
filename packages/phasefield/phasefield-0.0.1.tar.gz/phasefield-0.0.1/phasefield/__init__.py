from phasefield.stepper import PhaseStepper as PhaseStepper
from phasefield.ufl_phasefield import UflPhasefield as PhaseModel

try:
    import phasefield.useDune
except ImportError:
    pass
