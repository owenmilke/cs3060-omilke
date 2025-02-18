import pybullet as p
import pybullet_data
import time
import pyrosim.pyrosim as pyrosim
import numpy as np
import random

physicsClient = p.connect(p.GUI)
p.setAdditionalSearchPath(pybullet_data.getDataPath())
p.configureDebugVisualizer(p.COV_ENABLE_GUI,0)

p.setGravity(0,0,-9.8,physicsClient)
planeId = p.loadURDF("plane.urdf")
robotId = p.loadURDF("body.urdf")
p.loadSDF("world.sdf")

pyrosim.Prepare_To_Simulate(robotId)
backLegSensorValues = np.zeros(1000)
frontLegSensorValues = np.zeros(1000)

amplitudeBackLeg = np.pi / 5
frequencyBackLeg = (np.pi * 4) / 50
phaseOffsetBackLeg = np.pi / 8

amplitudeFrontLeg = np.pi / 5
frequencyFrontLeg = (np.pi * 4) / 50
phaseOffsetFrontLeg = 0

backLegAngles = np.zeros(1000)
frontLegAngles = np.zeros(1000)

for i in range(1000):
    backLegAngles[i] = amplitudeBackLeg * np.sin(frequencyBackLeg * i + phaseOffsetBackLeg)
    frontLegAngles[i] = amplitudeFrontLeg * np.sin(frequencyFrontLeg * i + phaseOffsetFrontLeg)
np.save("data/backLegAngles.npy", backLegAngles)
np.save("data/frontLegAngles.npy", frontLegAngles)

for i in range(1000):
    p.stepSimulation()
    backLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("BackLeg")
    frontLegSensorValues[i] = pyrosim.Get_Touch_Sensor_Value_For_Link("FrontLeg")
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_BackLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = backLegAngles[i],
        maxForce = 100
    )
    pyrosim.Set_Motor_For_Joint(
        bodyIndex = robotId,
        jointName = "Torso_FrontLeg",
        controlMode = p.POSITION_CONTROL,
        targetPosition = frontLegAngles[i],
        maxForce = 100
    )
    time.sleep(1/60)

np.save("data/backLegSensorValues.npy", backLegSensorValues)
np.save("data/frontLegSensorValues.npy", frontLegSensorValues)

p.disconnect()