from physics.aerodynamics import Aerodynamics
from data.cessna_172s import Cessna172S

class FlightDynamics:
    def __init__(self):
        self.ac_specs = Cessna172S()

    def calculate_forces(self, velocity_kts, altitude_ft, power_percent, weight_lbs):
        return Aerodynamics.calculate_forces(velocity_kts, altitude_ft, weight_lbs, power_percent)

    def calculate_attitude(self, lift_to_weight_ratio, velocity_kts):
        pitch_deg = 0.0
        if lift_to_weight_ratio > 1.01:
            pitch_deg = min(15.0, (lift_to_weight_ratio - 1.0) * 40)
        elif lift_to_weight_ratio < 0.99:
            pitch_deg = max(-15.0, (lift_to_weight_ratio - 1.0) * 40)
        
        roll_deg = 0.0 
        return pitch_deg, roll_deg
