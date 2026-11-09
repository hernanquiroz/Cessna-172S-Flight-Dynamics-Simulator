"""
Datos reales del Cessna 172S extraídos del Pilot's Operating Handbook (POH)
"""

class Cessna172S:
    """Especificaciones del Cessna 172S según POH"""
    
    # === PESOS (lbs) ===
    MAX_RAMP_WEIGHT = 2558
    MAX_TAKEOFF_WEIGHT = 2550
    MAX_LANDING_WEIGHT = 2550
    STANDARD_EMPTY_WEIGHT = 1663
    MAX_USEFUL_LOAD = 895
    MAX_BAGGAGE = 120
    
    # === MOTOR ===
    ENGINE_MODEL = "Lycoming IO-360-L2A"
    MAX_POWER_BHP = 180  # Brake Horse Power
    MAX_POWER_RPM = 2700
    ENGINE_TYPE = "Normally aspirated, fuel injected, 4-cylinder"
    
    # === HÉLICE ===
    PROPELLER_DIAMETER_IN = 76
    PROPELLER_TYPE = "Fixed pitch"
    
    # === ALA ===
    WING_AREA_SQFT = 174
    WING_SPAN_FT = 36.08  # 36 ft 1 in
    WING_LOADING = 14.7  # lbs/sq ft
    POWER_LOADING = 14.2  # lbs/hp
    
    # === COMBUSTIBLE ===
    FUEL_CAPACITY_TOTAL_GAL = 56
    FUEL_USABLE_GAL = 53
    FUEL_UNUSABLE_GAL = 3
    
    # === VELOCIDADES (KIAS) ===
    V_NE = 163  # Never exceed
    V_NO = 129  # Max structural cruising
    V_A_2550 = 105  # Maneuvering (2550 lbs)
    V_FE_10 = 110  # Max flaps extended (10°)
    V_FE_30 = 85  # Max flaps extended (30°)
    V_S0 = 48  # Stall speed flaps down
    V_S1 = 53  # Stall speed flaps up
    
    # === PERFORMANCE ===
    MAX_SPEED_KTAS_SL = 126  # Max speed at sea level
    CRUISE_75_8500FT_KTAS = 124  # Cruise 75% @ 8500 ft
    RATE_OF_CLIMB_SL_FPM = 730  # Rate of climb at sea level
    SERVICE_CEILING_FT = 14000
    
    # === DISTANCIAS (ft) ===
    TAKEOFF_GROUND_ROLL = 960
    TAKEOFF_OVER_50FT = 1630
    LANDING_GROUND_ROLL = 575
    LANDING_OVER_50FT = 1335
    
    # === COEFICIENTES AERODINÁMICOS (estimados) ===
    # CL_max (coeficiente de sustentación máximo)
    CL_MAX_FLAPS_UP = 1.5
    CL_MAX_FLAPS_DOWN = 1.8
    
    # CD0 (coeficiente de arrastre parásito)
    CD0 = 0.027
    
    # Eficiencia aerodinámica (Oswald efficiency factor)
    OSWALD_EFFICIENCY = 0.8
    
    # === CONVERSIONES ===
    LBS_TO_KG = 0.453592
    FT_TO_M = 0.3048
    KTS_TO_MS = 0.514444
    HP_TO_WATTS = 745.7
    
    @classmethod
    def get_specs_dict(cls):
        """Retorna todas las especificaciones en un diccionario"""
        return {
            'Pesos': {
                'Peso máximo rampa': f"{cls.MAX_RAMP_WEIGHT} lbs",
                'Peso máximo despegue': f"{cls.MAX_TAKEOFF_WEIGHT} lbs",
                'Peso vacío': f"{cls.STANDARD_EMPTY_WEIGHT} lbs",
                'Carga útil máxima': f"{cls.MAX_USEFUL_LOAD} lbs",
            },
            'Motor': {
                'Modelo': cls.ENGINE_MODEL,
                'Potencia máxima': f"{cls.MAX_POWER_BHP} BHP @ {cls.MAX_POWER_RPM} RPM",
                'Tipo': cls.ENGINE_TYPE,
            },
            'Ala': {
                'Superficie': f"{cls.WING_AREA_SQFT} sq ft",
                'Envergadura': f"{cls.WING_SPAN_FT} ft",
                'Carga alar': f"{cls.WING_LOADING} lbs/sq ft",
            },
            'Velocidades': {
                'Vne (Nunca exceder)': f"{cls.V_NE} KIAS",
                'Vno (Crucero máximo)': f"{cls.V_NO} KIAS",
                'Va (Maniobra)': f"{cls.V_A_2550} KIAS",
                'Vs0 (Pérdida flaps down)': f"{cls.V_S0} KIAS",
                'Vs1 (Pérdida flaps up)': f"{cls.V_S1} KIAS",
            },
            'Performance': {
                'Velocidad máxima': f"{cls.MAX_SPEED_KTAS_SL} KTAS",
                'Tasa de ascenso': f"{cls.RATE_OF_CLIMB_SL_FPM} fpm",
                'Techo de servicio': f"{cls.SERVICE_CEILING_FT} ft",
            }
        }
