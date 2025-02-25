import pybullet as p
import pyrosim.pyrosim as pyrosim
import numpy as np
import constants as c

class MOTOR:
    def __init__(self, jointName):
        self.jointName = jointName
        self.Prepare_To_Act()

    def Prepare_To_Act(self):
        self.motorValues = np.zeros(c.num_iterations)
        self.amplitude = c.amplitude
        self.frequency = c.frequency
        self.phaseOffset = c.phaseOffset

        if self.jointName == "Torso_BackLeg":
            self.frequency = self.frequency * 0.5
        x = np.linspace(0, 2 * np.pi, c.num_iterations)
        self.motorValues = self.amplitude * np.sin(self.frequency * x + self.phaseOffset)
        
    def Set_Value(self, robotId, i):
        pyrosim.Set_Motor_For_Joint(
            bodyIndex = robotId,
            jointName = self.jointName,
            controlMode = p.POSITION_CONTROL,
            targetPosition = self.motorValues[i],
            maxForce = c.maxForce
        )

    def Save_Values(self):
        np.save('data/motorValues.npy', self.motorValues)