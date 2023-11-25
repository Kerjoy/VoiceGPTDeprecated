import sounddevice as sd
from pydub import AudioSegment
import numpy as np
import keyboard

# Configuración de la grabación
fs = 44100  # Frecuencia de muestreo
channels = 2  # Número de canales de audio

# Lista para almacenar los datos de audio
audio_data = []

# Función para la grabación de audio
def callback(indata, frames, time, status):
    if status:
        print(status)
    audio_data.extend(indata.copy())

# Ajustar el tamaño del bloque para adaptarse mejor al sistema
blocksize = 8192

# Iniciar la grabación
with sd.InputStream(callback=callback, channels=channels, samplerate=fs, blocksize=blocksize):
    print("Presiona cualquier tecla para detener la grabación...")
    keyboard.read_event(suppress=True)  # Limpiar cualquier tecla que ya esté presionada
    keyboard.wait("enter")

# Convertir los datos de audio a un formato compatible con pydub
audio_array = np.array(audio_data)
audio_segment = AudioSegment(audio_array.tobytes(), frame_rate=fs, sample_width=audio_array.dtype.itemsize, channels=channels)

# Liberar la memoria del búfer
sd.stop()

# Guardar la grabación en un archivo .mp3
output_filename = "grabacion.mp3"
audio_segment.export(output_filename, format="mp3")

print(f"La grabación ha sido guardada en {output_filename}")