import paho.mqtt.client as paho
import time
import streamlit as st
import json
import platform

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
st.markdown("<h1>MQTT Control</h1>", unsafe_allow_html=True)

# Muestra la versión de Python
st.write("Versión de Python:", platform.python_version())

values = 0.0
act1 = "OFF"

def on_publish(client, userdata, result):
    print("el dato ha sido publicado \n")

def on_message(client, userdata, message):
    global message_received
    time.sleep(2)
    message_received = str(message.payload.decode("utf-8"))
    st.write(message_received)

# Configuración MQTT
broker = "157.230.214.127"
port = 1883
client1 = paho.Client("GIT-HUB")
client1.on_message = on_message

# 🔘 Botón ON
if st.button('Encender (ON)'):
    act1 = "ON"
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    client1.publish("cmqtt_s", message)

# 🔘 Botón OFF
if st.button('Apagar (OFF)'):
    act1 = "OFF"
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Act1": act1})
    client1.publish("cmqtt_s", message)

# 🎚️ Slider mejor presentado
values = st.slider('Selecciona el rango de valores (0 a 100)', 0.0, 100.0)
st.write('Valor seleccionado:', values)

# 📤 Enviar valor analógico
if st.button('📨 Enviar valor analógico'):
    client1 = paho.Client("GIT-HUB")
    client1.on_publish = on_publish
    client1.connect(broker, port)
    message = json.dumps({"Analog": float(values)})
    client1.publish("cmqtt_a", message)
