import bpy
import math

# Function to create a grid of spheres
def create_op_art_sphere_grid(columns=10, rows=10, spacing=2.0, radius=0.5):
    spheres = []
    
    for i in range(columns):
        for j in range(rows):
            x = (i - columns / 2) * spacing
            y = (j - rows / 2) * spacing
            z = 0
            sphere = create_sphere(location=(x, y, z), radius=radius)
            spheres.append(sphere)
    
    return spheres

# Function to create a single sphere
def create_sphere(location=(0, 0, 0), radius=0.5):
    bpy.ops.mesh.primitive_uv_sphere_add(radius=radius, location=location)
    sphere = bpy.context.object
    
    # Create a material
    material = bpy.data.materials.new(name="SphereMaterial")
    material.use_nodes = True
    bsdf = material.node_tree.nodes["Principled BSDF"]
    bsdf.inputs["Base Color"].default_value = (0, 0, 0, 1)  # Black color
    sphere.data.materials.append(material)
    
    return sphere

# Function to animate the grid of spheres
def animate_op_art_sphere_grid(spheres, start_frame=1, end_frame=250):
    for i, sphere in enumerate(spheres):
        # Calculate distance from the center
        distance = math.sqrt(sphere.location[0] ** 2 + sphere.location[1] ** 2)
        scale_factor = 1 + 0.5 * math.sin(distance)
        
        for frame in range(start_frame, end_frame):
            scale = scale_factor * (1 + 0.3 * math.sin(frame / 10 + distance))
            sphere.scale = (scale, scale, scale)
            sphere.keyframe_insert(data_path="scale", frame=frame)

# Function to create an Op Art radial pattern with spheres
def create_op_art_sphere_radial(rings=10, segments=36, inner_radius=1.0, ring_spacing=1.0):
    spheres = []
    
    for i in range(rings):
        radius = inner_radius + i * ring_spacing
        angle_step = 2 * math.pi / segments
        
        for j in range(segments):
            angle = j * angle_step
            x = math.cos(angle) * radius
            y = math.sin(angle) * radius
            z = 0
            sphere = create_sphere(location=(x, y, z), radius=ring_spacing / 2)
            spheres.append(sphere)
    
    return spheres

# Function to animate the radial pattern of spheres
def animate_op_art_sphere_radial(spheres, start_frame=1, end_frame=250):
    for i, sphere in enumerate(spheres):
        angle_offset = math.atan2(sphere.location[1], sphere.location[0])
        for frame in range(start_frame, end_frame):
            scale = 1 + 0.3 * math.sin((frame / 10) + angle_offset)
            sphere.scale = (scale, scale, scale)
            sphere.keyframe_insert(data_path="scale", frame=frame)

# Clear existing objects
bpy.ops.object.select_all(action='SELECT')
bpy.ops.object.delete(use_global=False)

# Create Op Art grid pattern with spheres
grid_spheres = create_op_art_sphere_grid(columns=10, rows=10, spacing=3.0, radius=1.0)

# Create Op Art radial pattern with spheres
radial_spheres = create_op_art_sphere_radial(rings=6, segments=36, inner_radius=2.0, ring_spacing=2.0)

# Animate the Op Art patterns with spheres
animate_op_art_sphere_grid(grid_spheres, start_frame=1, end_frame=250)
animate_op_art_sphere_radial(radial_spheres, start_frame=1, end_frame=250)

# Set up camera
camera = bpy.data.objects['Camera']
camera.location = (0, 0, 30)
camera.rotation_euler = (math.radians(90), 0, 0)
camera.data.lens = 50

# Add lighting
bpy.ops.object.light_add(type='SUN', location=(10, -10, 20))
light = bpy.context.object
light.data.energy = 5

# Set background to white
bpy.context.scene.world.color = (1, 1, 1)
