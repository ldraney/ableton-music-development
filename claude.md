# Ableton Music Development

## Vision
Make Ableton Live accessible through conversational AI. Users develop and modify songs through dialogue with Claude Code while observing changes in Ableton's UI. Reduce the expert-level learning curve by letting AI handle the interface complexity.

## Architecture

```
Claude Code
    ↓ MCP protocol
MCP Server (tools organized by domain)
    ↓ Python calls
OSC Client (thin wrapper around python-osc)
    ↓ UDP ports 11000/11001
AbletonOSC (MIDI Remote Script)
    ↓ Live Object Model
Ableton Live
```

## Development Phases

### Phase 1: OSC Client Wrapper
Minimal, well-tested Python wrapper around `python-osc` for AbletonOSC's API.

**Goals:**
- Thin wrapper - don't over-abstract
- Mirror AbletonOSC's hierarchical API structure
- Comprehensive test coverage against live Ableton instance
- Clear error handling for connection issues

**Structure:**
```
osc_client/
├── __init__.py
├── client.py          # Core OSC send/receive
├── song.py            # /live/song/* operations
├── track.py           # /live/track/* operations
├── clip.py            # /live/clip/* operations
├── clip_slot.py       # /live/clip_slot/* operations
├── device.py          # /live/device/* operations
├── scene.py           # /live/scene/* operations
└── tests/
    ├── conftest.py    # Fixtures, live Ableton connection
    ├── test_song.py
    ├── test_track.py
    └── ...
```

### Phase 2: MCP Server
Wrap OSC client in MCP server exposing tools to Claude Code.

**Tool organization by domain:**
- `song_*` - tempo, time signature, play/stop, scenes
- `track_*` - create, volume, pan, mute, solo
- `clip_*` - create, edit notes, launch, properties
- `device_*` - add effects/instruments, tweak parameters

### Phase 3: Langgraph Agents (future)
Multi-step orchestration for complex production tasks.

## Key Repos
- `ideoforms/AbletonOSC` - upstream OSC bridge (install this in Ableton)
- `ldraney/AbletonOSC` - fork for any customizations needed
- `ldraney/ableton-manual` - RAG for Ableton Live 12 manual reference

## Tech Stack
- Python 3.11+
- `python-osc` - OSC protocol client
- `pytest` - testing
- Ableton Live 12 with AbletonOSC installed

## Development Principles
- **"If Ableton can do it, expose it"** - comprehensive LOM access over convenience shortcuts
- **Transparency** - user watches Ableton while Claude works
- **Test against real Ableton** - no mocks for OSC layer, integration tests are the source of truth
- **Minimal first** - get something working end-to-end before expanding

## AbletonOSC API Reference
API follows pattern: `/live/{object}/{action}/{property}`

Examples:
```
/live/song/get/tempo          → returns current BPM
/live/song/set/tempo [120.0]  → sets BPM to 120
/live/song/start_playback     → starts playing
/live/song/stop_playback      → stops
/live/track/get/volume [0]    → get track 0 volume
/live/clip/get/notes [0, 0]   → get notes from track 0, clip 0
```

Full API: https://github.com/ideoforms/AbletonOSC#api-documentation
