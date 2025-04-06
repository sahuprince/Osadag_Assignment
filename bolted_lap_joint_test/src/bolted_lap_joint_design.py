import math

class IS800_2007:
    @staticmethod
    def cl_10_3_3_bolt_shear_capacity(bolt_fy, A_bolt, A_nc, n_shear, long_joint_factor, connection_location):
        """
        Calculate bolt shear capacity according to IS 800:2007 clause 10.3.3
        :param bolt_fy: Yield strength of the bolt
        :param A_bolt: Cross-sectional area of the bolt
        :param A_nc: Net cross-sectional area of the bolt at threads
        :param n_shear: Number of shear planes
        :param long_joint_factor: Long joint factor
        :param connection_location: Location of the connection ('Field' or 'Shop')
        :return: Shear capacity of the bolt
        """
        # Simplified implementation for demonstration
        # In a real implementation, this would follow the actual IS 800:2007 formula
        gamma_mb = 1.25  # Partial safety factor for bolt material
        f_ub = bolt_fy * 1.1  # Ultimate strength is approx 1.1 times yield strength
        
        # Basic shear capacity formula
        V_b = 0.6 * f_ub * A_bolt / gamma_mb
        
        # Adjust for shear planes
        if n_shear > 0:
            V_b *= n_shear
        else:
            # Default to single shear
            V_b *= 1
        
        # Apply long joint factor (simplified)
        if long_joint_factor > 0:
            V_b *= long_joint_factor
        
        # Adjust for connection location (simplified)
        if connection_location == 'Field':
            V_b *= 0.9  # 10% reduction for field connections
        
        return V_b

    @staticmethod
    def cl_10_3_4_bolt_bearing_capacity(fu_plate, bolt_fy, plate_thickness, bolt_diameter, end_distance, pitch, hole_type, connection_location):
        """
        Calculate bolt bearing capacity according to IS 800:2007 clause 10.3.4
        :param fu_plate: Ultimate tensile strength of the plate
        :param bolt_fy: Yield strength of the bolt
        :param plate_thickness: Thickness of the plate
        :param bolt_diameter: Diameter of the bolt
        :param end_distance: End distance
        :param pitch: Pitch distance
        :param hole_type: Type of hole ('Standard' or 'Oversized')
        :param connection_location: Location of the connection ('Field' or 'Shop')
        :return: Bearing capacity of the bolt
        """
        # Simplified implementation for demonstration
        # In a real implementation, this would follow the actual IS 800:2007 formula
        gamma_mb = 1.25  # Partial safety factor for bolt material
        
        # Calculate k1 (simplified)
        k1 = min(end_distance / (3 * bolt_diameter), pitch / (3 * bolt_diameter) - 0.25, 1)
        
        # Calculate k2 (simplified)
        k2 = 0.9  # For standard holes
        if hole_type == 'Oversized':
            k2 = 0.7
        
        # Basic bearing capacity formula
        V_dpb = 2.5 * k1 * k2 * fu_plate * bolt_diameter * plate_thickness / gamma_mb
        
        # Adjust for connection location (simplified)
        if connection_location == 'Field':
            V_dpb *= 0.9  # 10% reduction for field connections
        
        return V_dpb

def design_lap_joint(P, w, t1, t2):
    """
    Design a bolted lap joint connecting two plates.
    :param P: Tensile force in kN
    :param w: Width of the plates in mm
    :param t1: Thickness of plate 1 in mm
    :param t2: Thickness of plate 2 in mm
    :return: Dictionary of design parameters and results
    """
    
    # Validate input parameters
    if P < 0:
        raise ValueError("Tensile force P cannot be negative")
    
    if w <= 0:
        raise ValueError("Width w must be positive")
    
    if t1 <= 0:
        raise ValueError("Thickness t1 must be positive")
    
    if t2 <= 0:
        raise ValueError("Thickness t2 must be positive")
    
    # Add practical limits to prevent unreasonable values
    if w > 1000:
        raise ValueError("Width w is too large (> 1000 mm), please check your input")
    
    if t1 > 100 or t2 > 100:
        raise ValueError("Plate thickness is too large (> 100 mm), please check your input")

    # Convert tensile force to Newtons
    P_N = P * 1000

    # Available data
    d_list = [10, 12, 16, 20, 24]  # Bolt diameters in mm
    GB_list = [3.6, 4.6, 4.8, 5.6, 5.8]  # Bolt grades
    GP_list = ["E250", "E275", "E300", "E350", "E410"]  # Plate grades

    # Define a mapping from plate grade to yield and ultimate strength
    plate_grades = {
        "E250": (250, 410),
        "E275": (275, 440),
        "E300": (300, 470),
        "E350": (350, 510),
        "E410": (410, 550)
    }

    # Select the best plate grade based on the given thicknesses
    plate_grade = GP_list[-1]  # Choose the highest grade for the design
    fy_plate, fu_plate = plate_grades[plate_grade]  # Get the yield and ultimate strengths for the chosen grade

    # Initialize variables to store the best design
    best_design = None
    min_length = float('inf')

    for d in d_list:
        for GB in GB_list:
            # Calculate the bolt strength
            bolt_fu, bolt_fy = calculate_bolt_strength(GB)
            
            # Calculate the shear strength of one bolt
            A_bolt = math.pi * (d / 2) ** 2  # Cross-sectional area of the bolt
            V_b = IS800_2007.cl_10_3_3_bolt_shear_capacity(bolt_fy, A_bolt, A_bolt, 0, 0, 'Field')  # Shear capacity
            
            # Calculate the required number of bolts
            N_b = math.ceil(P_N / (V_b * 0.75))  # Using a safety factor of 1.33
            
            if N_b < 2:
                N_b = 2  # Ensure at least 2 bolts are used

            # Calculate distances
            e = max(d + 5, 1.5 * d)  # End distance (typically 5 mm larger than bolt diameter or 1.5 times diameter)
            p = max(d + 10, 2.5 * d)  # Pitch distance (typically 10 mm larger than bolt diameter or 2.5 times diameter)
            g = w / 2  # Gauge distance (for simplicity, use half of the plate width)

            # Calculate the length of the connection
            length_of_connection = 2 * e + (N_b - 1) * p

            # Calculate the bearing strength of the bolt
            V_dpb = IS800_2007.cl_10_3_4_bolt_bearing_capacity(fu_plate, bolt_fy, min(t1, t2), d, e, p, 'Standard', 'Field')

            # Calculate the efficiency of the connection
            Utilization_ratio = P_N / (N_b * min(V_b, V_dpb) * 0.75)  # Using a safety factor of 1.33
            
            # Check if this design is better
            if Utilization_ratio <= 1 and length_of_connection < min_length:
                min_length = length_of_connection
                best_design = {
                    "bolt_diameter": d,
                    "bolt_grade": GB,
                    "number_of_bolts": N_b,
                    "pitch_distance": p,
                    "gauge_distance": g,
                    "end_distance": e,
                    "edge_distance": e,
                    "number_of_rows": 1,  # Simple design assumption, can be improved
                    "number_of_columns": N_b,  # One column for simplicity
                    "hole_diameter": d + 2,  # Diameter of hole is slightly larger than the bolt
                    "strength_of_connection": N_b * min(V_b, V_dpb) * 0.75,  # Strength based on shear capacity
                    "yield_strength_plate_1": fy_plate,
                    "yield_strength_plate_2": fy_plate,
                    "length_of_connection": length_of_connection,
                    "efficiency_of_connection": Utilization_ratio
                }

    if best_design is None:
        raise ValueError("No suitable design found that meets the requirements.")

    return best_design


def calculate_bolt_strength(bolt_grade):
    """
    Calculate the ultimate tensile strength and yield strength of the bolt based on its grade.
    :param bolt_grade: Bolt grade (e.g., 4.6, 5.6)
    :return: List containing [ultimate tensile strength, yield strength] of the bolt
    """
    bolt_fu = float(int(bolt_grade) * 100)  # Ultimate tensile strength (MPa)
    bolt_fy = float((bolt_grade - int(bolt_grade)) * 10 * 100)  # Yield strength (MPa)
    return [bolt_fu, bolt_fy]


# Example usage
if __name__ == "__main__":
    P = 100  # Tensile force in kN
    w = 150  # Width of the plates in mm
    t1 = 10  # Thickness of plate 1 in mm
    t2 = 12  # Thickness of plate 2 in mm

    design = design_lap_joint(P, w, t1, t2)
    for key, value in design.items():
        print(f"{key}: {value}") 