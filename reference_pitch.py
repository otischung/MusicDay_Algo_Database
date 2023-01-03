"""
Provides some librosa functions
"""
import sys

import librosa
import numpy as np


def ref_pitch(src: str, fmin: int | str = "G2", fmax: int | str = "C6") -> list:
    """
    Get the five reference pitch of given source audio file.

    You can specify the minimum and maximum frequencies by MIDI integer value
    or note name string, e.g. "C#3", "Ab4".

    Parameters
    ----------
    src: str
        Input audio file path.

    fmin: int|str
        The minimum frequency. The default value is G2 (43)

    fmax: int|str
        The maximum frequency. The default value is C6 (84)

    Returns
    -------
    out: list
        The list containing five reference pitch. The order is [low, avg. low, avg., avg high, high].

    Raises
    ------
    FileNotFoundError
        If the given source audio file doesn't exist.

    ParameterError
        If the input frequencies are not in valid note format
    """
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

    if type(fmin) == str:
        fmin = librosa.note_to_midi(fmin)
    if type(fmax) == str:
        fmax = librosa.note_to_midi(fmax)
    # This will take few times.
    f0, voiced_flag, voiced_probabilities = librosa.pyin(
        y, frame_length=2048,
        fmin=librosa.midi_to_hz(fmin), fmax=librosa.midi_to_hz(fmax))

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
    # high = int(appear[int(len(appear) - 2)])
    # print(int(appear[int(98 * len(appear) / 100)]))
    return [low, avg_low, avg, avg_high, high]
