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
    "🎯 Mechanics": ["Projectile Motion", "Kinematics", "Momentum & Collisions"],
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

# ── Momentum & Collisions ────────────────────────────────
elif topic == "Momentum & Collisions":
    st.markdown("## Momentum & Collisions")
    st.latex(r"p = mv \qquad \text{Conservation: } \sum p_{\text{before}} = \sum p_{\text{after}}")

    mode = st.radio("Mode", ["1D Collision (Straight Line)", "2D Collision (With Angle)",
                             "Types of Collisions"], horizontal=True)

    if mode == "1D Collision (Straight Line)":
        st.markdown("### 1D Collision")
        st.latex(r"m_1 u_1 + m_2 u_2 = m_1 v_1 + m_2 v_2")

        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown("**Object 1**")
            m1 = st.slider("m₁ (kg)", 0.5, 20.0, 3.0, 0.1, key="mom_m1")
            u1 = st.slider("u₁ (m/s)", -20.0, 20.0, 5.0, 0.5, key="mom_u1")
        with col2:
            st.markdown("**Object 2**")
            m2 = st.slider("m₂ (kg)", 0.5, 20.0, 1.0, 0.1, key="mom_m2")
            u2 = st.slider("u₂ (m/s)", -20.0, 20.0, 0.0, 0.5, key="mom_u2")
        with col3:
            st.markdown("**Coefficient of Restitution**")
            e = st.slider("e", 0.0, 1.0, 1.0, 0.01, key="mom_e")

        # Final velocities
        total_mass = m1 + m2
        v1 = (m1 * u1 + m2 * u2 - m2 * e * (u1 - u2)) / total_mass
        v2 = (m1 * u1 + m2 * u2 + m1 * e * (u1 - u2)) / total_mass

        p_before = m1 * u1 + m2 * u2
        p_after = m1 * v1 + m2 * v2

        ke_before = 0.5 * m1 * u1**2 + 0.5 * m2 * u2**2
        ke_after = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
        ke_loss = ((ke_before - ke_after) / ke_before * 100) if ke_before > 0 else 0

        # Collision type
        if abs(e - 1.0) < 0.001:
            ctype = "🟢 Perfectly Elastic"
        elif abs(e) < 0.001:
            ctype = "🔴 Perfectly Inelastic (stick together)"
        else:
            ctype = "🟡 Partially Inelastic"

        st.markdown(
            f'<div class="result-box">'
            f'<strong>{ctype}</strong> (e = {e:.2f})<br>'
            f'<strong>v₁</strong> = {v1:.3f} m/s &nbsp;|&nbsp; '
            f'<strong>v₂</strong> = {v2:.3f} m/s<br>'
            f'<strong>p_before</strong> = {p_before:.3f} kg·m/s &nbsp;|&nbsp; '
            f'<strong>p_after</strong> = {p_after:.3f} kg·m/s<br>'
            f'<strong>KE before</strong> = {ke_before:.3f} J &nbsp;|&nbsp; '
            f'<strong>KE after</strong> = {ke_after:.3f} J '
            f'({"↘ lost" if ke_loss > 0.5 else "≈ conserved"} {ke_loss:.1f}%)'
            f'</div>',
            unsafe_allow_html=True,
        )

        # Bar chart: momentum before vs after
        labels = [
            f"Object 1<br>(m₁={m1:.1f}kg, u₁={u1:.1f})",
            f"Object 2<br>(m₂={m2:.1f}kg, u₂={u2:.1f})",
            f"Object 1<br>(v₁={v1:.2f})",
            f"Object 2<br>(v₂={v2:.2f})",
        ]
        p_vals = [m1 * u1, m2 * u2, m1 * v1, m2 * v2]
        colors = ["#6366f1", "#10b981", "#f59e0b", "#ef4444"]

        fig = go.Figure()
        fig.add_trace(go.Bar(x=["Before", "Before", "After", "After"],
                              y=p_vals, marker_color=colors,
                              text=[f"{v:.1f}" for v in p_vals],
                              textposition="outside",
                              hovertemplate="%{customdata}<br>p = %{y:.2f} kg·m/s",
                              customdata=labels,
                              showlegend=False))
        fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
        fig.update_layout(height=350,
                          yaxis_title="Momentum (kg·m/s)",
                          margin=dict(l=20, r=20, t=10, b=20))
        st.plotly_chart(fig, use_container_width=True)

    elif mode == "2D Collision (With Angle)":
        st.markdown("### 2D Elastic Collision")
        st.markdown("Ball 1 moves toward stationary Ball 2. Conservation in x and y:")
        st.latex(r"m_1\vec{v}_1 = m_1\vec{v}'_1 + m_2\vec{v}'_2")

        col1, col2 = st.columns(2)
        with col1:
            m1 = st.slider("m₁ (kg)", 0.5, 10.0, 2.0, 0.1, key="mom2d_m1")
            m2 = st.slider("m₂ (kg)", 0.5, 10.0, 1.0, 0.1, key="mom2d_m2")
            v1 = st.slider("|v₁| (m/s)", 1.0, 20.0, 5.0, 0.5, key="mom2d_v1")
        with col2:
            theta = st.slider("Approach angle θ (° from +x)", -89, 89, 30, 1, key="mom2d_th")
            phi1 = st.slider("Ball 1 deflection φ₁ (°)", -89, 89, -20, 1, key="mom2d_p1")

        # Elastic: solve for v2' and phi2 using conservation
        th_r = math.radians(theta)
        p1_r = math.radians(phi1)

        # Momentum components before
        px_before = m1 * v1 * math.cos(th_r)
        py_before = m1 * v1 * math.sin(th_r)

        # After collision: unknown v1', v2', phi2
        # We'll let user choose phi1, solve for v2' and phi2
        # Elastic + momentum conservation
        # Use quadratic in v1':
        # From momentum x: m1*v1*cosθ = m1*v1'*cosφ1 + m2*v2'*cosφ2  → (1)
        # From momentum y: m1*v1*sinθ = m1*v1'*sinφ1 + m2*v2'*sinφ2  → (2)
        # From energy: m1*v1² = m1*v1'² + m2*v2'²  → (3)

        # Square and add (1)+(2): (m1v1cosθ - m1v1'cosφ1)² + (m1v1sinθ - m1v1'sinφ1)² = (m2v2')²
        # => m2²v2'² = m1²[v1² + v1'² - 2v1v1'(cosθcosφ1 + sinθsinφ1)]
        # => m2²v2'² = m1²[v1² + v1'² - 2v1v1'cos(θ-φ1)]
        # Substitute into energy: m1v1² = m1v1'² + m2*v2'²
        # => m1(v1² - v1'²) = m1²/m2 * [v1² + v1'² - 2v1v1'cos(θ-φ1)]
        # Multiply both sides by m2:
        # m1*m2(v1² - v1'²) = m1²[v1² + v1'² - 2v1v1'cos(θ-φ1)]

        cos_diff = math.cos(th_r - p1_r)

        A = m1 * (m1 + m2)
        B = -2 * m1 * m2 * v1 * cos_diff
        C = m1 * m2 * v1**2 - m1**2 * v1**2

        discriminant = B**2 - 4 * A * C

        if discriminant >= 0:
            v1p = (-B - math.sqrt(discriminant)) / (2 * A)  # Take the smaller root
            v1p = max(0, v1p)

            # Now find v2' and phi2 from momentum
            px_after_1 = m1 * v1p * math.cos(p1_r)
            py_after_1 = m1 * v1p * math.sin(p1_r)

            px_2 = px_before - px_after_1
            py_2 = py_before - py_after_1

            v2p = math.sqrt(px_2**2 + py_2**2) / m2 if m2 > 0 else 0
            phi2 = math.degrees(math.atan2(py_2, px_2)) if v2p > 0.01 else 0

            p_before = math.sqrt(px_before**2 + py_before**2)
            p_after = math.sqrt((m1*v1p*math.cos(p1_r) + m2*v2p*math.cos(math.radians(phi2)))**2 +
                                (m1*v1p*math.sin(p1_r) + m2*v2p*math.sin(math.radians(phi2)))**2)

            ke_before = 0.5 * m1 * v1**2
            ke_after = 0.5 * m1 * v1p**2 + 0.5 * m2 * v2p**2
            ke_loss = ((ke_before - ke_after) / ke_before * 100) if ke_before > 0 else 0

            st.markdown(
                f'<div class="result-box">'
                f'<strong>After collision:</strong><br>'
                f'Ball 1: |v\'₁| = {v1p:.3f} m/s, φ₁ = {phi1:.0f}°<br>'
                f'Ball 2: |v\'₂| = {v2p:.3f} m/s, φ₂ = {phi2:.1f}°<br>'
                f'KE {"↘ lost" if ke_loss > 0.5 else "≈ conserved"} ({ke_loss:.1f}%)'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Vector diagram
            s = max(v1, v1p, v2p) * 1.5
            origin = np.array([0.0, 0.0])
            v1_vec = np.array([v1 * math.cos(th_r), v1 * math.sin(th_r)])
            v1p_vec = np.array([v1p * math.cos(p1_r), v1p * math.sin(p1_r)])
            v2p_vec = np.array([v2p * math.cos(math.radians(phi2)), v2p * math.sin(math.radians(phi2))])

            fig = go.Figure()
            # Before: v1
            fig.add_trace(go.Scatter(x=[0, v1_vec[0]], y=[0, v1_vec[1]],
                                      mode="lines+text",
                                      line=dict(color="#6366f1", width=3),
                                      text=["", f"v₁ ({v1} m/s)"], textposition="middle right",
                                      name="Before: Ball 1"))
            # After: v1'
            fig.add_trace(go.Scatter(x=[0, v1p_vec[0]], y=[0, v1p_vec[1]],
                                      mode="lines+text",
                                      line=dict(color="#f59e0b", width=3, dash="dash"),
                                      text=["", f"v\'₁ ({v1p:.2f})"], textposition="middle right",
                                      name="After: Ball 1"))
            # After: v2'
            fig.add_trace(go.Scatter(x=[0, v2p_vec[0]], y=[0, v2p_vec[1]],
                                      mode="lines+text",
                                      line=dict(color="#ef4444", width=3, dash="dash"),
                                      text=["", f"v\'₂ ({v2p:.2f})"], textposition="middle right",
                                      name="After: Ball 2"))

            fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
            fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
            fig.update_layout(height=400,
                              xaxis=dict(range=[-s, s], scaleanchor="y", constrain="domain"),
                              yaxis=dict(range=[-s, s]),
                              margin=dict(l=20, r=80, t=20, b=20),
                              legend=dict(orientation="h", y=1.02))
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.warning("No valid 2D elastic collision for these parameters. Try a different deflection angle.")

    elif mode == "Types of Collisions":
        st.markdown("### Types of Collisions")
        st.latex(r"e = \frac{\text{relative speed after}}{\text{relative speed before}} = \frac{v_2 - v_1}{u_1 - u_2}")

        col1, col2 = st.columns(2)
        with col1:
            m1 = st.slider("m₁ (kg)", 0.5, 10.0, 3.0, 0.1, key="type_m1")
            u1 = st.slider("u₁ (m/s)", 1.0, 20.0, 5.0, 0.5, key="type_u1")
        with col2:
            m2 = st.slider("m₂ (kg)", 0.5, 10.0, 3.0, 0.1, key="type_m2")
            u2 = st.slider("u₂ (m/s)", -10.0, 10.0, 0.0, 0.5, key="type_u2")

        total_mass = m1 + m2
        p_total = m1 * u1 + m2 * u2
        ke0 = 0.5 * m1 * u1**2 + 0.5 * m2 * u2**2

        rows = []
        for e_val, label in [(1.0, "🟢 Elastic"), (0.5, "🟡 Partially Inelastic"), (0.0, "🔴 Perfectly Inelastic")]:
            v1f = (p_total - m2 * e_val * (u1 - u2)) / total_mass
            v2f = (p_total + m1 * e_val * (u1 - u2)) / total_mass
            p_final = m1 * v1f + m2 * v2f
            ke_final = 0.5 * m1 * v1f**2 + 0.5 * m2 * v2f**2
            ke_pct = ((ke0 - ke_final) / ke0 * 100) if ke0 > 0 else 0

            stick = (abs(v1f - v2f) < 0.001)
            rows.append(
                f"<tr>"
                f"<td style='padding:6px 10px'><b>{label}</b></td>"
                f"<td style='text-align:center'>{e_val}</td>"
                f"<td style='text-align:center'>{v1f:.3f}</td>"
                f"<td style='text-align:center'>{v2f:.3f}</td>"
                f"<td style='text-align:center'>{'Yes' if stick else 'No'}</td>"
                f"<td style='text-align:center'>{ke_pct:.1f}%</td>"
                f"</tr>"
            )

        st.markdown(
            f'<table style="width:100%; border-collapse:collapse">'
            f'<tr style="background:#1a1a2e; border-bottom:1px solid #333">'
            f'<th style="padding:8px 10px; text-align:left">Type</th>'
            f'<th style="padding:8px 10px">e</th>'
            f'<th style="padding:8px 10px">v₁ (m/s)</th>'
            f'<th style="padding:8px 10px">v₂ (m/s)</th>'
            f'<th style="padding:8px 10px">Stick?</th>'
            f'<th style="padding:8px 10px">KE lost</th>'
            f'</tr>'
            + ''.join(rows) +
            f'</table>',
            unsafe_allow_html=True,
        )

        # Bar chart comparing KE
        labels = ["Elastic (e=1)", "Partially Inelastic (e=0.5)", "Perfectly Inelastic (e=0)"]
        ke_vals = []
        for e_val in [1.0, 0.5, 0.0]:
            v1f = (p_total - m2 * e_val * (u1 - u2)) / total_mass
            v2f = (p_total + m1 * e_val * (u1 - u2)) / total_mass
            ke_vals.append(0.5 * m1 * v1f**2 + 0.5 * m2 * v2f**2)

        fig = go.Figure()
        fig.add_trace(go.Bar(x=labels, y=[ke0, ke0, ke0],
                              marker_color="#333", opacity=0.4,
                              name="KE before", showlegend=True))
        fig.add_trace(go.Bar(x=labels, y=ke_vals,
                              marker_color=["#10b981", "#f59e0b", "#ef4444"],
                              name="KE after", showlegend=True))
        fig.update_layout(height=350,
                          yaxis_title="Kinetic Energy (J)",
                          barmode="overlay",
                          margin=dict(l=20, r=20, t=10, b=20))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Overlay bars: dark = KE before, colored = KE after")

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

    if theta2 is not None:
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
