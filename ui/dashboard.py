"""
Tablero de instrumentos tipo cabina Cessna 172S
Incluye: velocímetro, altímetro, VSI, horizonte artificial, indicadores de fuerzas
"""
import streamlit as st
import plotly.graph_objects as go
from data.cessna_172s import Cessna172S
import math


class Dashboard:
    """Tablero de instrumentos visual tipo cabina"""
    
    @staticmethod
    def create_airspeed_indicator(airspeed_kts, stall_speed_kts=53):
        """Crea un velocímetro tipo cabina con aguja tradicional"""
        fig = go.Figure()
        
        # Arco blanco (flaps): 40-85 KIAS
        fig.add_trace(go.Scatter(
            x=[40, 85],
            y=[0, 0],
            mode='lines',
            line=dict(color='white', width=15),
            name='Flaps'
        ))
        
        # Arco verde (normal): 48-129 KIAS
        fig.add_trace(go.Scatter(
            x=[48, 129],
            y=[0, 0],
            mode='lines',
            line=dict(color='green', width=15),
            name='Normal'
        ))
        
        # Arco amarillo (caución): 129-163 KIAS
        fig.add_trace(go.Scatter(
            x=[129, 163],
            y=[0, 0],
            mode='lines',
            line=dict(color='yellow', width=15),
            name='Caución'
        ))
        
        # Línea roja (Vne): 163 KIAS
        fig.add_trace(go.Scatter(
            x=[163, 163],
            y=[0, 0],
            mode='lines',
            line=dict(color='red', width=15),
            name='Vne'
        ))
        
        # Calcular posición de la aguja
        angle = -90 + (airspeed_kts / 180) * 180  # De -90° a +90°
        needle_length = 0.85
        
        # Crear aguja
        needle_x = [0, needle_length * math.cos(math.radians(angle))]
        needle_y = [0, needle_length * math.sin(math.radians(angle))]
        
        fig.add_trace(go.Scatter(
            x=needle_x,
            y=needle_y,
            mode='lines',
            line=dict(color='black', width=4),
            name='Aguja',
            showlegend=False
        ))
        
        # Círculo central
        fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers',
            marker=dict(size=10, color='black'),
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"🛩️ Velocímetro<br>{airspeed_kts:.0f} KIAS",
            xaxis=dict(range=[-100, 200], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-100, 100], showgrid=False, zeroline=False, showticklabels=False),
            height=280,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            xaxis_fixedrange=True,
            yaxis_fixedrange=True,
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_altitude_indicator(altitude_ft):
        """Crea un altímetro con agujas tradicionales"""
        fig = go.Figure()
        
        # Calcular posición de las agujas
        # Aguja de 10,000 pies (una vuelta = 10,000 ft)
        angle_10k = -90 + ((altitude_ft % 10000) / 10000) * 360
        
        # Aguja de 1,000 pies (una vuelta = 1,000 ft)
        angle_1k = -90 + ((altitude_ft % 1000) / 1000) * 360
        
        # Aguja de 100 pies (una vuelta = 100 ft)
        angle_100 = -90 + ((altitude_ft % 100) / 100) * 360
        
        # Crear agujas
        for angle, length, width, color in [
            (angle_10k, 0.5, 3, 'orange'),   # Aguja corta - 10,000 ft
            (angle_1k, 0.75, 3, 'green'),    # Aguja mediana - 1,000 ft
            (angle_100, 0.9, 2, 'white')     # Aguja larga - 100 ft
        ]:
            needle_x = [0, length * math.cos(math.radians(angle))]
            needle_y = [0, length * math.sin(math.radians(angle))]
            
            fig.add_trace(go.Scatter(
                x=needle_x,
                y=needle_y,
                mode='lines',
                line=dict(color=color, width=width),
                showlegend=False
            ))
        
        # Círculo central
        fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers',
            marker=dict(size=8, color='black'),
            showlegend=False
        ))
        
        fig.update_layout(
            title=f" Altímetro<br>{altitude_ft:.0f} ft",
            xaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False),
            height=280,
            margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_attitude_indicator(pitch_deg=0, roll_deg=0):
        """Horizonte artificial (Attitude Indicator)"""
        fig = go.Figure()
        
        # Cielo (azul) - rotado según roll
        sky_angle = math.radians(roll_deg)
        sky_x = [-1, 1, 1, -1]
        sky_y = [0, 0, 1, 1]
        
        # Aplicar rotación
        sky_x_rot = [x * math.cos(sky_angle) - y * math.sin(sky_angle) for x, y in zip(sky_x, sky_y)]
        sky_y_rot = [x * math.sin(sky_angle) + y * math.cos(sky_angle) for x, y in zip(sky_x, sky_y)]
        
        # Ajustar por pitch
        sky_y_rot = [y + (pitch_deg / 30) for y in sky_y_rot]
        
        fig.add_trace(go.Scatter(
            x=sky_x_rot,
            y=sky_y_rot,
            fill='toself',
            fillcolor='#4A90E2',
            line=dict(width=0),
            showlegend=False
        ))
        
        # Tierra (marrón)
        ground_x = [-1, 1, 1, -1]
        ground_y = [-1, -1, 0, 0]
        
        ground_x_rot = [x * math.cos(sky_angle) - y * math.sin(sky_angle) for x, y in zip(ground_x, ground_y)]
        ground_y_rot = [x * math.sin(sky_angle) + y * math.cos(sky_angle) for x, y in zip(ground_x, ground_y)]
        ground_y_rot = [y + (pitch_deg / 30) for y in ground_y_rot]
        
        fig.add_trace(go.Scatter(
            x=ground_x_rot,
            y=ground_y_rot,
            fill='toself',
            fillcolor='#8B4513',
            line=dict(width=0),
            showlegend=False
        ))
        
        # Línea del horizonte
        horizon_x = [-1, 1]
        horizon_y = [0, 0]
        horizon_x_rot = [x * math.cos(sky_angle) - y * math.sin(sky_angle) for x, y in zip(horizon_x, horizon_y)]
        horizon_y_rot = [x * math.sin(sky_angle) + y * math.cos(sky_angle) for x, y in zip(horizon_x, horizon_y)]
        horizon_y_rot = [y + (pitch_deg / 30) for y in horizon_y_rot]
        
        fig.add_trace(go.Scatter(
            x=horizon_x_rot,
            y=horizon_y_rot,
            mode='lines',
            line=dict(color='white', width=3),
            showlegend=False
        ))
        
        # Símbolo del avión (cruz central) - fijo
        fig.add_trace(go.Scatter(
            x=[-0.3, 0.3],
            y=[0, 0],
            mode='lines',
            line=dict(color='orange', width=4),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=[0, 0],
            y=[-0.1, 0.1],
            mode='lines',
            line=dict(color='orange', width=4),
            showlegend=False
        ))
        
        # Círculo central
        fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers',
            marker=dict(size=10, color='orange'),
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"🎯 Horizonte Artificial<br>Pitch: {pitch_deg:.1f}° | Roll: {roll_deg:.1f}°",
            xaxis=dict(range=[-1, 1], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-1, 1], showgrid=False, zeroline=False, showticklabels=False, 
                      scaleanchor="x", scaleratio=1),
            height=280,
            margin=dict(l=10, r=10, t=60, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_forces_panel(forces_data):
        """Panel de las 4 fuerzas"""
        fig = go.Figure()
        
        fuerzas = ['Sustentación\n(Lift)', 'Peso\n(Weight)', 
                   'Empuje\n(Thrust)', 'Arrastre\n(Drag)']
        valores = [
            forces_data['lift_lbs'],
            forces_data['weight_lbs_force'],
            forces_data['thrust_lbs'],
            forces_data['drag_lbs']
        ]
        colores = ['#2ca02c', '#d62728', '#1f77b4', '#ff7f0e']
        
        fig.add_trace(go.Bar(
            x=fuerzas,
            y=valores,
            marker_color=colores,
            text=[f'{v:.0f} lbs' for v in valores],
            textposition='auto',
        ))
        
        fig.update_layout(
            title="⚖️ Fuerzas Actuando sobre la Aeronave",
            yaxis_title="Fuerza (lbs)",
            height=300,
            margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            yaxis=dict(gridcolor='lightgray')
        )
        
        return fig
    
    @staticmethod
    def create_power_indicator(power_percent, rpm=2400):
        """Indicador de potencia del motor con aguja"""
        fig = go.Figure()
        
        # Calcular ángulo de la aguja
        angle = -90 + (power_percent / 100) * 180
        needle_length = 0.85
        
        # Crear aguja
        needle_x = [0, needle_length * math.cos(math.radians(angle))]
        needle_y = [0, needle_length * math.sin(math.radians(angle))]
        
        fig.add_trace(go.Scatter(
            x=needle_x,
            y=needle_y,
            mode='lines',
            line=dict(color='red', width=4),
            name='Aguja',
            showlegend=False
        ))
        
        # Círculo central
        fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers',
            marker=dict(size=10, color='black'),
            showlegend=False
        ))
        
        # Arcos de colores
        fig.add_trace(go.Scatter(
            x=[0, 25, 50, 75, 100],
            y=[0, 0, 0, 0, 0],
            mode='lines',
            line=dict(color='green', width=10),
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"🔧 Potencia del Motor<br>{power_percent:.0f}% ({rpm} RPM)",
            xaxis=dict(range=[-100, 100], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-100, 100], showgrid=False, zeroline=False, showticklabels=False),
            height=280,
            margin=dict(l=10, r=10, t=60, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            showlegend=False
        )
        
        return fig
    
    @staticmethod
    def create_flight_status_panel(forces_data):
        """Panel de estado de vuelo"""
        lift_weight_ratio = forces_data['lift_to_weight']
        thrust_drag_ratio = forces_data['thrust_to_drag']
        stall_margin = (forces_data['velocity_kts'] - forces_data['stall_speed_kts']) / forces_data['stall_speed_kts'] * 100
        
        if forces_data['velocity_kts'] < forces_data['stall_speed_kts']:
            status = "🚨 ¡PÉRDIDA! (STALL)"
            status_color = "red"
        elif lift_weight_ratio > 1.02:
            status = "📈 Ascendiendo"
            status_color = "green"
        elif lift_weight_ratio < 0.98:
            status = " Descendiendo"
            status_color = "orange"
        else:
            status = "️ Vuelo Nivelado"
            status_color = "blue"
        
        return status, status_color, {
            'Lift/Weight': f"{lift_weight_ratio:.2f}",
            'Thrust/Drag': f"{thrust_drag_ratio:.2f}",
            'Margen al Stall': f"{stall_margin:.1f}%",
            'CL actual': f"{forces_data['cl']:.3f}",
            'CL requerido': f"{forces_data['cl_required']:.3f}",
            'Velocidad Stall': f"{forces_data['stall_speed_kts']:.1f} KIAS"
        }
    
    @classmethod
    def render_full_dashboard(cls, forces_data, pitch_deg=0, roll_deg=0):
        """Renderiza el tablero completo"""
        
        status, status_color, metrics = cls.create_flight_status_panel(forces_data)
        
        # Header con estado de vuelo
        st.markdown(f"""
        <div style='background-color: {status_color}; padding: 15px; border-radius: 10px; 
                    text-align: center; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0;'>{status}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Primera fila: Instrumentos principales
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.plotly_chart(cls.create_airspeed_indicator(
                forces_data['velocity_kts'],
                forces_data['stall_speed_kts']
            ), width="stretch")
        
        with col2:
            st.plotly_chart(cls.create_altitude_indicator(
                forces_data['altitude_ft']
            ), width="stretch")
        
        with col3:
            st.plotly_chart(cls.create_power_indicator(
                forces_data['power_percent']
            ), width="stretch")
        
        # Segunda fila: Horizonte y fuerzas
        col4, col5 = st.columns(2)
        
        with col4:
            st.plotly_chart(cls.create_attitude_indicator(pitch_deg, roll_deg), 
                          width="stretch")
        
        with col5:
            st.plotly_chart(cls.create_forces_panel(forces_data), 
                          width="stretch")
        
        # Métricas clave
        st.markdown("### 📊 Métricas de Vuelo")
        metric_cols = st.columns(6)
        
        for i, (key, value) in enumerate(metrics.items()):
            with metric_cols[i]:
                st.metric(label=key, value=value)
