import numpy as np

num_iterations = 1000

num_generations = 10
populationSize = 10
numSensorNeurons = 4
numMotorNeurons = 8
motorJointRange = 0.2

time_step = [1/30, 1/60, 1/240]

maxForce = 100

amplitude = np.pi / 4.0
frequency = 25
phaseOffset = np.pi / 8.0