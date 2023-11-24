import tkinter as tk
import sounddevice as sd
from pydub import AudioSegment
import numpy as np

# Configuración de la grabación
fs = 48000  # Frecuencia de muestreo
channels = 2  # Número de canales de audio

# Lista para almacenar los datos de audio
audio_data = []

# Estado de la grabación
grabando = False

# Objeto stream
stream = None
blocksize = 8192

# Función para la grabación de audio
def callback(indata, frames, time, status):
    if status:
        print(status)
    if grabando:
        audio_data.extend(indata.copy())

# Función para iniciar la grabación
def start_recording():
    global grabando, stream
    grabando = True
    audio_data.clear()
    stream = sd.InputStream(callback=callback, channels=channels, samplerate=fs, blocksize=blocksize)
    stream.start()

# Función para detener la grabación
def stop_recording():
    global grabando, stream
    grabando = False
    if stream:
        stream.stop()
        stream.close()

# Función para exportar y guardar la grabación
def save_recording():
    global audio_data
    audio_array = np.array(audio_data)
    audio_segment = AudioSegment(audio_array.tobytes(), frame_rate=fs, sample_width=audio_array.dtype.itemsize, channels=channels)
    output_filename = "grabacion.mp3"
    audio_segment.export(output_filename, format="mp3")
    print(f"La grabación ha sido guardada en {output_filename}")

# Configuración de la interfaz gráfica
root = tk.Tk()
root.title("Grabadora de Audio")

# Botones
btn_start = tk.Button(root, text="Iniciar Grabación", command=start_recording)
btn_start.pack(pady=10)

btn_stop = tk.Button(root, text="Detener Grabación", command=stop_recording)
btn_stop.pack(pady=10)

btn_save = tk.Button(root, text="Guardar Grabación", command=save_recording)
btn_save.pack(pady=10)

# Iniciar la interfaz gráfica
root.mainloop()