"""
Modelo de dinámica de vuelo completo
"""
import numpy as np
from data.cessna_172s import Cessna172S
from physics.aerodynamics import Aerodynamics

class FlightDynamics:
    """Simulación completa de dinámica de vuelo"""
    
    def __init__(self):
        self.aero = Aerodynamics()
        
    def calculate_forces(self, velocity_kts, altitude_ft, power_percent, 
                        weight_lbs, flaps_deg=0, temperature_c=None):
        """Calcula todas las fuerzas actuando sobre la aeronave"""
        power_hp = (power_percent / 100) * Cessna172S.MAX_POWER_BHP
        
        cl_base = 0.5
        if flaps_deg == 10:
            cl_base += 0.2
        elif flaps_deg == 20:
            cl_base += 0.4
        elif flaps_deg == 30:
            cl_base += 0.6
        
        cl_required = self.aero.calculate_cl_required(
            weight_lbs, velocity_kts, altitude_ft
        )
        
        cl = max(cl_base, cl_required)
        cl_max = Cessna172S.CL_MAX_FLAPS_DOWN if flaps_deg > 0 else Cessna172S.CL_MAX_FLAPS_UP
        cl = min(cl, cl_max)
        
        lift = self.aero.calculate_lift(velocity_kts, altitude_ft, cl)
        drag = self.aero.calculate_drag(velocity_kts, altitude_ft, cl)
        thrust = self.aero.calculate_thrust(power_hp, velocity_kts)
        weight = weight_lbs * Cessna172S.LBS_TO_KG * 9.81
        
        stall_speed_ms, stall_speed_kts = self.aero.calculate_stall_speed(
            weight_lbs, cl_max, altitude_ft
        )
        
        air_density = self.aero.air_density(altitude_ft, temperature_c)
        
        lift_to_weight = lift / weight if weight > 0 else 0
        thrust_to_drag = thrust / drag if drag > 0 else 0
        
        if lift_to_weight >= 0.98 and lift_to_weight <= 1.02:
            flight_status = "Vuelo nivelado"
        elif lift_to_weight > 1.02:
            flight_status = "Ascendiendo"
        else:
            flight_status = "Descendiendo"
        
        if velocity_kts < stall_speed_kts:
            flight_status = "¡PÉRDIDA!"
        
        return {
            'velocity_kts': velocity_kts,
            'altitude_ft': altitude_ft,
            'weight_lbs': weight_lbs,
            'power_percent': power_percent,
            'flaps_deg': flaps_deg,
            'lift_n': lift,
            'drag_n': drag,
            'thrust_n': thrust,
            'weight_n': weight,
            'lift_lbs': lift / (Cessna172S.LBS_TO_KG * 9.81),
            'drag_lbs': drag / (Cessna172S.LBS_TO_KG * 9.81),
            'thrust_lbs': thrust / (Cessna172S.LBS_TO_KG * 9.81),
            'weight_lbs_force': weight_lbs,
            'cl': cl,
            'cl_required': cl_required,
            'air_density_kg_m3': air_density,
            'density_ratio': air_density / 1.225,
            'stall_speed_kts': stall_speed_kts,
            'lift_to_weight': lift_to_weight,
            'thrust_to_drag': thrust_to_drag,
            'flight_status': flight_status
        }
    
    def calculate_performance_metrics(self, velocity_kts, altitude_ft, 
                                     power_percent, weight_lbs):
        """Calcula métricas de performance"""
        forces = self.calculate_forces(velocity_kts, altitude_ft, 
                                      power_percent, weight_lbs)
        
        power_available_hp = (power_percent / 100) * Cessna172S.MAX_POWER_BHP
        power_required_hp = (forces['drag_n'] * velocity_kts * Cessna172S.KTS_TO_MS) / Cessna172S.HP_TO_WATTS
        excess_power_hp = power_available_hp - power_required_hp
        
        rate_of_climb_fpm = (excess_power_hp * 33000) / weight_lbs if weight_lbs > 0 else 0
        
        if velocity_kts > 0:
            climb_angle_rad = np.arcsin(rate_of_climb_fpm / (velocity_kts * 101.27))
            climb_angle_deg = np.degrees(climb_angle_rad)
        else:
            climb_angle_deg = 0
        
        return {
            'excess_power_hp': excess_power_hp,
            'rate_of_climb_fpm': rate_of_climb_fpm,
            'climb_angle_deg': climb_angle_deg,
            'power_required_hp': power_required_hp
        }
