"""Audio synthesis engine for HTTP events."""
from midiutil import MIDIFile
import numpy as np
from typing import Dict, List
from datetime import datetime


class APISynthesizer:
    """Converts HTTP events into MIDI sequences."""
    
    # Musical scales for different endpoint patterns
    SCALES = {
        'major': [0, 2, 4, 5, 7, 9, 11],      # Happy/success
        'minor': [0, 2, 3, 5, 7, 8, 10],      # Neutral
        'diminished': [0, 2, 3, 5, 6, 8, 9],  # Tension/errors
        'chromatic': [0, 1, 2, 3, 4, 5, 6]    # Chaos/alerts
    }
    
    def __init__(self, base_tempo: int = 120):
        self.base_tempo = base_tempo
        self.midi = MIDIFile(4)  # 4 tracks
        self.current_time = 0.0
        self.event_count = 0
        
        # Track assignments
        self.MELODY_TRACK = 0    # 2xx responses
        self.HARMONY_TRACK = 1   # 3xx redirects
        self.BASS_TRACK = 2      # 4xx errors
        self.DRUMS_TRACK = 3     # 5xx errors
        
        # Initialize tracks
        for track in range(4):
            self.midi.addTempo(track, 0, self.base_tempo)
            self.midi.addProgramChange(track, track, 0, 
                                      self._get_instrument(track))
    
    def _get_instrument(self, track: int) -> int:
        """Map track to MIDI instrument."""
        instruments = {
            0: 1,   # Acoustic Grand Piano (melody)
            1: 4,   # Electric Piano (harmony)
            2: 33,  # Acoustic Bass (bass)
            3: 118  # Synth Drum (percussion)
        }
        return instruments.get(track, 0)
    
    def _status_to_track(self, status: int) -> int:
        """Map HTTP status code to MIDI track."""
        if 200 <= status < 300:
            return self.MELODY_TRACK
        elif 300 <= status < 400:
            return self.HARMONY_TRACK
        elif 400 <= status < 500:
            return self.BASS_TRACK
        else:  # 5xx
            return self.DRUMS_TRACK
    
    def _status_to_scale(self, status: int) -> List[int]:
        """Map HTTP status to musical scale."""
        if 200 <= status < 300:
            return self.SCALES['major']
        elif 300 <= status < 400:
            return self.SCALES['minor']
        elif 400 <= status < 500:
            return self.SCALES['diminished']
        else:
            return self.SCALES['chromatic']
    
    def _response_time_to_pitch(self, response_time: float) -> int:
        """Map response time to MIDI pitch (slower = lower)."""
        # Fast: 0-100ms → high notes (72-84)
        # Slow: >1s → low notes (48-60)
        base_pitch = 60  # Middle C
        
        if response_time < 0.1:
            offset = int((0.1 - response_time) / 0.01) + 12
        elif response_time > 1.0:
            offset = -int((response_time - 1.0) / 0.5) * 3
        else:
            offset = 0
        
        return max(36, min(84, base_pitch + offset))
    
    def _path_to_note(self, path: str, scale: List[int]) -> int:
        """Map endpoint path to scale degree."""
        # Hash path to scale index
        path_hash = hash(path.split('?')[0])  # Ignore query params
        scale_degree = scale[abs(path_hash) % len(scale)]
        base_pitch = 60  # Middle C
        return base_pitch + scale_degree
    
    def add_event(self, event: Dict):
        """Convert HTTP event to MIDI note."""
        status = event['status']
        track = self._status_to_track(status)
        scale = self._status_to_scale(status)
        
        # Determine pitch
        if event.get('response_time', 0) > 0:
            pitch = self._response_time_to_pitch(event['response_time'])
        else:
            pitch = self._path_to_note(event['path'], scale)
        
        # Determine duration based on request size
        bytes_val = event.get('bytes', 0)
        if bytes_val < 1000:
            duration = 0.25  # Short note
        elif bytes_val < 10000:
            duration = 0.5
        else:
            duration = 1.0  # Long note
        
        # Determine velocity (volume) based on status
        if status < 300:
            velocity = 80   # Normal volume
        elif status < 400:
            velocity = 60   # Quieter (redirects)
        elif status < 500:
            velocity = 100  # Louder (client errors)
        else:
            velocity = 120  # Loudest (server errors - alert!)
        
        # Add note to MIDI
        self.midi.addNote(track, track, pitch, self.current_time,
                         duration, velocity)
        
        # Advance time (creates rhythm based on request rate)
        self.current_time += 0.5  # 120 BPM = 0.5 beats per second
        self.event_count += 1
    
    def save_midi(self, filepath: str):
        """Save MIDI sequence to file."""
        with open(filepath, 'wb') as f:
            self.midi.writeFile(f)
        print(f"🎵 Saved {self.event_count} events to {filepath}")
    
    def get_stats(self) -> Dict:
        """Get synthesis statistics."""
        return {
            'event_count': self.event_count,
            'duration_seconds': self.current_time / 2,  # Convert beats to seconds
            'tempo': self.base_tempo
        }
