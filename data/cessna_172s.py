class Cessna172S:
    """Especificaciones reales extraídas del POH del Cessna 172S"""
    
    # ========== PESOS (POH Sección 1 y 6) ==========
    EMPTY_WEIGHT_LBS = 1663.0
    MAX_RAMP_WEIGHT_LBS = 2558.0
    MAX_TAKEOFF_WEIGHT_LBS = 2550.0
    MAX_USEFUL_LOAD_LBS = 895.0
    
    # ========== DIMENSIONES Y AERODINÁMICA ==========
    WING_AREA_FT2 = 174.0
    WING_SPAN_FT = 36.1
    ASPECT_RATIO = 7.32
    CD0 = 0.031
    OSWALD_E = 0.85
    
    # ========== MOTOR (POH Sección 1 y 2) ==========
    ENGINE_MODEL = "Lycoming IO-360-L2A"
    MAX_POWER_BHP = 180.0
    MAX_RPM = 2700
    PROP_EFFICIENCY = 0.80
    
    # ========== VELOCIDADES LÍMITE (POH Sección 2 - KIAS) ==========
    V_STALL_FLAPS = 40.0
    V_STALL_CLEAN = 48.0
    V_FE_MAX = 85.0
    V_NO = 129.0
    V_NE = 163.0
    
    # ========== RENDIMIENTO (POH Sección 5) ==========
    SERVICE_CEILING_FT = 14000
    V_BEST_GLIDE = 68.0
    V_BEST_CLIMB = 74.0
    
    def __init__(self, weight_lbs=None, altitude_ft=0):
        self.weight_lbs = weight_lbs or self.MAX_TAKEOFF_WEIGHT_LBS
        self.altitude_ft = altitude_ft
