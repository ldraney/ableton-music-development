#!/usr/bin/env python3
"""Lofi Hip-Hop Song Creator (Nujabes style).

Creates a classic lofi hip-hop track using the OSC client to control Ableton Live.
Features jazzy 7th chords, boom-bap drums, and a mellow vibe.

Usage:
    python scripts/lofi_song.py

Requirements:
    - Ableton Live running with AbletonOSC enabled
    - Our AbletonOSC fork with device insertion support
"""

import sys
import time

# Add the main repo to path when running from worktree
sys.path.insert(0, '/Users/ldraney/ableton-music-development')

from osc_client import connect, chords, scales
from osc_client.clip import Clip, Note
from osc_client.clip_slot import ClipSlot
from osc_client.song import Song
from osc_client.track import Track
from osc_client.view import View


def create_lofi_song():
    """Create a complete lofi hip-hop track."""
    print("Connecting to Ableton...")
    osc_client = connect()

    # Instantiate the domain classes
    song = Song(osc_client)
    track = Track(osc_client)
    clip = Clip(osc_client)
    clip_slot = ClipSlot(osc_client)
    view = View(osc_client)

    # Get initial track count to know where our new tracks start
    initial_tracks = song.get_num_tracks()
    print(f"Current track count: {initial_tracks}")

    # =========================================================================
    # Step 1: Song Setup
    # =========================================================================
    print("\n[Step 1] Setting up song parameters...")
    song.set_tempo(78.0)
    song.set_root_note(2)  # D
    song.set_scale_name("Minor")
    song.set_groove_amount(0.3)  # 30% swing
    print(f"  Tempo: 78 BPM")
    print(f"  Key: D minor")
    print(f"  Groove: 30%")

    # =========================================================================
    # Step 2: Create 4 MIDI Tracks
    # =========================================================================
    print("\n[Step 2] Creating MIDI tracks...")
    track_names = ["Keys", "Bass", "Melody", "Drums"]

    for name in track_names:
        song.create_midi_track(-1)  # Append to end
        time.sleep(0.3)  # Give Ableton time to create track

    # Name the tracks (they're at the end)
    new_track_count = song.get_num_tracks()
    base_index = new_track_count - 4

    for i, name in enumerate(track_names):
        track_idx = base_index + i
        track.set_name(track_idx, name)
        print(f"  Created track {track_idx}: {name}")

    # Track indices for reference
    KEYS = base_index
    BASS = base_index + 1
    MELODY = base_index + 2
    DRUMS = base_index + 3

    # =========================================================================
    # Step 3: Load Instruments
    # =========================================================================
    print("\n[Step 3] Loading instruments...")

    # Helper to load device - must select track first since browser.load_item
    # loads to the currently selected track
    def load_device(track_idx, device_name):
        view.set_selected_track(track_idx)
        time.sleep(0.1)
        result = track.insert_device(track_idx, device_name)
        time.sleep(0.3)
        return result

    # Keys - try Electric (Rhodes), fall back to Wavetable
    result = load_device(KEYS, "Electric")
    if result < 0:
        result = load_device(KEYS, "Wavetable")
        print(f"  Keys: Wavetable (device index: {result})")
    else:
        print(f"  Keys: Electric (device index: {result})")

    # Bass - Operator for deep sub bass
    result = load_device(BASS, "Operator")
    if result < 0:
        result = load_device(BASS, "Wavetable")
        print(f"  Bass: Wavetable (device index: {result})")
    else:
        print(f"  Bass: Operator (device index: {result})")

    # Melody - Wavetable for soft lead
    result = load_device(MELODY, "Wavetable")
    print(f"  Melody: Wavetable (device index: {result})")

    # Drums - Drum Rack for 808 kit
    result = load_device(DRUMS, "Drum Rack")
    print(f"  Drums: Drum Rack (device index: {result})")

    # =========================================================================
    # Step 4: Create Clips (8 bars = 32 beats)
    # =========================================================================
    print("\n[Step 4] Creating clips (8 bars = 32 beats)...")
    clip_length = 32.0  # 8 bars at 4/4

    for track_idx, name in zip([KEYS, BASS, MELODY, DRUMS], track_names):
        clip_slot.create_clip(track_idx, 0, clip_length)
        time.sleep(0.2)
        print(f"  Created clip on {name}")

    # =========================================================================
    # Step 5: Program Keys (Jazzy 7th Chords)
    # =========================================================================
    print("\n[Step 5] Programming keys (jazzy 7th chords)...")

    # Chord progression: i - VI - III - VII in D minor
    # Dm7 (bars 1-2), Bbmaj7 (bars 3-4), Fmaj7 (bars 5-6), C7 (bars 7-8)
    chord_data = [
        ("D", "min7", 0.0),    # Dm7 at beat 0
        ("Bb", "maj7", 8.0),   # Bbmaj7 at beat 8
        ("F", "maj7", 16.0),   # Fmaj7 at beat 16
        ("C", "dom7", 24.0),   # C7 at beat 24
    ]

    keys_notes = []
    for root, chord_type, start_beat in chord_data:
        # Get chord in octave 3 (warm, not too high)
        chord_tones = chords.get_chord(root, chord_type, 3)
        # Spread for wider voicing
        chord_tones = chords.spread(chord_tones)

        for pitch in chord_tones:
            # Each chord lasts 8 beats (2 bars), velocity 70-80 for warmth
            keys_notes.append(Note(
                pitch=pitch,
                start_time=start_beat,
                duration=7.5,  # Slightly shorter than 8 for breathing room
                velocity=75,
                mute=False
            ))

    clip.add_notes(KEYS, 0, keys_notes)
    print(f"  Added {len(keys_notes)} notes (4 chords with extensions)")

    # =========================================================================
    # Step 6: Program Bass (Root Notes)
    # =========================================================================
    print("\n[Step 6] Programming bass (root movement)...")

    # Bass pattern: root notes with quarter note rhythm and octave jumps
    # D2=38, Bb1=34, F2=41, C2=36
    bass_pattern = [
        # Bars 1-2: D
        (38, 0.0), (38, 1.0), (50, 2.0), (38, 3.0),  # D with octave jump
        (38, 4.0), (38, 5.0), (38, 6.0), (50, 7.0),
        # Bars 3-4: Bb
        (34, 8.0), (34, 9.0), (46, 10.0), (34, 11.0),
        (34, 12.0), (34, 13.0), (34, 14.0), (46, 15.0),
        # Bars 5-6: F
        (41, 16.0), (41, 17.0), (53, 18.0), (41, 19.0),
        (41, 20.0), (41, 21.0), (41, 22.0), (53, 23.0),
        # Bars 7-8: C
        (36, 24.0), (36, 25.0), (48, 26.0), (36, 27.0),
        (36, 28.0), (36, 29.0), (36, 30.0), (48, 31.0),
    ]

    bass_notes = []
    for pitch, start in bass_pattern:
        bass_notes.append(Note(
            pitch=pitch,
            start_time=start,
            duration=0.8,  # Slightly staccato
            velocity=95,
            mute=False
        ))

    clip.add_notes(BASS, 0, bass_notes)
    print(f"  Added {len(bass_notes)} bass notes")

    # =========================================================================
    # Step 7: Program Melody (D Pentatonic Minor)
    # =========================================================================
    print("\n[Step 7] Programming melody (D pentatonic minor)...")

    # D pentatonic minor: D, F, G, A, C
    # Notes: D4=62, F4=65, G4=67, A4=69, C5=72
    # Sparse, melodic phrases with space
    melody_pattern = [
        # Bar 1-2: Opening phrase
        (69, 0.5, 1.0, 70),   # A
        (67, 2.0, 0.5, 65),   # G
        (65, 3.0, 1.5, 75),   # F
        # Bar 3-4: Response
        (72, 9.0, 0.75, 68),  # C
        (69, 10.0, 1.0, 72),  # A
        (67, 12.0, 2.0, 60),  # G (long)
        # Bar 5-6: Development
        (62, 16.5, 0.5, 65),  # D
        (65, 17.5, 0.75, 70), # F
        (67, 19.0, 1.0, 75),  # G
        (69, 21.0, 1.5, 68),  # A
        # Bar 7-8: Resolution
        (72, 24.0, 0.5, 72),  # C
        (69, 25.0, 0.5, 65),  # A
        (67, 26.0, 0.5, 60),  # G
        (65, 27.0, 2.0, 70),  # F (resolve)
        (62, 30.0, 1.5, 55),  # D (tonic, soft)
    ]

    melody_notes = []
    for pitch, start, duration, velocity in melody_pattern:
        melody_notes.append(Note(
            pitch=pitch,
            start_time=start,
            duration=duration,
            velocity=velocity,
            mute=False
        ))

    clip.add_notes(MELODY, 0, melody_notes)
    print(f"  Added {len(melody_notes)} melody notes")

    # =========================================================================
    # Step 8: Program Drums (Boom-Bap)
    # =========================================================================
    print("\n[Step 8] Programming drums (boom-bap pattern)...")

    # Drum mapping (General MIDI / typical Drum Rack):
    # Kick = 36 (C1)
    # Snare = 38 (D1)
    # Closed Hi-hat = 42 (F#1)
    # Open Hi-hat = 46 (A#1)

    KICK = 36
    SNARE = 38
    HIHAT_CLOSED = 42
    HIHAT_OPEN = 46

    drum_notes = []

    # Program 8 bars of drums
    for bar in range(8):
        bar_start = bar * 4.0

        # Kick on beats 1 and 3 (with slight variations)
        drum_notes.append(Note(KICK, bar_start + 0.0, 0.5, 110, False))
        drum_notes.append(Note(KICK, bar_start + 2.0, 0.5, 100, False))
        # Add ghost kick on some bars for groove
        if bar % 2 == 1:
            drum_notes.append(Note(KICK, bar_start + 2.75, 0.25, 70, False))

        # Snare on beats 2 and 4
        drum_notes.append(Note(SNARE, bar_start + 1.0, 0.5, 100, False))
        drum_notes.append(Note(SNARE, bar_start + 3.0, 0.5, 105, False))

        # Hi-hats: 8th notes with velocity swing
        hat_velocities = [100, 55, 75, 55, 90, 55, 75, 55]  # Swing feel
        for i, vel in enumerate(hat_velocities):
            hat_time = bar_start + (i * 0.5)
            # Open hat on the "and" of 4 occasionally
            if i == 7 and bar % 4 == 3:
                drum_notes.append(Note(HIHAT_OPEN, hat_time, 0.4, vel + 10, False))
            else:
                drum_notes.append(Note(HIHAT_CLOSED, hat_time, 0.25, vel, False))

    clip.add_notes(DRUMS, 0, drum_notes)
    print(f"  Added {len(drum_notes)} drum hits")

    # =========================================================================
    # Step 9: Set Mix Levels
    # =========================================================================
    print("\n[Step 9] Setting mix levels...")

    mix_levels = [
        (KEYS, 0.75, "Keys - slightly back"),
        (BASS, 0.80, "Bass - present"),
        (MELODY, 0.65, "Melody - subtle"),
        (DRUMS, 0.85, "Drums - foundation"),
    ]

    for track_idx, volume, desc in mix_levels:
        track.set_volume(track_idx, volume)
        print(f"  {desc}: {int(volume * 100)}%")

    # =========================================================================
    # Step 10: Launch!
    # =========================================================================
    print("\n[Step 10] Launching clips...")
    time.sleep(0.3)

    # Fire all clips in scene 0
    for track_idx in [KEYS, BASS, MELODY, DRUMS]:
        clip.fire(track_idx, 0)
        time.sleep(0.05)

    print("\n" + "=" * 50)
    print("LOFI SONG CREATED!")
    print("=" * 50)
    print(f"Tracks created: {KEYS}-{DRUMS}")
    print("Listen for: jazzy chords, boom-bap drums, melodic phrases")
    print("\nTip: Tweak instrument presets for different vibes!")
    print("     Try: Keys=EP/Rhodes, Bass=Sub, Melody=Pad/Lead")

    osc_client.close()


if __name__ == "__main__":
    create_lofi_song()
