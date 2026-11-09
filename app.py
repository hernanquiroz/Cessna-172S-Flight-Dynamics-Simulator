"""
Cessna 172S Flight Dynamics Simulator
Aplicación principal basada en datos reales del POH

Autor: Simulador Educativo de Vuelo
Versión: 1.0
Modelo: Cessna 172S Skyhawk
Motor: Lycoming IO-360-L2A (180 BHP)
"""

import streamlit as st
import numpy as np
import pandas as pd
import plotly.graph_objects as go
from data.cessna_172s import Cessna172S
from physics.flight_dynamics import FlightDynamics
from ui.dashboard import Dashboard
from ui.plots import FlightPlots


st.set_page_config(
    page_title="Cessna 172S Flight Simulator",
    page_icon="🛩️",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Función principal de la aplicación"""
    
    st.title("🛩️ Simulador de Dinámica de Vuelo - Cessna 172S")
    st.markdown("""
    **Simulador educativo basado en datos reales del Pilot's Operating Handbook (POH)**  
    Modelo: Cessna 172S Skyhawk | Motor: Lycoming IO-360-L2A (180 BHP)
    """)
    
    flight_dynamics = FlightDynamics()
    
    st.sidebar.header("🎛️ Controles de Vuelo")
    
    velocity_kts = st.sidebar.slider(
        "⚡ Velocidad (KIAS)",
        min_value=30, max_value=163, value=90, step=1,
        help="Velocidad indicada en nudos"
    )
    
    altitude_ft = st.sidebar.slider(
        "📍 Altitud (ft)",
        min_value=0, max_value=14000, value=0, step=100,
        help="Altitud de presión en pies"
    )
    
    power_percent = st.sidebar.slider(
        "🔧 Potencia del Motor (%)",
        min_value=0, max_value=100, value=75, step=5,
        help="Porcentaje de potencia (0-100%)"
    )
    
    weight_lbs = st.sidebar.slider(
        "⚖️ Peso Total (lbs)",
        min_value=1800, max_value=2550, value=2300, step=10,
        help="Peso total de la aeronave"
    )
    
    flaps_deg = st.sidebar.selectbox(
        "🔽 Deflexión de Flaps",
        options=[0, 10, 20, 30],
        index=0,
        help="Grados de deflexión de flaps"
    )
    
    temperature_offset = st.sidebar.slider(
        "🌡️ Desviación de Temperatura (°C vs ISA)",
        min_value=-20, max_value=40, value=0, step=1,
        help="Desviación de la temperatura estándar ISA"
    )
    
    isa_temp = 15 - (altitude_ft / 1000) * 2
    actual_temp = isa_temp + temperature_offset
    
    forces_data = flight_dynamics.calculate_forces(
        velocity_kts=velocity_kts,
        altitude_ft=altitude_ft,
        power_percent=power_percent,
        weight_lbs=weight_lbs,
        flaps_deg=flaps_deg,
        temperature_c=actual_temp
    )
    
    lift_weight_ratio = forces_data['lift_to_weight']
    if lift_weight_ratio > 1.02:
        pitch_deg = min((lift_weight_ratio - 1) * 50, 15)
    elif lift_weight_ratio < 0.98:
        pitch_deg = max((lift_weight_ratio - 1) * 50, -15)
    else:
        pitch_deg = 0
    
    st.markdown("---")
    st.subheader("📊 Tablero de Instrumentos")
    
    Dashboard.render_full_dashboard(forces_data, pitch_deg=pitch_deg)
    
    st.markdown("---")
    st.subheader("📈 Análisis de Performance")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "⚖️ Fuerzas vs Velocidad",
        "⚡ Potencia Req. vs Disp.",
        "📊 Diagrama V-n",
        "📐 CL vs Velocidad",
        "🌤️ Atmósfera"
    ])
    
    with tab1:
        fig1 = FlightPlots.plot_forces_vs_velocity(
            weight_lbs=weight_lbs,
            altitude_ft=altitude_ft,
            power_percent=power_percent,
            flaps_deg=flaps_deg
        )
        fig1.add_trace(go.Scatter(
            x=[velocity_kts],
            y=[forces_data['lift_lbs']],
            mode='markers',
            marker=dict(size=15, color='black', symbol='star'),
            name='Punto Actual (Lift)',
            showlegend=True
        ))
        st.plotly_chart(fig1, use_container_width=True)
        
        st.info(f"""
        **📌 Lectura del gráfico:**
        - 🟢 **Línea verde**: Sustentación (debe igualar al peso para vuelo nivelado)
        - 🟠 **Línea naranja**: Arrastre (aumenta con el cuadrado de la velocidad)
        - 🔵 **Línea azul**: Empuje disponible (disminuye con la velocidad)
        - 🔴 **Línea roja punteada**: Peso de la aeronave ({weight_lbs} lbs)
        - ⭐ **Estrella negra**: Tu punto de operación actual
        """)
    
    with tab2:
        fig2 = FlightPlots.plot_power_required_vs_available(
            weight_lbs=weight_lbs,
            altitude_ft=altitude_ft
        )
        st.plotly_chart(fig2, use_container_width=True)
        
        st.info("""
        **📌 Lectura del gráfico:**
        - 🔴 **Potencia Requerida**: La potencia necesaria para vencer el arrastre
        - 🟢 **Potencia Disponible (100%)**: Máxima potencia del motor
        - 🔵 **Potencia Disponible (75%)**: Potencia de crucero recomendada
        - La diferencia entre disponible y requerida es la **potencia excedente** para ascender
        """)
    
    with tab3:
        fig3 = FlightPlots.plot_vn_diagram(weight_lbs=weight_lbs)
        st.plotly_chart(fig3, use_container_width=True)
        
        st.info("""
        **📌 Lectura del Diagrama V-n:**
        - Muestra los **límites estructurales** de la aeronave
        - 🟢 **Zona verde**: Operación normal segura
        - 🔴 **Línea positiva**: Máximo factor de carga positivo (+3.8g)
        - 🔵 **Va**: Velocidad de maniobra
        - 🟠 **Vno**: Velocidad máxima de crucero estructural
        - 🔴 **Vne**: Velocidad que NUNCA debe excederse
        """)
    
    with tab4:
        fig4 = FlightPlots.plot_lift_coefficient_vs_velocity(
            weight_lbs=weight_lbs,
            altitude_ft=altitude_ft
        )
        st.plotly_chart(fig4, use_container_width=True)
        
        st.info("""
        **📌 Lectura del gráfico:**
        - Muestra el **CL necesario** para mantener vuelo nivelado a cada velocidad
        - A mayor velocidad → menor CL requerido
        - Si el CL requerido supera al CLmax → **PÉRDIDA (STALL)**
        - Los flaps aumentan el CLmax, permitiendo volar más lento
        """)
    
    with tab5:
        fig5 = FlightPlots.plot_density_altitude_effect()
        st.plotly_chart(fig5, use_container_width=True)
        
        st.info(f"""
        **📌 Condiciones Atmosféricas Actuales:**
        - Altitud: **{altitude_ft} ft**
        - Temperatura ISA: **{isa_temp:.1f}°C**
        - Temperatura real: **{actual_temp:.1f}°C**
        - Densidad del aire: **{forces_data['air_density_kg_m3']:.4f} kg/m³**
        - Ratio de densidad (σ): **{forces_data['density_ratio']:.4f}**
        """)
    
    with st.expander("📋 Especificaciones Técnicas del Cessna 172S (POH)"):
        specs = Cessna172S.get_specs_dict()
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("### ⚖️ Pesos")
            for k, v in specs['Pesos'].items():
                st.write(f"**{k}:** {v}")
        
        with col2:
            st.markdown("### 🔧 Motor")
            for k, v in specs['Motor'].items():
                st.write(f"**{k}:** {v}")
        
        with col3:
            st.markdown("### 🛩️ Ala")
            for k, v in specs['Ala'].items():
                st.write(f"**{k}:** {v}")
        
        col4, col5 = st.columns(2)
        
        with col4:
            st.markdown("### ⚡ Velocidades")
            for k, v in specs['Velocidades'].items():
                st.write(f"**{k}:** {v}")
        
        with col5:
            st.markdown("### 📈 Performance")
            for k, v in specs['Performance'].items():
                st.write(f"**{k}:** {v}")
    
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: gray; font-size: 12px;'>
    <p>🛩️ Simulador Educativo basado en el POH del Cessna 172S | 
    Datos reales de Cessna Aircraft Company</p>
    <p>⚠️ Este simulador es solo para fines educativos. No usar para operaciones reales de vuelo.</p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
