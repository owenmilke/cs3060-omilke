import pyrosim.pyrosim as pyrosim

def Create_World():
    pyrosim.Start_SDF("world.sdf")
    pyrosim.Send_Cube(name=f"Box", pos=[2, 2, 0.5], size=[1, 1, 1])
    pyrosim.End()

def Create_Robot():
    pyrosim.Start_URDF("body.urdf")

    pyrosim.Send_Cube(name=f"Torso", pos=[0, 0, 1.5], size=[1, 1, 1])

    pyrosim.Send_Joint(name="Torso_BackLeg", parent="Torso", child="BackLeg", type="revolute", position=[0.5, 0, 1])
    pyrosim.Send_Cube(name=f"BackLeg", pos=[0.5, 0, -0.5], size=[1, 1, 1])

    pyrosim.Send_Joint(name="Torso_FrontLeg", parent="Torso", child="FrontLeg", type="revolute", position=[-0.5, 0, 1])
    pyrosim.Send_Cube(name=f"FrontLeg", pos=[-0.5, 0, -0.5], size=[1, 1, 1])

    pyrosim.End()

Create_World()
Create_Robot()