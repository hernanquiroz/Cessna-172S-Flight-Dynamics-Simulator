"""
Tablero de instrumentos tipo cabina Cessna 172S
"""
import streamlit as st
import plotly.graph_objects as go
from data.cessna_172s import Cessna172S


class Dashboard:
    """Tablero de instrumentos visual tipo cabina"""
    
    @staticmethod
    def create_airspeed_indicator(airspeed_kts, stall_speed_kts=53):
        """Crea un velocímetro tipo cabina con arcos de colores"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=airspeed_kts,
            number={'suffix': " KIAS", 'font': {'size': 28}},
            title={'text': "🛩️ Velocímetro (Airspeed)", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [0, 180], 'tickwidth': 1},
                'bar': {'color': "#1f77b4"},
                'steps': [
                    {'range': [0, 40], 'color': 'lightgray'},
                    {'range': [40, 48], 'color': 'white'},
                    {'range': [48, 85], 'color': '#90EE90'},
                    {'range': [85, 129], 'color': 'green'},
                    {'range': [129, 163], 'color': 'yellow'},
                    {'range': [163, 180], 'color': 'red'}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 163
                }
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_altitude_indicator(altitude_ft):
        """Indicador de altitud"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=altitude_ft,
            number={'suffix': " ft", 'font': {'size': 28}},
            title={'text': "📍 Altímetro (Altitude)", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [0, 15000]},
                'bar': {'color': "#2ca02c"},
                'steps': [
                    {'range': [0, 5000], 'color': '#E8F5E9'},
                    {'range': [5000, 10000], 'color': '#C8E6C9'},
                    {'range': [10000, 14000], 'color': '#A5D6A7'},
                    {'range': [14000, 15000], 'color': '#FFCDD2'}
                ]
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig
    
    @staticmethod
    def create_attitude_indicator(pitch_deg=0, roll_deg=0):
        """Horizonte artificial"""
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            x=[-1, 1, 1, -1],
            y=[0, 0, 1, 1],
            fill='toself',
            fillcolor='#4A90E2',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=[-1, 1, 1, -1],
            y=[-1, -1, 0, 0],
            fill='toself',
            fillcolor='#8B4513',
            line=dict(width=0),
            showlegend=False
        ))
        
        fig.add_trace(go.Scatter(
            x=[-1, 1],
            y=[0, 0],
            mode='lines',
            line=dict(color='white', width=3),
            showlegend=False
        ))
        
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
        
        fig.add_trace(go.Scatter(
            x=[0],
            y=[0],
            mode='markers',
            marker=dict(size=10, color='orange'),
            showlegend=False
        ))
        
        fig.update_layout(
            title=f"🎯 Horizonte Artificial (Pitch: {pitch_deg:.1f}°, Roll: {roll_deg:.1f}°)",
            xaxis=dict(range=[-1, 1], showgrid=False, zeroline=False, showticklabels=False),
            yaxis=dict(range=[-1, 1], showgrid=False, zeroline=False, showticklabels=False, 
                      scaleanchor="x", scaleratio=1),
            height=280,
            margin=dict(l=10, r=10, t=50, b=10),
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
        """Indicador de potencia del motor"""
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=power_percent,
            number={'suffix': "%", 'font': {'size': 28}},
            title={'text': f"🔧 Potencia ({rpm} RPM)", 'font': {'size': 18}},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#ff7f0e"},
                'steps': [
                    {'range': [0, 25], 'color': '#E8F5E9'},
                    {'range': [25, 50], 'color': '#C8E6C9'},
                    {'range': [50, 75], 'color': '#FFF9C4'},
                    {'range': [75, 100], 'color': '#FFCDD2'}
                ]
            }
        ))
        
        fig.update_layout(
            height=250,
            margin=dict(l=10, r=10, t=40, b=10),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
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
            status = "📉 Descendiendo"
            status_color = "orange"
        else:
            status = "✈️ Vuelo Nivelado"
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
        
        st.markdown(f"""
        <div style='background-color: {status_color}; padding: 15px; border-radius: 10px; 
                    text-align: center; margin-bottom: 20px;'>
            <h2 style='color: white; margin: 0;'>{status}</h2>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.plotly_chart(cls.create_airspeed_indicator(
                forces_data['velocity_kts'],
                forces_data['stall_speed_kts']
            ), use_container_width=True)
        
        with col2:
            st.plotly_chart(cls.create_altitude_indicator(
                forces_data['altitude_ft']
            ), use_container_width=True)
        
        with col3:
            st.plotly_chart(cls.create_power_indicator(
                forces_data['power_percent']
            ), use_container_width=True)
        
        col4, col5 = st.columns(2)
        
        with col4:
            st.plotly_chart(cls.create_attitude_indicator(pitch_deg, roll_deg), 
                          use_container_width=True)
        
        with col5:
            st.plotly_chart(cls.create_forces_panel(forces_data), 
                          use_container_width=True)
        
        st.markdown("### 📊 Métricas de Vuelo")
        metric_cols = st.columns(6)
        
        for i, (key, value) in enumerate(metrics.items()):
            with metric_cols[i]:
                st.metric(label=key, value=value)
