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

def hex_to_rgb(hex_color):
    hex_color = hex_color.lstrip('#')
    return tuple(int(hex_color[i:i+2], 16)/255.0 for i in (0, 2, 4))

def create_box(length, width, height, material, color):
    """
    Creates a 3D box model using FreeCAD and exports it as an STL and FCStd file.

    Parameters:
    length (float): The length of the box.
    width (float): The width of the box.
    height (float): The height of the box.
    material (str): The material of the box.
    color (str): The color of the box in hex format.
    """
    try:
        # Create a new FreeCAD document
        doc = FreeCAD.newDocument("BoxDoc")
        
        # Create a box with the specified dimensions
        box = Part.makeBox(length, width, height)
        obj = doc.addObject("Part::Feature", "Box")
        obj.Shape = box
        doc.recompute()

        # Apply color properties
        rgb_color = hex_to_rgb(color)
        view_object = getattr(obj, 'ViewObject', None)
        if view_object:
            view_object.ShapeColor = rgb_color
        else:
            print("Warning: ViewObject not found. Skipping color assignment.")
        
        # Define the output directory and file paths
        output_dir = os.path.join(os.getcwd(), 'static')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        stl_file_path = os.path.join(output_dir, "box.stl")
        fcstd_file_path = os.path.join(output_dir, "box.FCStd")

        # Export the box as an STL file
        Part.export([obj], stl_file_path)
        
        # Save the FreeCAD document
        doc.saveAs(fcstd_file_path)
        
        print(f"Box created and exported successfully to {stl_file_path} and {fcstd_file_path}.")
        return stl_file_path
    except Exception as e:
        print(f"An error occurred while creating the box: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 6:
        print("Usage: python freecad_script.py <length> <width> <height> <material> <color>")
        sys.exit(1)

    try:
        # Parse the dimensions from command-line arguments
        length = float(sys.argv[1])
        width = float(sys.argv[2])
        height = float(sys.argv[3])
        material = sys.argv[4]
        color = sys.argv[5]

        # Check if dimensions are positive
        if length <= 0 or width <= 0 or height <= 0:
            raise ValueError("Dimensions must be positive numbers.")

        # Create the box with specified dimensions, material, and color
        create_box(length, width, height, material, color)
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)

