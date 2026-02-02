"""Audio synthesis core - maps API metrics to sound"""
import numpy as np
from typing import Dict, List, Tuple

class AudioSynthesizer:
    """Generate audio from API metrics"""
    
    SAMPLE_RATE = 44100  # CD quality
    
    def __init__(self):
        self.sample_rate = self.SAMPLE_RATE
    
    def request_rate_to_tempo(self, req_per_sec: float) -> float:
        """Map request rate to BPM (tempo)"""
        # 10 req/s = 120 BPM baseline
        return 60 + (req_per_sec * 6)
    
    def status_code_to_instrument(self, status_code: int) -> str:
        """Map status code to instrument type"""
        if 200 <= status_code < 300:
            return "major_melody"  # Happy
        elif 400 <= status_code < 500:
            return "minor_stab"    # Dissonant
        elif 500 <= status_code < 600:
            return "alarm"         # Alert!
        else:
            return "neutral"
    
    def response_time_to_pitch(self, response_ms: float) -> float:
        """Map response time to frequency (Hz)"""
        # <100ms: C5 (523 Hz)
        # 100-500ms: C4 (261 Hz)
        # >500ms: C3 (130 Hz) - warning zone
        if response_ms < 100:
            return 523.25
        elif response_ms < 500:
            return 261.63
        else:
            return 130.81
    
    def generate_sine_wave(self, freq: float, duration: float, amplitude: float = 0.5) -> np.ndarray:
        """Generate pure sine wave"""
        t = np.linspace(0, duration, int(self.sample_rate * duration))
        return amplitude * np.sin(2 * np.pi * freq * t)
    
    def apply_adsr(self, wave: np.ndarray, attack: float = 0.1, decay: float = 0.1, 
                   sustain: float = 0.7, release: float = 0.2) -> np.ndarray:
        """Apply ADSR envelope to wave"""
        length = len(wave)
        envelope = np.ones(length)
        
        # Attack
        attack_samples = int(attack * length)
        envelope[:attack_samples] = np.linspace(0, 1, attack_samples)
        
        # Decay
        decay_samples = int(decay * length)
        envelope[attack_samples:attack_samples+decay_samples] = np.linspace(1, sustain, decay_samples)
        
        # Sustain (already set to sustain level)
        
        # Release
        release_samples = int(release * length)
        envelope[-release_samples:] = np.linspace(sustain, 0, release_samples)
        
        return wave * envelope
    
    def generate_note(self, status_code: int, response_time: float, duration: float = 0.5) -> np.ndarray:
        """Generate a note from API metrics"""
        freq = self.response_time_to_pitch(response_time)
        instrument = self.status_code_to_instrument(status_code)
        
        # Generate base wave based on instrument
        if instrument == "major_melody":
            wave = self.generate_sine_wave(freq, duration, amplitude=0.5)
        elif instrument == "minor_stab":
            wave = self.generate_sine_wave(freq * 0.8, duration, amplitude=0.7)  # Lower pitch
        elif instrument == "alarm":
            # Alarm: sine + noise
            wave = self.generate_sine_wave(freq, duration, amplitude=0.8)
            noise = np.random.normal(0, 0.2, len(wave))
            wave = wave + noise
        else:
            wave = self.generate_sine_wave(freq, duration, amplitude=0.3)
        
        # Apply envelope
        return self.apply_adsr(wave)
    
    def save_wav(self, audio: np.ndarray, filename: str):
        """Save audio array to WAV file"""
        from scipy.io import wavfile
        # Normalize to 16-bit PCM
        audio_normalized = np.int16(audio / np.max(np.abs(audio)) * 32767)
        wavfile.write(filename, self.sample_rate, audio_normalized)
