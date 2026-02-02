#!/usr/bin/env python3
"""Command-line interface for API Sonification."""
import click
from pathlib import Path
from parser import LogParser
from synthesizer import APISynthesizer
import time


@click.group()
def cli():
    """Turn HTTP logs into music. Hear your API's rhythm."""
    pass


@cli.command()
@click.argument('logfile', type=click.Path(exists=True))
@click.option('--output', '-o', default='api_music.mid', help='Output MIDI file')
@click.option('--tempo', '-t', default=120, help='Base tempo (BPM)')
@click.option('--limit', '-n', type=int, help='Max events to process')
def sonify(logfile, output, tempo, limit):
    """Convert log file to MIDI music."""
    click.echo(f"🎼 Sonifying: {logfile}")
    
    parser = LogParser()
    synth = APISynthesizer(base_tempo=tempo)
    
    count = 0
    for event in parser.stream_file(logfile):
        synth.add_event(event)
        count += 1
        
        if limit and count >= limit:
            break
        
        if count % 100 == 0:
            click.echo(f"  Processed {count} events...")
    
    # Save MIDI
    synth.save_midi(output)
    
    # Show stats
    stats = synth.get_stats()
    click.echo(f"\n📊 Statistics:")
    click.echo(f"  Events: {stats['event_count']}")
    click.echo(f"  Duration: {stats['duration_seconds']:.1f}s")
    click.echo(f"  Tempo: {stats['tempo']} BPM")
    click.echo(f"\n🎧 Play with: timidity {output}")


@cli.command()
@click.argument('logfile', type=click.Path(exists=True))
@click.option('--follow', '-f', is_flag=True, help='Follow log file (like tail -f)')
def listen(logfile, follow):
    """Listen to logs in real-time (monitoring mode)."""
    click.echo(f"🎧 Listening to: {logfile}")
    click.echo("(Real-time audio output coming in next version)")
    
    parser = LogParser()
    
    if follow:
        click.echo("Following log file... Press Ctrl+C to stop")
        # TODO: Implement watchdog for real-time monitoring
        click.echo("⚠️  Follow mode not yet implemented - use 'sonify' for now")
    else:
        for event in parser.stream_file(logfile):
            status_emoji = '✅' if event['status'] < 300 else '⚠️' if event['status'] < 500 else '🚨'
            click.echo(f"{status_emoji} {event['method']} {event['path']} → {event['status']}")


@cli.command()
def demo():
    """Generate demo log data and sonify it."""
    click.echo("🎬 Generating demo API traffic...")
    
    # Create sample log data
    demo_log = Path("demo_access.log")
    with open(demo_log, 'w') as f:
        # Happy period
        for i in range(20):
            f.write(f'127.0.0.1 - - [01/Feb/2026:10:00:{i:02d}] "GET /api/users HTTP/1.1" 200 1234\n')
        
        # Some redirects
        for i in range(5):
            f.write(f'127.0.0.1 - - [01/Feb/2026:10:01:{i:02d}] "GET /old-path HTTP/1.1" 301 0\n')
        
        # Client errors appear
        for i in range(10):
            f.write(f'127.0.0.1 - - [01/Feb/2026:10:02:{i:02d}] "GET /api/missing HTTP/1.1" 404 512\n')
        
        # Server error spike!
        for i in range(8):
            f.write(f'127.0.0.1 - - [01/Feb/2026:10:03:{i:02d}] "POST /api/process HTTP/1.1" 500 256\n')
        
        # Recovery
        for i in range(15):
            f.write(f'127.0.0.1 - - [01/Feb/2026:10:04:{i:02d}] "GET /api/health HTTP/1.1" 200 89\n')
    
    click.echo(f"✅ Demo log created: {demo_log}")
    click.echo("\n🎵 Sonifying demo traffic...\n")
    
    # Sonify it
    parser = LogParser()
    synth = APISynthesizer(base_tempo=140)
    
    for event in parser.stream_file(str(demo_log)):
        synth.add_event(event)
    
    output = "demo_music.mid"
    synth.save_midi(output)
    
    click.echo(f"\n✨ Listen to your API's emotional journey:")
    click.echo(f"   - First 20s: Happy traffic (major scale)")
    click.echo(f"   - 20-25s: Redirects (minor scale)")
    click.echo(f"   - 25-35s: 404 errors (diminished scale, tense)")
    click.echo(f"   - 35-45s: 500 ERRORS (chromatic chaos, loud!)")
    click.echo(f"   - 45-60s: Recovery (back to major)")
    click.echo(f"\n🎧 Play: timidity {output}")


if __name__ == '__main__':
    cli()
