import math
from data.cessna_172s import Cessna172S

def compute_aerodynamic_forces(velocity_kts, altitude_ft, weight_lbs, power_percent):
    """Calcula las 4 fuerzas fundamentales y coeficientes"""
    ac = Cessna172S(weight_lbs, altitude_ft)
    
    # Estimación del CL requerido para vuelo nivelado
    v_fps = velocity_kts * 1.68781
    rho = ac.get_air_density()
    q = 0.5 * rho * (v_fps ** 2)
    
    # CL requerido para mantener el peso (L = W)
    cl_required = weight_lbs / (q * ac.WING_AREA_FT2)
    
    # Fuerzas
    lift = ac.compute_lift(velocity_kts, cl_required)
    drag = ac.compute_drag(velocity_kts, cl_required)
    thrust = ac.compute_thrust(power_percent)
    
    # Evitar división por cero
    stall_speed = math.sqrt((2 * weight_lbs) / (rho * ac.WING_AREA_FT2 * ac.CL_MAX)) / 1.68781
    
    return {
        'lift_lbs': lift,
        'weight_lbs_force': weight_lbs,
        'thrust_lbs': thrust,
        'drag_lbs': drag,
        'cl': cl_required,
        'cl_required': cl_required,
        'stall_speed_kts': stall_speed,
        'lift_to_weight': lift / weight_lbs if weight_lbs > 0 else 0,
        'thrust_to_drag': thrust / drag if drag > 0 else 0,
        'velocity_kts': velocity_kts,
        'altitude_ft': altitude_ft,
        'power_percent': power_percent
    }
