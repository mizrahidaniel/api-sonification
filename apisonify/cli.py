"""CLI interface for API sonification"""
import click
import json
import numpy as np
from pathlib import Path
from .audio import AudioSynthesizer

@click.command()
@click.argument('logfile', type=click.Path(exists=True))
@click.option('--output', '-o', default='output.wav', help='Output WAV file')
@click.option('--duration', '-d', default=0.5, help='Note duration in seconds')
def main(logfile, output, duration):
    """Transform API logs into audio"""
    click.echo(f"🎵 API Sonification - Generating audio from {logfile}")
    
    # Load logs
    with open(logfile) as f:
        logs = json.load(f)
    
    click.echo(f"📊 Loaded {len(logs)} log entries")
    
    # Initialize synthesizer
    synth = AudioSynthesizer()
    
    # Generate notes for each log entry
    audio_segments = []
    for i, log in enumerate(logs):
        status = log.get('status', 200)
        response_time = log.get('response_time_ms', 100)
        
        note = synth.generate_note(status, response_time, duration)
        audio_segments.append(note)
        
        # Add silence between notes
        silence = np.zeros(int(synth.sample_rate * 0.1))
        audio_segments.append(silence)
    
    # Concatenate all segments
    full_audio = np.concatenate(audio_segments)
    
    # Save to file
    synth.save_wav(full_audio, output)
    click.echo(f"✅ Saved audio to {output}")
    click.echo(f"🎼 Duration: {len(full_audio) / synth.sample_rate:.2f}s")

if __name__ == '__main__':
    main()
