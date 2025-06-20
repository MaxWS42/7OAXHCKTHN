import random as rand
import math as m
from vpython import *


from time import sleep

# Welcome screen
intro_label = label(
    pos=vector(0, 0, 0),
    text="Welcome to Slow Cities!",
    height=20,
    box=True,
    color=color.white,
    background=color.gray(0.2),
    border=10,
    line=True,
    opacity=0.9,
)

# Pause to show welcome screen
sleep(5)

# Hide intro label after delay
intro_label.visible = False

intro_label = label(
    pos=vector(0, 0, 0),
    text="Please enjoy this zero-player game, and play around with the label toggle.",
    height=15,
    box=True,
    color=color.white,
    background=color.gray(0.2),
    border=10,
    line=True,
    opacity=0.9,
)

# Pause to show welcome screen
sleep(3)

# Hide intro label after delay
intro_label.visible = False


target_position = vector(0, 0, 0)
scene.autoscale = False
scene.userzoom = False
scene.center = target_position
scene.range = 750
scene.forward = vector(-1, -1, -1).norm()

def create_icosahedron(pos, scale, color_val, opacity, shininess, edge_color=None, edge_thickness=None):
    import math
    phi = (1 + math.sqrt(5)) / 2

    base = [
        vector(-1,  phi, 0), vector( 1,  phi, 0),
        vector(-1, -phi, 0), vector( 1, -phi, 0),
        vector( 0, -1,  phi), vector( 0,  1,  phi),
        vector( 0, -1, -phi), vector( 0,  1, -phi),
        vector( phi,  0, -1), vector( phi,  0,  1),
        vector(-phi,  0, -1), vector(-phi,  0,  1),
    ]
    verts = [v.norm() * scale + pos for v in base]

    faces = [
        (0,11,5), (0,5,1), (0,1,7), (0,7,10), (0,10,11),
        (1,5,9), (5,11,4), (11,10,2), (10,7,6), (7,1,8),
        (3,9,4), (3,4,2), (3,2,6), (3,6,8), (3,8,9),
        (4,9,5), (2,4,11), (6,2,10), (8,6,7), (9,8,1)
    ]

    tris = []
    drawn = set()
    for a, b, c in faces:
        tris.append(triangle(
            v0=vertex(pos=verts[a], color=color_val, opacity=opacity),
            v1=vertex(pos=verts[b], color=color_val, opacity=opacity),
            v2=vertex(pos=verts[c], color=color_val, opacity=opacity),
            shininess=shininess
        ))
        if edge_color and edge_thickness:
            for u, v in ((a, b), (b, c), (c, a)):
                e = tuple(sorted((u, v)))
                if e in drawn: continue
                drawn.add(e)
                p1, p2 = verts[u], verts[v]
                cylinder(pos=p1, axis=p2 - p1, radius=edge_thickness, color=edge_color)

    return compound(tris)

radii = [50, 250, 450, 650, 850, 1050, 1250]

def arch_ring_cylinders(radius, arch_count, hoop_height=70, segments=30, thickness=1):
    for i in range(arch_count):
        theta0 = 2 * m.pi * i / arch_count
        theta1 = 2 * m.pi * (i + 1) / arch_count

        prev_point = None
        for j in range(segments + 1):
            t = j / segments
            theta = (1 - t) * theta0 + t * theta1
            x = radius * m.cos(theta)
            z = radius * m.sin(theta)
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
    directions = [
        vector(max_radius, 0, 0),
        vector(-max_radius, 0, 0),
        vector(0, 0, max_radius),
        vector(0, 0, -max_radius)
    ]
    for dir_vec in directions:
        cylinder(
            pos=vector(0, y, 0),
            axis=dir_vec,
            radius=thickness,
            color=color_val,
            shininess=0.8
        )

def towers():
    tower_width = 5
    tower_height = 100
    for radius in radii:
        for angle in [0, m.pi/4, m.pi/2, 3*m.pi/4, m.pi, 5*m.pi/4, 3*m.pi/2, 7*m.pi/4]:
            x = radius * m.cos(angle)
            z = radius * m.sin(angle)
            if x >= sum(radii):
                break
            box(
                pos=vector(x, tower_height / 2, z),
                size=vector(tower_width, tower_height, tower_width),
                color=color.gray(0.5),
                texture=textures.stucco
            )
        ring(
            pos=vector(0, 95, 0),
            axis=vector(0, 1, 0),
            radius=radius,
            thickness=4.5,
            color=color.white,
            opacity=0.6,
            shininess=0.8
        )
        arch_ring_cylinders(radius=radius, arch_count=8, hoop_height=95, thickness=1.2)

class Node:
    def __init__(self):
        pass

    def residential(self):
        node_max_occupancy = [rand.randint(10, 50), rand.randint(60, 170), rand.randint(200, 500), rand.randint(750, 1000)]
        self.occupancy = rand.randrange(4, 1000)
        self.capacity = rand.choices(node_max_occupancy, [0.5, 0.3, 0.15, 0.05])[0]
        self.node_size = m.floor((int(self.capacity) * (25 / m.pi)) ** 0.5)
        self.type = 'residential'

    def hospital(self):
        self.node_size = m.floor((75 * 25 / m.pi) ** 0.5)
        self.working_radius = 50
        self.treatment_capacity = 50
        self.type = 'hospital'

    def school(self):
        self.node_size = m.floor((50 * 25 / m.pi) ** 0.5)
        self.capacity = 200
        self.type = 'school'

dome_count = 500
domes = []
for _ in range(dome_count):
    home = Node()
    home.residential()
    domes.append(home)

ground = cylinder(pos=vector(0, -2.5, 0), radius=(radii[-1] + 100), up=vector(1, 0, 0), color=color.orange, texture=textures.rock, shininess=0)
sky = sphere(
    pos=scene.center,
    radius=2000,
    texture="https://i.imgur.com/OnOJuOd.jpeg",
    shininess=0,
    emissive=True
)

placed = []
MAX_TRIES = 5000
domes_sorted = sorted(domes, key=lambda d: d.node_size, reverse=True)

# 🔄 Progress Label at floor level
progress_label = label(pos=vector(0, 10, 0), text="0% buildings positioned.", box=False, height=10, color=color.white)

def generate_domes():
    total = len(domes_sorted)

    for i, dome in enumerate(domes_sorted):
        r_new = dome.node_size
        for ring_idx in range(len(radii) - 1):
            R1, R2 = radii[ring_idx], radii[ring_idx + 1]
            for attempt in range(MAX_TRIES):
                θ = rand.random() * 2 * m.pi
                ρ = rand.uniform(R1 + r_new, R2 - r_new)
                x, z = ρ * m.cos(θ), ρ * m.sin(θ)
                if all(m.hypot(x - xi, z - zi) >= (r_new + ri) for xi, zi, ri in placed):
                    dome.x, dome.z = x, z
                    dome.ring_idx = ring_idx
                    placed.append((x, z, r_new))
                    break
            if hasattr(dome, 'x'):
                break

        # 🔄 Update progress
        percent = (i + 1) / total * 100
        progress_label.text = f"{int(percent)}% buildings positioned"
        rate(60)

    # Connect domes
    residential_domes = [d for d in domes_sorted if d.type == 'residential' and hasattr(d, 'x')]
    for source in residential_domes:
        closest = None
        closest_dist = float('inf')
        for target in residential_domes:
            if target.node_size <= source.node_size:
                continue
            dx = target.x - source.x
            dz = target.z - source.z
            dist = m.sqrt(dx ** 2 + dz ** 2)
            if dist < closest_dist:
                closest = target
                closest_dist = dist
        if closest:
            start = vector(source.x, 0, source.z)
            end = vector(closest.x, 0, closest.z)
            axis = end - start
            cylinder(pos=start, axis=axis, radius=3.5, color=color.white, opacity=0.5, shininess=0.7, emissive=True)

generate_domes()

progress_label.visible = False


# Replace some domes
medium_domes = [d for d in domes_sorted if 25 <= d.node_size <= 75 and hasattr(d, 'x')]
by_ring = {i: [] for i in range(len(radii) - 1)}
for d in medium_domes:
    by_ring[d.ring_idx].append(d)
for ring_idx, nodes in by_ring.items():
    replace_count = 4
    rand.shuffle(nodes)
    for i, node in enumerate(nodes[:replace_count * 2]):
        if i < replace_count:
            node.hospital()
        else:
            node.school()

for dome in domes_sorted:
    if not hasattr(dome, 'x'):
        continue
    radius = dome.node_size
    if dome.type == 'hospital':
        cylinder(pos=vector(dome.x, 0, dome.z), radius=radius*0.75, axis=vector(0, 1, 0), color=color.red, length=80)
    elif dome.type == 'school':
        box(pos=vector(dome.x, 40, dome.z), size=vector(radius*1.25, 80, radius*1.25), color=vector(1.0, 0.84, 0.0))
    else:
        color_val = vector(0.8, 0.8, 0.8)
        create_icosahedron(
            pos=vector(dome.x, 0, dome.z),
            scale=radius,
            color_val=color_val,
            opacity=0.6,
            shininess=0.8,
            edge_color=vector(0.9, 0.9, 0.9),
            edge_thickness=0.9
        )

cardinal_spokes(max_radius=radii[-1], y=80, thickness=3, color_val=color.white)
towers()

labels = []
labels.append(label(pos=vector(-1400, 600, 0), text="Residential", color=vector(0.8, 0.8, 0.8), box=False, height=8))
labels.append(label(pos=vector(-1400, 500, 0), text="Hospital", color=color.red, box=False, height=8))
labels.append(label(pos=vector(-1400, 400, 0), text="School", color=vector(1.0, 0.84, 0.0), box=False, height=8))
for idx, radius in enumerate(radii[1:], start=1):
    route_label = label(
        pos=vector(0, 120, radius),
        text=f"Orbital train route {idx}",
        color=color.cyan,
        height=8,
        box=False
    )
    labels.append(route_label)

labels_visible = True
def toggle_labels():
    global labels_visible
    labels_visible = not labels_visible
    for lbl in labels:
        lbl.visible = labels_visible

button(text='Toggle Labels', bind=lambda _: toggle_labels())

elevator_base = cylinder(pos=vector(0, 50, 0), axis=vector(0, 1, 0), color=color.white, emissive=False, length=500, radius=25, texture=textures.metal)
elevator_shaft = cylinder(pos=vector(0, 100, 0), axis=vector(0, 1, 0), color=color.white, emissive=True, length=10000, radius=10, texture=textures.metal)

while True:
    rate(1)
