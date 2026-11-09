"""
Modelos aerodinámicos para el Cessna 172S
"""
import numpy as np
from data.cessna_172s import Cessna172S

class Aerodynamics:
    """Cálculos aerodinámicos basados en física real"""
    
    @staticmethod
    def air_density(altitude_ft, temperature_c=None):
        """
        Calcula la densidad del aire usando la atmósfera estándar ISA
        
        Args:
            altitude_ft: Altitud en pies
            temperature_c: Temperatura en Celsius (opcional, usa ISA si es None)
        
        Returns:
            Densidad del aire en kg/m³
        """
        # Constantes
        R = 287.05  # Constante del aire (J/(kg·K))
        g = 9.81  # Gravedad (m/s²)
        P0 = 101325  # Presión al nivel del mar (Pa)
        T0 = 288.15  # Temperatura estándar al nivel del mar (K)
        L = 0.0065  # Gradiente de temperatura (K/m)
        
        # Convertir altitud a metros
        altitude_m = altitude_ft * Cessna172S.FT_TO_M
        
        # Temperatura en la altitud (ISA)
        if temperature_c is None:
            T = T0 - L * altitude_m
        else:
            T = temperature_c + 273.15
        
        # Presión en la altitud
        P = P0 * (1 - L * altitude_m / T0) ** (g / (R * L))
        
        # Densidad
        rho = P / (R * T)
        
        return rho
    
    @staticmethod
    def calculate_lift(velocity_kts, altitude_ft, cl, wing_area_sqft=None):
        """
        Calcula la fuerza de sustentación
        
        L = ½ρv²SCl
        
        Args:
            velocity_kts: Velocidad en nudos
            altitude_ft: Altitud en pies
            cl: Coeficiente de sustentación
            wing_area_sqft: Superficie alar en pies cuadrados
        
        Returns:
            Sustentación en Newtons
        """
        if wing_area_sqft is None:
            wing_area_sqft = Cessna172S.WING_AREA_SQFT
        
        # Conversiones
        velocity_ms = velocity_kts * Cessna172S.KTS_TO_MS
        wing_area_m2 = wing_area_sqft * (Cessna172S.FT_TO_M ** 2)
        
        # Densidad del aire
        rho = Aerodynamics.air_density(altitude_ft)
        
        # Sustentación
        lift = 0.5 * rho * velocity_ms**2 * wing_area_m2 * cl
        
        return lift
    
    @staticmethod
    def calculate_drag(velocity_kts, altitude_ft, cl, wing_area_sqft=None, aspect_ratio=None):
        """
        Calcula la fuerza de arrastre total (parásito + inducido)
        
        D = ½ρv²S(CD0 + Cl²/(π·AR·e))
        
        Args:
            velocity_kts: Velocidad en nudos
            altitude_ft: Altitud en pies
            cl: Coeficiente de sustentación
            wing_area_sqft: Superficie alar en pies cuadrados
            aspect_ratio: Relación de aspecto (opcional)
        
        Returns:
            Arrastre en Newtons
        """
        if wing_area_sqft is None:
            wing_area_sqft = Cessna172S.WING_AREA_SQFT
        
        if aspect_ratio is None:
            aspect_ratio = (Cessna172S.WING_SPAN_FT**2) / wing_area_sqft
        
        # Conversiones
        velocity_ms = velocity_kts * Cessna172S.KTS_TO_MS
        wing_area_m2 = wing_area_sqft * (Cessna172S.FT_TO_M ** 2)
        
        # Densidad del aire
        rho = Aerodynamics.air_density(altitude_ft)
        
        # Coeficiente de arrastre inducido
        cd_induced = (cl**2) / (np.pi * aspect_ratio * Cessna172S.OSWALD_EFFICIENCY)
        
        # Coeficiente de arrastre total
        cd_total = Cessna172S.CD0 + cd_induced
        
        # Arrastre
        drag = 0.5 * rho * velocity_ms**2 * wing_area_m2 * cd_total
        
        return drag
    
    @staticmethod
    def calculate_thrust(power_hp, velocity_kts, efficiency=0.85):
        """
        Calcula el empuje disponible
        
        T = (P · η) / v
        
        Args:
            power_hp: Potencia del motor en HP
            velocity_kts: Velocidad en nudos
            efficiency: Eficiencia de la hélice (típicamente 0.80-0.85)
        
        Returns:
            Empuje en Newtons
        """
        # Conversiones
        power_watts = power_hp * Cessna172S.HP_TO_WATTS
        velocity_ms = velocity_kts * Cessna172S.KTS_TO_MS
        
        # Evitar división por cero
        if velocity_ms < 1:
            velocity_ms = 1
        
        # Empuje
        thrust = (power_watts * efficiency) / velocity_ms
        
        return thrust
    
    @staticmethod
    def calculate_cl_required(weight_lbs, velocity_kts, altitude_ft, wing_area_sqft=None):
        """
        Calcula el coeficiente de sustentación requerido para vuelo nivelado
        
        Cl = W / (½ρv²S)
        
        Args:
            weight_lbs: Peso en libras
            velocity_kts: Velocidad en nudos
            altitude_ft: Altitud en pies
            wing_area_sqft: Superficie alar en pies cuadrados
        
        Returns:
            Coeficiente de sustentación requerido
        """
        if wing_area_sqft is None:
            wing_area_sqft = Cessna172S.WING_AREA_SQFT
        
        # Conversiones
        weight_n = weight_lbs * Cessna172S.LBS_TO_KG * 9.81
        velocity_ms = velocity_kts * Cessna172S.KTS_TO_MS
        wing_area_m2 = wing_area_sqft * (Cessna172S.FT_TO_M ** 2)
        
        # Densidad del aire
        rho = Aerodynamics.air_density(altitude_ft)
        
        # CL requerido
        cl_required = weight_n / (0.5 * rho * velocity_ms**2 * wing_area_m2)
        
        return cl_required
    
    @staticmethod
    def calculate_stall_speed(weight_lbs, cl_max, altitude_ft=0, wing_area_sqft=None):
        """
        Calcula la velocidad de pérdida
        
        Vs = √(2W / (ρ·S·Cl_max))
        
        Args:
            weight_lbs: Peso en libras
            cl_max: Coeficiente de sustentación máximo
            altitude_ft: Altitud en pies
            wing_area_sqft: Superficie alar en pies cuadrados
        
        Returns:
            Velocidad de pérdida en nudos
        """
        if wing_area_sqft is None:
            wing_area_sqft = Cessna172S.WING_AREA_SQFT
        
        # Conversiones
        weight_n = weight_lbs * Cessna172S.LBS_TO_KG * 9.81
        wing_area_m2 = wing_area_sqft * (Cessna172S.FT_TO_M ** 2)
        
        # Densidad del aire
        rho = Aerodynamics.air_density(altitude_ft)
        
        # Velocidad de pérdida
        stall_speed_ms = np.sqrt((2 * weight_n) / (rho * wing_area_m2 * cl_max))
        stall_speed_kts = stall_speed_ms / Cessna172S.KTS_TO_MS
        
        return stall_speed_ms, stall_speed_kts
