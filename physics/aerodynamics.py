import math
from data.cessna_172s import Cessna172S

class Aerodynamics:
    
    @staticmethod
    def get_air_density(altitude_ft):
        """Atmósfera estándar ISA (slugs/ft³)"""
        rho0 = 0.0023769
        T0 = 288.15
        L = 0.0065
        g = 9.80665
        R = 287.05
        
        h_m = altitude_ft * 0.3048
        T = T0 - L * h_m
        p = 101325 * (T / T0) ** (g / (L * R))
        rho_kg_m3 = p / (R * T)
        return rho_kg_m3 * 0.00194032

    @staticmethod
    def calculate_forces(velocity_kts, altitude_ft, weight_lbs, power_percent):
        """Calcula sustentación, peso, empuje y arrastre"""
        ac = Cessna172S(weight_lbs, altitude_ft)
        rho = Aerodynamics.get_air_density(altitude_ft)
        
        # Presión dinámica (q)
        v_fps = velocity_kts * 1.68781
        q = 0.5 * rho * (v_fps ** 2)
        
        # Evitar división por cero a bajas velocidades
        if q <= 0:
            return None
            
        # 1. Peso (Fuerza constante hacia abajo)
        weight = weight_lbs
        
        # 2. Sustentación (Igual al peso para vuelo nivelado, calculamos el CL requerido)
        cl_required = weight / (q * ac.WING_AREA_FT2)
        lift = q * ac.WING_AREA_FT2 * cl_required
        
        # 3. Arrastre (Polar de arrastre: CD = CD0 + CL^2 / (pi * e * AR))
        cd = ac.CD0 + (cl_required ** 2) / (math.pi * ac.OSWALD_E * ac.ASPECT_RATIO)
        drag = q * ac.WING_AREA_FT2 * cd
        
        # 4. Empuje (Potencia * Eficiencia / Velocidad)
        power_hp = (power_percent / 100) * ac.MAX_POWER_BHP
        power_watts = power_hp * 745.7
        v_ms = velocity_kts * 0.514444
        thrust_n = (power_watts * ac.PROP_EFFICIENCY) / v_ms if v_ms > 0 else 0
        thrust = thrust_n * 0.224809 # Newtons a Libras
        
        # Velocidad de pérdida dinámica según el peso actual
        # Vs = sqrt(2 * W / (rho * S * CL_max))
        cl_max_clean = 1.5 # Estimado
        stall_speed = math.sqrt((2 * weight) / (rho * ac.WING_AREA_FT2 * cl_max_clean)) / 1.68781
        
        return {
            'lift_lbs': lift,
            'weight_lbs_force': weight,
            'thrust_lbs': thrust,
            'drag_lbs': drag,
            'cl': cl_required,
            'cl_required': cl_required,
            'stall_speed_kts': stall_speed,
            'lift_to_weight': lift / weight if weight > 0 else 0,
            'thrust_to_drag': thrust / drag if drag > 0 else 0,
            'velocity_kts': velocity_kts,
            'altitude_ft': altitude_ft,
            'power_percent': power_percent
        }
