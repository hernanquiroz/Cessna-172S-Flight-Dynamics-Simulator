import math

class Cessna172S:
    """Modelo de datos y especificaciones reales del Cessna 172S"""
    
    # Especificaciones geométricas y de peso (POH / AOPA)[reference:3]
    WING_AREA_FT2 = 174.0
    WING_SPAN_FT = 36.1
    ASPECT_RATIO = 7.32
    EMPTY_WEIGHT_LBS = 1680.0
    MAX_GROSS_WEIGHT_LBS = 2550.0
    MAX_POWER_HP = 180.0
    PROP_EFFICIENCY = 0.80  # Eficiencia típica de hélice de paso fijo

    # Coeficientes aerodinámicos (basados en test de vuelo)[reference:4][reference:5]
    CD0 = 0.027          # Coeficiente de arrastre parásito
    OSWALD_E = 0.88      # Factor de eficiencia de Oswald
    CL_MAX = 1.6         # CL máximo sin flaps
    CL_MAX_FLAPS = 2.1   # CL máximo con flaps (aprox)

    # Velocidades límite (KIAS)[reference:6]
    V_STALL_CLEAN_KT = 48
    V_STALL_FLAPS_KT = 40
    V_NE_KT = 163
    V_CRUISE_KT = 124

    def __init__(self, weight_lbs=None, altitude_ft=0):
        self.weight_lbs = weight_lbs or self.MAX_GROSS_WEIGHT_LBS
        self.altitude_ft = altitude_ft

    def get_air_density(self):
        """Modelo de atmósfera estándar ISA simplificado"""
        # Densidad al nivel del mar en slugs/ft³
        rho0 = 0.0023769
        # Temperatura y presión estándar
        T0 = 288.15  # K
        L = 0.0065   # K/m
        g = 9.80665  # m/s²
        R = 287.05   # J/(kg·K)
        
        h_m = self.altitude_ft * 0.3048
        T = T0 - L * h_m
        p = 101325 * (T / T0) ** (g / (L * R))
        rho_kg_m3 = p / (R * T)
        # Convertir a slugs/ft³
        return rho_kg_m3 * 0.00194032

    def compute_lift(self, velocity_kts, cl=None):
        """Calcula la fuerza de sustentación en lbs"""
        if cl is None:
            cl = self.CL_MAX  # Simplificación para cálculo estático
        v_fps = velocity_kts * 1.68781
        rho = self.get_air_density()
        q = 0.5 * rho * (v_fps ** 2)
        return q * self.WING_AREA_FT2 * cl

    def compute_drag(self, velocity_kts, cl):
        """Calcula el arrastre total en lbs usando la polar de arrastre"""
        v_fps = velocity_kts * 1.68781
        rho = self.get_air_density()
        q = 0.5 * rho * (v_fps ** 2)
        # CD = CD0 + CL^2 / (pi * e * AR)
        cd = self.CD0 + (cl ** 2) / (math.pi * self.OSWALD_E * self.ASPECT_RATIO)
        return q * self.WING_AREA_FT2 * cd

    def compute_thrust(self, power_percent):
        """Calcula el empuje disponible en lbs"""
        # Potencia en Watts
        power_w = (self.MAX_POWER_HP * 745.7) * (power_percent / 100.0)
        # Asumimos una velocidad de referencia para el empuje estático
        # T = (P * eta) / V (V en m/s)
        # Para simplificar el panel, usamos una velocidad de referencia de crucero
        v_ref_ms = self.V_CRUISE_KT * 0.514444
        thrust_n = (power_w * self.PROP_EFFICIENCY) / v_ref_ms
        return thrust_n * 0.224809  # Convertir N a lbs
