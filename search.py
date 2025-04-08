import os
from parallelHillClimber import PARALLEL_HILL_CLIMBER
import numpy as np
import constants as c

phc = PARALLEL_HILL_CLIMBER()

phc.Evolve()
phc.Show_Best()

# Load and print the best sensor values
try:
    best_sensor_data = np.load('best_sensor_values.npy')
    binary_sensor_data = (best_sensor_data > 0).astype(int)
    print("\nBest robot's sensor data:")

    # print(best_sensor_data)
    # Print sensor 0 values for all timesteps
    # print("Sensor 0 values:", best_sensor_data[:, 0])

    print("First 10 timesteps:")
    print(binary_sensor_data[:10])
    print("\nLast 10 timesteps):")
    print(binary_sensor_data[-10:])

     # Print summary statistics
    sensors = ["Torso", "LeftShoulder", "RightShoulder", "LeftArm", "RightArm",
               "LeftLeg", "RightLeg", "LeftKnee", "RightKnee", "LeftFoot", "RightFoot"]
    print("\nSensor activation summary (percentage of time active):")
    for sensor_idx in range(c.numSensorNeurons):
        activation_percent = 100 * np.mean(binary_sensor_data[:, sensor_idx])
        print(f"Sensor {sensors[sensor_idx]}: {activation_percent:.1f}%")

except FileNotFoundError:
    print("\nCould not find best_sensor_values.npy file")

print("\nSimulation complete.")