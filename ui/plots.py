import plotly.graph_objects as go
import numpy as np

def plot_drag_polar(cl_max=1.6, cd0=0.027, e=0.88, ar=7.32):
    """Genera la gráfica de la polar de arrastre (CL vs CD)"""
    cl = np.linspace(-0.2, cl_max, 100)
    cd = cd0 + (cl**2) / (np.pi * e * ar)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=cd, y=cl, mode='lines', name='Polar de Arrastre', line=dict(color='blue', width=3)))
    fig.update_layout(
        title="Polar de Arrastre (CL vs CD)",
        xaxis_title="Coeficiente de Arrastre (CD)",
        yaxis_title="Coeficiente de Sustentación (CL)",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='lightgray'),
        yaxis=dict(gridcolor='lightgray')
    )
    return fig

def plot_power_required_vs_available(weight_lbs, altitude_ft, max_power_hp=180, prop_eff=0.8):
    """Gráfica de potencia requerida vs potencia disponible"""
    from data.cessna_172s import Cessna172S
    ac = Cessna172S(weight_lbs, altitude_ft)
    
    v_kts = np.linspace(40, 160, 100)
    p_req = []
    for v in v_kts:
        # Potencia requerida = Drag * Velocity
        cl = weight_lbs / (0.5 * ac.get_air_density() * (v*1.68781)**2 * ac.WING_AREA_FT2)
        drag = ac.compute_drag(v, cl)
        p_req.append((drag * v * 1.68781) / 550)  # HP
        
    p_avail = [max_power_hp * prop_eff] * len(v_kts)
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=v_kts, y=p_req, mode='lines', name='Potencia Requerida', line=dict(color='red', width=3)))
    fig.add_trace(go.Scatter(x=v_kts, y=p_avail, mode='lines', name='Potencia Disponible', line=dict(color='green', width=3, dash='dash')))
    
    fig.update_layout(
        title="Potencia Requerida vs Disponible",
        xaxis_title="Velocidad (KTAS)",
        yaxis_title="Potencia (HP)",
        height=350,
        margin=dict(l=20, r=20, t=50, b=20),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis=dict(gridcolor='lightgray'),
        yaxis=dict(gridcolor='lightgray'),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
    )
    return fig
