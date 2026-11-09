"""
Modelos aerodinámicos para el Cessna 172S
"""
import numpy as np
from data.cessna_172s import Cessna172S

class Aerodynamics:
    """Cálculos aerodinámicos basados en física real"""
    
    @staticmethod
    def air_density(altitude_ft, temperature_c=None):
        """Calcula la densidad del aire usando la atmósfera estándar ISA"""
        R = 287.05
        g = 9.81
        P0 = 101325
        T0 = 288.15
        L = 0.0065
        
        altitude_m = altitude_ft * Cessna172S.FT_TO_M
        
        if temperature_c is None:
            T = T0 - L * altitude_m
        else:
            T = temperature_c + 273.15
        
        P = P0 * (1 - L * altitude_m / T0) ** (g / (R * L))
        rho = P / (R * T)
        
        return rho
    
    @staticmethod
    def calculate_lift(velocity_kts, altitude_ft, cl, wing_area_sqft=None):
        """Calcula la fuerza de sustentación: L = ½ρv²SCl"""
        if wing_area_sqft is None:
            wing_area_sqft = Cessna172S.WING_AREA_SQFT
        
        velocity_ms = velocity_kts * Cessna172S.KTS_TO_MS
        wing_area_m2 = wing_area_sqft * (Cessna172S.FT_TO_M ** 2)
        rho = Aerodynamics.air_density(altitude_ft)
        
        lift = 0.5 * rho * velocity_ms**2 * wing_area_m2 * cl
        return lift
    
    @staticmethod
    def calculate_drag(velocity_kts, altitude_ft, cl, wing_area_sqft=None, aspect_ratio=None):
        """Calcula la fuerza de arrastre total"""
        if wing_area_sqft is None:
            wing_area_sqft = Cessna172S.WING_AREA_SQFT
        if aspect_ratio is None:
            aspect_ratio = (Cessna172S.WING_SPAN_FT**2) / wing_area_sqft
        
        velocity_ms = velocity_kts * Cessna172S.KTS_TO_MS
        wing_area_m2 = wing_area_sqft * (Cessna172S.FT_TO_M ** 2)
        rho = Aerodynamics.air_density(altitude_ft)
        
        cd_induced = (cl**2) / (np.pi * aspect_ratio * Cessna172S.OSWALD_EFFICIENCY)
        cd_total = Cessna172S.CD0 + cd_induced
        
        drag = 0.5 * rho * velocity_ms**2 * wing_area_m2 * cd_total
        return drag
    
    @staticmethod
    def calculate_thrust(power_hp, velocity_kts, efficiency=0.85):
        """Calcula el empuje disponible: T = (P · η) / v"""
        power_watts = power_hp * Cessna172S.HP_TO_WATTS
        velocity_ms = velocity_kts * Cessna172S.KTS_TO_MS
        
        if velocity_ms < 1:
            velocity_ms = 1
        
        thrust = (power_watts * efficiency) / velocity_ms
        return thrust
    
    @staticmethod
    def calculate_cl_required(weight_lbs, velocity_kts, altitude_ft, wing_area_sqft=None):
        """Calcula el CL requerido para vuelo nivelado"""
        if wing_area_sqft is None:
            wing_area_sqft = Cessna172S.WING_AREA_SQFT
        
        weight_n = weight_lbs * Cessna172S.LBS_TO_KG * 9.81
        velocity_ms = velocity_kts * Cessna172S.KTS_TO_MS
        wing_area_m2 = wing_area_sqft * (Cessna172S.FT_TO_M ** 2)
        rho = Aerodynamics.air_density(altitude_ft)
        
        cl_required = weight_n / (0.5 * rho * velocity_ms**2 * wing_area_m2)
        return cl_required
    
    @staticmethod
    def calculate_stall_speed(weight_lbs, cl_max, altitude_ft=0, wing_area_sqft=None):
        """Calcula la velocidad de pérdida"""
        if wing_area_sqft is None:
            wing_area_sqft = Cessna172S.WING_AREA_SQFT
        
        weight_n = weight_lbs * Cessna172S.LBS_TO_KG * 9.81
        wing_area_m2 = wing_area_sqft * (Cessna172S.FT_TO_M ** 2)
        rho = Aerodynamics.air_density(altitude_ft)
        
        stall_speed_ms = np.sqrt((2 * weight_n) / (rho * wing_area_m2 * cl_max))
        stall_speed_kts = stall_speed_ms / Cessna172S.KTS_TO_MS
        
        return stall_speed_ms, stall_speed_kts
