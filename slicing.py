from os import makedirs

from mido import MidiFile
from pydub import AudioSegment


def do_slice(create_path, wav_path, midi_path, renamer_file, bpm: float):
    makedirs(create_path, exist_ok=True)
    wav = AudioSegment.from_wav(wav_path)
    mid = MidiFile(midi_path)
    renamer_file = open(renamer_file, "r")
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
                    elif msg.time == 0:
                        # This note is a chord with another note in mid2bms chord mode, can simply ignore
                        pass
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
                        wavslice.export(create_path / line, format="wav")
                    prevtime = curtime

    if renamer_file.readline()[:-1] == "//":
        print("All wav files defined in renamer file have been sliced!")
    else:
        print("Not all wav files in renamer file have been sliced, please check output")

    renamer_file.close()