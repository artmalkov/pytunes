import os
from PIL import Image
import pytunes.musicbasics as musicbasics

INSTRUMENT_WIDTH = 300

FLUTE_IMAGE = "flute.png"
FLUTE_FINGERING_FILES = [
    ["flute1_1.png", "flute1_07.png"],
    ["flute2_1.png"],
    ["flute3_1.png", "flute3_05.png"],
    ["flute4_1.png"],
    ["flute5_1.png"],
    ["flute6_1.png"],
    ["flute7_1.png", "flute7_05.png"],
    ["flute8_1.png", "flute8_05.png"]
]
FLUTE_FINGERPRINTS = ".@%"
FLUTE_FINGERING = [
    "C   @ @ @ @ @ @ @ @",
    "C#  @ @ @ @ @ @ @ %",
    "D   @ @ @ @ @ @ @ .",
    "D#  @ @ @ @ @ @ % .",
    "E   @ @ @ @ @ @ . .",
    "F   @ @ @ @ @ . . .",
    "F#  @ @ @ @ . @ @ @",
    "G   @ @ @ @ . . . .",
    "G#  @ @ @ . @ @ % .",
    "A   @ @ @ . . . . .",
    "A#  @ @ . @ @ . . .",
    "B   @ @ . . . . . .",

    "c   @ . @ . . . . .",
    "c#  . @ @ . . . . .",
    "d   . . @ . . . . .",
    "d#  . . @ @ @ @ @ .",
    "e   % @ @ @ @ @ . .",
    "f   % @ @ @ @ . . .",
    "f#  % @ @ @ . @ . @",
    "g   % @ @ @ . . . .",
    "g#  % @ @ @ . @ @ @",
    "a   % @ @ . . . . .",
    "a#  % @ @ . @ @ @ .",
    "b   % @ @ . @ @ . .",
    "cc  % @ . . @ @ . .",
    "cc# % @ % @ @ . @ @",
    "dd  % @ . @ @ . @ %"
]

# Clarinet
CLARINET_IMAGE = "clarinet.png"
CLARINET_FINGERING_FILES = [
    "clarinet1.png",
    "clarinet2.png",
    "clarinet3.png",
    "clarinet4.png",
    "clarinet5.png",
    "clarinet6.png",
    "clarinet7.png",

    # left thumb
    "clarinet_12.png",

    # left index finger
    "clarinet_10.png",
    "clarinet_9.png",

    # left middle finger
    "clarinet_7bis.png",

    # left ring finger
    "clarinet_6.png",

    # left litte finger
    "clarinet_c.png",
    "clarinet_2.png",
    "clarinet_1.png",

    # right hand
    "clarinet_11.png",
    "clarinet_10bis.png",
    "clarinet_8.png",
    "clarinet_7.png",

    # right middle finger
    "clarinet_5.png",

    # right little finger
    "clarinet_4.png",
    "clarinet_3.png",
    "clarinet_b.png",
    "clarinet_a.png"
]
CLARINET_FINGERPRINTS = ".@"
CLARINET_FINGERING = [

    #    A B C D E F G  12 10 9 7bis 6  c 2 1   11 10bis 8 7 5  4 3 b a
    "EE  @ @ @ @ @ @ @  .   . .  .   .  . . @     . . . .    .  . . . .",
    "EE  @ @ @ @ @ @ @  .   . .  .   .  . . .     . . . .    .  . . . @",

    "FF  @ @ @ @ @ @ @  .   . .  .   .  . . .     . . . .    .  . @ . .",
    "FF  @ @ @ @ @ @ @  .   . .  .   .  @ . .     . . . .    .  . . . .",

    "FF# @ @ @ @ @ @ @  .   . .  .   .  . @ .     . . . .    .  . . . .",
    "FF# @ @ @ @ @ @ @  .   . .  .   .  . . .     . . . .    .  . . @ .",

    "GG  @ @ @ @ @ @ @  .   . .  .   .  . . .     . . . .    .  . . . .",

    "GG# @ @ @ @ @ @ @  .   . .  .   .  . . .     . . . .    .  @ . . .",

    "AA  @ @ @ @ @ @ .  .   . .  .   .  . . .     . . . .    .  . . . .",

    "AA# @ @ @ @ @ . .  .   . .  .   .  . . .     . . . .    .  . . . .",

    "BB  @ @ @ @ . @ .  .   . .  .   .  . . .     . . . .    .  . . . .",
    "BB  @ @ @ @ . . @  .   . .  .   .  . . .     . . . .    .  . . . .",
    "BB  @ @ @ @ @ . .  .   . .  .   .  . . .     . . . .    @  . . . .",

    #    1 2 3 4 5 6 7  12 10 9 7bis 6  C 2 1  11 10bis 8 7  5  4 3 b a

    "C   @ @ @ @ . . .  .   . .  .   .  . . .     . . . .    .  . . . .",

    "C#  @ @ @ @ . . .  .   . .  .   @  . . .     . . . .    .  . . . .",

    "D   @ @ @ . . . .  .   . .  .   .  . . .     . . . .    .  . . . .",

    "D#  @ @ . . @ . .  .   . .  .   .  . . .     . . . .    .  . . . .",
    "D#  @ @ . . . @ .  .   . .  .   .  . . .     . . . .    .  . . . .",
    "D#  @ @ . . . . @  .   . .  .   .  . . .     . . . .    .  . . . .",
    "D#  @ @ @ . . . .  .   . .  .   .  . . .     . . . @    .  . . . .",
    "D#  @ @ @ . . . .  .   . .  @   .  . . .     . . . .    .  . . . .",

    "E   @ @ . . . . .  .   . .  .   .  . . .     . . . .    .  . . . .",

    "F   @ . . . . . .  .   . .  .   .  . . .     . . . .    .  . . . .",

    "F#  @ . . . . . .  .   . .  .   .  . . .     . . @ @    .  . . . .",
    "F#  . @ . . . . .  .   . .  .   .  . . .     . . . .    .  . . . .",

    #    1 2 3 4 5 6 7  12 10 9 7bis 6  C 2 1  11 10bis 8 7  5  4 3 b a

    "G   . . . . . . .  .   . .  .   .  . . .     . . . .    .  . . . .",

    "G#  . . . . . . .  .   . @  .   .  . . .     . . . .    .  . . . .",

    "A   . . . . . . .  .   @ .  .   .  . . .     . . . .    .  . . . .",
    "A   . . . . . . .  .   . .  .   .  . . .     . @ . .    .  . . . .",

    "A#  . . . . . . .  @   @ .  .   .  . . .     . . . .    .  . . . .",
    "A#  . . . . . . .  .   @ .  .   .  . . .     . @ . .    .  . . . .",

    "B   @ @ @ @ @ @ @  @   . .  .   .  . . @     . . . .    .  . . . .",
    "B   @ @ @ @ @ @ @  @   . .  .   .  . . .     . . . .    .  . . . @",

    "c   @ @ @ @ @ @ @  @   . .  .   .  . . .     . . . .    .  . @ . .",
    "c   @ @ @ @ @ @ @  @   . .  .   .  @ . .     . . . .    .  . . . .",

    #    1 2 3 4 5 6 7  12 10 9 7bis 6  C 2 1  11 10bis 8 7  5  4 3 b a

    "c#  @ @ @ @ @ @ @  @   . .  .   .  . @ .     . . . .    .  . . . .",
    "c#  @ @ @ @ @ @ @  @   . .  .   .  . . .     . . . .    .  . . @ .",

    "d   @ @ @ @ @ @ @  @   . .  .   .  . . .     . . . .    .  . . . .",

    "d#  @ @ @ @ @ @ @  @   . .  .   .  . . .     . . . .    .  . . . .",

    "e   @ @ @ @ @ @ .  @   . .  .   .  . . .     . . . .    .  . . . .",

    "f   @ @ @ @ @ . .  @   . .  .   .  . . .     . . . .    .  . . . .",

    "f#  @ @ @ @ . @ .  @   . .  .   .  . . .     . . . .    .  . . . .",
    "f#  @ @ @ @ . . @  @   . .  .   .  . . .     . . . .    .  . . . .",
    "f#  @ @ @ @ @ . .  @   . .  .   .  . . .     . . . .    @  . . . .",

    #    1 2 3 4 5 6 7  12 10 9 7bis 6  C 2 1  11 10bis 8 7  5  4 3 b a

    "g   @ @ @ @ . . .  @   . .  .   .  . . .     . . . .    .  . . . .",

    "g#  @ @ @ @ . . .  @   . .  .   @  . . .     . . . .    .  . . . .",
    "g#  @ @ @ . @ @ .  @   . .  .   .  . . .     . . . .    .  . . . .",

    "a   @ @ @ @ @ @ .  @   . .  .   .  . . .     . . . .    .  . . . .",  # unclear
    "a   @ @ @ @ @ @ .  @   . .  .   .  . . .     . . . .    .  . . . .",  # unclear

    "a#  @ @ @ @ @ @ .  @   . .  .   .  . . .     . . . .    .  . . . .",  # unclear
    "a#  @ @ @ @ @ @ .  @   . .  .   .  . . .     . . . .    .  . . . .",  # unclear
    "a#  @ @ @ . . . .  @   . .  .   .  . . .     . . . @    .  . . . .",  # unclear
    "a#  @ @ @ . . . .  @   . .  @   .  . . .     . . . .    .  . . . .",
    "a#  @ @ . @ @ @ @  @   . .  .   .  . . .     . . . .    .  . . . .",

    "b   @ @ . . . . .  @   . .  .   .  . . .     . . . .    .  . . . .",

    #    1 2 3 4 5 6 7  12 10 9 7bis 6  C 2 1  11 10bis 8 7  5  4 3 b a

    "cc  @ . . . . . .  @   . .  .   .  . . .     . . . .    .  . . . .",

    "cc# @ . @ @ @ @ .  @   . .  .   .  . . .     . . . .    .  . . . .",
    "cc# @ . . . . . .  @   . .  .   .  . . .     . . @ @    .  . . . .",
    "cc# @ . @ . . . .  @   . .  .   .  . . .     . . . .    .  . . . .",

    "dd  @ . @ @ @ . .  @   . .  .   .  . . .     . . . .    .  . . . .",
    "dd  @ . . . . . .  @   . @  .   .  . . .     . . . .    .  . . . .",
    "dd  . . . . . . .  @   . .  .   .  . . .     . . . .    .  . . . .",

    "dd# @ . @ @ @ . .  @   . .  .   .  . . .     . . . .    @  . . . .",
    "dd# @ . @ @ . @ .  @   . .  .   .  . . .     . . . .    .  @ . . .",
    "dd# @ . @ @ . . @  @   . .  .   .  . . .     . . . .    .  @ . . .",
    "dd# . . . . . . .  @   . @  .   .  . . .     . . . .    .  . . . .",

    #    1 2 3 4 5 6 7  12 10 9 7bis 6  C 2 1  11 10bis 8 7  5  4 3 b a

    "ee  @ . @ @ . . .  @   . .  .   .  . . .     . . . .    .  . . . .",
    "ee  . . . . . . .  @   @ .  .   .  . . .     . . . .    .  . . . .",

    "ff  @ . @ @ . . .  @   . .  .   @  . . .     . . . .    .  . . . .",
    "ff  @ @ @ @ @ @ @  @   . .  .   @  . . .     . . . .    .  . . . .",
    "ff  @ . @ @ . . .  @   . .  .   .  . . .     @ . . .    .  . . . .",
    "ff  @ @ @ @ . . .  @   . .  @   .  . . .     . . . .    .  . . . .",

    "ff# @ . @ . . . .  @   . .  .   .  . . .     . . . .    .  . . . .",
    "ff# @ @ @ . @ @ @  @   . .  .   .  . . .     . . . .    .  @ . . .",

    "gg  @ @ . . @ @ .  @   . .  .   .  . . .     . . . .    .  . @ . .",
    "gg  @ . @ . @ @ .  @   . .  .   .  . . .     . . . .    .  . @ . .",
    "gg  @ @ . . @ . .  @   . .  .   .  . . .     . . . .    .  @ . . .",
    "gg  @ @ @ @ @ @ @  @   . .  .   .  . . .     . . . .    .  . . @ .",
    "gg  @ @ . . @ . .  @   . .  .   .  . . .     . . . .    .  . . . .",

    #    1 2 3 4 5 6 7  12 10 9 7bis 6  C 2 1  11 10bis 8 7  5  4 3 b a

    "gg# @ . @ . @ . .  @   . .  .   .  . . .     . . . .    .  . . @ .",
    "gg# @ . @ @ @ . .  @   . .  .   .  . . .     . . . .    .  . @ . .",
    "gg# @ . @ @ @ @ @  @   . .  .   .  . @ .     . . . .    .  . . . .",
    "gg# @ . @ @ @ @ @  @   . .  .   .  . . .     . . . .    .  . . @ .",

    "aa  @ . @ @ . . .  @   . .  .   .  . . .     . . . .    .  . . . .",
    "aa  @ . @ @ . . .  @   . .  .   .  @ . .     . . . .    .  . . . .",
    "aa  @ . @ @ . . .  @   . .  .   .  . . .     . . . .    .  . . @ .",

    "aa# @ . @ @ @ @ @  @   . .  .   @  . . .     . . . .    .  . @ . .",
    "aa# . @ @ @ @ @ @  @   . .  .   .  . . .     . . . .    .  . @ . .",
    "aa# . @ @ @ . . .  @   . @  .   @  . . .     . . . .    .  . . . .",
    "aa# . . @ @ . . .  @   . .  .   .  . . .     . . @ @    .  . . . .",
    "aa# @ . @ @ . . .  @   . @  .   @  . . .     . . . .    .  @ . . .",

    #    1 2 3 4 5 6 7  12 10 9 7bis 6  C 2 1  11 10bis 8 7  5  4 3 b a

    "bb  @ . @ . @ @ .  @   . .  .   .  . @ .     . . . .    .  . . . .",
    "bb  @ . @ . @ @ .  @   . .  .   .  . . .     . . . .    .  . . @ .",
    "bb  @ @ @ . @ @ .  @   . .  .   .  . @ .     . . . .    .  . . . .",
    "bb  @ @ @ . @ @ .  @   . .  .   .  . . .     . . . .    .  . . @ .",
    "bb  @ @ @ . @ @ .  @   . @  .   .  . . .     . . . .    .  @ . . .",

    "ccc @ @ . . @ . .  @   . .  @   .  . . .     . . . .    @  @ . . .",
    "ccc @ @ . . @ . .  @   . .  .   @  . . .     . . . .    .  @ . . .",
    "ccc @ @ . . @ @ .  @   . .  .   .  . . .     . . . .    .  @ . . .",
    "ccc @ @ . . @ . .  @   . .  .   .  . @ .     . . . .    .  . . . .",
    "ccc @ @ . . @ . .  @   . .  .   .  . . .     . . . .    .  . . @ .",
    "ccc @ . . . @ @ .  @   @ .  .   .  . . .     . . . .    .  @ . . ."
]


class Instrument:
    def __init__(self, transpose_to_C_from="C"):
        self.name = ""
        self._transpose_to_C_from = transpose_to_C_from
        self._transposition = 0
        self._images = {}
        self._fingers = {}

    def _load_and_store(self, file, key):
        img = Image.open(os.path.join(musicbasics.IMAGE_FOLDER, file))
        self._images[key] = img

    def load_images(self, instrument_image_file, fingering_files, fingering_data, fingerprints=".@"):
        # read files and put into images
        self._load_and_store(instrument_image_file, self.name)

        for i in range(len(fingering_files)):
            key = self.name + str(i) + "_"
            row = fingering_files[i]
            if type(row) is str:
                self._load_and_store(row, key + fingerprints[1])
            elif type(row) == list:
                for j in range(0, len(row)):
                    file = row[j]
                    self._load_and_store(file, key + fingerprints[j + 1])

        # remember fingering data
        key = self.name
        for fingers in fingering_data:
            s = fingers.split(" ")
            while s.count('') > 0:
                s.remove('')

            tone = musicbasics.tone_from_string(s[0])
            if tone is not None:
                fingerlist = []
                for i in range(1, len(s)):
                    if s[i] != "0" and s[i] != ".":
                        fingerlist.append(key + str(i - 1) + "_" + s[i])

                if not (tone in self._fingers):
                    self._fingers[tone] = []

                self._fingers[tone].append(fingerlist)

    def transpose_to_C_from(self, real_instrument_note="C"):
        self._transpose_to_C_from = real_instrument_note

        instrument_tone = musicbasics.tone_from_string(real_instrument_note, base_tone="")
        c = musicbasics.tone_from_string("C", base_tone="")

        self._transposition = instrument_tone - c

    def _package_image(self, base_image, finger_images):
        for finger in finger_images:
            base_image.paste(finger, (0, 0), finger)
        return base_image

    def image(self, tone, give_a_list_if_many=False):
        key = self.name
        tone += self._transposition

        if tone in self._fingers:
            fingers = self._fingers[tone]
            if give_a_list_if_many:
                output_list = []
                for finger_options in fingers:
                    img = self._images[key].copy()
                    finger_images = [self._images[finger_key] for finger_key in finger_options]
                    output_list.append(self._package_image(img, finger_images))
                return output_list
            else:
                img = self._images[key].copy()
                finger_images = [self._images[finger_key] for finger_key in fingers[0]]
                output = self._package_image(img, finger_images)
                return self._package_image(img, finger_images)
        else:
            # tone is not possible to play, showing empty instrument
            img = self._images[key].copy()
            if give_a_list_if_many:
                return [img]
            else:
                return img


class Flute(Instrument):
    def __init__(self):
        super().__init__()
        self.name = "Flute"
        self.load_images(FLUTE_IMAGE, FLUTE_FINGERING_FILES, FLUTE_FINGERING, FLUTE_FINGERPRINTS)


class Clarinet(Instrument):
    def __init__(self):
        super().__init__()
        self.name = "Clarinet"
        self.transpose_to_C_from("FF")
        self.load_images(CLARINET_IMAGE, CLARINET_FINGERING_FILES, CLARINET_FINGERING, CLARINET_FINGERPRINTS)