# abletonosc-client

## Vision
Make Ableton Live accessible through conversational AI. Users develop and modify songs through dialogue with Claude Code while observing changes in Ableton's UI. Reduce the expert-level learning curve by letting AI handle the interface complexity.

## Architecture

```
Claude Code
    ↓ MCP protocol
MCP Server (tools organized by domain)
    ↓ Python calls
abletonosc-client (PyPI package)
    ↓ UDP ports 11000/11001
AbletonOSC (MIDI Remote Script)
    ↓ Live Object Model
Ableton Live
```

## Development Phases

### Phase 1: OSC Client Wrapper ✅ COMPLETE (v1.0.0)
Comprehensive Python wrapper around `python-osc` for AbletonOSC's API.
Published to PyPI as `abletonosc-client`.

**Installation:**
```bash
pip install abletonosc-client
```

**Status:** 263 tests, ~220 endpoints implemented (near-complete AbletonOSC coverage)

**Capabilities:**
- **Application**: Version info, reload script, log level, status bar messages
- **Song**: Tempo, transport, time signature, tracks, scenes, loops, recording, quantization, cue points, key/scale, bulk queries (track names), nudge tempo, session record status
- **Track**: Volume, pan, mute, solo, arm, color, routing (types + channels), monitoring (get/set), meters, device management, sends, bulk clip/device queries
- **Clip**: Notes (add/get/remove), properties (loop, warp, gain, pitch, muted, markers, position), launch mode/quantization, recording state, playing position listener
- **ClipSlot**: Create/delete/duplicate clips, launch, stop, stop button control
- **Device**: Parameters (get/set by index or name, bulk get/set), enable/disable, device info, value strings, parameter listeners
- **Scene**: Name, color, color_index, tempo (with enable), time signature (with enable), is_empty, fire_selected
- **View**: Track/scene/clip/device selection, view focus
- **MidiMap**: MIDI CC mapping to device parameters
- **Listeners**: Real-time callbacks for tempo, transport, loop, record, beat, song time, track properties, view selection, clip playing position, device parameters

**Structure:**
```
abletonosc_client/
├── __init__.py
├── client.py          # Core OSC send/receive with listener support
├── application.py     # /live/application/*, /live/api/*
├── song.py            # /live/song/* operations + listeners
├── track.py           # /live/track/* operations + per-track listener dispatcher
├── clip.py            # /live/clip/* operations + playing position listener
├── clip_slot.py       # /live/clip_slot/* operations
├── device.py          # /live/device/* operations + parameter listeners
├── scene.py           # /live/scene/* operations
├── view.py            # /live/view/* operations + listeners
├── midimap.py         # /live/midimap/* MIDI CC mapping
├── scales.py          # Music theory: scales
├── chords.py          # Music theory: chords
└── tests/
    ├── conftest.py    # Fixtures, live Ableton connection
    ├── test_application.py
    ├── test_song.py
    ├── test_track.py
    ├── test_clip.py
    ├── test_clip_slot.py
    ├── test_device.py
    ├── test_scene.py
    ├── test_view.py
    ├── test_midimap.py
    ├── test_scales.py
    └── test_chords.py
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
- `ldraney/AbletonOSC` - fork with device insertion support (PR #173 pending)
- `ldraney/abletonosc-client` - this library (PyPI package)
- `ldraney/ableton-manual` - RAG for Ableton Live 12 manual reference

## AbletonOSC Fork Setup

Our fork adds `/live/track/insert_device` for loading devices via OSC. To set it up:

```bash
# Clone the fork
cd ~
git clone https://github.com/ldraney/AbletonOSC.git

# Symlink to Ableton's Remote Scripts (so edits are immediately available)
rm -rf "/Users/$USER/Music/Ableton/User Library/Remote Scripts/AbletonOSC"
ln -s ~/AbletonOSC "/Users/$USER/Music/Ableton/User Library/Remote Scripts/AbletonOSC"

# Restart Ableton or reload via OSC
python3 -c "from abletonosc_client import connect; connect().send('/live/api/reload')"
```

**Why symlink?** Without it, you have two copies (git repo vs Remote Scripts) and must manually sync changes. The symlink makes them the same directory.

**After editing AbletonOSC code:** Just send `/live/api/reload` - no Ableton restart needed.

## Tech Stack
- Python 3.11+
- `python-osc` - OSC protocol client
- `pytest` - testing
- `poetry` - package management
- Ableton Live 12 with AbletonOSC installed

## Development Principles
- **"If Ableton can do it, expose it"** - comprehensive LOM access over convenience shortcuts
- **Transparency** - user watches Ableton while Claude works
- **Test against real Ableton** - no mocks for OSC layer, integration tests are the source of truth
- **Minimal first** - get something working end-to-end before expanding

## Code Organization

### abletonosc_client: Published Library
The `abletonosc_client/` directory is published to PyPI as `abletonosc-client`.

**Usage:**
```python
from abletonosc_client import connect, Song, Track, Clip

client = connect()
song = Song(client)
song.set_tempo(120.0)
```

### Songs: Use Git Worktrees
Each song should be developed in its own git worktree to:
- Keep song experiments isolated
- Allow parallel work on multiple songs
- Prevent song code from polluting the main branch

```bash
# Create a worktree for a new song
git worktree add ../songs/lofi-study-beats -b song/lofi-study-beats

# Work in that directory
cd ../songs/lofi-study-beats

# Install the library from PyPI
pip install abletonosc-client

# When done, optionally remove the worktree
git worktree remove ../songs/lofi-study-beats
```

**Song structure in worktree:**
```
songs/lofi-study-beats/
├── main.py          # Song creation script
├── README.md        # Song notes, BPM, key, etc.
└── exports/         # Rendered audio files
```

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

**Response format:** Responses include input indices before value:
- Song: `(value)` - no indices
- Track: `(track_index, value)`
- Scene: `(scene_index, value)`
- Clip/ClipSlot: `(track_index, scene_index, value)`
- Device: `(track_index, device_index, value)`
- Parameter: `(track_index, device_index, param_index, value)`

Full API: https://github.com/ideoforms/AbletonOSC#api-documentation

## Setup (Development)
```bash
# Clone and install with Poetry
git clone https://github.com/ldraney/abletonosc-client.git
cd abletonosc-client
poetry install

# Run tests (requires Ableton with AbletonOSC enabled)
poetry run pytest -v
```

## Test Requirements

### Automated Tests (No Setup Required)
- **Song, Track, Scene, View tests**: Run automatically against any Ableton project
- **Clip tests**: Create their own MIDI track and clip via `test_clip_with_notes` fixture
  - You should hear a C major chord briefly when clip tests run (proves end-to-end)
  - Track count returns to original after tests complete

### Manual Setup Required (Device Parameter Tests)
Device parameter tests (in `test_device.py`) require a device on track 0:
1. Open Ableton Live with AbletonOSC enabled
2. Add any device to track 0 (e.g., drag "Simpler" or "Wavetable" onto track 0)
3. Run `pytest -v`

Without a device on track 0, device parameter tests will skip with a clear message.

### Device Insertion Tests (Fully Automated)
Device insertion tests (in `test_track.py`) are fully automated - they create their own tracks and devices:
- `test_insert_device` - Creates MIDI track, inserts Wavetable
- `test_insert_audio_effect` - Creates audio track, inserts Compressor
- `test_delete_device` - Creates track, adds device, deletes it

**Note:** Device insertion requires our AbletonOSC fork with `/live/track/insert_device`.
