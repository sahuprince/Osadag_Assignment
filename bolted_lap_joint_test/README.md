# Bolted Lap Joint Design - Unit Testing

This project contains unit tests for a bolted lap joint design module, verifying that the design algorithm always provides a minimum of two bolts regardless of the load or plate thicknesses.

## Project Objective

The main objective is to verify whether the bolted lap joint design module ensures a minimum of two bolts in the joint for any combination of:
- Load (P) ranging from 0 to 100 kN
- Plate thicknesses (t1, t2) from the set [6, 8, 10, 12, 16, 20, 24] mm

## Project Structure

```
bolted_lap_joint_test/
├── src/
│   └── bolted_lap_joint_design.py   # The module to be tested
├── tests/
│   └── test_lap_joint.py            # PyTest test cases
├── conftest.py                      # PyTest configuration
├── requirements.txt                 # Project dependencies
└── README.md                        # This file
```

## Requirements

- Python 3.7+
- PyTest
- NumPy

## Installation

1. Clone the repository
2. Install the dependencies:
```
pip install -r requirements.txt
```

## Running the Tests

To run all tests:
```
python -m pytest
```

To run tests with coverage report:
```
python -m pytest --cov=src
```

To run a specific test:
```
python -m pytest tests/test_lap_joint.py::test_minimum_two_bolts
```

## Test Cases

1. **Minimum Two Bolts Test**: Verifies that for any combination of loads (0-100 kN) and thicknesses from the specified set, the design always includes at least 2 bolts.

2. **Zero Load Test**: Confirms that even with zero load, the design includes at least 2 bolts.

3. **Small Load Test**: Tests with very small loads to ensure minimum of 2 bolts.

4. **Parameter Selection Test**: Verifies that appropriate design parameters are selected for various load cases.

5. **Error Handling Test**: Checks that the module properly handles invalid inputs like negative loads.

## Implementation Details

The tests use PyTest's parametrize feature to generate test cases for all combinations of loads and thicknesses, ensuring comprehensive testing of the module's behavior. 