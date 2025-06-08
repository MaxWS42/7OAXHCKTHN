import random as rand
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import math as m
import vpython as vp
from vpython import *

radii = [50, 250, 450, 650, 850, 1050, 1250]
#find the area of each ring
#maximise area taken up by nodes within each ring?

for a in range(len(radii)):
    Ring = plt.Circle(( 0 , 0 ), radii[0])
    
class Node:
    def __init__(self):
        pass

    def residential(self):
        node_max_occupancy = [50, 100, 250, 1000]
        self.occupancy = rand.randrange(4,1000)
        self.capacity = rand.choices(node_max_occupancy, [0.5, 0.3, 0.15, 0.05])[0] #smaller houses are cheaper so are more weighted,
        self.node_size = m.floor((int(self.capacity)*(25/m.pi))**0.5)
        
    def hospital(self):
        self.node_size = m.floor((75*25/m.pi)**0.5) #hospital size is fixed
        self.working_radius = 50 #placeholder value
        self.treatment_capacity = 50 #placeholder value
    
n1 = Node()
n1.residential()

dome_count = 500
domes = []

#home generator
for i in range(dome_count):
    home = Node()
    home.residential()
    domes.append(home)

###new bit from chatgpt###

# --- placement parameters ---
placed = []                      # list of (x, z, r) for already‐placed nodes
MAX_TRIES = 1000                 # give up after this many attempts per dome

#sort domes largest‐first for greedy packing
domes_sorted = sorted(domes, key=lambda d: d.node_size, reverse=True) 

#place each dome in the first ring where it fits (greedy) ---
for dome in domes_sorted:                                                
    r_new = dome.node_size

    #try rings in ascending order until placement succeeds
    for ring_idx in range(len(radii) - 1):                                
        R1, R2 = radii[ring_idx], radii[ring_idx + 1]                    

        for attempt in range(MAX_TRIES):                                  
            θ = rand.random() * 2 * m.pi
            ρ = rand.uniform(R1 + r_new, R2 - r_new)
            x, z = ρ * m.cos(θ), ρ * m.sin(θ)

            # reject if overlapping any existing node
            if all(m.hypot(x - xi, z - zi) >= (r_new + ri) 
                   for xi, zi, ri in placed):                            
                dome.x, dome.z = x, z                                     
                placed.append((x, z, r_new))                             
                break                                                  

        # if we placed successfully, stop trying further rings
        if hasattr(dome, 'x'):                                           
            break                                                       

#3d stuff
#ground = box(pos=vector(0,-2.5,0), size=vector(2000,0.2,2000), color=color.red) 
ground = cylinder(pos=vector(0,-2.5,0), radius=(radii[-1]+100), up=vector(1,0,0), color=color.red)

for i in range(len(placed)):
    dome = sphere(pos=vector(placed[i][0], 0,placed[i][1]), radius=placed[i][2], color=color.cyan)

while True:
    rate(30)