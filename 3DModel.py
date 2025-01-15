import numpy as np
import trimesh
import pyrender

# Function to generate the L-system string
def generate_l_system(axiom, rule, generations):
    current_string = axiom
    for _ in range(generations):
        next_string = ""
        for char in current_string:
            if char == "F":
                next_string += rule
            else:
                next_string += char
        current_string = next_string
    return current_string

# Function to generate the 3D L-System geometry
def draw_l_system_3d(l_system_string, step=1, angle=25, radius=0.05):
    position = np.array([0, 0, 0])  # Starting position
    direction = np.array([0, 1, 0])  # Initial direction (upward)
    stack = []  # Stack to save position and direction
    cylinders = []  # List of cylinder meshes

    for command in l_system_string:
        if command == "F":
            # Move forward and create a cylinder segment
            new_position = position + step * direction
            vector = new_position - position
            length = np.linalg.norm(vector)
            if length > 0:
                cylinder = trimesh.creation.cylinder(radius=radius, height=length, sections=12)
                # Align the cylinder along the vector
                z_axis = np.array([0, 0, 1])
                #rotation, _ = trimesh.geometry.align_vectors(z_axis, vector)
                cylinder.apply_transform(trimesh.transformations.rotation_matrix(angle=0, direction=vector, point=position))
                cylinder.apply_translation(position + vector / 2)
                cylinders.append(cylinder)
            position = new_position
        elif command == "+":
            # Rotate left around Z-axis
            theta = np.radians(angle)
            rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                         [np.sin(theta), np.cos(theta), 0],
                                         [0, 0, 1]])
            direction = np.dot(rotation_matrix, direction)
        elif command == "-":
            # Rotate right around Z-axis
            theta = np.radians(-angle)
            rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                         [np.sin(theta), np.cos(theta), 0],
                                         [0, 0, 1]])
            direction = np.dot(rotation_matrix, direction)
        elif command == "&":
            # Rotate down around X-axis
            theta = np.radians(angle)
            rotation_matrix = np.array([[1, 0, 0],
                                         [0, np.cos(theta), -np.sin(theta)],
                                         [0, np.sin(theta), np.cos(theta)]])
            direction = np.dot(rotation_matrix, direction)
        elif command == "^":
            # Rotate up around X-axis
            theta = np.radians(-angle)
            rotation_matrix = np.array([[1, 0, 0],
                                         [0, np.cos(theta), -np.sin(theta)],
                                         [0, np.sin(theta), np.cos(theta)]])
            direction = np.dot(rotation_matrix, direction)
        elif command == "[":
            # Save position and direction
            stack.append((position.copy(), direction.copy()))
        elif command == "]":
            # Restore position and direction
            position, direction = stack.pop()

    # Combine all cylinders into a single mesh
    solid_model = trimesh.util.concatenate(cylinders)
    return solid_model

# Function to visualize the model
def visualize_model(mesh):
    scene = pyrender.Scene()
    mesh_pyrender = pyrender.Mesh.from_trimesh(mesh)
    scene.add(mesh_pyrender)
    viewer = pyrender.Viewer(scene, use_raymond_lighting=True)

# Define the axiom, rule, and number of generations
axiom = "F"
rule = "F&&^[F^^F]^^F"  # Example rule for 3D branching
generations = 1

# Generate the L-system string
l_system_string = generate_l_system(axiom, rule, generations)

# Generate the 3D solid geometry
solid_model = draw_l_system_3d(l_system_string, step=1, angle=25, radius=0.05)

# Visualize the 3D model
visualize_model(solid_model)

# Export the result to a file
solid_model.export('cactus_3d.stl')
print("3D solid model saved as cactus_3d.stl")
