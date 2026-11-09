# ✈️ Simulador de Dinámica de Vuelo - Cessna 172S

Este proyecto implementa un **simulador interactivo de dinámica de vuelo** para el avión Cessna 172S, con un tablero de instrumentos tipo cabina y gráficas de rendimiento aerodinámico.

## 🚀 Características
- **Instrumentos reales**: Velocímetro, altímetro, horizonte artificial e indicador de potencia con agujas funcionales.
- **Modelo físico**: Cálculo de sustentación, peso, empuje y arrastre basado en coeficientes aerodinámicos reales (CD0=0.027, e=0.88).
- **Gráficas de rendimiento**: Polar de arrastre y curva de potencia requerida vs disponible.
- **Controles interactivos**: Sliders para velocidad, altitud, peso y potencia.

## 📦 Instalación local
```bash
pip install -r requirements.txt
streamlit run app.py
