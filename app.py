import streamlit as st
import streamlit.components.v1 as components
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
    "⚡ Electricity": ["Ohm's Law", "Potential Divider", "I-V Characteristics",
                      "Static Electricity (Coulomb)", "Capacitor"],
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

        # ── Momentum vs Time graph ──
        st.markdown("### Momentum vs Time")
        # Time axis: 0 → 1 before collision, 1 → 2 after collision
        t_before = np.linspace(0, 1, 50)
        t_after = np.linspace(1, 2, 50)

        p1_before = m1 * u1
        p2_before = m2 * u2
        p1_after = m1 * v1
        p2_after = m2 * v2
        p_total_val = p_before  # conserved

        fig = go.Figure()

        # Object 1 momentum: stepped
        fig.add_trace(go.Scatter(
            x=t_before, y=[p1_before] * len(t_before),
            mode="lines", line=dict(color="#6366f1", width=3),
            name=f"Object 1 (m₁={m1:.1f} kg)",
            hovertemplate="Time: %{x:.2f} s<br>p₁ = %{y:.2f} kg·m/s<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=t_after, y=[p1_after] * len(t_after),
            mode="lines", line=dict(color="#6366f1", width=3),
            showlegend=False,
            hovertemplate="Time: %{x:.2f} s<br>p₁ = %{y:.2f} kg·m/s<extra></extra>",
        ))
        # Vertical line at collision for object 1
        fig.add_trace(go.Scatter(
            x=[1, 1], y=[p1_before, p1_after],
            mode="lines", line=dict(color="#6366f1", width=2, dash="dot"),
            showlegend=False,
            hovertemplate="Collision<br>Δp₁ = {p1_after - p1_before:+.2f} kg·m/s<extra></extra>",
        ))

        # Object 2 momentum: stepped
        fig.add_trace(go.Scatter(
            x=t_before, y=[p2_before] * len(t_before),
            mode="lines", line=dict(color="#10b981", width=3),
            name=f"Object 2 (m₂={m2:.1f} kg)",
            hovertemplate="Time: %{x:.2f} s<br>p₂ = %{y:.2f} kg·m/s<extra></extra>",
        ))
        fig.add_trace(go.Scatter(
            x=t_after, y=[p2_after] * len(t_after),
            mode="lines", line=dict(color="#10b981", width=3),
            showlegend=False,
            hovertemplate="Time: %{x:.2f} s<br>p₂ = %{y:.2f} kg·m/s<extra></extra>",
        ))
        # Vertical line at collision for object 2
        fig.add_trace(go.Scatter(
            x=[1, 1], y=[p2_before, p2_after],
            mode="lines", line=dict(color="#10b981", width=2, dash="dot"),
            showlegend=False,
            hovertemplate="Collision<br>Δp₂ = {p2_after - p2_before:+.2f} kg·m/s<extra></extra>",
        ))

        # Total momentum (conserved)
        fig.add_trace(go.Scatter(
            x=[0, 2], y=[p_total_val, p_total_val],
            mode="lines", line=dict(color="#f59e0b", width=2, dash="dash"),
            name=f"Total p = {p_total_val:.2f} kg·m/s (conserved)",
            hovertemplate="Time: %{x:.2f} s<br>p_total = %{y:.2f} kg·m/s<extra></extra>",
        ))

        # Collision zone annotation
        fig.add_vrect(x0=0.95, x1=1.05, fillcolor="#ef4444", opacity=0.08,
                       annotation_text="Collision", annotation_position="top",
                       annotation_font=dict(size=11, color="#ef4444"))

        fig.update_layout(
            height=350,
            xaxis=dict(title="Time (s)", range=[-0.1, 2.1], tickvals=[0, 0.5, 1, 1.5, 2]),
            yaxis=dict(title="Momentum (kg·m/s)"),
            plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
            font_color="#ccc", margin=dict(l=20, r=20, t=10, b=30),
            hovermode="x unified",
            legend=dict(orientation="h", y=1.08, x=0, xanchor="left"),
        )
        st.plotly_chart(fig, use_container_width=True)

        # Annotations for momentum change
        dp1 = p1_after - p1_before
        dp2 = p2_after - p2_before
        st.markdown(f"""
        <div style="display:flex;gap:16px;flex-wrap:wrap;">
            <div style="background:#1a1d2a;padding:8px 14px;border-radius:8px;border-left:4px solid #6366f1;">
                <b>Object 1</b>: Δp = {dp1:+.2f} kg·m/s
            </div>
            <div style="background:#1a1d2a;padding:8px 14px;border-radius:8px;border-left:4px solid #10b981;">
                <b>Object 2</b>: Δp = {dp2:+.2f} kg·m/s
            </div>
            <div style="background:#1a1d2a;padding:8px 14px;border-radius:8px;border-left:4px solid #f59e0b;">
                <b>Total</b>: Δp = {dp1 + dp2:.2f} kg·m/s (conserved ✓)
            </div>
        </div>
        """, unsafe_allow_html=True)

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

    pd_type = st.radio("Type", ["Potentiometer", "Variable Resistor"], horizontal=True, key="pd_type")

    if pd_type == "Potentiometer":
        st.latex(r"V_{\text{out}} = V_{\text{in}} \times \frac{R_{\text{below}}}{R_{\text{total}}}")

        col_a, col_b = st.columns(2)
        with col_a:
            vin = st.number_input("Vin (V)", 0.0, 100.0, 12.0, 0.5, key="pd_vin_pot")
        with col_b:
            r_total = st.number_input("Rₜₒₜₐₗ (Ω)", 0.0, 1e6, 3000.0, 100.0, key="pd_rt",
                                       help="Total resistance of the potentiometer")

        pot_pct = st.slider("Wiper position (%)", 0, 100, 67, 1, key="pd_pct",
                             help="0% = bottom (Vout=0), 100% = top (Vout=Vin)")

        r2_val = (pot_pct / 100) * r_total
        r1_val = r_total - r2_val
        vout_pot = vin * r2_val / r_total if r_total > 0 else 0

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Vin", f"{vin:.2f} V")
        with col_m2:
            st.metric("Vout", f"{vout_pot:.3f} V")
        with col_m3:
            st.metric("Ratio", f"{(vout_pot/vin*100) if vin > 0 else 0:.1f}%")

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.metric("R₁ (above)", f"{r1_val:.0f} Ω")
        with col_r2:
            st.metric("R₂ (below)", f"{r2_val:.0f} Ω")

        # Loading effect
        with st.expander("🔍 Loading Effect", expanded=False):
            rl = st.number_input("Load R_L (Ω)", 0.0, 1e6, 10000.0, 100.0, key="pd_rl_pot",
                                 help="Across R₂. Lower R_L = more loading")
            if rl > 0:
                r2_eff = 1 / (1 / r2_val + 1 / rl) if r2_val > 0 else 0
                vout_loaded = vin * r2_eff / (r1_val + r2_eff) if (r1_val + r2_eff) > 0 else 0
                diff_pct = (1 - vout_loaded / vout_pot) * 100 if vout_pot > 0 else 0
                st.metric("Vout with load", f"{vout_loaded:.3f} V")
                st.info(f"{'📉' if diff_pct > 0.5 else '✅'} {'Drop' if diff_pct > 0.5 else 'Minimal'}: {diff_pct:.1f}%")

        # Potentiometer SVG
        wiper_y = 280 - (pot_pct / 100) * 240
        svg_circuit = f'''<svg viewBox="0 0 460 340" style="width:100%;max-width:460px;display:block;margin:0 auto;">
            <style>
                .wire {{ stroke: #7c8cf0; stroke-width: 2; fill: none; }}
                .label {{ fill: #aaa; font-size: 12px; font-family: sans-serif; }}
                .val {{ fill: #fff; font-size: 13px; font-weight: bold; font-family: sans-serif; }}
                .title {{ fill: #7c8cf0; font-size: 11px; font-family: sans-serif; }}
            </style>
            <line x1="70" y1="40" x2="70" y2="280" class="wire"/>
            <line x1="70" y1="40" x2="200" y2="40" class="wire"/>
            <polyline points="200,40 190,55 210,70 190,85 210,100 190,115 210,130 190,145 210,160 190,175 210,190 190,205 210,220 190,235 210,250 190,265 200,280" class="wire" stroke-width="2.5"/>
            <line x1="200" y1="280" x2="70" y2="280" class="wire"/>
            <line x1="60" y1="55" x2="60" y2="100" stroke="#f0ad4e" stroke-width="3"/>
            <line x1="55" y1="70" x2="65" y2="70" stroke="#f0ad4e" stroke-width="3"/>
            <line x1="52" y1="85" x2="68" y2="85" stroke="#f0ad4e" stroke-width="3"/>
            <line x1="280" y1="{wiper_y}" x2="215" y2="{wiper_y}" stroke="#10b981" stroke-width="2"/>
            <polygon points="215,{wiper_y - 5} 205,{wiper_y} 215,{wiper_y + 5}" fill="#10b981"/>
            <circle cx="200" cy="{wiper_y}" r="5" fill="#10b981"/>
            <line x1="280" y1="{wiper_y}" x2="410" y2="{wiper_y}" class="wire"/>
            <polygon points="410,{wiper_y - 5} 425,{wiper_y} 410,{wiper_y + 5}" fill="#10b981"/>
            <text x="33" y="32" class="label" text-anchor="end">Vin</text>
            <text x="33" y="48" class="val" text-anchor="end" fill="#f0ad4e">{vin:.1f} V</text>
            <text x="430" y="{wiper_y - 8}" class="label" text-anchor="start">Vout</text>
            <text x="430" y="{wiper_y + 8}" class="val" text-anchor="start" fill="#10b981">{vout_pot:.2f} V</text>
            <text x="200" y="25" class="title" text-anchor="middle" font-size="13">Potentiometer</text>
            <text x="150" y="{40 + (wiper_y - 40) * 0.5 - 5}" class="title" text-anchor="end">R₁ = {r1_val:.0f} Ω</text>
            <text x="150" y="{40 + (wiper_y - 40) * 0.5 + 8}" class="title" text-anchor="end">({100 - pot_pct:.0f}%)</text>
            <text x="150" y="{wiper_y + (280 - wiper_y) * 0.5 - 5}" class="title" text-anchor="end">R₂ = {r2_val:.0f} Ω</text>
            <text x="150" y="{wiper_y + (280 - wiper_y) * 0.5 + 8}" class="title" text-anchor="end">({pot_pct:.0f}%)</text>
            <text x="285" y="{wiper_y + 15}" class="label" fill="#10b981" font-size="10">Wiper</text>
        </svg>'''

        components.html(
            f'<div style="text-align:center;background:#0f0f1a;border:1px solid #2a2a3a;border-radius:12px;padding:10px;margin:12px 0;">{svg_circuit}</div>',
            height=370, scrolling=False,
        )

    else:  # Variable Resistor
        st.latex(r"V_{\text{out}} = V_{\text{in}} \times \frac{R_{\text{fixed}}}{R_{\text{var}} + R_{\text{fixed}}}")

        col_a, col_b = st.columns(2)
        with col_a:
            vin = st.number_input("Vin (V)", 0.0, 100.0, 12.0, 0.5, key="pd_vin_vr")
        with col_b:
            r_fixed = st.number_input("R_fixed (Ω)", 0.0, 1e6, 1000.0, 100.0, key="pd_rf",
                                       help="Fixed resistor (e.g. 1 kΩ)")

        r_var = st.slider("R_var (Ω)", 0, 10000, 2000, 100, key="pd_rvar",
                           help="Variable resistor value")

        vout_vr = vin * r_fixed / (r_var + r_fixed) if (r_var + r_fixed) > 0 else 0

        col_m1, col_m2, col_m3 = st.columns(3)
        with col_m1:
            st.metric("Vin", f"{vin:.2f} V")
        with col_m2:
            st.metric("Vout", f"{vout_vr:.3f} V")
        with col_m3:
            st.metric("Ratio", f"{(vout_vr/vin*100) if vin > 0 else 0:.1f}%")

        col_r1, col_r2 = st.columns(2)
        with col_r1:
            st.metric("R_var", f"{r_var:.0f} Ω")
        with col_r2:
            st.metric("R_fixed", f"{r_fixed:.0f} Ω")

        # SVG with box-style resistor symbols
        svg_circuit = f'''<svg viewBox="0 0 460 340" style="width:100%;max-width:460px;display:block;margin:0 auto;">
            <style>
                .wire {{ stroke: #7c8cf0; stroke-width: 2; fill: none; }}
                .label {{ fill: #aaa; font-size: 12px; font-family: sans-serif; }}
                .val {{ fill: #fff; font-size: 13px; font-weight: bold; font-family: sans-serif; }}
                .title {{ fill: #7c8cf0; font-size: 11px; font-family: sans-serif; }}
                .box {{ fill: #1a1d2a; stroke: #7c8cf0; stroke-width: 2; }}
            </style>
            <!-- Left vertical wire -->
            <line x1="70" y1="40" x2="70" y2="280" class="wire"/>
            <line x1="70" y1="40" x2="185" y2="40" class="wire"/>

            <!-- Variable resistor: box + diagonal arrow -->
            <rect x="180" y="50" width="40" height="155" class="box" fill="#2a1a0a" stroke="#f59e0b"/>
            <!-- Arrow through the box -->
            <line x1="175" y1="55" x2="225" y2="200" stroke="#f59e0b" stroke-width="2"/>
            <polygon points="225,200 218,193 230,193" fill="#f59e0b"/>

            <!-- Wire from var resistor to junction -->
            <line x1="200" y1="205" x2="200" y2="215" class="wire"/>
            <!-- Junction dot -->
            <circle cx="200" cy="215" r="4" fill="#7c8cf0"/>

            <!-- Vout wire from junction to right -->
            <line x1="200" y1="215" x2="410" y2="215" class="wire"/>
            <polygon points="410,210 425,215 410,220" fill="#10b981"/>

            <!-- Fixed resistor: box only -->
            <rect x="180" y="225" width="40" height="45" class="box" fill="#0a1a2a" stroke="#10b981"/>
            <line x1="200" y1="270" x2="200" y2="280" class="wire"/>

            <!-- Bottom wire -->
            <line x1="200" y1="280" x2="70" y2="280" class="wire"/>

            <!-- Battery -->
            <line x1="60" y1="55" x2="60" y2="100" stroke="#f0ad4e" stroke-width="3"/>
            <line x1="55" y1="70" x2="65" y2="70" stroke="#f0ad4e" stroke-width="3"/>
            <line x1="52" y1="85" x2="68" y2="85" stroke="#f0ad4e" stroke-width="3"/>

            <!-- Labels -->
            <text x="33" y="32" class="label" text-anchor="end">Vin</text>
            <text x="33" y="48" class="val" text-anchor="end" fill="#f0ad4e">{vin:.1f} V</text>
            <text x="430" y="207" class="label" text-anchor="start">Vout</text>
            <text x="430" y="223" class="val" text-anchor="start" fill="#10b981">{vout_vr:.2f} V</text>

            <text x="200" y="130" class="title" text-anchor="middle" fill="#f59e0b" font-size="12">R<sub>var</sub></text>
            <text x="200" y="145" class="val" text-anchor="middle" fill="#f59e0b">{r_var:.0f} Ω</text>

            <text x="230" y="243" class="title" text-anchor="start" fill="#10b981" font-size="12">R<sub>fixed</sub></text>
            <text x="230" y="258" class="val" text-anchor="start" fill="#10b981">{r_fixed:.0f} Ω</text>
        </svg>'''

        components.html(
            f'<div style="text-align:center;background:#0f0f1a;border:1px solid #2a2a3a;border-radius:12px;padding:10px;margin:12px 0;">{svg_circuit}</div>',
            height=370, scrolling=False,
        )

        # Voltage range info
        st.info(f"""
        💡 **Range:** R_var = 0 to 10 kΩ → Vout ranges from **{vin * r_fixed / (0 + r_fixed):.2f} V** to **{vin * r_fixed / (10000 + r_fixed):.2f} V**
        """)

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

# ── Static Electricity (Coulomb) ──────────────────────────
elif topic == "Static Electricity (Coulomb)":
    st.markdown("## ⚡ Static Electricity — Coulomb's Law")
    st.latex(r"F = k\frac{q_1 q_2}{r^2}")
    st.info("Pick a layout: two charges in a line, three in a triangle, or four in a square. "
            "Charges are coloured by sign (red = +, blue = −). Like signs repel, opposite signs attract. "
            "The yellow arrow on each charge is the **net (resultant) Coulomb force**. "
            "The faint blue grid shows the **electric field**.")

    sim_html = """
    <!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
    <style>
    body{margin:0;background:#0f172a;color:#e2e8f0;font-family:system-ui,Arial,sans-serif}
    canvas{background:#0b1220;border-radius:10px;width:100%}
    .row{display:flex;gap:8px;margin:6px 0;align-items:center;font-size:13px}
    .row label{flex:1}
    input[type=range]{flex:2}
    select{flex:2;background:#1e293b;color:#e2e8f0;border:none;border-radius:6px;padding:4px}
    .out{background:#0b1220;border-radius:8px;padding:8px;font-size:13px;margin-top:6px;line-height:1.7}
    b{color:#38bdf8}
    </style></head><body>
    <canvas id="cv" width="640" height="340"></canvas>
    <div class="row"><label>Layout</label>
      <select id="layout"><option value="line">Two charges (line)</option>
        <option value="tri">Three charges (triangle)</option>
        <option value="sq">Four charges (square)</option></select></div>
    <div class="row"><label>q1 (nC): <b id="lq1">5</b></label>
      <input id="q1" type="range" min="-10" max="10" value="5" step="1"></div>
    <div class="row"><label>q2 (nC): <b id="lq2">-5</b></label>
      <input id="q2" type="range" min="-10" max="10" value="-5" step="1"></div>
    <div class="row" id="rowq3"><label>q3 (nC): <b id="lq3">5</b></label>
      <input id="q3" type="range" min="-10" max="10" value="5" step="1"></div>
    <div class="row" id="rowq4"><label>q4 (nC): <b id="lq4">-5</b></label>
      <input id="q4" type="range" min="-10" max="10" value="-5" step="1"></div>
    <div class="row"><label>Separation d (cm): <b id="ld">8</b></label>
      <input id="d" type="range" min="2" max="20" value="8" step="1"></div>
    <div class="out" id="out"></div>
    <script>
    const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),k=8.99e9;
    const W=cv.width,H=cv.height,cx=W/2,cy=H/2;
    function draw(){
      const layout=document.getElementById('layout').value,d=+document.getElementById('d').value;
      const qs=[1,2,3,4].map(i=>+document.getElementById('q'+i).value);
      document.getElementById('lq1').textContent=qs[0];document.getElementById('lq2').textContent=qs[1];
      document.getElementById('lq3').textContent=qs[2];document.getElementById('lq4').textContent=qs[3];
      document.getElementById('ld').textContent=d;
      document.getElementById('rowq3').style.display=(layout==='line')?'none':'flex';
      document.getElementById('rowq4').style.display=(layout==='sq')?'flex':'none';
      const n=(layout==='line')?2:(layout==='tri')?3:4;
      const R=(Math.min(W,H)/2-60)*(d/20);
      let P;
      if(layout==='line')P=[[cx-R,cy],[cx+R,cy]];
      else if(layout==='tri'){P=[];for(let i=0;i<3;i++){let a=(-90+i*120)*Math.PI/180;P.push([cx+R*Math.cos(a),cy+R*Math.sin(a)]);}}
      else{P=[];const c=[[-1,-1],[1,-1],[1,1],[-1,1]];for(const v of c)P.push([cx+R*v[0],cy+R*v[1]]);}
      const sep=(layout==='line')?2*R:(layout==='tri')?R*Math.sqrt(3):2*R;
      const mpp=(d/100)/sep;
      const Q=qs.slice(0,n).map(q=>q*1e-9);
      ctx.clearRect(0,0,W,H);
      for(let i=1;i<18;i++)for(let j=1;j<12;j++){
        const px=W*i/18,py=H*j/12;let ex=0,ey=0,near=false;
        for(let m=0;m<n;m++){const dx=px-P[m][0],dy=py-P[m][1],pr=Math.sqrt(dx*dx+dy*dy)||1;if(pr<20)near=true;const rm=pr*mpp;ex+=k*Q[m]*dx/(pr*rm*rm);ey+=k*Q[m]*dy/(pr*rm*rm);}
        if(near)continue;const em=Math.hypot(ex,ey);if(em<1)continue;
        const L=Math.min(22,Math.max(4,em*6e-4)),ux=ex/em,uy=ey/em;
        ctx.strokeStyle='rgba(56,189,248,0.35)';ctx.lineWidth=1;
        ctx.beginPath();ctx.moveTo(px-ux*L/2,py-uy*L/2);ctx.lineTo(px+ux*L/2,py+uy*L/2);ctx.stroke();
        ctx.fillStyle='rgba(56,189,248,0.35)';ctx.beginPath();ctx.arc(px+ux*L/2,py+uy*L/2,1.5,0,7);ctx.fill();
      }
      const netF=[];
      for(let i=0;i<n;i++){let fx=0,fy=0;for(let j=0;j<n;j++){if(j===i)continue;const dx=P[i][0]-P[j][0],dy=P[i][1]-P[j][1],pr=Math.sqrt(dx*dx+dy*dy)||1,rm=pr*mpp,F=k*Q[i]*Q[j]/(rm*rm);fx+=F*dx/pr;fy+=F*dy/pr;}netF.push([fx,fy]);}
      for(let i=0;i<n;i++){
        chg(P[i][0],P[i][1],qs[i]);
        const fm=Math.hypot(netF[i][0],netF[i][1]);
        if(fm>1e-30){const L=Math.min(120,Math.max(20,fm*1e7)),ux=netF[i][0]/fm,uy=netF[i][1]/fm;
          ctx.strokeStyle='#facc15';ctx.lineWidth=3;ctx.beginPath();ctx.moveTo(P[i][0],P[i][1]);ctx.lineTo(P[i][0]+ux*L,P[i][1]+uy*L);ctx.stroke();
          const hx=P[i][0]+ux*L,hy=P[i][1]+uy*L;ctx.fillStyle='#facc15';ctx.beginPath();
          if(ux>=0){ctx.moveTo(hx,hy);ctx.lineTo(hx-12,hy-6);ctx.lineTo(hx-12,hy+6);}else{ctx.moveTo(hx,hy);ctx.lineTo(hx+12,hy-6);ctx.lineTo(hx+12,hy+6);}ctx.closePath();ctx.fill();
          ctx.fillStyle='#facc15';ctx.font='11px sans-serif';ctx.fillText('F='+fm.toExponential(2)+'N',P[i][0]+ux*L+4,P[i][1]+uy*L-4);
        }
      }
      let s='';
      for(let i=0;i<n;i++){const fm=Math.hypot(netF[i][0],netF[i][1]);const deg=Math.atan2(netF[i][1],netF[i][0])*180/Math.PI;
        s+='<b>q'+(i+1)+'</b>: F = '+fm.toExponential(2)+' N '+(fm>1e-30?('('+deg.toFixed(0)+'°)')+'<br>':'<br>');}
      document.getElementById('out').innerHTML=s;
    }
    function chg(x,y,q){ctx.beginPath();ctx.arc(x,y,24,0,7);ctx.fillStyle=q>0?'#ef4444':(q<0?'#3b82f6':'#64748b');ctx.fill();ctx.strokeStyle='#0b1220';ctx.lineWidth=2;ctx.stroke();ctx.fillStyle='#fff';ctx.font='bold 18px sans-serif';ctx.textAlign='center';ctx.fillText(q>0?'+':'−',x,y+6);ctx.textAlign='left';}
    [document.getElementById('layout'),document.getElementById('q1'),document.getElementById('q2'),document.getElementById('q3'),document.getElementById('q4'),document.getElementById('d')].forEach(el=>el.addEventListener('input',draw));draw();
    </script></body></html>
    """
    components.html(sim_html, height=520, scrolling=False)

# ── Capacitor ─────────────────────────────────────────────
elif topic == "Capacitor":
    st.markdown("## 🔋 Capacitor")
    st.latex(r"C = \varepsilon_0 \, \varepsilon_r \frac{A}{d} \qquad Q = C\,V \qquad U = \tfrac{1}{2} C V^2")
    st.info("Increase A or decrease d → C increases. A dielectric (εᵣ>1) raises C. "
            "Stored charge Q ∝ C·V; energy U ∝ C·V².")

    cap_html = """
    <!DOCTYPE html><html lang="id"><head><meta charset="utf-8">
    <style>
    body{margin:0;background:#0f172a;color:#e2e8f0;font-family:system-ui,Arial,sans-serif}
    canvas{background:#0b1220;border-radius:10px;width:100%}
    .row{display:flex;gap:8px;margin:6px 0;align-items:center;font-size:13px}
    .row label{flex:1}input[type=range]{flex:2}
    select{flex:2;background:#1e293b;color:#e2e8f0;border:none;border-radius:6px;padding:4px}
    .out{background:#0b1220;border-radius:8px;padding:8px;font-size:13px;margin-top:6px;line-height:1.7}
    b{color:#38bdf8}
    </style></head><body>
    <canvas id="cv" width="640" height="320"></canvas>
    <div class="row"><label>A (cm²): <b id="lA">100</b></label>
      <input id="A" type="range" min="20" max="200" value="100" step="5"></div>
    <div class="row"><label>d (mm): <b id="ld">5</b></label>
      <input id="d" type="range" min="1" max="20" value="5" step="1"></div>
    <div class="row"><label>V (V): <b id="lV">12</b></label>
      <input id="V" type="range" min="1" max="24" value="12" step="1"></div>
    <div class="row"><label>Dielektrik (εᵣ)</label>
      <select id="er"><option value="1">Udara (1)</option><option value="2.5">Kertas (2.5)</option>
      <option value="3">Plastik (3)</option><option value="80">Air (80)</option></select></div>
    <div class="out" id="out"></div>
    <script>
    const cv=document.getElementById('cv'),ctx=cv.getContext('2d'),eps0=8.854e-12;
    function draw(){
      let A=+document.getElementById('A').value,d=+document.getElementById('d').value,V=+document.getElementById('V').value,er=+document.getElementById('er').value;
      document.getElementById('lA').textContent=A;document.getElementById('ld').textContent=d;document.getElementById('lV').textContent=V;
      ctx.clearRect(0,0,cv.width,cv.height);
      const plW=200,plH=22,lx=cv.width/2-80,rx=cv.width/2+80,ty=cv.height/2-plH/2;
      ctx.fillStyle='#cbd5e1';
      ctx.fillRect(lx-plW/2,ty,plW/2,plH);ctx.fillRect(rx,ty,plW/2,plH);
      pchg(lx-plW/2,ty,plW/2,plH,+1);pchg(rx,ty,plW/2,plH,-1);
      const gap=rx-(lx-plW/2+plW/2);
      ctx.fillStyle='rgba(56,189,248,'+(0.05*er)+')';ctx.fillRect(rx,ty,gap,plH);
      ctx.strokeStyle='#38bdf8';ctx.lineWidth=1;
      for(let i=0;i<5;i++){const y=ty+4+i*3.4;ctx.beginPath();ctx.moveTo(lx,y);ctx.lineTo(rx,y);ctx.stroke();}
      ctx.fillStyle='#ef4444';ctx.fillText('+Q',lx-plW/2+8,ty+16);
      ctx.fillStyle='#3b82f6';ctx.fillText('−Q',rx+8,ty+16);
      const a=A*1e-4,dd=d*1e-3,C=eps0*er*a/dd,Q=C*V,E=V/dd,U=0.5*C*V*V;
      out.innerHTML='Kapasitans <b>C</b> = '+(C*1e12).toFixed(2)+' pF<br>'+
        'Muatan <b>Q</b> = '+(Q*1e9).toFixed(2)+' nC<br>'+
        'Medan <b>E</b> = '+E.toFixed(0)+' V/m<br>'+
        'Energi <b>U</b> = '+(U*1e12).toFixed(2)+' pJ';
    }
    function pchg(x,y,w,h,s){ctx.fillStyle=s>0?'#ef4444':'#3b82f6';ctx.font='10px sans-serif';
      for(let i=0;i<8;i++)ctx.fillText(s>0?'+':'−',x+8+i*(w/8),y+h/2+4);}
    [document.getElementById('A'),document.getElementById('d'),document.getElementById('V'),document.getElementById('er')].forEach(el=>el.addEventListener('input',draw));draw();
    </script></body></html>
    """
    # avoid JS id clash with Python globals: elements referenced as A_, d_, V_ in JS
    components.html(cap_html, height=470, scrolling=False)

# ── FOOTER ────────────────────────────────────────────────
st.markdown("---")
st.caption("Built with Python · Streamlit · Plotly · NumPy")
