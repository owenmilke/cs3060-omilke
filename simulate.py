from simulation import SIMULATION
import sys
import numpy as np
import constants as c
import os

directOrGUI = sys.argv[1]
solutionID = sys.argv[2]

simulation = SIMULATION(directOrGUI, solutionID)
simulation.Run()

# Save sensor data for this robot
sensor_matrix = np.zeros((c.num_iterations, len(simulation.robot.sensors)))
for i, (sensor_name, sensor) in enumerate(simulation.robot.sensors.items()):
    sensor_matrix[:, i] = sensor.sensorValues
    
temp_sensor_file = f'sensor_values_{solutionID}.npy'
np.save(temp_sensor_file, sensor_matrix)

simulation.Get_Fitness()

# Clean up if this is a DIRECT simulation (not the final GUI one)
if directOrGUI == "DIRECT":
    if os.path.exists(temp_sensor_file):
        os.remove(temp_sensor_file)