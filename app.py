import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import math

st.set_page_config(page_title="StudyLab — Physics", page_icon="⚡", layout="wide")

st.markdown("""
<style>
    .main-title { font-size: 2.5rem; font-weight: 700; text-align: center; margin-bottom: 0.3rem; }
    .sub-title { text-align: center; color: #888; margin-bottom: 2rem; }
    .result-box { background: #1a1a2e; border-radius: 8px; padding: 0.8rem 1rem; margin: 0.5rem 0; border-left: 4px solid #10b981; }
    h2 { border-bottom: 1px solid #333; padding-bottom: 0.3rem; }
    .stApp { background: #0f0f1a; }
    .block-container { padding-top: 1.5rem !important; }
</style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">⚡ StudyLab — Physics</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Interactive physics simulations</div>', unsafe_allow_html=True)

# ── SIDEBAR: Category → Topic ─────────────────────────────
category = st.sidebar.selectbox("Category", [
    "🎯 Mechanics",
    "💡 Optics",
    "⚡ Electricity",
    "🔄 Oscillations",
])

topic_map = {
    "🎯 Mechanics": ["Projectile Motion", "Kinematics"],
    "💡 Optics": ["Snell's Law (Refraction)"],
    "⚡ Electricity": ["Ohm's Law"],
    "🔄 Oscillations": ["Simple Pendulum"],
}

topic = st.sidebar.radio("Topic", topic_map[category])

# ── Projectile ────────────────────────────────────────────
if topic == "Projectile Motion":
    st.markdown("## Projectile Motion Simulator")
    col1, col2 = st.columns(2)
    with col1:
        v0 = st.slider("Initial velocity (m/s)", 1.0, 100.0, 30.0, 1.0)
        angle = st.slider("Launch angle (°)", 1.0, 89.0, 45.0, 1.0)
    with col2:
        h0 = st.slider("Initial height (m)", 0.0, 50.0, 0.0, 1.0)
        g = st.slider("Gravity (m/s²)", 1.0, 20.0, 9.81, 0.01)

    rad = math.radians(angle)
    vx = v0 * math.cos(rad)
    vy0 = v0 * math.sin(rad)
    
    t_flight = (vy0 + math.sqrt(vy0**2 + 2*g*h0)) / g
    max_h = h0 + vy0**2 / (2*g)
    x_range = vx * t_flight

    t = np.linspace(0, t_flight, 300)
    x_pos = vx * t
    y_pos = h0 + vy0 * t - 0.5 * g * t**2

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x_pos, y=y_pos, mode="lines",
                              name="Trajectory", line=dict(color="#6366f1", width=3)))
    fig.add_trace(go.Scatter(x=[x_pos[-1]], y=[y_pos[-1]], mode="markers",
                              marker=dict(size=10, color="#ef4444"), name="Landing"))
    fig.update_layout(height=400, margin=dict(l=20, r=20, t=20, b=20),
                      xaxis_title="Distance (m)", yaxis_title="Height (m)",
                      yaxis_range=[0, max_h * 1.1])
    st.plotly_chart(fig, use_container_width=True)

    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("Flight time", f"{t_flight:.2f} s")
    with col2: st.metric("Range", f"{x_range:.2f} m")
    with col3: st.metric("Max height", f"{max_h:.2f} m")
    with col4: st.metric("Final velocity", f"{math.sqrt(vx**2 + (vy0 - g*t_flight)**2):.2f} m/s")

# ── Kinematics ────────────────────────────────────────────
elif topic == "Kinematics":
    st.markdown("## Kinematics — Motion Graphs")
    st.latex(r"v = u + at \quad\quad s = ut + \frac{1}{2}at^2 \quad\quad v^2 = u^2 + 2as")

    u = st.slider("Initial velocity u (m/s)", -50.0, 50.0, 10.0, 1.0)
    a_val = st.slider("Acceleration a (m/s²)", -20.0, 20.0, 2.0, 0.5)
    t_max = st.slider("Time range (s)", 1.0, 20.0, 10.0, 0.5)

    t = np.linspace(0, t_max, 400)
    v = u + a_val * t
    s = u * t + 0.5 * a_val * t**2

    fig = make_subplots(rows=2, cols=1, subplot_titles=("Velocity vs Time", "Displacement vs Time"),
                         shared_xaxes=True, vertical_spacing=0.08)
    fig.add_trace(go.Scatter(x=t, y=v, line=dict(color="#6366f1", width=2), name="v(t)"), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=s, line=dict(color="#10b981", width=2), name="s(t)"), row=2, col=1)
    fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dash"), row=1, col=1)
    fig.update_layout(height=500, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
    fig.update_xaxes(title_text="Time (s)", row=2, col=1)
    st.plotly_chart(fig, use_container_width=True)

# ── Snell's Law ──────────────────────────────────────────
elif topic == "Snell's Law (Refraction)":
    st.markdown("## Snell's Law of Refraction")
    st.latex(r"n_1 \sin\theta_1 = n_2 \sin\theta_2")

    n1 = st.number_input("Refractive index n₁", 1.0, 3.0, 1.0, 0.01)
    n2 = st.number_input("Refractive index n₂", 1.0, 3.0, 1.5, 0.01)
    theta1 = st.slider("Angle of incidence θ₁ (°)", 0, 89, 45, 1)

    sin_theta2 = n1 * math.sin(math.radians(theta1)) / n2
    if sin_theta2 > 1:
        st.error("🔴 Total internal reflection — sin(θ₂) > 1")
        theta2 = None
    else:
        theta2 = math.degrees(math.asin(sin_theta2))
        st.success(f"**Angle of refraction θ₂:** {theta2:.2f}°")

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=[-2, 2], y=[0, 0], mode="lines",
                              line=dict(color="#555", width=2), name="Interface"))
    x1 = -2 * math.sin(math.radians(theta1))
    y1 = 2 * math.cos(math.radians(theta1))
    fig.add_trace(go.Scatter(x=[0, x1], y=[0, y1], mode="lines",
                              line=dict(color="#f59e0b", width=2), name="Incident ray"))
    fig.add_annotation(x=x1/2, y=y1/2, text=f"θ₁={theta1}°", showarrow=False,
                       font=dict(color="#f59e0b"))

    if theta2:
        x2 = 2 * math.sin(math.radians(theta2))
        y2 = -2 * math.cos(math.radians(theta2))
        fig.add_trace(go.Scatter(x=[0, x2], y=[0, y2], mode="lines",
                                  line=dict(color="#6366f1", width=2), name="Refracted ray"))
        fig.add_annotation(x=x2/2, y=y2/2, text=f"θ₂={theta2:.1f}°", showarrow=False,
                           font=dict(color="#6366f1"))

    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
                              marker=dict(size=8, color="white"), name="Point"))
    fig.update_layout(height=450, xaxis_range=[-2.5, 2.5], yaxis_range=[-2.5, 2.5],
                      xaxis=dict(scaleanchor="y"), margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ── Ohm's Law ────────────────────────────────────────────
elif topic == "Ohm's Law":
    st.markdown("## Ohm's Law")
    st.latex(r"V = I \times R")
    mode = st.radio("Calculate:", ["V from I & R", "I from V & R", "R from V & I"], horizontal=True)

    if mode == "V from I & R":
        I = st.slider("Current I (A)", 0.0, 10.0, 2.0, 0.1)
        R = st.slider("Resistance R (Ω)", 0.1, 100.0, 10.0, 0.1)
        V = I * R
        st.success(f"**V = {V:.2f} V**")
    elif mode == "I from V & R":
        V = st.slider("Voltage V (V)", 0.0, 240.0, 12.0, 0.1)
        R = st.slider("Resistance R (Ω)", 0.1, 100.0, 10.0, 0.1)
        I = V / R
        st.success(f"**I = {I:.4f} A**")
    else:
        V = st.slider("Voltage V (V)", 0.0, 240.0, 12.0, 0.1)
        I = st.slider("Current I (A)", 0.0, 10.0, 1.2, 0.1)
        R = V / I if I > 0 else float("inf")
        st.success(f"**R = {R:.2f} Ω**")

    st.markdown("### I-V Characteristic")
    r_fixed = st.slider("Fixed resistance for graph (Ω)", 1.0, 100.0, 10.0, 1.0, key="iv_r")
    v_vals = np.linspace(0, 50, 200)
    i_vals = v_vals / r_fixed
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=v_vals, y=i_vals, mode="lines",
                              line=dict(color="#6366f1", width=2), name=f"R = {r_fixed}Ω"))
    fig.update_layout(height=350, xaxis_title="Voltage (V)", yaxis_title="Current (A)",
                      margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ── Pendulum ─────────────────────────────────────────────
elif topic == "Simple Pendulum":
    st.markdown("## Simple Pendulum")
    st.latex(r"T = 2\pi\sqrt{\frac{L}{g}}")

    L = st.slider("Length L (m)", 0.1, 5.0, 1.0, 0.1)
    g_p = st.slider("Gravity g (m/s²)", 1.0, 20.0, 9.81, 0.01)
    
    T = 2 * math.pi * math.sqrt(L / g_p)
    st.success(f"**Period T = {T:.4f} s**")
    st.info(f"Frequency f = {1/T:.4f} Hz")

    time = st.slider("Time (s)", 0.0, T * 2, 0.0, 0.01)
    theta0 = math.radians(30)
    theta_t = theta0 * math.cos(2 * math.pi * time / T)

    fig = go.Figure()
    x_bob = L * math.sin(theta_t)
    y_bob = -L * math.cos(theta_t)
    fig.add_trace(go.Scatter(x=[0, x_bob], y=[0, y_bob], mode="lines+markers",
                              line=dict(color="#6366f1", width=3),
                              marker=dict(size=[0, 12], color=["#6366f1", "#ef4444"]),
                              name="Pendulum"))
    fig.add_trace(go.Scatter(x=[0], y=[0], mode="markers",
                              marker=dict(size=6, color="#555"), name="Pivot"))
    fig.update_layout(height=450, xaxis_range=[-L-0.3, L+0.3], yaxis_range=[-L-0.3, 0.3],
                      xaxis=dict(scaleanchor="y"), margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig, use_container_width=True)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
