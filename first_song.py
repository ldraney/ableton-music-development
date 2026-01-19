#!/usr/bin/env python3
"""First Song Experiment - Prove end-to-end song creation with Claude + Ableton.

Run this script with Ableton Live open and AbletonOSC enabled.
"""

import time
import abletonosc_client
from abletonosc_client.clip import Note


def create_tracks(client):
    """Step 1: Create 5 MIDI tracks for our song."""
    song = abletonosc_client.Song(client)
    track = abletonosc_client.Track(client)

    initial_tracks = song.get_num_tracks()
    print(f"Current track count: {initial_tracks}")

    # Track names for our song
    track_names = ["Drums", "Bass", "Lead", "Chords", "Accent"]

    print("\nCreating 5 MIDI tracks...")
    for i, name in enumerate(track_names):
        song.create_midi_track(i)
        time.sleep(0.1)  # Small delay for Ableton to process

    # Name the tracks
    print("Naming tracks...")
    for i, name in enumerate(track_names):
        track.set_name(i, name)
        time.sleep(0.05)

    # Verify
    print("\nCreated tracks:")
    for i in range(5):
        print(f"  Track {i}: {track.get_name(i)}")

    return track_names


def compose_song(client):
    """Step 3: Compose a simple 8-bar loop on all tracks."""
    clip_slot = abletonosc_client.ClipSlot(client)
    clip = abletonosc_client.Clip(client)
    song = abletonosc_client.Song(client)
    scene = abletonosc_client.Scene(client)

    # Set tempo
    song.set_tempo(120.0)
    print(f"Set tempo to {song.get_tempo()} BPM")

    # Create 8-bar clips (32 beats at 4/4) on scene 0
    clip_length = 32.0  # 8 bars

    print("\nCreating clips...")
    for track_idx in range(5):
        clip_slot.create_clip(track_idx, 0, clip_length)
        time.sleep(0.1)

    # Name the clips
    clip_names = ["Drum Loop", "Bass Line", "Melody", "Pad Chords", "Accents"]
    for i, name in enumerate(clip_names):
        clip.set_name(i, 0, name)

    # Name the scene
    scene.set_name(0, "Main Loop")

    print("Composing notes...")

    # ===== DRUMS (Track 0) =====
    # Standard kick/snare/hihat pattern
    # Kick: C1 (36), Snare: D1 (38), Hi-hat: F#1 (42)
    drum_notes = []
    for bar in range(8):
        bar_start = bar * 4
        # Kick on 1 and 3
        drum_notes.append(Note(36, bar_start + 0.0, 0.5, 100))
        drum_notes.append(Note(36, bar_start + 2.0, 0.5, 100))
        # Snare on 2 and 4
        drum_notes.append(Note(38, bar_start + 1.0, 0.5, 100))
        drum_notes.append(Note(38, bar_start + 3.0, 0.5, 100))
        # Hi-hats on every 8th note
        for eighth in range(8):
            vel = 80 if eighth % 2 == 0 else 60
            drum_notes.append(Note(42, bar_start + eighth * 0.5, 0.25, vel))

    clip.add_notes(0, 0, drum_notes)
    print(f"  Drums: {len(drum_notes)} notes")

    # ===== BASS (Track 1) =====
    # Simple chord root pattern following Am - F - C - G progression
    # Each chord gets 2 bars
    bass_pattern = [
        (45, 0),   # A2 for bars 1-2
        (41, 8),   # F2 for bars 3-4
        (48, 16),  # C3 for bars 5-6
        (43, 24),  # G2 for bars 7-8
    ]
    bass_notes = []
    for root_pitch, start_bar in bass_pattern:
        # Bass plays on beats 1, 2.5, 4 in each bar
        for bar_offset in range(2):  # 2 bars per chord
            bar_start = start_bar + bar_offset * 4
            bass_notes.append(Note(root_pitch, bar_start + 0.0, 0.75, 100))
            bass_notes.append(Note(root_pitch, bar_start + 1.5, 0.5, 90))
            bass_notes.append(Note(root_pitch, bar_start + 2.5, 0.75, 95))

    clip.add_notes(1, 0, bass_notes)
    print(f"  Bass: {len(bass_notes)} notes")

    # ===== LEAD (Track 2) =====
    # Simple melody over the progression
    # Am pentatonic: A C D E G
    melody_notes = []
    # Bar 1-2: A minor feel
    melody_notes.extend([
        Note(69, 0.0, 1.0, 90),   # A4
        Note(72, 1.0, 0.5, 85),   # C5
        Note(74, 1.5, 1.5, 90),   # D5
        Note(72, 4.0, 2.0, 85),   # C5
        Note(69, 6.0, 2.0, 80),   # A4
    ])
    # Bar 3-4: F major feel
    melody_notes.extend([
        Note(77, 8.0, 1.0, 90),   # F5 (from F chord)
        Note(76, 9.0, 0.5, 85),   # E5
        Note(74, 9.5, 1.5, 90),   # D5
        Note(72, 12.0, 2.0, 85),  # C5
        Note(69, 14.0, 2.0, 80),  # A4
    ])
    # Bar 5-6: C major feel
    melody_notes.extend([
        Note(72, 16.0, 1.0, 95),  # C5
        Note(76, 17.0, 1.0, 90),  # E5
        Note(79, 18.0, 2.0, 95),  # G5
        Note(76, 20.0, 1.0, 85),  # E5
        Note(74, 21.0, 1.0, 80),  # D5
        Note(72, 22.0, 2.0, 85),  # C5
    ])
    # Bar 7-8: G major feel, building back to A
    melody_notes.extend([
        Note(79, 24.0, 1.0, 95),  # G5
        Note(76, 25.0, 0.5, 90),  # E5
        Note(74, 25.5, 1.5, 90),  # D5
        Note(71, 28.0, 1.0, 85),  # B4 (leading tone)
        Note(72, 29.0, 1.0, 90),  # C5
        Note(69, 30.0, 2.0, 95),  # A4 (resolve)
    ])

    clip.add_notes(2, 0, melody_notes)
    print(f"  Lead: {len(melody_notes)} notes")

    # ===== CHORDS/PAD (Track 3) =====
    # Sustained chords: Am - F - C - G
    chord_notes = []
    chords = [
        ([57, 60, 64, 69], 0),    # Am: A3, C4, E4, A4 - bars 1-2
        ([53, 57, 60, 65], 8),    # F: F3, A3, C4, F4 - bars 3-4
        ([48, 55, 60, 64], 16),   # C: C3, G3, C4, E4 - bars 5-6
        ([55, 59, 62, 67], 24),   # G: G3, B3, D4, G4 - bars 7-8
    ]
    for pitches, start_beat in chords:
        for pitch in pitches:
            chord_notes.append(Note(pitch, start_beat, 7.5, 70))

    clip.add_notes(3, 0, chord_notes)
    print(f"  Chords: {len(chord_notes)} notes")

    # ===== ACCENT (Track 4) =====
    # Sparse accent hits for interest
    accent_notes = []
    # Add accents at key moments
    accent_hits = [
        (72, 7.5, 0.5, 100),   # End of bar 2 - transition marker
        (74, 15.5, 0.5, 100),  # End of bar 4
        (76, 23.5, 0.5, 100),  # End of bar 6
        (79, 31.0, 1.0, 110),  # Downbeat before loop
    ]
    for pitch, start, dur, vel in accent_hits:
        accent_notes.append(Note(pitch, start, dur, vel))

    clip.add_notes(4, 0, accent_notes)
    print(f"  Accent: {len(accent_notes)} notes")

    total_notes = len(drum_notes) + len(bass_notes) + len(melody_notes) + len(chord_notes) + len(accent_notes)
    print(f"\nTotal notes composed: {total_notes}")

    return True


def play_song(client):
    """Step 4: Fire the scene and start playback."""
    scene = abletonosc_client.Scene(client)
    song = abletonosc_client.Song(client)

    print("\nFiring scene 0 (Main Loop)...")
    scene.fire(0)

    # Start playback if not already playing
    if not song.get_is_playing():
        song.start_playing()

    print("Playing! Listen to your creation in Ableton.")
    print("Press Ctrl+C to stop, or let it loop.")


def stop_song(client):
    """Stop playback."""
    song = abletonosc_client.Song(client)
    song.stop_playing()
    print("Playback stopped.")


def main():
    print("=" * 60)
    print("FIRST SONG EXPERIMENT")
    print("Prove end-to-end song creation: Claude + Ableton")
    print("=" * 60)

    # Connect to Ableton
    print("\nConnecting to Ableton Live...")
    client = abletonosc_client.connect()
    song = abletonosc_client.Song(client)

    try:
        tempo = song.get_tempo()
        print(f"Connected! Current tempo: {tempo} BPM")
    except Exception as e:
        print(f"ERROR: Could not connect to Ableton. Is AbletonOSC running?")
        print(f"Error: {e}")
        return

    # Interactive steps
    while True:
        print("\n" + "-" * 40)
        print("What would you like to do?")
        print("  1. Create 5 MIDI tracks (Drums, Bass, Lead, Chords, Accent)")
        print("  2. Compose the song (after you add instruments)")
        print("  3. Play the song")
        print("  4. Stop playback")
        print("  5. Exit")
        print("-" * 40)

        choice = input("Enter choice (1-5): ").strip()

        if choice == "1":
            create_tracks(client)
            print("\n>>> NOW: Drag instruments onto each track in Ableton!")
            print("    - Track 0 (Drums): Drum Rack or 808")
            print("    - Track 1 (Bass): Bass synth (e.g., Wavetable)")
            print("    - Track 2 (Lead): Lead synth")
            print("    - Track 3 (Chords): Pad/keys")
            print("    - Track 4 (Accent): Any percussive/accent sound")
            print(">>> Press Enter when ready to compose...")

        elif choice == "2":
            compose_song(client)
            print("\n>>> Song composed! Ready to play.")

        elif choice == "3":
            play_song(client)

        elif choice == "4":
            stop_song(client)

        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1-5.")


if __name__ == "__main__":
    main()
