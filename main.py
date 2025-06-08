import random as rand
import numpy as np
import math as m
import vpython as vp
from vpython import *
import matplotlib as plt

radii = [50, 250, 450, 650, 850, 1050, 1250]
#find the area of each ring
#maximise area taken up by nodes within each ring?

#for a in range(len(radii)):
 #   Ring = plt.Circle(( 0 , 0 ), radii[0]

# --- TOWER GENERATION --- heereee we are 
tower_width = 5
tower_height = 100

for radius in radii:
    for angle in [0, m.pi/2, m.pi, 3*m.pi/2]:  # E, N, W, S
        x = radius * m.cos(angle)
        z = radius * m.sin(angle)
        if x >= sum(radii):
            break

        tower = box(
            pos=vector(x, tower_height / 2, z),  # height/2 so base is on ground
            size=vector(tower_width, tower_height, tower_width),
            color=color.gray(0.5),
            texture=textures.stucco
        )
    
class Node:
    def __init__(self):
        pass

    def residential(self):
        node_max_occupancy = [rand.randint(10, 50), rand.randint(60, 170), rand.randint(200, 500), rand.randint(750, 1000)]
        self.occupancy = rand.randrange(4,1000)
        self.capacity = rand.choices(node_max_occupancy, [0.5, 0.3, 0.15, 0.05])[0] #smaller houses are cheaper so are more weighted,
        self.node_size = m.floor((int(self.capacity)*(25/m.pi))**0.5)
        self.type = 'residential'
        
    def hospital(self):
        self.node_size = m.floor((75*25/m.pi)**0.5) #hospital size is fixed
        self.working_radius = 50 #placeholder value
        self.treatment_capacity = 50 #placeholder value
        self.type = 'hospital'

    def school(self):
        self.node_size = m.floor((50 * 25 / m.pi) ** 0.5)
        self.capacity = 200
        self.type = 'school'
    
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
ground = cylinder(pos=vector(0,-2.5,0), radius=(radii[-1]+100), up=vector(1,0,0), color=color.orange, texture=textures.rock, shininess=0.1)

for i in range(len(placed)):
    dome = sphere(pos=vector(placed[i][0], 0,placed[i][1]), radius=placed[i][2], color=vector(0.8,0.8,0.8), texture=textures.metal)

while True:
    rate(30)