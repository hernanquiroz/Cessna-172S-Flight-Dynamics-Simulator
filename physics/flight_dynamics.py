def compute_pitch_roll(velocity_kts, power_percent, lift_to_weight):
    """Simula actitud básica (Pitch y Roll) basada en parámetros de vuelo"""
    # Heurística simple para dar realismo al horizonte artificial
    pitch_deg = 0.0
    if lift_to_weight > 1.02:
        pitch_deg = min(15.0, (lift_to_weight - 1.0) * 50)
    elif lift_to_weight < 0.98:
        pitch_deg = max(-15.0, (lift_to_weight - 1.0) * 50)
    
    # El roll se deja en 0 para vuelo nivelado, pero se puede animar
    roll_deg = 0.0
    
    return pitch_deg, roll_deg
