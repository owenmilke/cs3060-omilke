import numpy as np
import random
import os
import time
import pyrosim.pyrosim as pyrosim
import constants as c

class SOLUTION:
    def __init__(self, nextAvailableID):
        self.myID = nextAvailableID
        self.weights = np.array(
            [[np.random.rand() for i in range(c.numMotorNeurons)] for j in range(c.numSensorNeurons)]
        )
        self.weights = (self.weights * 2) - 1

    def Start_Simulation(self, directOrGUI):
        self.Create_World()
        self.Create_Body()
        self.Create_Brain()
        os.system("python3 simulate.py " + directOrGUI + " " + str(self.myID) + " 2&>1 &")

    def Wait_For_Simulation_To_End(self):
        while not os.path.exists("fitness" + str(self.myID) + ".txt"):
            time.sleep(0.01)
        with open("fitness" + str(self.myID) + ".txt", "r") as f:
            self.fitness = float(f.read())
        os.system("rm fitness" + str(self.myID) + ".txt")

    def Create_World(self):
        pyrosim.Start_SDF("world.sdf")
        pyrosim.Send_Cube(name="Box", pos=[2, 2, 0.5], size=[1, 1, 1])
        pyrosim.End()

    def Create_Body(self):
        pyrosim.Start_URDF("body.urdf")

        # Torso
        pyrosim.Send_Cube(name="Torso", pos=[1, 0, 2.25], size=[1, 0.5, 1.25])

        # Left Leg
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", type="revolute", position=[0.75, 0, 1.89], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[-0.25, 0, -1], size=[0.5, 0.5, 1.5])

        # Right Leg
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", type="revolute", position=[1.25, 0, 1.89], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0.25, 0, -1], size=[0.5, 0.5, 1.5])

        # Left Arm
        pyrosim.Send_Joint(name="Torso_LeftArm", parent="Torso", child="LeftArm", type="revolute", position=[0.5, 0, 2.875], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftArm", pos=[-0.25, 0, -0.375], size=[0.5, 0.25, 0.75])

        # Right Arm
        pyrosim.Send_Joint(name="Torso_RightArm", parent="Torso", child="RightArm", type="revolute", position=[1.5, 0, 2.875], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightArm", pos=[0.25, 0, -0.375], size=[0.5, 0.25, 0.75])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # Sensor Neurons
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftArm") 
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightArm")

        # Motor Neurons
        pyrosim.Send_Motor_Neuron(name=5, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=6, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=7, jointName="Torso_LeftArm") 
        pyrosim.Send_Motor_Neuron(name=8, jointName="Torso_RightArm")

        # Synapses
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=5, weight=-1.0)
        pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=6, weight=-1.0)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=7, weight=-0.5)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=8, weight=-0.5)


        for currentRow in range(c.numSensorNeurons):
            for currentColumn in range(c.numMotorNeurons):
                pyrosim.Send_Synapse(sourceNeuronName = currentRow, targetNeuronName = currentColumn + c.numSensorNeurons, weight = self.weights[currentRow][currentColumn])
        pyrosim.End()

    def Mutate(self):
        randomRow = random.randint(0, c.numSensorNeurons - 1)
        randomColumn = random.randint(0, c.numMotorNeurons - 1)
        self.weights[randomRow][randomColumn] = (random.random() * 2) - 1

    def Set_ID(self, id):
        self.myID = id