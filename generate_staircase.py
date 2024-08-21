import sys
import os

# Specify the path to FreeCAD library
freecad_path = '/usr/lib/freecad/lib'  # Adjust this path based on your installation
sys.path.append(freecad_path)

try:
    import FreeCAD
    import Part
except ImportError as e:
    print(f"Error importing FreeCAD modules: {e}")
    sys.exit(1)

def create_staircase(num_steps, step_length, step_width, step_height):
    """
    Creates a 3D staircase model using FreeCAD and exports it as an STL and FCStd file.

    Parameters:
    num_steps (int): The number of steps in the staircase.
    step_length (float): The length of each step.
    step_width (float): The width of each step.
    step_height (float): The height of each step.
    """
    try:
        # Create a new FreeCAD document
        doc = FreeCAD.newDocument("StaircaseDoc")

        steps = []
        for i in range(num_steps):
            step = Part.makeBox(step_length, step_width, step_height)
            step.translate(FreeCAD.Vector(0, i * step_width, i * step_height))
            steps.append(step)
        
        staircase = steps[0]
        for step in steps[1:]:
            staircase = staircase.fuse(step)
        
        # Add the staircase to the document
        obj = doc.addObject("Part::Feature", "Staircase")
        obj.Shape = staircase
        doc.recompute()

        # Define the output directory and file paths
        output_dir = os.path.join(os.getcwd(), 'static')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        stl_file_path = os.path.join(output_dir, "staircase.stl")
        fcstd_file_path = os.path.join(output_dir, "staircase.FCStd")

        # Export the staircase as an STL file
        Part.export([obj], stl_file_path)
        
        # Save the FreeCAD document
        doc.saveAs(fcstd_file_path)
        
        print(f"Staircase created and exported successfully to {stl_file_path} and {fcstd_file_path}.")
        return stl_file_path
    except Exception as e:
        print(f"An error occurred while creating the staircase: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 5:
        print("Usage: python generate_staircase.py <num_steps> <step_length> <step_width> <step_height>")
        sys.exit(1)

    try:
        # Parse the dimensions from command-line arguments
        num_steps = int(sys.argv[1])
        step_length = float(sys.argv[2])
        step_width = float(sys.argv[3])
        step_height = float(sys.argv[4])

        # Check if dimensions are positive
        if num_steps <= 0 or step_length <= 0 or step_width <= 0 or step_height <= 0:
            raise ValueError("All dimensions must be positive numbers.")

        # Create the staircase with specified dimensions
        create_staircase(num_steps, step_length, step_width, step_height)
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)

