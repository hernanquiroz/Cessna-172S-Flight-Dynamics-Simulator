import streamlit as st
import pandas as pd
from data.cessna_172s import Cessna172S
from physics.flight_dynamics import FlightDynamics
from ui.dashboard import Dashboard

st.set_page_config(page_title="Cessna 172S - POH Simulator", page_icon="✈️", layout="wide")

st.title("✈️ Simulador de Dinámica de Vuelo - Cessna 172S")
st.markdown("Modelo basado en el **Pilot's Operating Handbook (POH)** real del Cessna 172S. Modifica los controles para ver cómo interactúan las 4 fuerzas fundamentales.")

flight_dynamics = FlightDynamics()

# ========== SIDEBAR: CONTROLES ==========
st.sidebar.header("🎛️ Controles de Vuelo")
velocity_kts = st.sidebar.slider("Velocidad (KIAS)", min_value=30, max_value=180, value=90, step=1)
altitude_ft = st.sidebar.slider("Altitud (ft)", min_value=0, max_value=14000, value=5000, step=100)
weight_lbs = st.sidebar.slider("Peso (lbs)", min_value=1663, max_value=2550, value=2300, step=10)
power_percent = st.sidebar.slider("Potencia del Motor (%)", min_value=0, max_value=100, value=65, step=1)

# ========== CÁLCULO DE FUERZAS ==========
forces_data = flight_dynamics.calculate_forces(
    velocity_kts=velocity_kts,
    altitude_ft=altitude_ft,
    power_percent=power_percent,
    weight_lbs=weight_lbs
)

pitch_deg, roll_deg = flight_dynamics.calculate_attitude(forces_data['lift_to_weight'], velocity_kts)

# ========== PANEL DE ESTADO ==========
lift_weight_ratio = forces_data['lift_to_weight']
if forces_data['velocity_kts'] < forces_data['stall_speed_kts']:
    status = "🚨 ¡PÉRDIDA! (STALL)"
    status_color = "red"
elif lift_weight_ratio > 1.02:
    status = "📈 Ascendiendo"
    status_color = "green"
elif lift_weight_ratio < 0.98:
    status = "📉 Descendiendo"
    status_color = "orange"
else:
    status = "✈️ Vuelo Nivelado"
    status_color = "blue"

st.markdown(f"""
<div style='background-color: {status_color}; padding: 15px; border-radius: 10px; 
            text-align: center; margin-bottom: 20px;'>
    <h2 style='color: white; margin: 0;'>{status}</h2>
</div>
""", unsafe_allow_html=True)

# ========== TABLERO DE INSTRUMENTOS ==========
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(Dashboard.create_airspeed_indicator(velocity_kts), use_container_width=True)
with col2:
    st.plotly_chart(Dashboard.create_altitude_indicator(altitude_ft), use_container_width=True)
with col3:
    st.plotly_chart(Dashboard.create_power_indicator(power_percent), use_container_width=True)

col4, col5 = st.columns(2)
with col4:
    st.plotly_chart(Dashboard.create_attitude_indicator(pitch_deg, roll_deg), use_container_width=True)
with col5:
    st.plotly_chart(Dashboard.create_forces_panel(forces_data), use_container_width=True)

# ========== MÉTRICAS ==========
st.markdown("### 📊 Métricas de Vuelo (Basadas en POH)")
metric_cols = st.columns(6)
metrics = {
    'Lift/Weight': f"{forces_data['lift_to_weight']:.2f}",
    'Thrust/Drag': f"{forces_data['thrust_to_drag']:.2f}",
    'CL Requerido': f"{forces_data['cl']:.3f}",
    'Velocidad Stall': f"{forces_data['stall_speed_kts']:.1f} KIAS",
    'Sustentación': f"{forces_data['lift_lbs']:.0f} lbs",
    'Arrastre': f"{forces_data['drag_lbs']:.0f} lbs"
}

for i, (key, value) in enumerate(metrics.items()):
    with metric_cols[i]:
        st.metric(label=key, value=value)

# ========== DATOS TÉCNICOS DEL POH ==========
with st.expander("📖 Ver Especificaciones Técnicas del POH"):
    st.markdown(f"""
    *   **Motor:** {Cessna172S.ENGINE_MODEL} ({Cessna172S.MAX_POWER_BHP} BHP)
    *   **Peso Máximo de Despegue:** {Cessna172S.MAX_TAKEOFF_WEIGHT_LBS} lbs
    *   **Velocidad de Pérdida (Vs0):** {Cessna172S.V_STALL_FLAPS} KIAS
    *   **Velocidad de Pérdida Limpia (Vs1):** {Cessna172S.V_STALL_CLEAN} KIAS
    *   **Velocidad Máxima de Crucero (Vno):** {Cessna172S.V_NO} KIAS
    *   **Velocidad Nunca Exceder (Vne):** {Cessna172S.V_NE} KIAS
    *   **Techo de Servicio:** {Cessna172S.SERVICE_CEILING_FT} ft
    """)
