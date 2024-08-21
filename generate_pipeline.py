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

def create_pipeline(length, diameter, thickness):
    print(f"Creating pipeline with dimensions: length={length}, diameter={diameter}, thickness={thickness}")  # Debugging line
    try:
        # Create a new FreeCAD document
        doc = FreeCAD.newDocument("PipelineDoc")

        # Create a cylinder for the outer part of the pipeline
        outer_cylinder = Part.makeCylinder(diameter / 2, length)

        # Create a cylinder for the inner part of the pipeline to create a hollow effect
        inner_diameter = diameter - 2 * thickness
        if inner_diameter <= 0:
            raise ValueError("Inner diameter must be greater than zero")
        inner_cylinder = Part.makeCylinder(inner_diameter / 2, length)

        # Cut the inner cylinder from the outer cylinder to create the pipeline wall
        pipeline_wall = outer_cylinder.cut(inner_cylinder)
        
        # Add the pipeline to the document
        obj = doc.addObject("Part::Feature", "Pipeline")
        obj.Shape = pipeline_wall
        doc.recompute()

        # Define the output directory and file paths
        output_dir = os.path.join(os.getcwd(), 'static')
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        stl_file_path = os.path.join(output_dir, "pipeline.stl")
        fcstd_file_path = os.path.join(output_dir, "pipeline.FCStd")

        # Export the pipeline as an STL file
        Part.export([obj], stl_file_path)
        
        # Save the FreeCAD document
        doc.saveAs(fcstd_file_path)
        
        print(f"Pipeline created and exported successfully to {stl_file_path} and {fcstd_file_path}.")
        return stl_file_path
    except Exception as e:
        print(f"An error occurred while creating the pipeline: {e}")
        sys.exit(1)

if __name__ == "__main__":
    # Ensure the correct number of arguments are provided
    if len(sys.argv) != 4:
        print("Usage: python generate_pipeline.py <length> <diameter> <thickness>")
        sys.exit(1)

    try:
        # Parse the dimensions from command-line arguments
        length = float(sys.argv[1])
        diameter = float(sys.argv[2])
        thickness = float(sys.argv[3])

        # Check if dimensions are positive
        if length <= 0 or diameter <= 0 or thickness <= 0:
            raise ValueError("Dimensions must be positive numbers.")

        # Create the pipeline with specified dimensions
        create_pipeline(length, diameter, thickness)
    except ValueError as e:
        print(f"Invalid input: {e}")
        sys.exit(1)

