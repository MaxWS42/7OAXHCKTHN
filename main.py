import random as rand
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
import math as m
import scipy as sp
import pandas as p

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
        self.working_radius = 50 #placeholder value
        self.treatment_capacity = 50 #placeholder value
    
n1 = Node()
n1.residential()

dome_count = 1000
domes = []

#home generator
for i in range(dome_count):
    home = Node()
    home.residential()
    domes.append(home)

###new bit from chatgpt###

# --- placement parameters ---
placed = []                      # list of (x, y, r) for already‐placed nodes
MAX_TRIES = 1000                 # give up after this many attempts per dome

#sort domes largest‐first for greedy packing
domes_sorted = sorted(domes, key=lambda d: d.node_size, reverse=True) 

# --- place each dome in the first ring where it fits (greedy) ---
for dome in domes_sorted:                                                
    r_new = dome.node_size

    # **CHANGED**: try rings in ascending order until placement succeeds
    for ring_idx in range(len(radii) - 1):                                
        R1, R2 = radii[ring_idx], radii[ring_idx + 1]                    

        for attempt in range(MAX_TRIES):                                  
            θ = rand.random() * 2 * m.pi
            ρ = rand.uniform(R1 + r_new, R2 - r_new)
            x, y = ρ * m.cos(θ), ρ * m.sin(θ)

            # reject if overlapping any existing node
            if all(m.hypot(x - xi, y - yi) >= (r_new + ri) 
                   for xi, yi, ri in placed):                            
                dome.x, dome.y = x, y                                     
                placed.append((x, y, r_new))                             
                break                                                  

        # if we placed successfully, stop trying further rings
        if hasattr(dome, 'x'):                                           
            break                                                       

# --- finally, plot rings and nodes (unchanged) ---
fig, ax = plt.subplots()
for R in radii:
    ax.add_patch(plt.Circle((0, 0), R, fill=False, linestyle='--'))

for x, y, r in placed:
    ax.add_patch(plt.Circle((x, y), r, alpha=0.5))

ax.set_aspect('equal')
ax.set_xlim(-radii[-1], radii[-1])
ax.set_ylim(-radii[-1], radii[-1])
plt.show()
