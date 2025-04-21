import numpy as np

num_iterations = 10000

num_generations = 50
populationSize = 10

# Test A
numSensorNeurons = 11
numMotorNeurons = 10
# Test B
# numSensorNeurons = 7
# numMotorNeurons = 6

motorJointRange = 0.75

time_step = [1/30, 1/60, 1/240]

maxForce = 100

amplitude = np.pi / 4.0
frequency = 25
phaseOffset = np.pi / 8.0