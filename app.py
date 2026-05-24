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
    "⚡ Electricity": ["Ohm's Law", "Potential Divider", "I-V Characteristics"],
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
    max_v = max(abs(v.min()), abs(v.max()))
    max_s = max(abs(s.min()), abs(s.max()))

    col1, col2 = st.columns(2)
    with col1:
        v_ylim = st.slider("Velocity axis range ±", 5.0, 500.0,
                           max(20.0, float(np.ceil(max_v / 10) * 10)), 5.0)
    with col2:
        s_ylim = st.slider("Displacement axis range ±", 5.0, 2000.0,
                           max(20.0, float(np.ceil(max_s / 50) * 50)), 5.0)

    # Time marker — vertical line across both plots
    t_mark = st.slider("Time marker (s)", 0.0, t_max, t_max, 0.1)
    v_mark = u + a_val * t_mark
    s_mark = u * t_mark + 0.5 * a_val * t_mark**2

    fig.update_layout(height=500, margin=dict(l=20, r=20, t=30, b=20), showlegend=False)
    fig.update_yaxes(range=[-v_ylim, v_ylim], row=1, col=1)
    fig.update_yaxes(range=[-s_ylim, s_ylim], row=2, col=1)
    fig.update_xaxes(title_text="Time (s)", row=2, col=1,
                      range=[0, t_max * 1.05])
    # Vertical marker lines on both subplots
    fig.add_vline(x=t_mark, line=dict(color="#ef4444", width=2, dash="dash"),
                  row=1, col=1)
    fig.add_vline(x=t_mark, line=dict(color="#ef4444", width=2, dash="dash"),
                  row=2, col=1)
    st.plotly_chart(fig, use_container_width=True)

    st.markdown(
        f'<div class="result-box">'
        f'<strong>At t = {t_mark:.1f} s:</strong><br>'
        f'v = {v_mark:.2f} m/s &nbsp;|&nbsp; s = {s_mark:.2f} m'
        f'</div>',
        unsafe_allow_html=True,
    )

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
        st.markdown("Both balls adjustable. Set φ₁ (ball 1's deflection) — φ₂ is calculated.")
        st.latex(r"m_1\vec{v}_1 + m_2\vec{v}_2 = m_1\vec{v}'_1 + m_2\vec{v}'_2")

        col1, col2 = st.columns(2)
        with col1:
            st.markdown("**Ball 1**")
            m1 = st.slider("m₁ (kg)", 0.5, 10.0, 3.0, 0.1, key="mom2d_m1")
            v1 = st.slider("v₁ (m/s, negative = opposite direction)", -20.0, 20.0, 5.0, 0.5, key="mom2d_v1")
            theta1 = st.slider("θ₁ (° from +x)", -179, 180, 0, 1, key="mom2d_th1")
            phi1 = st.slider("φ₁ (°) — deflection of ball 1", -89, 89, 15, 1, key="mom2d_phi1")
        with col2:
            st.markdown("**Ball 2**")
            m2 = st.slider("m₂ (kg)", 0.5, 10.0, 2.0, 0.1, key="mom2d_m2")
            v2 = st.slider("v₂ (m/s, negative = opposite direction)", -20.0, 20.0, 0.0, 0.5, key="mom2d_v2")
            theta2 = st.slider("θ₂ (° from +x)", -179, 180, 0, 1, key="mom2d_th2")

        # Convert to radians
        t1_r = math.radians(theta1)
        t2_r = math.radians(theta2)
        p1_r = math.radians(phi1)

        # Initial total momentum components
        px = m1 * v1 * math.cos(t1_r) + m2 * v2 * math.cos(t2_r)
        py = m1 * v1 * math.sin(t1_r) + m2 * v2 * math.sin(t2_r)

        if abs(v1) < 0.001 and abs(v2) < 0.001:
            st.warning("Both balls are stationary — no collision.")
            v1p, v2p = 0, 0
        else:
            # Quadratic in v₁' from momentum + energy conservation:
            # (m₁+m₂)v₁'² - 2(px·cosφ₁ + py·sinφ₁)·v₁'
            #   - [m₂v₁² + (m₂²v₂² - px² - py²)/m₁] = 0
            S = px * math.cos(p1_r) + py * math.sin(p1_r)

            A = m1 + m2
            B = -2 * S
            C = -(m2 * v1**2 + (m2**2 * v2**2 - px**2 - py**2) / m1)

            discriminant = B**2 - 4 * A * C

            if discriminant >= 0:
                sqrtD = math.sqrt(discriminant)
                v1_small = (-B - sqrtD) / (2 * A)
                v1_large = (-B + sqrtD) / (2 * A)

                # Pick the physical root:
                # For m₁ > m₂: smaller (positive) root = ball slows down
                # For m₁ < m₂: negative root = ball bounces back
                # For m₁ ≈ m₂ and v₂=0: v₁_small=0 is non-physical for φ₁≠0
                near_equal_mass = abs(m1 - m2) / max(m1, m2) < 0.05 if max(m1, m2) > 0 else False

                if v1_small >= 0:
                    # Equal/near-equal masses: v₁'=0 is correct only for head-on
                    # (θ₁≈φ₁, ball barely deflects). For glancing, take v₁·cos(θ₁-φ₁).
                    same_direction = abs(math.cos(t1_r - p1_r) - 1.0) < 0.01
                    if abs(v1_small) < 0.001 and abs(v1_large) > 0.5 and near_equal_mass and not same_direction:
                        v1p = v1_large
                    else:
                        v1p = v1_small
                else:
                    # v₁_small < 0 → m₁ < m₂, ball bounces back (keep negative)
                    v1p = v1_small

                if v1p < -abs(v1) - abs(v2) - 1:
                    v1p = 0.0  # sanity clamp
            else:
                st.warning("No valid elastic collision for this deflection angle. Try a smaller |φ₁|.")
                v1p = -1

        if v1p >= 0 and (abs(v1) > 0.001 or abs(v2) > 0.001):
            # Compute v₂' components and φ₂
            v1px = v1p * math.cos(p1_r)
            v1py = v1p * math.sin(p1_r)

            px2 = px - m1 * v1px
            py2 = py - m1 * v1py

            v2p = math.hypot(px2, py2) / m2 if m2 > 0 else 0
            v2px = px2 / m2
            v2py = py2 / m2
            phi2 = math.degrees(math.atan2(v2py, v2px)) if v2p > 0.001 else 0

            ke_before = 0.5 * m1 * v1**2 + 0.5 * m2 * v2**2
            ke_after = 0.5 * m1 * v1p**2 + 0.5 * m2 * v2p**2

            # Velocity components shown signed for direction
            st.markdown(
                f'<div class="result-box">'
                f'<strong>After collision:</strong><br>'
                f'Ball 1: v\'₁<sub>x</sub> = {v1px:+.3f}, v\'₁<sub>y</sub> = {v1py:+.3f} m/s '
                f'(φ₁ = {phi1:.0f}°)<br>'
                f'Ball 2: v\'₂<sub>x</sub> = {v2px:+.3f}, v\'₂<sub>y</sub> = {v2py:+.3f} m/s '
                f'(φ₂ = {phi2:.1f}°)<br>'
                f'KE conserved (elastic)'
                f'</div>',
                unsafe_allow_html=True,
            )

            # Vector diagram — before arrows point TOWARD origin, after point AWAY
            v1_before = np.array([v1 * math.cos(t1_r), v1 * math.sin(t1_r)])
            v2_before = np.array([v2 * math.cos(t2_r), v2 * math.sin(t2_r)])
            v1_after = np.array([v1px, v1py])
            v2_after = np.array([v2px, v2py])

            max_r = max(abs(v1), abs(v2), abs(v1p), abs(v2p), 1) * 1.5

            fig = go.Figure()
            # Collision point marker
            fig.add_trace(go.Scatter(
                x=[0], y=[0], mode="markers",
                marker=dict(size=8, color="white", line=dict(color="#888", width=1)),
                showlegend=False, name="Collision"))
            # Before: v1 (mirrored — tail opposite, arrowhead at origin)
            fig.add_trace(go.Scatter(
                x=[-v1_before[0], 0], y=[-v1_before[1], 0],
                mode="lines+text",
                line=dict(color="#6366f1", width=3),
                text=[f"v₁ ({v1:.1f})", ""], textposition="middle left",
                name="Before: Ball 1"))
            # Before: v2 (mirrored)
            if abs(v2) > 0.1:
                fig.add_trace(go.Scatter(
                    x=[-v2_before[0], 0], y=[-v2_before[1], 0],
                    mode="lines+text",
                    line=dict(color="#ef4444", width=2),
                    text=[f"v₂ ({v2:.1f})", ""], textposition="middle left",
                    name="Before: Ball 2"))
            # After: v1' (from origin outward)
            fig.add_trace(go.Scatter(
                x=[0, v1_after[0]], y=[0, v1_after[1]],
                mode="lines+markers+text",
                line=dict(color="#f59e0b", width=3, dash="dash"),
                marker=dict(size=7, symbol="circle", color="#f59e0b"),
                text=["", f"v\'₁ ({v1p:.2f})"], textposition="middle right",
                name="After: Ball 1"))
            # After: v2' (from origin outward)
            fig.add_trace(go.Scatter(
                x=[0, v2_after[0]], y=[0, v2_after[1]],
                mode="lines+markers+text",
                line=dict(color="#22d3ee", width=3, dash="dash"),
                marker=dict(size=7, symbol="circle", color="#22d3ee"),
                text=["", f"v\'₂ ({v2p:.2f})"], textposition="middle right",
                name="After: Ball 2"))

            fig.add_hline(y=0, line=dict(color="#555", width=1, dash="dot"))
            fig.add_vline(x=0, line=dict(color="#555", width=1, dash="dot"))
            fig.update_layout(height=400,
                              xaxis=dict(range=[-max_r, max_r], scaleanchor="y", constrain="domain"),
                              yaxis=dict(range=[-max_r, max_r]),
                              margin=dict(l=20, r=80, t=20, b=20),
                              legend=dict(orientation="h", y=1.02))
            st.plotly_chart(fig, use_container_width=True)

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

# ================================================================
#                 ⚡ POTENTIAL DIVIDER
# ================================================================
elif topic == "Potential Divider":
    st.markdown("## ⚡ Potential Divider")
    st.latex(r"V_{\text{out}} = V_{\text{in}} \times \frac{R_2}{R_1 + R_2}")

    solve = st.radio("Solve for:", ["Vout", "R₁", "R₂", "Vin"], horizontal=True, key="pd_solve")

    col_a, col_b, col_c = st.columns(3)
    with col_a:
        vin = st.number_input("Vin (V)", 0.0, 100.0, 12.0, 0.5, key="pd_vin")
    with col_b:
        r1 = st.number_input("R₁ (Ω)", 0.0, 1e6, 1000.0, 100.0, key="pd_r1")
    with col_c:
        r2 = st.number_input("R₂ (Ω)", 0.0, 1e6, 2000.0, 100.0, key="pd_r2")

    if solve == "Vout":
        vout = vin * r2 / (r1 + r2) if (r1 + r2) > 0 else 0
        st.success(f"**Vout = {vout:.4f} V**")
    elif solve == "R₁":
        vout = st.number_input("Vout (V)", 0.0, vin, vin * r2 / (r1 + r2), 0.1, key="pd_vout_r1")
        r1_calc = r2 * (vin / vout - 1) if vout > 0 else 0
        st.success(f"**R₁ = {r1_calc:.2f} Ω**")
    elif solve == "R₂":
        vout = st.number_input("Vout (V)", 0.0, vin, vin * r2 / (r1 + r2), 0.1, key="pd_vout_r2")
        r2_calc = r1 / (vin / vout - 1) if vout < vin else 0
        st.success(f"**R₂ = {r2_calc:.2f} Ω**")
    else:
        vout = st.number_input("Vout (V)", 0.0, 100.0, vin * r2 / (r1 + r2), 0.1, key="pd_vout_vin")
        r_total = r1 + r2
        vin_calc = vout * r_total / r2 if r2 > 0 else 0
        st.success(f"**Vin = {vin_calc:.4f} V**")

    # Potentiometer mode
    st.subheader("🔧 Potentiometer Mode")
    pot_pct = st.slider("Wiper position (%)", 0, 100, 67, 1, help="0% = Vout = 0, 100% = Vout = Vin")
    r2_pot = (pot_pct / 100) * (r1 + r2)
    vout_pot = vin * r2_pot / (r1 + r2)
    st.metric("Vout at wiper", f"{vout_pot:.3f} V")

    # Loading effect
    with st.expander("🔍 Loading Effect", expanded=False):
        rl = st.number_input("Load resistor R_L (Ω)", 0.0, 1e6, 10000.0, 100.0, key="pd_rl",
                             help="Placed across R₂. Lower R_L = more loading = lower Vout")
        if rl > 0:
            r2_eff = 1 / (1 / r2 + 1 / rl) if r2 > 0 else 0
            vout_loaded = vin * r2_eff / (r1 + r2_eff) if (r1 + r2_eff) > 0 else 0
            st.metric("Vout with load", f"{vout_loaded:.3f} V")
            st.metric("Effective R₂", f"{r2_eff:.2f} Ω")
            diff_pct = (1 - vout_loaded / vout_pot) * 100 if vout_pot > 0 else 0
            st.info(f"📉 Vout dropped by {diff_pct:.1f}% due to loading")

    # Circuit diagram SVG
    pct = (vout_pot / vin * 100) if vin > 0 else 0
    svg_circuit = f'''<svg viewBox="0 0 420 340" style="width:100%;max-width:420px;display:block;margin:0 auto;">
        <defs>
            <marker id="dot" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6">
                <circle cx="5" cy="5" r="3" fill="#7c8cf0"/>
            </marker>
        </defs>
        <style>
            .wire {{ stroke: #7c8cf0; stroke-width: 2; fill: none; }}
            .label {{ fill: #aaa; font-size: 12px; font-family: sans-serif; }}
            .val {{ fill: #fff; font-size: 13px; font-weight: bold; font-family: sans-serif; }}
            .title {{ fill: #7c8cf0; font-size: 11px; font-family: sans-serif; }}
        </style>

        <!-- Left vertical wire: top to bottom -->
        <line x1="80" y1="40" x2="80" y2="280" class="wire"/>

        <!-- Top wire: left to R1 -->
        <line x1="80" y1="40" x2="140" y2="40" class="wire"/>

        <!-- R1 zigzag (between 140,40 and 260,40) -->
        <polyline points="140,40 150,20 170,60 190,20 210,60 230,20 250,40 260,40" class="wire" stroke-width="2.5"/>

        <!-- Wire from R1 to junction -->
        <line x1="260" y1="40" x2="320" y2="40" class="wire"/>
        <line x1="320" y1="40" x2="320" y2="130" class="wire"/>

        <!-- Junction dot -->
        <circle cx="320" cy="40" r="4" fill="#7c8cf0"/>

        <!-- Top-right wire to Vout arrow -->
        <line x1="320" y1="40" x2="380" y2="40" class="wire"/>
        <polygon points="380,35 395,40 380,45" fill="#10b981"/>

        <!-- R2 zigzag (vertical, between 320,130 and 320,210) -->
        <polyline points="320,130 310,140 330,160 310,180 330,200 310,210 320,220" class="wire" stroke-width="2.5"/>

        <!-- Wire from R2 to bottom -->
        <line x1="320" y1="220" x2="320" y2="280" class="wire"/>
        <!-- Bottom wire back to left -->
        <line x1="80" y1="280" x2="320" y2="280" class="wire"/>

        <!-- Battery symbol (left side) -->
        <line x1="70" y1="55" x2="70" y2="100" stroke="#f0ad4e" stroke-width="3"/>
        <line x1="65" y1="70" x2="75" y2="70" stroke="#f0ad4e" stroke-width="3"/>
        <line x1="62" y1="85" x2="78" y2="85" stroke="#f0ad4e" stroke-width="3"/>

        <!-- Ground symbol (bottom left) -->
        <line x1="80" y1="280" x2="80" y2="300" class="wire"/>
        <line x1="65" y1="300" x2="95" y2="300" stroke="#ef4444" stroke-width="2.5"/>
        <line x1="71" y1="306" x2="89" y2="306" stroke="#ef4444" stroke-width="2"/>
        <line x1="77" y1="312" x2="83" y2="312" stroke="#ef4444" stroke-width="1.5"/>

        <!-- Labels -->
        <text x="40" y="32" class="label" text-anchor="end">Vin</text>
        <text x="40" y="48" class="val" text-anchor="end" fill="#f0ad4e">{vin:.1f} V</text>
        <text x="398" y="36" class="label">Vout</text>
        <text x="398" y="52" class="val" fill="#10b981">{vout_pot:.2f} V</text>

        <!-- R1 label above zigzag -->
        <text x="200" y="18" class="title" text-anchor="middle">R₁</text>
        <text x="200" y="72" class="val" text-anchor="middle" fill="#f59e0b">{r1:.0f} Ω</text>
        <text x="200" y="86" class="title" text-anchor="middle">V = {vin - vout_pot:.2f} V</text>

        <!-- R2 label beside zigzag -->
        <text x="338" y="180" class="title" text-anchor="start">R₂</text>
        <text x="338" y="194" class="val" text-anchor="start" fill="#10b981">{r2:.0f} Ω</text>
        <text x="338" y="208" class="title" text-anchor="start">V = {vout_pot:.2f} V</text>

        <!-- Ground label -->
        <text x="105" y="306" class="label" fill="#ef4444">GND (0 V)</text>

        <!-- Current flow arrows (small) -->
        <polygon points="95,36 105,40 95,44" fill="#f0ad4e" opacity="0.7"/>
        <polygon points="340,225 340,215 344,220" fill="#10b981" opacity="0.7"/>
    </svg>'''

    st.markdown(f'<div style="text-align:center;background:#0f0f1a;border:1px solid #2a2a3a;border-radius:12px;padding:10px;margin:12px 0;">{svg_circuit}</div>', unsafe_allow_html=True)

    # Summary card
    v1 = vin - vout_pot
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.metric("Vin", f"{vin:.2f} V")
    with col_s2:
        st.metric("V across R₁", f"{v1:.2f} V")
    with col_s3:
        st.metric("Vout (across R₂)", f"{vout_pot:.2f} V")

# ================================================================
#                📈 I-V CHARACTERISTICS
# ================================================================
elif topic == "I-V Characteristics":
    st.markdown("## 📈 I-V Characteristics")
    st.markdown("Compare how different components behave under varying voltage.")

    component = st.selectbox("Component", ["Ohmic Resistor", "Filament Lamp", "Diode"], key="iv_comp")

    voltage = np.linspace(0, 12, 400)

    if component == "Ohmic Resistor":
        r_iv = st.slider("Resistance (Ω)", 1.0, 100.0, 10.0, 1.0, key="iv_r_ohmic")
        current = voltage / r_iv
        st.markdown(f"""<div class="result-box">
            <b>Ohmic conductor</b> — obeys Ohm's law: I = V/R<br>
            Gradient = 1/R = {1/r_iv:.4f} S (Siemens)<br>
            At V = 12 V: I = {12/r_iv:.4f} A
        </div>""", unsafe_allow_html=True)
        desc = f"Linear: I = V / {r_iv:.0f}"
        color = "#6366f1"

    elif component == "Filament Lamp":
        temp_factor = st.slider("Temperature coefficient", 0.5, 5.0, 2.0, 0.1, key="iv_temp",
                                help="Higher = resistance increases more with current (heating effect)")
        # Non-ohmic: resistance increases with current due to heating
        current = voltage / (10 + temp_factor * voltage)
        color = "#f59e0b"
        st.markdown(f"""<div class="result-box">
            <b>Non-ohmic (filament lamp)</b> — resistance <b>increases</b> with temperature<br>
            As current flows, filament heats up → lattice vibrations increase → more collisions → higher R<br>
            The graph <b>curves</b> away from the straight line
        </div>""", unsafe_allow_html=True)
        desc = "Non-linear: R increases with I"

    else:  # Diode
        fwd_bias = np.linspace(0, 12, 400)
        # Diode equation approximation: I = Is * (exp(V/(n*Vt)) - 1)
        vt = 0.025  # Thermal voltage at room temp
        n_val = st.slider("Ideality factor (n)", 1.0, 2.0, 1.5, 0.1, key="iv_n",
                          help="1 = ideal, ~2 = real diode")
        is_sat = st.number_input("Reverse saturation current Iₛ (μA)", 0.001, 100.0, 10.0, 1.0,
                                 key="iv_is", format="%.3f") * 1e-6
        current_fwd = is_sat * (np.exp(fwd_bias / (n_val * vt)) - 1)

        # Reverse bias
        rev_voltage = np.linspace(-12, 0, 200)
        current_rev = -is_sat * (np.exp(rev_voltage / (n_val * vt)) - 1)

        fig = go.Figure()
        # Forward bias
        fig.add_trace(go.Scatter(
            x=fwd_bias, y=current_fwd * 1000, mode="lines",
            line=dict(color="#10b981", width=2.5),
            name="Forward bias",
            hovertemplate="V = %{x:.2f} V<br>I = %{y:.4f} mA<extra></extra>",
        ))
        # Reverse bias
        fig.add_trace(go.Scatter(
            x=rev_voltage, y=current_rev * 1000, mode="lines",
            line=dict(color="#ef4444", width=2.5),
            name="Reverse bias",
            hovertemplate="V = %{x:.2f} V<br>I = %{y:.6f} mA<extra></extra>",
        ))
        # Knee voltage annotation
        knee_v = n_val * vt * math.log(2)  # Approximate knee
        fig.add_vline(x=knee_v, line=dict(color="#888", width=1, dash="dot"),
                       annotation_text=f"Knee ≈ {knee_v:.2f} V")

        fig.update_layout(
            height=400,
            xaxis=dict(title="Voltage (V)", range=[-13, 13]),
            yaxis=dict(title="Current (mA)", type="log",
                       tickvals=[0.001, 0.01, 0.1, 1, 10, 100]),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ccc", margin=dict(l=10, r=10, t=10, b=30),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        st.info(f"""
        💡 **Diode characteristics:**
        - **Forward bias** (V > 0): Current grows exponentially past ~{knee_v:.2f} V (knee voltage)
        - **Reverse bias** (V < 0): Negligible current ≈ {is_sat*1e6:.3f} μA (saturation current)
        - The ideality factor n = {n_val:.1f} indicates {'ideal' if n_val < 1.3 else 'realistic'} diode behavior
        """)
        st.markdown("""
        ---
        <div style="background:#1a1d2a;padding:12px;border-radius:8px;">
        <b>Key Formula:</b> I = Iₛ(e<sup>V/(nV<sub>T</sub>)</sup> − 1)  where V<sub>T</sub> ≈ 25 mV at room temperature
        </div>
        """, unsafe_allow_html=True)
        st.stop()  # Don't show the generic graph below

    # Generic I-V graph for ohmic and filament lamp
    if component != "Diode":
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=voltage, y=current, mode="lines",
                                  line=dict(color=color, width=2.5),
                                  name=component,
                                  hovertemplate="V = %{x:.2f} V<br>I = %{y:.4f} A<extra></extra>"))
        # Ohmic reference line for filament lamp
        if component == "Filament Lamp":
            ohmic_i = voltage / 10
            fig.add_trace(go.Scatter(x=voltage, y=ohmic_i, mode="lines",
                                      line=dict(color="#555", width=1, dash="dot"),
                                      name="Ohmic reference (R=10Ω)"))
        fig.update_layout(
            height=400,
            xaxis=dict(title="Voltage (V)", range=[0, 13]),
            yaxis=dict(title="Current (A)"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ccc", margin=dict(l=10, r=10, t=10, b=30),
            hovermode="x unified",
        )
        st.plotly_chart(fig, use_container_width=True)

        if component == "Filament Lamp":
            st.info("""
            💡 **Filament lamp:** The curve shows current increasing less at higher voltages because
            the filament gets hotter → resistance increases. This is non-ohmic behavior.
            """)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
