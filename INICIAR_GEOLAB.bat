@echo off
chcp 65001 >nul
title GEOLAB 3D - Streamlit
cd /d "%~dp0"
echo ===============================
echo       GEOLAB 3D
 echo ===============================
where py >nul 2>&1
if errorlevel 1 (
    echo ERROR: No se encontro el lanzador de Python 'py'.
    echo Instala Python desde https://www.python.org/downloads/
    echo Asegurate de instalar el lanzador de Windows.
    pause
    exit /b 1
)
py -m pip show streamlit >nul 2>&1
if errorlevel 1 (
    echo Instalando dependencias por primera vez...
    py -m pip install -r requirements.txt
    if errorlevel 1 (
        echo No fue posible instalar dependencias.
        pause
        exit /b 1
    )
)
echo Iniciando GEOLAB 3D...
py -m streamlit run app.py
if errorlevel 1 pause
