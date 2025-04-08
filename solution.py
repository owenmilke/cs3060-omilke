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

        # Base height to prevent spawning inside ground
        base_height = 2.65

        # Torso
        pyrosim.Send_Cube(name="Torso", pos=[0.5, 0, base_height], size=[1.15, 0.5, 1.25])

        # === ARMS ===
        # Left Shoulder
        pyrosim.Send_Joint(name="Torso_LeftShoulder", parent="Torso", child="LeftShoulder", 
                        type="revolute", position=[0, 0, base_height + 0.25], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftShoulder", pos=[-0.25, 0, 0], size=[0.5, 0.25, 0.25])

        # Left Arm
        pyrosim.Send_Joint(name="LeftShoulder_LeftArm", parent="LeftShoulder", child="LeftArm", 
                        type="revolute", position=[-0.6, 0, 0], jointAxis="0 0 1")
        pyrosim.Send_Cube(name="LeftArm", pos=[-0.25, 0, 0], size=[0.75, 0.25, 0.25])

        # Right Shoulder
        pyrosim.Send_Joint(name="Torso_RightShoulder", parent="Torso", child="RightShoulder", 
                        type="revolute", position=[1, 0, base_height + 0.25], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightShoulder", pos=[0.25, 0, 0], size=[0.5, 0.25, 0.25])

        # Right Arm
        pyrosim.Send_Joint(name="RightShoulder_RightArm", parent="RightShoulder", child="RightArm", 
                        type="revolute", position=[0.6, 0, 0], jointAxis="0 0 1")
        pyrosim.Send_Cube(name="RightArm", pos=[0.25, 0, 0], size=[0.75, 0.25, 0.25])

        # === LEGS ===
        # Left Leg
        pyrosim.Send_Joint(name="Torso_LeftLeg", parent="Torso", child="LeftLeg", 
                        type="revolute", position=[0.15, 0, base_height - 0.625], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftLeg", pos=[0, 0, -0.375], size=[0.5, 0.25, 0.75])

        # Right Leg
        pyrosim.Send_Joint(name="Torso_RightLeg", parent="Torso", child="RightLeg", 
                        type="revolute", position=[0.85, 0, base_height - 0.625], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightLeg", pos=[0, 0, -0.375], size=[0.5, 0.25, 0.75])

        # Knees
        pyrosim.Send_Joint(name="LeftLeg_LeftKnee", parent="LeftLeg", child="LeftKnee", 
                        type="revolute", position=[0, 0, -0.75], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="LeftKnee", pos=[0, 0, -0.5], size=[0.5, 0.25, 1.0])

        pyrosim.Send_Joint(name="RightLeg_RightKnee", parent="RightLeg", child="RightKnee", 
                        type="revolute", position=[0, 0, -0.75], jointAxis="1 0 0")
        pyrosim.Send_Cube(name="RightKnee", pos=[0, 0, -0.5], size=[0.5, 0.25, 1.0])

        # Feet
        pyrosim.Send_Joint(name="LeftKnee_LeftFoot", parent="LeftKnee", child="LeftFoot", 
                        type="revolute", position=[0, 0, -1.0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="LeftFoot", pos=[0, 0, -0.125], size=[0.5, 0.5, 0.25])

        pyrosim.Send_Joint(name="RightKnee_RightFoot", parent="RightKnee", child="RightFoot", 
                        type="revolute", position=[0, 0, -1.0], jointAxis="0 1 0")
        pyrosim.Send_Cube(name="RightFoot", pos=[0, 0, -0.125], size=[0.5, 0.5, 0.25])

        pyrosim.End()

    def Create_Brain(self):
        pyrosim.Start_NeuralNetwork("brain" + str(self.myID) + ".nndf")

        # === SENSOR NEURONS ===
        pyrosim.Send_Sensor_Neuron(name=0, linkName="Torso")
        pyrosim.Send_Sensor_Neuron(name=1, linkName="LeftShoulder")
        pyrosim.Send_Sensor_Neuron(name=2, linkName="RightShoulder")
        pyrosim.Send_Sensor_Neuron(name=3, linkName="LeftArm")
        pyrosim.Send_Sensor_Neuron(name=4, linkName="RightArm")
        pyrosim.Send_Sensor_Neuron(name=5, linkName="LeftLeg")
        pyrosim.Send_Sensor_Neuron(name=6, linkName="RightLeg")
        pyrosim.Send_Sensor_Neuron(name=7, linkName="LeftKnee")
        pyrosim.Send_Sensor_Neuron(name=8, linkName="RightKnee")
        pyrosim.Send_Sensor_Neuron(name=9, linkName="LeftFoot")
        pyrosim.Send_Sensor_Neuron(name=10, linkName="RightFoot")

        # === MOTOR NEURONS ===
        pyrosim.Send_Motor_Neuron(name=11, jointName="Torso_LeftShoulder")
        pyrosim.Send_Motor_Neuron(name=12, jointName="LeftShoulder_LeftArm")
        pyrosim.Send_Motor_Neuron(name=13, jointName="Torso_RightShoulder")
        pyrosim.Send_Motor_Neuron(name=14, jointName="RightShoulder_RightArm")
        pyrosim.Send_Motor_Neuron(name=15, jointName="Torso_LeftLeg")
        pyrosim.Send_Motor_Neuron(name=16, jointName="Torso_RightLeg")
        pyrosim.Send_Motor_Neuron(name=17, jointName="LeftLeg_LeftKnee")
        pyrosim.Send_Motor_Neuron(name=18, jointName="RightLeg_RightKnee")
        pyrosim.Send_Motor_Neuron(name=19, jointName="LeftKnee_LeftFoot")
        pyrosim.Send_Motor_Neuron(name=20, jointName="RightKnee_RightFoot")

        # === SYNAPSES (simple mapping: sensor to corresponding motor) ===
        pyrosim.Send_Synapse(sourceNeuronName=1, targetNeuronName=11, weight=-0.5)
        pyrosim.Send_Synapse(sourceNeuronName=3, targetNeuronName=12, weight=-0.5)

        pyrosim.Send_Synapse(sourceNeuronName=2, targetNeuronName=13, weight=-0.5)
        pyrosim.Send_Synapse(sourceNeuronName=4, targetNeuronName=14, weight=-0.5)

        pyrosim.Send_Synapse(sourceNeuronName=5, targetNeuronName=15, weight=-1.0)
        pyrosim.Send_Synapse(sourceNeuronName=6, targetNeuronName=16, weight=-1.0)

        pyrosim.Send_Synapse(sourceNeuronName=7, targetNeuronName=17, weight=-1.0)
        pyrosim.Send_Synapse(sourceNeuronName=8, targetNeuronName=18, weight=-1.0)

        pyrosim.Send_Synapse(sourceNeuronName=9, targetNeuronName=19, weight=-1.0)
        pyrosim.Send_Synapse(sourceNeuronName=10, targetNeuronName=20, weight=-1.0)

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