# Bolted Lap Joint Design

This project provides tools for designing bolted lap joints according to IS800:2007 standards. It features a computational module for calculating optimal bolt arrangements and a command-line interface for quick access to design functionality.

## Features

- Design of bolted lap joints connecting two plates under tensile load
- Automatic selection of bolt diameter, grade, and number of bolts
- Calculation of pitch distances, end distances, and edge distances
- Determination of connection efficiency and strength
- Command-line interface for easy access to design functionality
- Comprehensive test suite to ensure reliability and correctness

## Project Structure

```
bolted_lap_joint_test/
├── src/
│   ├── bolted_lap_joint_design.py   # Core design module
│   └── cli.py                       # Command-line interface
├── tests/
│   └── test_lap_joint.py            # PyTest test cases
├── main.py                          # Main entry point
├── conftest.py                      # PyTest configuration
├── requirements.txt                 # Project dependencies
└── README.md                        # This file
```

## Requirements

- Python 3.7+
- NumPy
- ArgParse (for CLI functionality)
- PyTest (for running tests)

## Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/bolted-lap-joint-design.git
cd bolted-lap-joint-design
```

2. Install the dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line Interface

The project includes a command-line interface for quick access to design functionality:

```bash
# Using positional parameters
python main.py 50 100 10 12

# Using named parameters
python main.py --load 50 --width 100 --thickness1 10 --thickness2 12

# Output in JSON format
python main.py 50 100 10 12 --json
```

Parameters:
- `load`: Tensile force in kN (must be positive)
- `width`: Width of the plates in mm (must be positive, max 1000 mm)
- `thickness1`: Thickness of plate 1 in mm (must be positive, max 100 mm)
- `thickness2`: Thickness of plate 2 in mm (must be positive, max 100 mm)

### Using as a Module

You can also use the design functionality in your own Python code:

```python
from src.bolted_lap_joint_design import design_lap_joint

# Design a bolted lap joint
design = design_lap_joint(load=50, width=100, thickness1=10, thickness2=12)

# Access design parameters
print(f"Bolt Diameter: {design['bolt_diameter']} mm")
print(f"Number of Bolts: {design['number_of_bolts']}")
print(f"Connection Efficiency: {design['efficiency_of_connection']:.2%}")
```

## Running the Tests

To run all tests:
```bash
python -m pytest
```

To run tests with coverage report:
```bash
python -m pytest --cov=src
```

To run a specific test:
```bash
python -m pytest tests/test_lap_joint.py::test_minimum_two_bolts
```

## Test Cases

1. **Minimum Two Bolts Test**: Verifies that for any combination of loads and thicknesses, the design always includes at least 2 bolts.
2. **Zero Load Test**: Confirms that even with zero load, the design includes at least 2 bolts.
3. **Small Load Test**: Tests with very small loads to ensure minimum of 2 bolts.
4. **Parameter Selection Test**: Verifies that appropriate design parameters are selected for various load cases.
5. **Error Handling Test**: Checks that the module properly handles invalid inputs like negative loads.

## Design Methodology

The design follows the guidelines specified in IS800:2007, focusing on:
- Shear capacity calculation for bolts
- Bearing capacity calculation for connected plates
- Minimum spacing requirements for bolts
- Minimum edge and end distances
- Connection efficiency calculation

## Author

- Prince Sahu

## License

This project is licensed under the MIT License - see the LICENSE file for details. # Osadag_Assignment
