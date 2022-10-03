from mido import MidiFile, bpm2tempo, tick2second
from pydub import AudioSegment
from os import makedirs


def sayaka_original_procedure():
    bpm = int(input("BPM? (120) ") or "120")
    midfile = input("MIDI file? (text3_tanon_smf_blue.mid) ") or "text3_tanon_smf_blue.mid"
    wavfile = input("WAV file? (untitled.wav) ") or "untitled.wav"
    renamerfile = input("Renamer file? (text5_renamer_array.txt) ") or "text5_renamer_array.txt"

    makedirs("out", exist_ok=True)
    wav = AudioSegment.from_wav(wavfile)
    mid = MidiFile(midfile)
    renamer_file = open(renamerfile, "r")
    next(renamer_file)
    next(renamer_file)
    next(renamer_file)

    for i, track in enumerate(mid.tracks):
        print('Track {}: {}'.format(i, track.name))
        prevtime = curtime = 0
        first = True
        for msg in track:
            print(msg)
            if msg.type == 'note_on' or msg.type == 'note_off' or msg.type == 'end_of_track' and not first:
                curtime += msg.time / mid.ticks_per_beat / bpm * 60 * 1000
                if msg.type == 'end_of_track' or msg.velocity > 0:
                    if first:
                        first = False
                    else:
                        # keysound processing here
                        print(f'{prevtime} => {curtime}')
                        line = renamer_file.readline()[:-1]
                        if line == "//":
                            next(renamer_file)
                            if line == "\n":
                                continue
                            next(renamer_file)
                            next(renamer_file)
                            line = renamer_file.readline()[:-1]
                        wavslice = wav[int(prevtime):int(curtime)]
                        wavslice.export(f'out/{line}', format="wav")
                    prevtime = curtime

    if renamer_file.readline()[:-1] == "//":
        print("All wav files defined in renamer file have been sliced!")
    else:
        print("Not all wav files in renamer file have been sliced, please check output")

    renamer_file.close()
