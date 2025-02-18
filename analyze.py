import numpy as np
import matplotlib.pyplot as plt

backLegSensorValues = np.load("data/backLegSensorValues.npy")
frontLegSensorValues = np.load("data/frontLegSensorValues.npy")
backLegAngles = np.load("data/backLegAngles.npy")
frontLegAngles = np.load("data/frontLegAngles.npy")

# plt.plot(backLegSensorValues, label="backLeg", linewidth=5)
# plt.plot(frontLegSensorValues, label="frontLeg")

plt.plot(backLegAngles, label="backLegAngles")
plt.plot(frontLegAngles, label="frontLegAngles")
plt.legend()
plt.title("Motor Commands")
plt.xlabel("Steps")
plt.ylabel("Value in Radians")
plt.show()