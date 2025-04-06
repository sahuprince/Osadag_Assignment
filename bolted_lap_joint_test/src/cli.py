#!/usr/bin/env python
"""
Command-line interface for the Bolted Lap Joint Design tool.
This script provides a simple way to use the design functionality from the command line.
"""

import argparse
import json
import sys
from bolted_lap_joint_design import design_lap_joint

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Design a bolted lap joint connecting two plates."
    )
    
    # Create a group for positional arguments
    positional_group = parser.add_argument_group("Positional Parameters")
    positional_group.add_argument(
        "load", type=float, nargs="?", help="Tensile force in kN (must be positive)"
    )
    positional_group.add_argument(
        "width", type=float, nargs="?", help="Width of the plates in mm (must be positive, max 1000 mm)"
    )
    positional_group.add_argument(
        "thickness1", type=float, nargs="?", help="Thickness of plate 1 in mm (must be positive, max 100 mm)"
    )
    positional_group.add_argument(
        "thickness2", type=float, nargs="?", help="Thickness of plate 2 in mm (must be positive, max 100 mm)"
    )
    
    # Create a group for named arguments
    named_group = parser.add_argument_group("Named Parameters")
    named_group.add_argument(
        "--load", type=float, dest="named_load", help="Tensile force in kN (must be positive)"
    )
    named_group.add_argument(
        "--width", type=float, dest="named_width", help="Width of the plates in mm (must be positive, max 1000 mm)"
    )
    named_group.add_argument(
        "--thickness1", type=float, dest="named_thickness1", help="Thickness of plate 1 in mm (must be positive, max 100 mm)"
    )
    named_group.add_argument(
        "--thickness2", type=float, dest="named_thickness2", help="Thickness of plate 2 in mm (must be positive, max 100 mm)"
    )
    
    parser.add_argument(
        "--json", action="store_true", help="Output results in JSON format"
    )
    
    args = parser.parse_args()
    
    # Determine if we're using named parameters
    named_params_provided = any([
        args.named_load is not None,
        args.named_width is not None,
        args.named_thickness1 is not None,
        args.named_thickness2 is not None
    ])
    
    # Ensure we're not mixing positional and named parameters
    positional_params_provided = any([
        args.load is not None,
        args.width is not None,
        args.thickness1 is not None,
        args.thickness2 is not None
    ])
    
    if named_params_provided and positional_params_provided:
        parser.error("Please use either all positional or all named parameters, but not a mix of both.")
    
    # If named parameters are provided, use them
    if named_params_provided:
        args.load = args.named_load
        args.width = args.named_width
        args.thickness1 = args.named_thickness1
        args.thickness2 = args.named_thickness2
    
    # Ensure all parameters are provided
    if any([args.load is None, args.width is None, args.thickness1 is None, args.thickness2 is None]):
        parser.error("All parameters (load, width, thickness1, thickness2) must be provided.")
    
    return args

def display_results(design, json_output=False):
    """Display the design results in a formatted way."""
    if json_output:
        print(json.dumps(design, indent=2))
        return

    print("\n====== BOLTED LAP JOINT DESIGN RESULTS ======")
    print(f"Bolt Diameter:           {design['bolt_diameter']} mm")
    print(f"Bolt Grade:              {design['bolt_grade']}")
    print(f"Number of Bolts:         {design['number_of_bolts']}")
    print(f"Pitch Distance:          {design['pitch_distance']:.2f} mm")
    print(f"End Distance:            {design['end_distance']:.2f} mm")
    print(f"Edge Distance:           {design['edge_distance']:.2f} mm")
    print(f"Hole Diameter:           {design['hole_diameter']:.2f} mm")
    print(f"Connection Length:       {design['length_of_connection']:.2f} mm")
    print(f"Connection Efficiency:   {design['efficiency_of_connection']:.2%}")
    print(f"Connection Strength:     {design['strength_of_connection']/1000:.2f} kN")
    print("===========================================")

def main():
    """Main function for the CLI."""
    args = parse_arguments()
    
    try:
        # Design the bolted lap joint
        design = design_lap_joint(args.load, args.width, args.thickness1, args.thickness2)
        
        # Display the results
        display_results(design, args.json)
        return 0
    except ValueError as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1

if __name__ == "__main__":
    sys.exit(main()) 