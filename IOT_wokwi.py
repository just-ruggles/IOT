import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

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
        h1 {
            color: red;
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

# 🔺 Título principal
st.markdown('<h1>MQTT Control</h1>', unsafe_allow_html=True)

# Muestra la versión de Python
st.markdown('<h3 style="color: black;">Versión de Python:</h3>', unsafe_allow_html=True)
st.write(platform.python_version())

# Variables iniciales
values = 0.0
act1 = "OFF"

# Callbacks MQTT
def on_publish(client, userdata, result):
    print("El dato ha sido publicado.")

def on_message(client, userdata, message):
    message_received = message.payload.decode("utf-8")
    st.write("📩 Mensaje recibido:", message_received)

# Configuración MQTT
broker = "157.230.214.127"
port = 1883

# 🔘 Botón ON
if st.button('Encender (ON)'):
    act1 = "ON"
    client = paho.Client("GIT-HUB")
    client.on_publish = on_publish
    client.connect(broker, port)
    message = json.dumps({"Act1": act1})
    client.publish("cmqtt_s", message)

# 🔘 Botón OFF
if st.button('Apagar (OFF)'):
    act1 = "OFF"
    client = paho.Client("GIT-HUB")
    client.on_publish = on_publish
    client.connect(broker, port)
    message = json.dumps({"Act1": act1})
    client.publish("cmqtt_s", message)

# 🎚️ Slider y valor mostrado
values = st.slider('Selecciona el rango de valores (0 a 100)', 0.0, 100.0)
st.markdown('<h3 style="color: black;">Valor seleccionado:</h3>', unsafe_allow_html=True)
st.write(values)

# 📤 Botón para enviar valor analógico
if st.button('📨 Enviar valor analógico'):
    client = paho.Client("GIT-HUB")
    client.on_publish = on_publish
    client.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client.publish("cmqtt_a", message)
