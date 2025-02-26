import numpy as np
import trimesh
import pyrender

# Function to generate the L-system string
def generate_l_system(axiom, rules, generations):
    current_string = axiom
    for _ in range(generations):
        next_string = ""
        for char in current_string:
            next_string += rules.get(char, char)  # Apply rule if exists, else keep char
        current_string = next_string
    return current_string

# Function to create the 3D L-System geometry
def draw_l_system_3d(l_system_string, step=1, angle=25, radius=0.05):
    position = np.array([0, 0, 0])  # Starting position
    direction = np.array([0, 1, 0])  # Initial direction (upward)
    stack = []  # Stack to save position and direction
    cylinders = []  # List of cylinder meshes
    leaf_positions = []  # Store leaf positions

    for command in l_system_string:
        if command == "F":
            new_position = position + step * direction
            vector = new_position - position
            length = np.linalg.norm(vector)

            if length > 0:
                # Create cylinder (branch)
                cylinder = trimesh.creation.cylinder(radius=radius, height=length, sections=12)

                # Align the cylinder along the vector
                rotation = trimesh.geometry.align_vectors([0, 0, 1], vector)
                cylinder.apply_transform(rotation)
                cylinder.apply_translation(position + vector / 2)

                # Set brown color (trunk/branches)
                color = np.array([139, 69, 19, 255]) / 255.0  # RGBA brown
                cylinder.visual.vertex_colors = color

                cylinders.append(cylinder)

            position = new_position
        elif command == "+":
            # Rotate left around Z-axis
            theta = np.radians(angle)
            rotation_matrix = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])
            direction = np.dot(rotation_matrix, direction)
        elif command == "-":
            # Rotate right around Z-axis
            theta = np.radians(-angle)
            rotation_matrix = np.array([
                [np.cos(theta), -np.sin(theta), 0],
                [np.sin(theta), np.cos(theta), 0],
                [0, 0, 1]
            ])
            direction = np.dot(rotation_matrix, direction)
        elif command == "&":
            # Rotate down around X-axis
            theta = np.radians(angle)
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ])
            direction = np.dot(rotation_matrix, direction)
        elif command == "^":
            # Rotate up around X-axis
            theta = np.radians(-angle)
            rotation_matrix = np.array([
                [1, 0, 0],
                [0, np.cos(theta), -np.sin(theta)],
                [0, np.sin(theta), np.cos(theta)]
            ])
            direction = np.dot(rotation_matrix, direction)
        elif command == "[":
            # Save position and direction
            stack.append((position.copy(), direction.copy()))
        elif command == "]":
            # Restore position and direction
            position, direction = stack.pop()
            leaf_positions.append(position)  # Mark this as a leaf position

    # Create leaves as small spheres
    leaves = []
    leaf_radius = radius * 1.5
    for leaf_pos in leaf_positions:
        leaf = trimesh.creation.icosphere(subdivisions=2, radius=leaf_radius)
        leaf.apply_translation(leaf_pos)

        # Set green color (leaves)
        color = np.array([34, 139, 34, 255]) / 255.0  # RGBA green
        leaf.visual.vertex_colors = color

        leaves.append(leaf)

    # Combine all cylinders and leaves into a single mesh
    solid_model = trimesh.util.concatenate(cylinders + leaves)
    return solid_model

# Function to visualize the 3D model
def visualize_model(mesh):
    scene = pyrender.Scene()
    
    # Convert the mesh with colors to pyrender
    mesh_pyrender = pyrender.Mesh.from_trimesh(mesh, smooth=True)
    
    scene.add(mesh_pyrender)
    viewer = pyrender.Viewer(scene, use_raymond_lighting=True)

# Define L-system rules
axiom = "F"
rules = {
    "F": "F[+F]F[-F]F"  # Branching rule for tree-like structure
}
generations = 4  # Increase for more complexity

# Generate the L-system string
l_system_string = generate_l_system(axiom, rules, generations)

# Generate the 3D tree model
solid_model = draw_l_system_3d(l_system_string, step=1, angle=25, radius=0.05)

# Visualize the 3D tree
visualize_model(solid_model)

# Export the result to a file
solid_model.export('tree_3d.stl')
print("3D tree model saved as tree_3d.stl")
