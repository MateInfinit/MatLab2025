import matplotlib.pyplot as plt
import numpy as np

# Function to generate the L-system
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

# Function to draw the L-system with fixed 90° turns
def draw_l_system(l_system_string, step=5):
    stack = []  # Stack to save positions and directions
    position = np.array([0, 0])  # Initial position
    direction = np.array([0, 1])  # Initial direction (upward)
    lines = []  # List to store line segments

    for command in l_system_string:
        if command == "F":
            # Move forward, add line segment
            new_position = position + step * direction
            lines.append((position, new_position))
            position = new_position
        elif command == "+":
            # Turn left (90 degrees)
            direction = np.array([-direction[1], direction[0]])  # Rotate left
        elif command == "-":
            # Turn right (90 degrees)
            direction = np.array([direction[1], -direction[0]])  # Rotate right
        elif command == "[":
            # Save the current position and direction
            stack.append((position.copy(), direction.copy()))
        elif command == "]":
            # Restore the saved position and direction
            position, direction = stack.pop()

    # Plot the lines
    for start, end in lines:
        plt.plot([start[0], end[0]], [start[1], end[1]], 'g', lw=1)

    plt.title("90° Complex Cactus L-System")
    plt.axis('equal')  # Keep aspect ratio equal for better proportions
    plt.show()

# Define the axiom, rule, and number of generations
axiom = "F"
rule = "FF[+F-F[F-F+F][FFF--F++]]FF[-F+F[F+F-F][FFF--FF+F]]FF"  # Updated for 90° branching
generations = 3  # Adjust for more complexity

# Generate the L-system string
l_system_string = generate_l_system(axiom, rule, generations)

# Draw the L-system cactus
draw_l_system(l_system_string, step=5)
