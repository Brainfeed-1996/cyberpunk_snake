import numpy as np
import wave
import struct

# Génération d'un son synthétique pour l'effet "manger"
def generate_eat_sound():
    # Paramètres du son
    duration = 0.1  # secondes
    sample_rate = 44100
    frequency = 440.0  # fréquence en Hz

    # Génération du son
    t = np.linspace(0, duration, int(sample_rate * duration))
    # Onde sinusoïdale avec fréquence qui augmente
    signal = np.sin(2 * np.pi * frequency * t * (1 + t * 10))
    
    # Normalisation et conversion en entiers 16 bits
    signal = np.int16(signal * 32767)
    
    # Écriture du fichier WAV
    with wave.open('sounds/eat.wav', 'w') as wav_file:
        # Paramètres du fichier WAV
        nchannels = 1
        sampwidth = 2
        nframes = len(signal)
        
        # Configuration de l'en-tête WAV
        wav_file.setnchannels(nchannels)
        wav_file.setsampwidth(sampwidth)
        wav_file.setframerate(sample_rate)
        wav_file.setnframes(nframes)
        
        # Écriture des données
        for sample in signal:
            wav_file.writeframes(struct.pack('h', sample))

if __name__ == "__main__":
    import os
    os.makedirs('sounds', exist_ok=True)
    generate_eat_sound()
