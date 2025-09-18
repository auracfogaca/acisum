import librosa
import numpy as np
from pydub import AudioSegment

def process_audio(filepath):
    # 1. Carregar áudio e converter para WAV mono 44.1 kHz
    sound = AudioSegment.from_file(filepath)
    sound = sound.set_channels(1).set_frame_rate(44100)
    wav_path = "temp.wav"
    sound.export(wav_path, format="wav")

    # 2. Carregar com librosa
    y, sr = librosa.load(wav_path)

    # 3. Detectar BPM
    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)

    # 4. Estimar tom (key detection)
    chroma = librosa.feature.chroma_cqt(y=y, sr=sr)
    # chave simplificada — pode evoluir com Essentia depois
    key_index = chroma.mean(axis=1).argmax()
    possible_keys = ['C','C#','D','D#','E','F','F#','G','G#','A','A#','B']
    key_detected = possible_keys[key_index % 12]

    # 5. Pitch tuning — detectar desvio em cents
    tuning = librosa.pitch_tuning(librosa.piptrack(y=y, sr=sr)[0])
    tuning_cents = tuning * 100

    # 6. Montar texto resultado
    result = (f"🎵 Análise Musical\n"
              f"- Tom (estimado): {key_detected}\n"
              f"- BPM: {tempo:.1f}\n"
              f"- Desvio de afinação: {tuning_cents:.1f} cents\n"
              f"- (Acordes: implementar com Essentia)")
    return result
