import librosa
import reference_pitch
import recommendation_system


if __name__ == "__main__":
    user_vocal_sound_path = "/home/otischung/Desktop/untitled.wav"
    # Get user's five reference pitches.
    ref = reference_pitch.ref_pitch(user_vocal_sound_path, fmin="C2", fmax="C6")
    print("Your five reference pitches are:")
    print(librosa.midi_to_note(ref))
    print("\n----------------\n")

    # Search for recommendations.
    dic = recommendation_system.recommendation(ref, db="./MusicDay.db")
    print(f"You have {len(dic)} recommendations shown below.")
    print(*dic, sep="\n")
    print("\n----------------\n")

    # Search for recommendations if you set your voice to be one octave higher
    # , which means you can sing the song by set your pitch to be one octave lower.
    dic = recommendation_system.recommendation([x + 12 for x in ref])
    print(f"You have {len(dic)} recommendations shown below if you could sing by one octave lower.")
    print(*dic, sep="\n")
    print("\n----------------\n")

    # Search for recommendations if you set your voice to be one octave lower
    # , which means you can sing the song by set your pitch to be one octave higher.
    dic = recommendation_system.recommendation([x - 12 for x in ref])
    print(f"You have {len(dic)} recommendations shown below if you could sing by one octave higher.")
    print(*dic, sep="\n")
