"""
Provides some librosa functions
"""
import sys

import librosa
import numpy as np


def ref_pitch(src: str) -> list:
    y0, sr = librosa.load(src)
    n_fft = 2048
    S = librosa.stft(y0, n_fft=n_fft, hop_length=n_fft // 2)
    D = librosa.amplitude_to_db(np.abs(S), ref=np.max)
    np.max(abs(D))

    nonMuteSections = librosa.effects.split(y0, top_db=20)
    y = []

    for sliced in nonMuteSections:
        y.extend(y0[sliced[0]:sliced[1]])

    y = np.array(y)

    # This will take few times.
    f0, voiced_flag, voiced_probabilities = librosa.pyin(
        y, frame_length=2048, fmin=librosa.note_to_hz('G2'), fmax=librosa.note_to_hz('C6'))  # 110~1046Hz

    appear = []
    midi_note = np.around(librosa.hz_to_midi(f0))
    i = len(midi_note) - 1

    while i >= 0:
        if midi_note[i] != 'nan':
            is_a_note = True
            for t in range(3):
                if midi_note[i - t - 1] != midi_note[i]:
                    is_a_note = False
                    break
            if is_a_note:
                appear.append(midi_note[i])
                i -= 5
            else:
                i -= 1

    if len(appear) == 0:
        print(f"Error, the music {src} has zero note.", file=sys.stderr)
        return [0, 0, 0, 0, 0]

    # This will take few times.
    appear.sort()

    # 5 index
    # print("average", librosa.midi_to_note(appear[(int)(len(appear) / 2)]))
    # print("average high", librosa.midi_to_note(appear[(int)(3 * len(appear) / 4)]))
    # print("average low", librosa.midi_to_note(appear[(int)(len(appear) / 4)]))
    # print("low", librosa.midi_to_note(appear[(int)(len(appear) / 100)]))
    # print("high", librosa.midi_to_note(appear[(int)(98 * len(appear) / 100)]))
    low = int(appear[int(len(appear) / 100)])
    avg_low = int(appear[int(len(appear) / 4)])
    avg = int(appear[int(len(appear) / 2)])
    avg_high = int(appear[int(3 * len(appear) / 4)])
    high = int(appear[int(98 * len(appear) / 100)])
    return [low, avg_low, avg, avg_high, high]
