from sensor import SENSOR
from motor import MOTOR
import pybullet as p
import pyrosim.pyrosim as pyrosim
from pyrosim.neuralNetwork import NEURAL_NETWORK
import constants as c
import os
import numpy as np

class ROBOT:
    def __init__(self, solutionID):
        self.solutionID = solutionID
        self.sensors = {}
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")
        self.nn = NEURAL_NETWORK("brain" + str(self.solutionID) + ".nndf")
        os.system("rm brain" + str(self.solutionID) + ".nndf")
        pyrosim.Prepare_To_Simulate(self.robotId)
        self.Prepare_To_Sense()
        self.Prepare_To_Act()

    def Prepare_To_Sense(self):
        for linkName in pyrosim.linkNamesToIndices:
            self.sensors[linkName] = SENSOR(linkName)

    def Sense(self, i):
        for sensor in self.sensors:
            self.sensors[sensor].Get_Value(i)

    def Prepare_To_Act(self):
        for jointName in pyrosim.jointNamesToIndices:
            self.motors[jointName] = MOTOR(jointName)

    def Act(self, i):
        for neuronName in self.nn.Get_Neuron_Names():
            if self.nn.Is_Motor_Neuron(neuronName):
                jointName = self.nn.Get_Motor_Neurons_Joint(neuronName)
                desiredAngle = self.nn.Get_Value_Of(neuronName) * c.motorJointRange
                self.motors[jointName].Set_Value(self.robotId, desiredAngle)

    def Think(self):
        self.nn.Update()
        #self.nn.Print()

    # def Get_Fitness(self):
    #     stateOfLinkZero = p.getLinkState(self.robotId, 0)
    #     positionOfLinkZero = stateOfLinkZero[0]
    #     xCoordinateOfLinkZero = positionOfLinkZero[0]
    #     zCoordinateOfLinkZero = positionOfLinkZero[2]

    #     fitness = xCoordinateOfLinkZero * max(0, zCoordinateOfLinkZero - 1.0)

    #     with open("tmp" + str(self.solutionID) + ".txt", "w") as f:
    #         f.write(str(fitness))
    #     os.system("mv tmp" + str(self.solutionID) + ".txt fitness" + str(self.solutionID) + ".txt")

    # def Get_Fitness(self):
    #     # Get torso position (for forward movement reward)
    #     torso_state = p.getLinkState(self.robotId, 0)
    #     x_position = torso_state[0][0]  # x-coordinate of the torso
    #     z_position = torso_state[0][2]  # z-coordinate (height) of the torso

    #     # Penalize if non-foot links touch the ground
    #     penalty = 0.0
    #     foot_links = ["LeftFoot", "RightFoot"]  # Links allowed to touch the ground
    #     for linkName, sensor in self.sensors.items():
    #         if linkName not in foot_links:
    #             # Sum all sensor values (touch) for non-foot links
    #             penalty += np.sum(sensor.sensorValues)  # Penalize heavily if non-foot touches ground

    #     # Fitness = Forward movement - Penalty for non-foot contact (+ optional height reward)
    #     fitness = x_position - penalty * 10.0  # Weight penalty heavily (e.g., *10)

    #     # Optional: Add reward for keeping torso upright (height)
    #     fitness += max(0, z_position - 1.0)  # Reward if torso stays above 1.0m

    #     # Save fitness
    #     with open("tmp" + str(self.solutionID) + ".txt", "w") as f:
    #         f.write(str(fitness))
    #     os.system("mv tmp" + str(self.solutionID) + ".txt fitness" + str(self.solutionID) + ".txt")

    def Get_Fitness(self):
        # Get torso position (x, y, z)
        torso_state = p.getLinkState(self.robotId, 0)
        x_position = torso_state[0][0]  # Forward movement (reward this)
        y_position = torso_state[0][1]  # Sideways movement (penalize this)
        z_position = torso_state[0][2]  # Height (reward if upright)

        # Penalize non-foot ground contact
        penalty = 0.0
        foot_links = ["LeftFoot", "RightFoot"]
        for linkName, sensor in self.sensors.items():
            if linkName not in foot_links:
                penalty += np.sum(sensor.sensorValues)

        # Penalize sideways movement (encourage straight-line walking)
        lateral_penalty = abs(y_position) * 2.0  # Weight for y-drift (adjust as needed)

        # Fitness = Forward movement - Penalties
        fitness = (
            x_position                # Reward moving forward
            - penalty * 10.0          # Penalize falling (non-foot contact)
            - lateral_penalty         # Penalize sideways drift
            + max(0, z_position - 1.0)  # Optional: Reward keeping torso upright
        )

        # Debug print (optional)
        print(f"Robot {self.solutionID} - Fitness: {fitness:.2f} (Forward: {x_position:.2f}, Lateral Penalty: {lateral_penalty:.2f}, Fall Penalty: {penalty:.2f})")

        # Save fitness
        with open("tmp" + str(self.solutionID) + ".txt", "w") as f:
            f.write(str(fitness))
        os.system("mv tmp" + str(self.solutionID) + ".txt fitness" + str(self.solutionID) + ".txt")