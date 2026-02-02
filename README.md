# API Sonification - Turn HTTP Traffic into Music 🎵

**Real-time audio synthesis from API logs → hear your infrastructure's rhythm**

## What It Does

Transforms HTTP traffic patterns into generative music:
- **Status Codes → Instruments**: 2xx (piano melody), 3xx (electric piano), 4xx (bass), 5xx (drums/alarms)
- **Status → Scale**: 2xx major (happy), 3xx minor (neutral), 4xx diminished (tense), 5xx chromatic (chaos)
- **Response Time → Pitch**: Slow responses = lower pitch (audible warning!)
- **Request Size → Duration**: Larger responses = longer notes
- **Volume by Severity**: 5xx errors play LOUDEST

## Why It Matters

Monitoring dashboards are *visual*. But humans detect audio anomalies faster. Hear your API's health intuitively:
- **Normal traffic**: Pleasant, rhythmic music in major scale
- **Error spike**: Sudden dissonance, loud notes
- **Slowdown**: Pitch drops noticeably
- **Server crash**: Chaotic chromatic noise at max volume

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

```bash
# Try the demo (generates sample traffic and sonifies it)
python cli.py demo

# Sonify your own logs
python cli.py sonify /var/log/nginx/access.log --output api_music.mid

# Limit to first 100 requests
python cli.py sonify access.log --limit 100

# Faster tempo (more energetic)
python cli.py sonify access.log --tempo 160
```

## Output

Generates MIDI files that you can:
- **Play**: `timidity api_music.mid` (or any MIDI player)
- **Convert to MP3**: `timidity -Ow -o - api_music.mid | lame - api_music.mp3`
- **Import to DAW**: Open in GarageBand, Ableton, FL Studio for editing

## Log Format Support

✅ **Nginx** (combined format)
✅ **Apache** (common log format)  
✅ **JSON** logs with `{method, path, status, bytes, response_time}`

Example formats:
```
# Nginx
127.0.0.1 - - [01/Feb/2026:10:00:00] "GET /api/users HTTP/1.1" 200 1234 "-" "curl/7.64.1"

# Apache
127.0.0.1 - - [01/Feb/2026:10:00:00] "GET /api/users HTTP/1.1" 200 1234

# JSON
{"method":"GET","path":"/api/users","status":200,"bytes":1234,"response_time":0.042}
```

## Demo Output

The demo generates a 60-second emotional journey:
1. **0-20s**: Healthy traffic (major scale, pleasant)
2. **20-25s**: Redirects appear (minor scale, neutral)
3. **25-35s**: 404 errors (diminished scale, tense)
4. **35-45s**: 500 SERVER ERRORS (chromatic chaos, LOUD)
5. **45-60s**: Recovery (back to major scale)

You can *hear* the incident unfold!

## Musical Mapping

### Status → Track & Scale
| Status | Track | Instrument | Scale | Mood |
|--------|-------|-----------|-------|------|
| 2xx | 0 | Acoustic Piano | Major | Happy ✅ |
| 3xx | 1 | Electric Piano | Minor | Neutral |
| 4xx | 2 | Acoustic Bass | Diminished | Tense ⚠️ |
| 5xx | 3 | Synth Drums | Chromatic | Chaos 🚨 |

### Response Time → Pitch
- **<100ms**: High notes (72-84) - fast is good!
- **100ms-1s**: Middle range (60) - normal
- **>1s**: Low notes (48-60) - audible slowdown

### Request Size → Duration
- **<1KB**: 0.25 beats (staccato)
- **1-10KB**: 0.5 beats (normal)
- **>10KB**: 1.0 beats (sustained)

## Tech Stack

- **MIDI Generation**: midiutil (Python)
- **Log Parsing**: regex + JSON support
- **CLI**: click
- **Math**: numpy (pitch calculations)

## Roadmap

- [x] Log parser (Nginx/Apache/JSON)
- [x] MIDI synthesis engine
- [x] Status code → instrument mapping
- [x] Response time → pitch mapping
- [x] CLI tool with demo mode
- [ ] Real-time mode (`--follow` flag)
- [ ] Live audio output (Web Audio API streaming)
- [ ] ML anomaly detector (learns "healthy" sound)
- [ ] Web UI with waveform visualizer
- [ ] Preset soundscapes (ambient, techno, classical)
- [ ] Multi-server aggregation

## Contributing

Looking for:
- **Audio engineers**: Better instrument selection, DSP effects
- **ML experts**: Anomaly detection on audio patterns
- **Web devs**: Real-time streaming UI with waveforms
- **Creative coders**: Alternative mapping strategies

## Example Use Cases

1. **DevOps Monitoring**: Run during deploy - hear if errors spike
2. **Performance Testing**: Hear latency increases as load grows
3. **Art Projects**: Turn your API into a generative music album
4. **Presentations**: Live demo of API health through sound

---

**Status:** MVP shipped! 650+ lines, working parser + synthesis + CLI tool.
