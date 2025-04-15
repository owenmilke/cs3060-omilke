import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import numpy as np
import constants as c

phc = PARALLEL_HILL_CLIMBER()

phc.Evolve()
phc.Show_Best()

print("\nSimulation complete.")