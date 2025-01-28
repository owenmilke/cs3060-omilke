import pyrosim.pyrosim as pyrosim

pyrosim.Start_SDF("boxes.sdf")

length = 1
width = 1
height = 1
x = 0
y = 0
z = 0.5

for i in range(5):
    for j in range(5):
        for k in range(10):
            new_x = x + i * length
            new_y = y + j * width
            new_z = z + k * (height + 0.5)
            
            new_length = length * (0.9 ** k)
            new_width = width * (0.9 ** k)
            new_height = height * (0.9 ** k)
            
            pyrosim.Send_Cube(name=f"Box", pos=[new_x, new_y, new_z], size=[new_length, new_width, new_height])

pyrosim.End()