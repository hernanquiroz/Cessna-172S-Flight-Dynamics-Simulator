import streamlit as st
from data.cessna_172s import Cessna172S
from physics.aerodynamics import compute_aerodynamic_forces
from physics.flight_dynamics import compute_pitch_roll
from ui.dashboard import Dashboard
from ui.plots import plot_drag_polar, plot_power_required_vs_available

# Configuración de página
st.set_page_config(page_title="Cessna 172S Simulator", page_icon="✈️", layout="wide")

# Inicializar el modelo de datos si no existe
if 'ac_model' not in st.session_state:
    st.session_state.ac_model = Cessna172S()

st.title("✈️ Simulador de Dinámica de Vuelo - Cessna 172S")
st.markdown("Modelo interactivo basado en datos reales de POH y coeficientes aerodinámicos de vuelo.")

# Barra lateral de controles
st.sidebar.header("🎛️ Controles de Vuelo")
velocity_kts = st.sidebar.slider("Velocidad (KIAS)", min_value=30, max_value=180, value=90, step=1)
altitude_ft = st.sidebar.slider("Altitud (ft)", min_value=0, max_value=14000, value=0, step=100)
weight_lbs = st.sidebar.slider("Peso (lbs)", min_value=1680, max_value=2550, value=2300, step=10)
power_percent = st.sidebar.slider("Potencia del Motor (%)", min_value=0, max_value=100, value=75, step=1)

# Calcular fuerzas
forces_data = compute_aerodynamic_forces(velocity_kts, altitude_ft, weight_lbs, power_percent)

# Calcular actitud (Pitch y Roll)
pitch_deg, roll_deg = compute_pitch_roll(velocity_kts, power_percent, forces_data['lift_to_weight'])

# Renderizar el tablero de instrumentos
status, status_color, metrics = Dashboard.create_flight_status_panel(forces_data)

st.markdown(f"""
<div style='background-color: {status_color}; padding: 15px; border-radius: 10px; 
            text-align: center; margin-bottom: 20px;'>
    <h2 style='color: white; margin: 0;'>{status}</h2>
</div>
""", unsafe_allow_html=True)

# Primera fila de instrumentos
col1, col2, col3 = st.columns(3)
with col1:
    st.plotly_chart(Dashboard.create_airspeed_indicator(velocity_kts, forces_data['stall_speed_kts']), width="stretch")
with col2:
    st.plotly_chart(Dashboard.create_altitude_indicator(altitude_ft), width="stretch")
with col3:
    st.plotly_chart(Dashboard.create_power_indicator(power_percent), width="stretch")

# Segunda fila: Horizonte y Fuerzas
col4, col5 = st.columns(2)
with col4:
    st.plotly_chart(Dashboard.create_attitude_indicator(pitch_deg, roll_deg), width="stretch")
with col5:
    st.plotly_chart(Dashboard.create_forces_panel(forces_data), width="stretch")

# Tercera fila: Gráficas de rendimiento
st.markdown("### 📊 Análisis de Rendimiento")
col6, col7 = st.columns(2)
with col6:
    st.plotly_chart(plot_drag_polar(), width="stretch")
with col7:
    st.plotly_chart(plot_power_required_vs_available(weight_lbs, altitude_ft), width="stretch")

# Métricas clave
st.markdown("### 📈 Métricas de Vuelo")
metric_cols = st.columns(6)
for i, (key, value) in enumerate(metrics.items()):
    with metric_cols[i]:
        st.metric(label=key, value=value)
