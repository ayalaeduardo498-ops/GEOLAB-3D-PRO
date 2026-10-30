# GEOLAB 3D · Geometría Analítica en Streamlit

Aplicación local interactiva para explorar la circunferencia 2D, esfera 3D, elipsoide triaxial 3D y plano 3D.

## Requisitos

- Windows 10/11
- Python 3.11, 3.12 o 3.13 instalado y accesible con `py`
- Visual Studio Code

## Instalación rápida (PowerShell de VS Code)

Abre la carpeta `GEOMETRIA_STREAMLIT_PRO` en VS Code y ejecuta:

```powershell
py --version
py -m pip install -r requirements.txt
py -m streamlit run app.py
```

Si `py` no funciona, prueba los mismos comandos con `python`. Si tampoco se reconoce, instala Python y configura PATH / App Execution Aliases.

El navegador abrirá la aplicación en `http://localhost:8501`.

## Características

- Circunferencia: radio, diámetro, punto angular, tangente, círculo interior y ecuación.
- Esfera: malla 3D con rotación, secciones horizontales, plano opcional, volumen y área de superficie.
- Elipsoide: tres semiejes independientes, plano y elipse de corte, volumen, área de superficie aproximada y métricas.
- Plano cartesiano 3D: pendientes, intercepto y vector normal.
- Interactividad con Plotly; exportación HTML autónomo y coordenadas CSV; menú y estilos profesionales.

## Fundamento matemático

- Esfera y elipsoide centrados en el origen.
- Volumen de esfera: `4/3*pi*r**3`.
- Volumen de elipsoide: `4/3*pi*a*b*c`.
- Sección del elipsoide a altura h: semiejes `a*sqrt(1-h**2/c**2)` y `b*sqrt(1-h**2/c**2)`.
- Área total del elipsoide: aproximación de Knud Thomsen, p=1.6075. Exacta solo en casos particulares; no se presenta como una fórmula exacta para un elipsoide triaxial general.

## Control del servidor

En la terminal usa `Ctrl + C` para detener Streamlit. Arrastrar el objeto 3D lo rota y la rueda ajusta el zoom.
