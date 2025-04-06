import pytest
import sys
import os
import numpy as np

# Add the src directory to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), '../src'))

from bolted_lap_joint_design import design_lap_joint, calculate_bolt_strength, IS800_2007

# Test parameters
load_values = np.linspace(1, 100, 10)  # 10 evenly spaced load values from 1 to 100 kN
thickness_values = [6, 8, 10, 12, 16, 20, 24]  # Specified thickness values
width_value = 150  # Common width value for all tests

# Define the test cases as combinations of loads and thicknesses
# Using parametrize for more readable test results
@pytest.mark.parametrize("load", load_values)
@pytest.mark.parametrize("t1", thickness_values)
@pytest.mark.parametrize("t2", thickness_values)
def test_minimum_two_bolts(load, t1, t2):
    """
    Test if the design always returns at least 2 bolts for any valid load and thickness combination.
    
    Args:
        load: Tensile force in kN
        t1: Thickness of plate 1 in mm
        t2: Thickness of plate 2 in mm
    """
    # Design the lap joint with the given parameters
    design = design_lap_joint(load, width_value, t1, t2)
    
    # Assert that the number of bolts is at least 2
    assert design["number_of_bolts"] >= 2, f"Design should have at least 2 bolts, but has {design['number_of_bolts']} for load={load}kN, t1={t1}mm, t2={t2}mm"

# Additional test for zero load
def test_zero_load():
    """Test that even with zero load, at least 2 bolts are provided."""
    load = 0
    t1 = 10
    t2 = 12
    
    design = design_lap_joint(load, width_value, t1, t2)
    assert design["number_of_bolts"] >= 2, f"Design should have at least 2 bolts even with zero load, but has {design['number_of_bolts']}"

# Test to verify if proper error handling exists for invalid inputs
def test_negative_load_error_handling():
    """Test that negative load raises a ValueError."""
    with pytest.raises((ValueError, AssertionError)):
        design_lap_joint(-10, width_value, 10, 12)

# Test to verify if the algorithm handles edge cases correctly
def test_very_small_load():
    """Test with very small load to ensure at least 2 bolts are used."""
    design = design_lap_joint(0.001, width_value, 10, 12)
    assert design["number_of_bolts"] >= 2, "Even with minimal load, at least 2 bolts should be used"

# Test to verify if the algorithm selects appropriate parameters for various load cases
@pytest.mark.parametrize("load", [20, 40, 60, 80, 100])
def test_parameters_selection(load):
    """Test that with increasing load, the design parameters (bolt diameter, bolt grade) are selected appropriately."""
    t1 = 12
    t2 = 12
    
    design = design_lap_joint(load, width_value, t1, t2)
    
    # Basic parameter checks
    assert 0 < design["bolt_diameter"] <= 24, f"Bolt diameter should be in valid range, got {design['bolt_diameter']}"
    assert 0 < design["bolt_grade"] <= 10, f"Bolt grade should be in valid range, got {design['bolt_grade']}"
    assert design["number_of_bolts"] >= 2, f"Number of bolts should be at least 2, got {design['number_of_bolts']}"
    
    # Check that efficiency is within acceptable range
    assert 0 < design["efficiency_of_connection"] <= 1.0, f"Efficiency should be between 0 and 1, got {design['efficiency_of_connection']}"

# Additional tests to improve code coverage

def test_is800_bolt_shear_capacity():
    """Test the bolt shear capacity calculation method in IS800_2007."""
    # Test without shear planes and joint factor
    shear_capacity_shop = IS800_2007.cl_10_3_3_bolt_shear_capacity(250, 100, 80, 1, 1.0, 'Shop')
    assert shear_capacity_shop > 0, "Shear capacity should be positive"
    
    # Test with same parameters but for field connection
    shear_capacity_field = IS800_2007.cl_10_3_3_bolt_shear_capacity(250, 100, 80, 1, 1.0, 'Field')
    assert shear_capacity_field > 0, "Shear capacity for field connection should be positive"
    assert shear_capacity_field < shear_capacity_shop, "Field connection should have lower capacity than shop with same parameters"
    
    # Test the effect of shear planes
    shear_capacity_multi = IS800_2007.cl_10_3_3_bolt_shear_capacity(250, 100, 80, 2, 1.0, 'Shop')
    assert shear_capacity_multi > shear_capacity_shop, "Multiple shear planes should increase capacity"

def test_is800_bolt_bearing_capacity():
    """Test the bolt bearing capacity calculation method in IS800_2007."""
    # Test standard holes
    bearing_capacity_standard = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
        410, 250, 12, 20, 30, 50, 'Standard', 'Shop'
    )
    assert bearing_capacity_standard > 0, "Bearing capacity should be positive"
    
    # Test oversized holes
    bearing_capacity_oversized = IS800_2007.cl_10_3_4_bolt_bearing_capacity(
        410, 250, 12, 20, 30, 50, 'Oversized', 'Field'
    )
    assert bearing_capacity_oversized > 0, "Bearing capacity for oversized holes should be positive"
    assert bearing_capacity_oversized < bearing_capacity_standard, "Oversized holes should have lower bearing capacity"

def test_no_suitable_design():
    """Test the case where no suitable design is found."""
    # We'll use extremely high load that can't be satisfied with available bolt diameters
    with pytest.raises(ValueError, match="No suitable design found that meets the requirements."):
        design_lap_joint(100000, width_value, 5, 5)  # Extremely high load

# Add test to cover calculate_bolt_strength function
def test_calculate_bolt_strength():
    """Test the calculate_bolt_strength function."""
    bolt_strength = calculate_bolt_strength(4.6)
    assert len(bolt_strength) == 2, "Should return a list with two values"
    assert bolt_strength[0] == 400, "Bolt ultimate tensile strength should be 400 MPa for grade 4.6"
    assert abs(bolt_strength[1] - 600) < 1e-10, "Bolt yield strength should be approximately 600 MPa for grade 4.6"
    
    # Test another grade
    bolt_strength_2 = calculate_bolt_strength(5.8)
    assert bolt_strength_2[0] == 500, "Bolt ultimate tensile strength should be 500 MPa for grade 5.8"
    assert abs(bolt_strength_2[1] - 800) < 1e-10, "Bolt yield strength should be approximately 800 MPa for grade 5.8"

# Add tests for input validation
@pytest.mark.parametrize("param_name,invalid_value,error_message", [
    ("width", -10, "Width w must be positive"),
    ("width", 0, "Width w must be positive"),
    ("width", 1500, "Width w is too large"),
    ("thickness_1", -5, "Thickness t1 must be positive"),
    ("thickness_1", 0, "Thickness t1 must be positive"),
    ("thickness_1", 150, "Plate thickness is too large"),
    ("thickness_2", -5, "Thickness t2 must be positive"),
    ("thickness_2", 0, "Thickness t2 must be positive"),
    ("thickness_2", 150, "Plate thickness is too large"),
])
def test_input_validation(param_name, invalid_value, error_message):
    """Test that invalid inputs raise appropriate errors with descriptive messages."""
    load = 50  # Use a standard load value
    width = 150  # Default width
    t1 = 12  # Default thickness 1
    t2 = 16  # Default thickness 2
    
    # Override the parameter that should be invalid
    if param_name == "width":
        width = invalid_value
    elif param_name == "thickness_1":
        t1 = invalid_value
    elif param_name == "thickness_2":
        t2 = invalid_value
    
    with pytest.raises(ValueError, match=error_message):
        design_lap_joint(load, width, t1, t2) 