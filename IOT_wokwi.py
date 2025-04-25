import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform
import pandas as pd

# Variables para graficar
data_received = []

# 🌄 Fondo personalizado
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://i.redd.it/cq8btdxz1x2b1.jpg");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🌟 Estilos personalizados
st.markdown("""
    <style>
        .custom-title {
            font-size: 40px;
            color: red;
            font-weight: bold;
        }
        .stButton>button {
            color: white;
            background-color: #007BFF;
            border-radius: 10px;
            padding: 0.5em 1em;
            font-weight: bold;
        }
        .stSlider > div {
            padding: 10px;
            background-color: #f0f8ff;
            border-radius: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# 🔺 Título principal rojo
st.markdown('<div class="custom-title">MQTT Control</div>', unsafe_allow_html=True)

# Versión de Python
st.markdown('<h3 style="color: black;">Versión de Python:</h3>', unsafe_allow_html=True)
st.write(platform.python_version())

# MQTT configuración
broker = "157.230.214.127"
port = 1883

# Inicializar cliente
client = paho.Client("GIT-HUB")

# Callback de publicación
def on_publish(client, userdata, result):
    print("Dato publicado.")

# Callback de recepción
def on_message(client, userdata, message):
    payload = message.payload.decode("utf-8")
    st.session_state["mensaje_actual"] = payload
    try:
        valor = float(payload)
        st.session_state["data"].append(valor)
    except:
        pass

# Conectar cliente
client.on_publish = on_publish
client.on_message = on_message
client.connect(broker, port)
client.loop_start()
client.subscribe("cmqtt_a")

# Inicializar estado de sesión
if "data" not in st.session_state:
    st.session_state["data"] = []
if "mensaje_actual" not in st.session_state:
    st.session_state["mensaje_actual"] = "Esperando datos..."

# 🔘 Botones de encendido/apagado
if st.button('Encender (ON)'):
    message = json.dumps({"Act1": "ON"})
    client.publish("cmqtt_s", message)

if st.button('Apagar (OFF)'):
    message = json.dumps({"Act1": "OFF"})
    client.publish("cmqtt_s", message)

# 🎚️ Slider
values = st.slider('Selecciona el rango de valores (0 a 100)', 0.0, 100.0)
st.markdown('<h3 style="color: black;">Valor seleccionado:</h3>', unsafe_allow_html=True)
st.write(values)

# 📤 Enviar valor
if st.button('📨 Enviar valor analógico'):
    message = json.dumps({"Analog": float(values)})
    client.publish("cmqtt_a", message)

# 📊 Mostrar valor recibido
st.markdown('<h3 style="color: black;">Último valor recibido:</h3>', unsafe_allow_html=True)
st.write(st.session_state["mensaje_actual"])

# 📈 Mostrar gráfico en tiempo real
if st.session_state["data"]:
    df = pd.DataFrame(st.session_state["data"], columns=["Valores"])
    st.line_chart(df)
