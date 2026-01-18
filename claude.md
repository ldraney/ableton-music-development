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

### Phase 1: OSC Client Wrapper ✅ COMPLETE
Minimal, well-tested Python wrapper around `python-osc` for AbletonOSC's API.

**Status:** Tests automated - clip tests create their own fixtures, only device tests require manual setup

**Structure:**
```
osc_client/
├── __init__.py
├── client.py          # Core OSC send/receive
├── application.py     # /live/application/*, /live/api/*
├── song.py            # /live/song/* operations
├── track.py           # /live/track/* operations
├── clip.py            # /live/clip/* operations
├── clip_slot.py       # /live/clip_slot/* operations
├── device.py          # /live/device/* operations
├── scene.py           # /live/scene/* operations
├── view.py            # /live/view/* operations
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
- `ldraney/AbletonOSC` - fork with device insertion support (PR #173 pending)
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
python3 -c "from osc_client import connect; connect().send('/live/api/reload')"
```

**Why symlink?** Without it, you have two copies (git repo vs Remote Scripts) and must manually sync changes. The symlink makes them the same directory.

**After editing AbletonOSC code:** Just send `/live/api/reload` - no Ableton restart needed.

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

## Code Organization

### osc_client: Foundational Library (Read-Only)
The `osc_client/` directory is the **foundation** of this project. It should be treated as read-only during normal song creation work.

**When working on songs:** Import and use `osc_client`, but don't modify it.

**When improving the library:**
1. Create an issue describing the enhancement
2. Open a PR with the changes
3. Include tests for new functionality
4. Merge only after tests pass

This keeps the foundation stable while songs are developed in worktrees.

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

# The osc_client is available via the main repo's install
# Song scripts go in this worktree, not in main

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

## Setup
```bash
# Create venv and install
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"

# Run tests (requires Ableton with AbletonOSC enabled)
pytest -v
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
