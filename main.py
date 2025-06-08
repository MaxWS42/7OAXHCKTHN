import random as rand
import math as m
from vpython import *

target_position = vector(0, 0, 0)
scene.autoscale = False
scene.userzoom = False


scene.center = target_position
scene.range = 750
scene.forward = vector(-1,-1,-1).norm()

def create_icosahedron(pos, scale, color_val, opacity, shininess, edge_color=None, edge_thickness=None):
    import math
    phi = (1 + math.sqrt(5)) / 2

    # raw unit vertices
    base = [
        vector(-1,  phi, 0), vector( 1,  phi, 0),
        vector(-1, -phi, 0), vector( 1, -phi, 0),
        vector( 0, -1,  phi), vector( 0,  1,  phi),
        vector( 0, -1, -phi), vector( 0,  1, -phi),
        vector( phi,  0, -1), vector( phi,  0,  1),
        vector(-phi,  0, -1), vector(-phi,  0,  1),
    ]
    # scale & move into place
    verts = [v.norm()*scale + pos for v in base]

    # all 20 triangular faces by index
    faces = [
        (0,11,5), (0,5,1), (0,1,7), (0,7,10), (0,10,11),
        (1,5,9), (5,11,4), (11,10,2), (10,7,6), (7,1,8),
        (3,9,4), (3,4,2), (3,2,6), (3,6,8), (3,8,9),
        (4,9,5), (2,4,11), (6,2,10), (8,6,7), (9,8,1)
    ]

    tris = []
    drawn = set()
    for a,b,c in faces:
        # face
        tris.append(triangle(
            v0=vertex(pos=verts[a], color=color_val, opacity=opacity),
            v1=vertex(pos=verts[b], color=color_val, opacity=opacity),
            v2=vertex(pos=verts[c], color=color_val, opacity=opacity),
            shininess=shininess
        ))
        # optional edges
        if edge_color and edge_thickness:
            for u,v in ((a,b),(b,c),(c,a)):
                e = tuple(sorted((u,v)))
                if e in drawn: continue
                drawn.add(e)
                p1,p2 = verts[u], verts[v]
                cylinder(pos=p1, axis=p2-p1, radius=edge_thickness, color=edge_color)

    return compound(tris)

  
radii = [50, 250, 450, 650, 850, 1050, 1250]
#find the area of each ring
#maximise area taken up by nodes within each ring?
def arch_ring_cylinders(radius, arch_count, hoop_height=70, segments=30, thickness=1):
    """
    Draws parabolic arch segments using cylinders instead of boxes.
    Each arch connects from y=0 to the next base point, peaking at hoop_height.
    """
    for i in range(arch_count):
        theta0 = 2 * m.pi * i / arch_count
        theta1 = 2 * m.pi * (i + 1) / arch_count

        prev_point = None

        for j in range(segments + 1):
            t = j / segments
            theta = (1 - t) * theta0 + t * theta1

            # Ring position
            x = radius * m.cos(theta)
            z = radius * m.sin(theta)

            # Parabolic height profile
            y = -4 * hoop_height * (t - 0.5) ** 2 + hoop_height

            current = vector(x, y, z)

            if prev_point is not None:
                axis = current - prev_point
                cylinder(
                    pos=prev_point,
                    axis=axis,
                    radius=thickness,
                    color=color.white,
                    opacity=0.6,
                    shininess=0.9
                )

            prev_point = current

def cardinal_spokes(max_radius, y=0, thickness=3, color_val=color.white):
    """
    Creates 4 cylinders extending from the center to the outermost edge in cardinal directions.
    """
    directions = [
        vector(max_radius, 0, 0),   # +X (East)
        vector(-max_radius, 0, 0),  # -X (West)
        vector(0, 0, max_radius),   # +Z (North)
        vector(0, 0, -max_radius)   # -Z (South)
    ]

    for dir_vec in directions:
        cylinder(
            pos=vector(0, y, 0),        # center of the scene
            axis=dir_vec,              # direction to extend
            radius=thickness,          # thickness of the spoke
            color=color_val,
            shininess=0.8
        )

# --- TOWER GENERATION --- 
def towers():
    tower_width = 5
    tower_height = 100
    for radius in radii:
        for angle in [0, m.pi/4, m.pi/2, 3*m.pi/4, m.pi, 5*m.pi/4, 3*m.pi/2, 7*m.pi/4]:  # E, N, W, S
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


    #help my life is an endless struggle
        hoop = ring(
            pos=vector(0, 95, 0),        # center of ring
            axis=vector(0, 1, 0),            # oriented vertically (hoop lies flat in XZ)
            radius=radius,                  # distance from center to tube middle
            thickness=4.5,       # diameter of the tube
            color=color.white,
            opacity=0.6,
            shininess=0.8
        )
        arch_ring_cylinders(radius=radius, arch_count = 8, hoop_height=95, thickness=1.2)

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

dome_count = 500
domes = []
for i in range(dome_count):
    home = Node()
    home.residential()
    domes.append(home)


#3d stuff
#ground = box(pos=vector(0,-2.5,0), size=vector(2000,0.2,2000), color=color.red) 
ground = cylinder(pos=vector(0,-2.5,0), radius=(radii[-1]+100), up=vector(1,0,0), color=color.orange, texture=textures.rock, shininess=0)
sky = sphere(
    pos=scene.center,          # same center as your scene
    radius=2000,               # must exceed your scene.range (750)
    texture="https://i.imgur.com/OnOJuOd.jpeg",
    #texture=textures.metal
    #color= vector(255, 214, 199)
    shininess=0,               # no specular highlights
    emissive=True              # so it’s unaffected by scene lighting
)


# --- placement parameters ---
placed = []                      # list of (x, z, r) for already‐placed nodes
MAX_TRIES = 1000                 # give up after this many attempts per dome

#sort domes largest‐first for greedy packing
domes_sorted = sorted(domes, key=lambda d: d.node_size, reverse=True) 

def generate_domes():
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
                    dome.ring_idx = ring_idx                                
                    placed.append((x, z, r_new))                             
                    break                                                  

            # if we placed successfully, stop trying further rings
            if hasattr(dome, 'x'):                                           
                break           
        # --- Connect domes to nearest larger dome ---
        residential_domes = [d for d in domes_sorted if d.type == 'residential' and hasattr(d, 'x')]

        for source in residential_domes:
            closest = None
            closest_dist = float('inf')

            for target in residential_domes:
                if target.node_size <= source.node_size:
                    continue  # only connect to strictly larger domes

                dx = target.x - source.x
                dz = target.z - source.z
                dist = m.sqrt(dx**2 + dz**2)

                if dist < closest_dist:
                    closest = target
                    closest_dist = dist

            if closest:
                start = vector(source.x, 0, source.z)
                end = vector(closest.x, 0, closest.z)
                axis = end - start
                cylinder(
                    pos=start,
                    axis=axis,
                    radius=3,
                    color=color.white,
                    opacity=0.5,
                    shininess=0.7
                )
                                       

generate_domes()
# Replace medium domes with hospitals and schools
medium_domes = [d for d in domes_sorted if 25 <= d.node_size <= 75 and hasattr(d, 'x')]
by_ring = {i: [] for i in range(len(radii) - 1)}
for d in medium_domes:
    by_ring[d.ring_idx].append(d)

for ring_idx, nodes in by_ring.items():
    replace_count = 4
    rand.shuffle(nodes)
    for i, node in enumerate(nodes[:replace_count * 2]):  # half hospitals, half schools
        if i < replace_count:
            node.hospital()
        else:
            node.school()



for dome in domes_sorted:
    # Skip any domes that weren't successfully placed
    if not hasattr(dome, 'x'):
        continue

    # Use actual computed radius based on occupancy/capacity
    radius = dome.node_size

    if dome.type == 'hospital':
        object = cylinder(pos=vector(dome.x, 0, dome.z), radius = radius, axis = vector(0,1,0), color = color.red, length=80)
    elif dome.type == 'school':
        object = box(pos=vector(dome.x, 50, dome.z), size=vector(radius, 100, radius), color =vector(1.0, 0.84, 0.0))
    else:
        color_val = vector(0.8, 0.8, 0.8)    # silver/gray (residential)
        create_icosahedron(
            pos=vector(dome.x, 0, dome.z),
            scale=dome.node_size,
            color_val=color_val,
            opacity=0.6,
            shininess=0.8,
            edge_color=vector(0.9, 0.9, 0.9),
            edge_thickness=0.9
            )

#card spokes
cardinal_spokes(max_radius=radii[-1], y=80, thickness=3, color_val=color.white)
#towers
towers()

# Create a list to hold all label objects
labels = []
# Add legend labels
labels.append(label(pos=vector(-1400, 600, 0), text="Residential", color=vector(0.8, 0.8, 0.8), box=False, height=8))
labels.append(label(pos=vector(-1400, 500, 0), text="Hospital", color=color.red, box=False, height=8))
labels.append(label(pos=vector(-1400, 400, 0), text="School", color=vector(1.0, 0.84, 0.0), box=False, height=8))
# Add orbital train route labels

for idx, radius in enumerate(radii[1:], start=1):  # Skip the innermost radius
    route_label = label(
        pos=vector(0, 120, radius), 
        text=f"Orbital train route {idx}", 
        color=color.cyan, 
        height=8, 
        box=False
    )
    labels.append(route_label)

# Global toggle state
labels_visible = True

# Toggle function
def toggle_labels():
    global labels_visible
    labels_visible = not labels_visible
    for lbl in labels:
        lbl.visible = labels_visible

# Button to toggle
button(text='Toggle Labels', bind=lambda _: toggle_labels())

elevator_base = cylinder(pos = vector(0, 50, 0), axis=vector(0,1,0), color=color.white, emissive=False, length=500, radius=25, texture=textures.metal)
elevator_shaft = cylinder(pos = vector(0,100,0), axis=vector(0,1,0), color=color.white, emissive=True, length=10000, radius=10, texture=textures.metal)

while True:
     rate(1)