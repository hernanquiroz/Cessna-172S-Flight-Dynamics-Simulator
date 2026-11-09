"""
Tablero de instrumentos tipo cabina Cessna 172S
Instrumentos circulares interactivos con agujas reales.
"""
import streamlit as st
import plotly.graph_objects as go
import math

class Dashboard:
    
    @staticmethod
    def create_airspeed_indicator(airspeed_kts, stall_speed_kts=53):
        fig = go.Figure()
        R = 1.0 
        
        def value_to_angle(val):
            return 225 - (val / 180) * 270

        def draw_arc(start_val, end_val, color, width=10):
            start_a = value_to_angle(start_val)
            end_a = value_to_angle(end_val)
            steps = 50
            angles = [math.radians(start_a + (end_a - start_a) * i / steps) for i in range(steps + 1)]
            x = [R * math.cos(a) for a in angles]
            y = [R * math.sin(a) for a in angles]
            fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color=color, width=width), showlegend=False))

        draw_arc(0, 180, 'rgba(200,200,200,0.3)', 14)
        draw_arc(40, 85, 'white', 10)
        draw_arc(48, 129, 'green', 10)
        draw_arc(129, 163, 'yellow', 10)
        draw_arc(163, 163, 'red', 10)

        angle = value_to_angle(airspeed_kts)
        needle_len = 0.85
        nx = [0, needle_len * math.cos(math.radians(angle))]
        ny = [0, needle_len * math.sin(math.radians(angle))]
        fig.add_trace(go.Scatter(x=nx, y=ny, mode='lines', line=dict(color='red', width=4), showlegend=False))
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=12, color='black'), showlegend=False))

        fig.update_layout(
            title=f"🛩️ Velocímetro<br>{airspeed_kts:.0f} KIAS",
            xaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False),
            height=280, margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        )
        return fig
    
    @staticmethod
    def create_altitude_indicator(altitude_ft):
        fig = go.Figure()
        R = 1.0
        theta = [math.radians(a) for a in range(0, 360, 2)]
        cx = [R * math.cos(t) for t in theta]
        cy = [R * math.sin(t) for t in theta]
        fig.add_trace(go.Scatter(x=cx, y=cy, mode='lines', line=dict(color='lightgray', width=3), showlegend=False))

        angle_100 = (altitude_ft % 1000) / 1000 * 360
        angle_1k = (altitude_ft % 10000) / 10000 * 360
        angle_10k = (altitude_ft % 100000) / 100000 * 360

        def draw_needle(angle, length, width, color):
            rad = math.radians(90 - angle)
            nx = [0, length * math.cos(rad)]
            ny = [0, length * math.sin(rad)]
            fig.add_trace(go.Scatter(x=nx, y=ny, mode='lines', line=dict(color=color, width=width), showlegend=False))

        draw_needle(angle_10k, 0.5, 4, 'orange')
        draw_needle(angle_1k, 0.75, 4, 'green')
        draw_needle(angle_100, 0.9, 3, 'black')

        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=10, color='black'), showlegend=False))

        fig.update_layout(
            title=f" Altímetro<br>{altitude_ft:.0f} ft",
            xaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False),
            height=280, margin=dict(l=10, r=10, t=50, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        )
        return fig
    
    @staticmethod
    def create_attitude_indicator(pitch_deg=0, roll_deg=0):
        fig = go.Figure()
        roll_rad = math.radians(roll_deg)
        
        L = 2.0
        sky_x = [-L, L, L, -L]
        sky_y = [0, 0, L, L]
        ground_x = [-L, L, L, -L]
        ground_y = [-L, -L, 0, 0]
        
        pitch_offset = pitch_deg / 30.0 
        
        def rotate_and_translate(x, y):
            xr = x * math.cos(roll_rad) - y * math.sin(roll_rad)
            yr = x * math.sin(roll_rad) + y * math.cos(roll_rad)
            return xr, yr + pitch_offset
            
        sky_xr, sky_yr = rotate_and_translate(sky_x, sky_y)
        ground_xr, ground_yr = rotate_and_translate(ground_x, ground_y)
        
        fig.add_trace(go.Scatter(x=sky_xr, y=sky_yr, fill='toself', fillcolor='#4A90E2', line=dict(width=0), showlegend=False))
        fig.add_trace(go.Scatter(x=ground_xr, y=ground_yr, fill='toself', fillcolor='#8B4513', line=dict(width=0), showlegend=False))
        
        horizon_x = [-L, L]
        horizon_y = [0, 0]
        hx, hy = rotate_and_translate(horizon_x, horizon_y)
        fig.add_trace(go.Scatter(x=hx, y=hy, mode='lines', line=dict(color='white', width=3), showlegend=False))
        
        theta = [math.radians(a) for a in range(0, 360, 2)]
        cx = [math.cos(t) for t in theta]
        cy = [math.sin(t) for t in theta]
        fig.add_trace(go.Scatter(x=cx, y=cy, mode='lines', line=dict(color='black', width=8), showlegend=False))
        
        fig.add_trace(go.Scatter(x=[-0.3, 0.3], y=[0, 0], mode='lines', line=dict(color='orange', width=4), showlegend=False))
        fig.add_trace(go.Scatter(x=[0, 0], y=[-0.1, 0.1], mode='lines', line=dict(color='orange', width=4), showlegend=False))
        
        fig.update_layout(
            title=f"🎯 Horizonte Artificial<br>Pitch: {pitch_deg:.1f}° | Roll: {roll_deg:.1f}°",
            xaxis=dict(range=[-1.1, 1.1], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.1, 1.1], showgrid=False, zeroline=False, showticklabels=False),
            height=280, margin=dict(l=10, r=10, t=60, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)'
        )
        return fig
    
    @staticmethod
    def create_forces_panel(forces_data):
        fig = go.Figure()
        fuerzas = ['Sustentación\n(Lift)', 'Peso\n(Weight)', 'Empuje\n(Thrust)', 'Arrastre\n(Drag)']
        valores = [forces_data['lift_lbs'], forces_data['weight_lbs_force'], forces_data['thrust_lbs'], forces_data['drag_lbs']]
        colores = ['#2ca02c', '#d62728', '#1f77b4', '#ff7f0e']
        
        fig.add_trace(go.Bar(x=fuerzas, y=valores, marker_color=colores, text=[f'{v:.0f} lbs' for v in valores], textposition='auto'))
        
        fig.update_layout(
            title="⚖️ Fuerzas Actuando sobre la Aeronave",
            yaxis_title="Fuerza (lbs)", height=300, margin=dict(l=20, r=20, t=50, b=20),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', yaxis=dict(gridcolor='lightgray')
        )
        return fig
    
    @staticmethod
    def create_power_indicator(power_percent, rpm=2400):
        fig = go.Figure()
        R = 1.0
        def value_to_angle(val):
            return 225 - (val / 100) * 270
        
        start_a = value_to_angle(0)
        end_a = value_to_angle(100)
        steps = 50
        angles = [math.radians(start_a + (end_a - start_a) * i / steps) for i in range(steps + 1)]
        x = [R * math.cos(a) for a in angles]
        y = [R * math.sin(a) for a in angles]
        fig.add_trace(go.Scatter(x=x, y=y, mode='lines', line=dict(color='green', width=12), showlegend=False))

        angle = value_to_angle(power_percent)
        needle_len = 0.85
        nx = [0, needle_len * math.cos(math.radians(angle))]
        ny = [0, needle_len * math.sin(math.radians(angle))]
        fig.add_trace(go.Scatter(x=nx, y=ny, mode='lines', line=dict(color='red', width=4), showlegend=False))
        fig.add_trace(go.Scatter(x=[0], y=[0], mode='markers', marker=dict(size=10, color='black'), showlegend=False))

        fig.update_layout(
            title=f"🔧 Potencia del Motor<br>{power_percent:.0f}% ({rpm} RPM)",
            xaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False, scaleanchor="y", scaleratio=1),
            yaxis=dict(range=[-1.2, 1.2], showgrid=False, zeroline=False, showticklabels=False),
            height=280, margin=dict(l=10, r=10, t=60, b=10),
            paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
        )
        return fig
    
    @staticmethod
    def create_flight_status_panel(forces_data):
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
