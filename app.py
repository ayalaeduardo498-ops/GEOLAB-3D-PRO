"""GEOLAB 3D | Laboratorio interactivo de geometría analítica.
Ejecutar: py -m streamlit run app.py
"""
from __future__ import annotations

import math
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st


PALETTES = {
    "Azul eléctrico": {
        "line": "#38BDF8", "light": "#7DD3FC", "shade": "rgba(56,189,248,0.14)",
        "scale": [[0, "#123566"], [0.48, "#2563EB"], [1, "#67E8F9"]],
    },
    "Turquesa": {
        "line": "#2DD4BF", "light": "#99F6E4", "shade": "rgba(45,212,191,0.15)",
        "scale": [[0, "#115E59"], [0.48, "#0D9488"], [1, "#99F6E4"]],
    },
    "Violeta": {
        "line": "#A78BFA", "light": "#DDD6FE", "shade": "rgba(167,139,250,0.15)",
        "scale": [[0, "#4C1D95"], [0.48, "#7C3AED"], [1, "#DDD6FE"]],
    },
}
BG = "#08111F"
PANEL = "#101D31"
GRID = "rgba(148,163,184,0.14)"
TEXT = "#E2E8F0"
MUTED = "#94A3B8"


STYLE = """
<style>
  .stApp {background: radial-gradient(ellipse at 85% 0%, #112748 0%, #08111F 45%, #070D18 100%);}
  [data-testid="stSidebar"] {background: #0C1729; border-right: 1px solid #253550;}
  [data-testid="stMetric"] {background: linear-gradient(145deg, #14223A, #0E1A2C); border: 1px solid #273A57;
    border-radius: 16px; padding: 16px 20px;}
  [data-testid="stMetricLabel"] {color: #A5B4CC;}
  [data-testid="stMetricValue"] {color: #F8FAFC;}
  .block-container {max-width: 1540px; padding-top: 1.35rem;}
  .hero {padding: 24px 30px; border: 1px solid #264162; border-radius: 22px;
    background: linear-gradient(112deg, #142B4A 0%, #13203A 42%, #0B1728 100%);
    margin: 7px 0 24px 0;}
  .hero h1 {font-size: clamp(1.9rem, 3vw, 2.65rem); margin: 0 0 6px; color: #F8FAFC; letter-spacing:-.035em;}
  .hero p {font-size: 1rem; color: #ADBFDA; margin: 0;}
  .eyebrow {font-size:.78rem; font-weight:700; color:#67E8F9; letter-spacing:.14em; margin-bottom:8px;}
  .info {padding: 16px 20px; border: 1px solid #2C405A; border-radius: 15px;
    background:#101D30; color:#B7C9E1; margin-bottom: 14px;}
  .foot {font-size:.85rem; color:#91A6C1; text-align:center; padding:18px 8px;}
  div.stButton > button, div.stDownloadButton > button {border-radius:10px;}
</style>
"""


def num(value: float, digits: int = 2) -> str:
    return f"{value:,.{digits}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def set_2d_style(fig: go.Figure, title: str, extent: tuple[float, float, float, float]) -> None:
    xmin, xmax, ymin, ymax = extent
    fig.update_layout(
        title=dict(text=title, font=dict(size=18, color=TEXT), x=0.03, y=0.95),
        height=610,
        paper_bgcolor=PANEL, plot_bgcolor=PANEL,
        font=dict(color=TEXT, family="Arial"),
        margin=dict(l=45, r=32, t=70, b=55),
        xaxis=dict(title="Eje X", range=[xmin, xmax], scaleanchor="y", scaleratio=1,
                   showgrid=True, gridcolor=GRID, zeroline=True, zerolinecolor="#7186A6"),
        yaxis=dict(title="Eje Y", range=[ymin, ymax], showgrid=True, gridcolor=GRID,
                   zeroline=True, zerolinecolor="#7186A6"),
        legend=dict(orientation="h", y=1.05, x=0.55, font=dict(size=11)),
        hoverlabel=dict(bgcolor="#17263D"),
    )


def circle_figure(cx: float, cy: float, r: float, angle_deg: float,
                  filled: bool, tangent: bool, color: dict) -> tuple[go.Figure, pd.DataFrame]:
    t = np.linspace(0, 2 * np.pi, 721)
    x, y = cx + r * np.cos(t), cy + r * np.sin(t)
    th = np.deg2rad(angle_deg)
    px, py = cx + r * math.cos(th), cy + r * math.sin(th)
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=x, y=y, mode="lines", fill="toself" if filled else "none",
        fillcolor=color["shade"], line=dict(color=color["line"], width=4),
        name="Circunferencia", hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<extra></extra>",
    ))
    fig.add_trace(go.Scatter(
        x=[cx - r, cx + r], y=[cy, cy], mode="lines",
        line=dict(color="#E2E8F0", width=2, dash="dot"), name="Diámetro", hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=[cx, px], y=[cy, py], mode="lines+markers",
        marker=dict(size=8, color=color["light"]),
        line=dict(color="#FBBF24", width=4), name="Radio", hoverinfo="skip",
    ))
    fig.add_trace(go.Scatter(
        x=[cx, px], y=[cy, py], mode="markers+text",
        marker=dict(size=[11, 11], color=["#FFFFFF", "#FBBF24"]),
        text=["  C", "  P"], textposition="top right", name="Puntos", hovertemplate="(%{x:.3f}, %{y:.3f})<extra></extra>",
    ))
    if tangent:
        L = r * 0.62
        tx, ty = -math.sin(th), math.cos(th)
        fig.add_trace(go.Scatter(
            x=[px - L * tx, px + L * tx], y=[py - L * ty, py + L * ty],
            mode="lines", line=dict(color="#FB7185", width=3, dash="dash"),
            name="Tangente", hoverinfo="skip",
        ))
    margin = max(0.8, 0.32 * r)
    set_2d_style(fig, "Plano cartesiano XY · circunferencia", (cx-r-margin, cx+r+margin, cy-r-margin, cy+r+margin))
    points = pd.DataFrame({"theta_rad": t, "x": x, "y": y})
    return fig, points


def axes_scene(bound: float, visible: bool) -> dict:
    common = dict(
        showbackground=False, showgrid=visible, gridcolor=GRID,
        zeroline=visible, zerolinecolor="#526B88", visible=visible,
        showspikes=False, tickfont=dict(color=MUTED, size=10),
    )
    return dict(
        xaxis=dict(**common, title="X", range=[-bound, bound]),
        yaxis=dict(**common, title="Y", range=[-bound, bound]),
        zaxis=dict(**common, title="Z", range=[-bound, bound]),
        aspectmode="cube",
        bgcolor=PANEL,
        camera=dict(eye=dict(x=1.6, y=1.75, z=1.18), projection=dict(type="perspective")),
    )


def ellipsoid_surface(a: float, b: float, c: float, n: int) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    u = np.linspace(0, 2 * np.pi, n)
    v = np.linspace(-np.pi / 2, np.pi / 2, max(35, n // 2))
    U, V = np.meshgrid(u, v)
    return a * np.cos(V) * np.cos(U), b * np.cos(V) * np.sin(U), c * np.sin(V)


def solid_figure(a: float, b: float, c: float, h: float, n: int,
                 show_section: bool, show_plane: bool, wireframe: bool,
                 visible_axes: bool, palette: dict, name: str) -> tuple[go.Figure, pd.DataFrame]:
    X, Y, Z = ellipsoid_surface(a, b, c, n)
    fig = go.Figure()
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z, surfacecolor=Z,
        cmin=-c, cmax=c, colorscale=palette["scale"], showscale=False,
        opacity=0.91, name=name,
        lighting=dict(ambient=0.54, diffuse=0.85, specular=0.55, roughness=0.45, fresnel=0.13),
        lightposition=dict(x=80, y=110, z=180),
        hovertemplate="X=%{x:.2f}<br>Y=%{y:.2f}<br>Z=%{z:.2f}<extra></extra>",
    ))
    if wireframe:
        tt = np.linspace(0, 2 * np.pi, 150)
        vv = np.linspace(-np.pi / 2, np.pi / 2, 110)
        for phi in np.linspace(0, 2 * np.pi, 12, endpoint=False):
            fig.add_trace(go.Scatter3d(
                x=a * np.cos(vv) * np.cos(phi), y=b * np.cos(vv) * np.sin(phi),
                z=c * np.sin(vv), mode="lines", showlegend=False,
                line=dict(color="rgba(226,232,240,0.34)", width=2), hoverinfo="skip",
            ))
        for lat in np.linspace(-np.pi / 2, np.pi / 2, 9)[1:-1]:
            fig.add_trace(go.Scatter3d(
                x=a*np.cos(lat)*np.cos(tt), y=b*np.cos(lat)*np.sin(tt),
                z=np.full_like(tt, c*np.sin(lat)), mode="lines", showlegend=False,
                line=dict(color="rgba(226,232,240,0.28)", width=2), hoverinfo="skip",
            ))
    k = max(0.0, 1.0 - (h / c) ** 2)
    sa, sb = a * math.sqrt(k), b * math.sqrt(k)
    tt = np.linspace(0, 2 * np.pi, 241)
    if show_plane:
        span = max(a, b) * 1.18
        g = np.linspace(-span, span, 2)
        GX, GY = np.meshgrid(g, g)
        fig.add_trace(go.Surface(
            x=GX, y=GY, z=np.full_like(GX, h), showscale=False,
            surfacecolor=np.zeros_like(GX), colorscale=[[0, "#FCD34D"], [1, "#FCD34D"]],
            opacity=0.20, name="Plano z = h", hoverinfo="skip",
        ))
    if show_section:
        if sa < 1e-10 or sb < 1e-10:
            fig.add_trace(go.Scatter3d(
                x=[0], y=[0], z=[h], mode="markers", showlegend=False,
                marker=dict(size=8, color="#FBBF24"), name="Punto de tangencia",
            ))
        else:
            fig.add_trace(go.Scatter3d(
                x=sa*np.cos(tt), y=sb*np.sin(tt), z=np.full_like(tt, h),
                mode="lines", line=dict(color="#FBBF24", width=7),
                name="Intersección con plano", hovertemplate="x=%{x:.3f}<br>y=%{y:.3f}<extra></extra>",
            ))
    bound = max(a, b, c) * 1.4
    fig.update_layout(
        title=dict(text=f"{name} · escena tridimensional", font=dict(size=18, color=TEXT), x=0.035),
        height=630, margin=dict(l=0, r=0, t=58, b=0),
        paper_bgcolor=PANEL, font=dict(color=TEXT), scene=axes_scene(bound, visible_axes),
        showlegend=False,
    )
    coords = pd.DataFrame({"x": X.ravel(), "y": Y.ravel(), "z": Z.ravel()})
    return fig, coords


def section_figure(a: float, b: float, c: float, h: float, palette: dict) -> go.Figure:
    factor = math.sqrt(max(0.0, 1 - (h/c)**2))
    u = np.linspace(0, 2*np.pi, 241)
    ra, rb = a*factor, b*factor
    fig = go.Figure()
    if ra > 1e-9 and rb > 1e-9:
        fig.add_trace(go.Scatter(
            x=ra*np.cos(u), y=rb*np.sin(u), mode="lines", fill="toself",
            line=dict(color="#FBBF24", width=3), fillcolor="rgba(251,191,36,0.09)",
            name="Sección", hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<extra></extra>",
        ))
        fig.add_trace(go.Scatter(x=[-ra, ra], y=[0, 0], mode="lines",
            line=dict(color=palette["line"], dash="dot", width=2),
            name="Diámetro X", hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[0, 0], y=[-rb, rb], mode="lines",
            line=dict(color="#FB7185", dash="dot", width=2),
            name="Diámetro Y", hoverinfo="skip"))
    else:
        fig.add_trace(go.Scatter(x=[0],y=[0],mode="markers",marker=dict(color="#FBBF24",size=11),name="Punto de tangencia"))
    set_2d_style(fig, f"Sección en z = {num(h)}", (-a*1.18,a*1.18,-b*1.18,b*1.18))
    fig.update_layout(height=405, margin=dict(l=40,r=25,t=60,b=45))
    return fig


def plane_figure(m: float, n: float, d: float, extent: float,
                 show_normal: bool, visible_axes: bool, palette: dict) -> tuple[go.Figure, pd.DataFrame]:
    grid = np.linspace(-extent, extent, 30)
    X, Y = np.meshgrid(grid, grid)
    Z = m*X + n*Y + d
    fig = go.Figure()
    fig.add_trace(go.Surface(
        x=X, y=Y, z=Z, surfacecolor=Z, colorscale=palette["scale"], showscale=False,
        opacity=0.93, lighting=dict(ambient=0.55, diffuse=0.9, specular=0.4),
        name="Plano", hovertemplate="x=%{x:.2f}<br>y=%{y:.2f}<br>z=%{z:.2f}<extra></extra>",
    ))
    if show_normal:
        vec = np.array([-m,-n,1.],dtype=float)
        vec = vec/np.linalg.norm(vec)*extent*.8
        fig.add_trace(go.Scatter3d(
            x=[0, vec[0]], y=[0, vec[1]], z=[d, d+vec[2]],
            mode="lines+markers", line=dict(color="#FBBF24",width=9),
            marker=dict(size=[3,7],color="#FBBF24"), name="Vector normal",
        ))
    bound = max(extent*1.6, float(np.max(np.abs(Z)))*1.1, abs(d)+extent)
    fig.update_layout(
        height=630, margin=dict(l=0,r=0,t=55,b=0),
        title=dict(text="Plano afín en el espacio · z = mx + ny + d", x=.035,
                   font=dict(color=TEXT,size=18)),
        paper_bgcolor=PANEL, font=dict(color=TEXT), scene=axes_scene(bound,visible_axes),
        showlegend=False,
    )
    return fig, pd.DataFrame({"x":X.ravel(),"y":Y.ravel(),"z":Z.ravel()})


def ellipsoid_area_approx(a: float, b: float, c: float) -> float:
    # Fórmula aproximada de Knud Thomsen para el área de un elipsoide triaxial.
    p = 1.6075
    return 4 * math.pi * ((a**p*b**p + a**p*c**p + b**p*c**p)/3) ** (1/p)


def exports(fig: go.Figure, points: pd.DataFrame, stem: str) -> None:
    st.markdown("#### Exportar resultados")
    left, right = st.columns(2)
    with left:
        st.download_button(
            "⬇ Descargar gráfico 3D/2D (HTML)",
            data=fig.to_html(full_html=True, include_plotlyjs=True),
            file_name=f"{stem}_interactivo.html", mime="text/html",
            width="stretch", key=f"html_{stem}",
        )
    with right:
        st.download_button(
            "⬇ Descargar coordenadas (CSV)",
            data=points.to_csv(index=False).encode("utf-8-sig"),
            file_name=f"{stem}_coordenadas.csv", mime="text/csv",
            width="stretch", key=f"csv_{stem}",
        )
    st.caption("El HTML funciona sin conexión a Internet; el CSV contiene los puntos calculados.")


def hero(label: str, title: str, subtitle: str) -> None:
    st.markdown(f"""
    <div class="hero"><div class="eyebrow">{label}</div>
    <h1>{title}</h1><p>{subtitle}</p></div>
    """, unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="GeoLab 3D | Geometría Interactiva", page_icon="🌐", layout="wide",
                       initial_sidebar_state="expanded")
    st.markdown(STYLE, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown("## ◈ GEOLAB 3D")
        st.caption("LABORATORIO DE GEOMETRÍA ANALÍTICA")
        st.divider()
        view = st.radio(
            "Selecciona la figura",
            ["◯ Circunferencia 2D", "◉ Esfera 3D", "⬭ Elipsoide 3D", "▱ Plano 3D", "▣ Comparador"],
            index=0,
        )
        st.divider()
        st.markdown("#### 🎨 Presentación")
        palette_name = st.selectbox("Paleta visual", list(PALETTES), index=0)
        palette = PALETTES[palette_name]
        unit = st.selectbox("Unidad", ["u", "cm", "m", "km"], index=0)
        show_axes = st.toggle("Ejes coordenados", value=True)
        res = st.slider("Calidad de malla 3D", 40, 160, 94, step=6)
        st.divider()
        st.caption("Arrastra para girar los objetos 3D · Rueda para acercar · Doble clic para reiniciar.")

    if "Circunferencia" in view:
        hero("MÓDULO 01 / GEOMETRÍA PLANA", "Circunferencia en el plano XY",
             "Coordenadas cartesianas, radio, diámetro, tangente y área del disco.")
        controls, chart = st.columns([1, 2.25], gap="large")
        with controls:
            st.markdown("### Parámetros")
            r = st.slider("Radio (r)", 0.5, 15.0, 5.0, 0.5)
            cx = st.number_input("Centro X", -20.0, 20.0, 0.0, 0.5)
            cy = st.number_input("Centro Y", -20.0, 20.0, 0.0, 0.5)
            angle = st.slider("Ángulo del punto P (°)", 0, 360, 45, 5)
            filled = st.toggle("Resaltar disco interior", value=True)
            tangent = st.toggle("Mostrar tangente en P", value=True)
            st.markdown("#### Ecuación")
            st.latex(r"(x-x_0)^2+(y-y_0)^2=r^2")
            st.code(f"(x - ({cx:g}))² + (y - ({cy:g}))² = {r*r:g}", language="text")
        fig, df = circle_figure(cx,cy,r,angle,filled,tangent,palette)
        with chart:
            st.plotly_chart(fig, width="stretch", theme=None, key="chart_circle")
        cols = st.columns(4)
        metrics = [("Radio", r,unit),("Diámetro",2*r,unit),
                   ("Longitud",2*math.pi*r,unit),("Área del disco",math.pi*r*r,unit+"²")]
        for col, (label,value,u) in zip(cols, metrics):
            col.metric(label, f"{num(value)} {u}")
        with st.expander("📐 Modelo y explicación", expanded=True):
            st.latex(r"C=2\pi r\qquad A=\pi r^2")
            st.write("La **circunferencia** es el contorno; el **círculo/disco** es la región interior. "
                     "El segmento amarillo representa un radio y la línea rosa discontinua, la tangente en P.")
            th=math.radians(angle)
            st.write(f"P = ({num(cx + r*math.cos(th))}, {num(cy + r*math.sin(th))})")
        exports(fig,df,"circunferencia")

    elif "Esfera" in view:
        hero("MÓDULO 02 / GEOMETRÍA ESPACIAL", "Esfera tridimensional",
             "Superficie paramétrica interactiva, retícula espacial y cortes horizontales.")
        with st.sidebar:
            st.markdown("#### 🔭 Opciones 3D")
            wire = st.toggle("Mostrar meridianos y paralelos", value=True)
            section = st.toggle("Mostrar línea de sección", value=True)
            plane = st.toggle("Mostrar plano de corte", value=True)
        left, right = st.columns([1,2.25],gap="large")
        with left:
            st.markdown("### Parámetros")
            r = st.slider("Radio de esfera (r)",0.5,15.0,5.0,0.5)
            h = st.slider("Altura del corte z = h",-r,r,0.0,0.1)
            st.markdown("#### Ecuación")
            st.latex(r"x^2+y^2+z^2=r^2")
            st.caption("Mueve la altura para estudiar la intersección con el plano horizontal.")
        fig,df = solid_figure(r,r,r,h,res,section,plane,wire,show_axes,palette,"Esfera")
        with right:
            st.plotly_chart(fig,width="stretch",theme=None,key="chart_sphere")
        cut_radius = math.sqrt(max(0,r*r-h*h))
        metrics = [("Radio",r,unit),("Superficie",4*math.pi*r*r,unit+"²"),
                   ("Volumen",4/3*math.pi*r**3,unit+"³"),("Radio de corte",cut_radius,unit)]
        for col,(label,v,u) in zip(st.columns(4),metrics):
            col.metric(label,f"{num(v)} {u}")
        l2,r2 = st.columns([1.2,1.0],gap="large")
        with l2:
            st.markdown("### Sección transversal")
            st.plotly_chart(section_figure(r,r,r,h,palette),width="stretch",theme=None,key="sphere_section")
        with r2:
            st.markdown("### Fórmulas")
            st.latex(r"S=4\pi r^2")
            st.latex(r"V=\frac{4}{3}\pi r^3")
            st.latex(r"r_{\mathrm{corte}}=\sqrt{r^2-h^2}")
            st.metric("Área de la sección",f"{num(math.pi*cut_radius**2)} {unit}²")
            st.info("En |h| = r, el plano es tangente a la esfera y la sección se reduce a un punto.")
        exports(fig,df,"esfera")

    elif "Elipsoide" in view:
        hero("MÓDULO 03 / GEOMETRÍA ESPACIAL", "Elipsoide triaxial",
             "Tres semiejes configurables y una intersección elíptica en cualquier altura válida.")
        with st.sidebar:
            st.markdown("#### 🔭 Opciones 3D")
            wire = st.toggle("Mostrar retícula",value=True)
            section = st.toggle("Mostrar línea de sección",value=True)
            plane = st.toggle("Mostrar plano de corte",value=True)
        left,right = st.columns([1,2.25],gap="large")
        with left:
            st.markdown("### Parámetros")
            a = st.slider("Semieje X (a)",0.5,15.0,7.0,0.5)
            b = st.slider("Semieje Y (b)",0.5,15.0,4.5,0.5)
            c = st.slider("Semieje Z (c)",0.5,15.0,3.0,0.5)
            h = st.slider("Altura del corte z = h",-c,c,0.0,0.1)
            st.markdown("#### Ecuación")
            st.latex(r"\frac{x^2}{a^2}+\frac{y^2}{b^2}+\frac{z^2}{c^2}=1")
        fig,df = solid_figure(a,b,c,h,res,section,plane,wire,show_axes,palette,"Elipsoide")
        with right:
            st.plotly_chart(fig,width="stretch",theme=None,key="chart_ellipsoid")
        vol=4/3*math.pi*a*b*c
        area=ellipsoid_area_approx(a,b,c)
        factor=max(0,1-h*h/(c*c))
        sec_a=a*math.sqrt(factor)
        sec_b=b*math.sqrt(factor)
        for col,(label,v,u) in zip(st.columns(4), [
            ("Volumen",vol,unit+"³"),("Superficie ≈",area,unit+"²"),
            ("Semieje de corte X",sec_a,unit),("Semieje de corte Y",sec_b,unit),
        ]):
            col.metric(label,f"{num(v)} {u}")
        l2,r2=st.columns([1.2,1.0],gap="large")
        with l2:
            st.markdown("### Sección transversal")
            st.plotly_chart(section_figure(a,b,c,h,palette),width="stretch",theme=None,key="ellipsoid_section")
        with r2:
            st.markdown("### Fórmulas")
            st.latex(r"V=\frac{4}{3}\pi abc")
            st.latex(r"A_{\mathrm{seccion}}=\pi ab\left(1-\frac{h^2}{c^2}\right)")
            st.metric("Área de la sección",f"{num(math.pi*sec_a*sec_b)} {unit}²")
            st.caption("El área total de superficie es una **aproximación de Knud Thomsen**, "
                       "con p = 1,6075. El volumen y el área de la sección son exactos.")
        exports(fig,df,"elipsoide")

    elif "Plano" in view:
        hero("MÓDULO 04 / GEOMETRÍA ANALÍTICA", "Plano cartesiano 3D",
             "Construcción del plano z = mx + ny + d y su vector normal.")
        left,right=st.columns([1,2.25],gap="large")
        with left:
            st.markdown("### Parámetros")
            m=st.slider("Pendiente en X (m)",-3.0,3.0,0.5,0.1)
            n=st.slider("Pendiente en Y (n)",-3.0,3.0,-0.3,0.1)
            d=st.slider("Desplazamiento vertical (d)",-6.0,6.0,1.0,0.5)
            extent=st.slider("Extensión del plano",2.0,10.0,5.0,1.0)
            show_normal=st.toggle("Vector normal",value=True)
            st.latex(r"z=mx+ny+d")
            st.code(f"z = ({m:g})x + ({n:g})y + ({d:g})",language="text")
        fig,df=plane_figure(m,n,d,extent,show_normal,show_axes,palette)
        with right:
            st.plotly_chart(fig,width="stretch",theme=None,key="chart_plane")
        normal=np.array([-m,-n,1.])
        with st.expander("📐 Interpretación analítica",expanded=True):
            st.write("La ecuación general del plano es **mx + ny − z + d = 0**. "
                     "Por tanto, un vector normal es **n = (m, n, −1)** (o su opuesto).")
            st.write(f"Norma del vector normal: {num(np.linalg.norm(normal),3)}")
            st.write(f"Intersección con el eje Z: (0, 0, {num(d)}).")
        exports(fig,df,"plano_cartesiano")

    else:
        hero("MÓDULO 05 / ANÁLISIS COMPARATIVO", "Esfera frente a elipsoide",
             "Diferencias geométricas entre una esfera y un elipsoide de tres semiejes.")
        st.markdown("### Dimensiones para la comparación")
        sc1,sc2,sc3,sc4=st.columns(4)
        with sc1:
            r=st.slider("Radio de la esfera",1.0,10.0,4.0,0.5)
        with sc2:
            a=st.slider("Semieje a",1.0,12.0,6.0,0.5)
        with sc3:
            b=st.slider("Semieje b",1.0,12.0,4.0,0.5)
        with sc4:
            c=st.slider("Semieje c",1.0,12.0,2.5,0.5)
        sphere_fig,_=solid_figure(r,r,r,0,res,False,False,True,show_axes,palette,"Esfera")
        ellipsoid_fig,_=solid_figure(a,b,c,0,res,False,False,True,show_axes,palette,"Elipsoide")
        p1,p2=st.columns(2,gap="large")
        with p1:
            st.plotly_chart(sphere_fig,width="stretch",theme=None,key="compare_sphere")
        with p2:
            st.plotly_chart(ellipsoid_fig,width="stretch",theme=None,key="compare_ellipsoid")
        sv=4/3*math.pi*r**3
        ev=4/3*math.pi*a*b*c
        sa=4*math.pi*r*r
        ea=ellipsoid_area_approx(a,b,c)
        st.markdown("### Tabla de propiedades")
        st.dataframe(pd.DataFrame({
            "Propiedad": ["Semiejes", "Volumen", "Área de superficie", "Simetría"],
            "Esfera": [f"{num(r)} / {num(r)} / {num(r)}",f"{num(sv)} {unit}³",
                       f"{num(sa)} {unit}²", "Igual en todas direcciones"],
            "Elipsoide": [f"{num(a)} / {num(b)} / {num(c)}",f"{num(ev)} {unit}³",
                          f"{num(ea)} {unit}² ≈", "Depende de sus semiejes"],
        }),hide_index=True,width="stretch")
        st.caption("El área de superficie del elipsoide se calcula con una aproximación; los volúmenes son exactos.")

    st.markdown("<div class='foot'>GEOLAB 3D · Visualización matemática interactiva · Streamlit + NumPy + Plotly</div>",unsafe_allow_html=True)


if __name__ == "__main__":
    main()
