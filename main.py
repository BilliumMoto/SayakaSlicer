from argparse import ArgumentParser
from pathlib import Path

from slicing import do_slice


def main(args=None):
    parser = ArgumentParser(description="Sayaka's slicer for mid2bms using midi info for precise slicing")
    parser.add_argument("-f", "--folder", type=str, help="Folder for slicing")
    parser.add_argument("-w", "--wave", type=str, help="Name of wav file")
    parser.add_argument("-b", "--bpm", type=int,
                        help="BPM of export, will read from text6_bms_blue.txt if not provided")
    opts = parser.parse_args(args=args)

    base_path = Path(opts.folder)
    wav_path = base_path / opts.wave
    midi_path = base_path / "text3_tanon_smf_blue.mid"
    renamer_path = base_path / "text5_renamer_array.txt"
    create_path = base_path / "out"
    bpm = opts.bpm
    if not bpm:
        # Try reading from the bms file created by mid2bms
        temp_bms_path = base_path / "text6_bms_blue.txt"
        with open(temp_bms_path, "r") as f:
            while line := f.readline():
                if "#BPM" in line:
                    bpm = float(line.strip()[5:])
                    break

    do_slice(create_path, wav_path, midi_path, renamer_path, bpm)


if __name__ == '__main__':
    main()
