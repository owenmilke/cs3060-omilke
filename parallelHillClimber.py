from solution import SOLUTION
import constants as c
import copy
import os
import numpy as np
import time

class PARALLEL_HILL_CLIMBER:
    def __init__(self):
        self.Clean_Files()
        self.parents = {}
        self.nextAvailableID = 0
        for i in range(0, c.populationSize - 1):
            self.parents[i] = SOLUTION(self.nextAvailableID)
            self.nextAvailableID += 1
        self.best_sensor_data = None
        self.best_id = None

    def Clean_Files(self):
        os.system("rm -f brain*.nndf 2>/dev/null")
        os.system("rm -f fitness*.txt 2>/dev/null")
        os.system("rm -f sensor_values_*.npy 2>/dev/null")
        os.system("rm -f world.sdf 2>/dev/null")
        os.system("rm -f body.urdf 2>/dev/null")

    def Evolve(self):
        self.Evaluate(self.parents)
        for currentGeneration in range(c.num_generations):
            self.Evolve_For_One_Generation()
        self.Clean_Intermediate_Files()

    def Clean_Intermediate_Files(self):
        os.system("rm -f brain*.nndf 2>/dev/null")
        os.system("rm -f fitness*.txt 2>/dev/null")

    def Evolve_For_One_Generation(self):
        self.Spawn()
        self.Mutate()
        self.Evaluate(self.children)
        self.Print()
        self.Select()

    def Spawn(self):
        self.children = {}
        for i in range(len(self.parents)):
            self.children[i] = copy.deepcopy(self.parents[i])
            self.children[i].Set_ID(self.nextAvailableID)
            self.nextAvailableID += 1

    def Mutate(self):
        for i in range(len(self.children)):
            self.children[i].Mutate()

    def Select(self):
        for i in range(len(self.parents)):
            if self.parents[i].fitness < self.children[i].fitness:
                self.parents[i] = self.children[i]

    def Print(self):
        # for key in self.parents.keys():
        #     print("\nParent fitness:", self.parents[key].fitness, "| Child fitness:", self.children[key].fitness)
        pass
    
    def Show_Best(self):
        best_index = 0
        max_fitness = self.parents[0].fitness
        for i in range(len(self.parents)):
            if self.parents[i].fitness > max_fitness:
                max_fitness = self.parents[i].fitness
                best_index = i
        
        self.best_id = self.parents[best_index].myID
        print(f"\nBest Robot: #{self.best_id}")
        
        # First run the GUI simulation to generate new sensor data
        self.parents[best_index].Start_Simulation("GUI")
        self.Wait_For_GUI_Simulation_To_End()
        
        # Now load and save the sensor data from the GUI run
        sensor_file = f"sensor_values_{self.best_id}.npy"
        if os.path.exists(sensor_file):
            self.best_sensor_data = np.load(sensor_file)
            np.save("best_sensor_values.npy", self.best_sensor_data)
            os.remove(sensor_file)  # Clean up temporary file
        
        # Clean up any other remaining sensor files
        os.system("find . -name 'sensor_values_*.npy' -delete 2>/dev/null")

    def Wait_For_GUI_Simulation_To_End(self):
        # Wait for the simulation to create its fitness file
        fitness_file = f"fitness{self.best_id}.txt"
        while not os.path.exists(fitness_file):
            time.sleep(0.1)
        
        # Clean up the fitness file
        if os.path.exists(fitness_file):
            os.remove(fitness_file)

    def Evaluate(self, solutions):
        for i in range(len(solutions)):
            solutions[i].Start_Simulation("DIRECT")
        for i in range(len(solutions)):
            solutions[i].Wait_For_Simulation_To_End()

    def __del__(self):
        # Final cleanup when the object is destroyed
        self.Clean_Files()