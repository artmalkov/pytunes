import re
from PIL import Image
import os
import enum



IMAGE_FOLDER = "images"

aa="(3dedb2 (3c=dca2   |  (3BcBg2 Aeae' | dgbd' g'b'e''d'' | "
bb=" G,,4^D,4 & G,,2[D,2B,2] ^D,2[F,2C2] | E,4C,4 & E,2[G,2B,2] C,2[A,2E2] | "



#            "CCCCC CCCCC# DDDDD DDDDD# EEEEE FFFFF FFFFF# GGGGG GGGGG# AAAAA AAAAA# BBBBB " \
#            "CCCC CCCC# DDDD DDDD# EEEE FFFF FFFF# GGGG GGGG# AAAA AAAA# BBBB " \
OCTAVE = 7
OCTAVE_TONES = 12
ALL_TONES = "" \
            "CCC CCC# DDD DDD# EEE FFF FFF# GGG GGG# AAA AAA# BBB " \
            "CC CC# DD DD# EE FF FF# GG GG# AA AA# BB " \
            "C C# D D# E F F# G G# A A# B " \
            "c c# d d# e f f# g g# a a# b " \
            "cc cc# dd dd# ee ff ff# gg gg# aa aa# bb " \
            "ccc ccc# ddd ddd# eee fff fff# ggg ggg# aaa aaa# bbb"
#            "cccc cccc# dddd dddd# eeee ffff ffff# gggg gggg# aaaa aaaa# bbbb " \
#            "ccccc ccccc# ddddd ddddd# eeeee fffff fffff# ggggg ggggg# aaaaa aaaaa# bbbbb"

ABC_TONES = "C,,,, ˆC,,,, D,,,, ˆD,,,, E,,,, F,,,, ˆF,,,, G,,,, ˆG,,,, A,,,, ˆA,,,, B,,,, " \
            "C,,, ˆC,,, D,,, ˆD,,, E,,, F,,, ˆF,,, G,,, ˆG,,, A,,, ˆA,,, B,,, " \
            "C,, ˆC,, D,, ˆD,, E,, F,, ˆF,, G,, ˆG,, A,, ˆA,, B,, " \
            "C, ˆC, D, ˆD, E, F, ˆF, G, ˆG, A, ˆA, B, " \
            "C ˆC D ˆD E F ˆF G ˆG A ˆA B " \
            "c ˆc d ˆd e f ˆf g ˆg a ˆa b " \
            "c' ˆc' d' ˆd' e' f' ˆf' g' ˆg' a' ˆa' b' " \
            "c'' ˆc'' d'' ˆd'' e'' f'' ˆf'' g'' ˆg'' a'' ˆa'' b''" \
            "c''' ˆc''' d''' ˆd''' e''' f''' ˆf''' g''' ˆg''' a''' ˆa''' b'''" \
            "c'''' ˆc'''' d'''' ˆd'''' e'''' f'''' ˆf'''' g'''' ˆg'''' a'''' ˆa'''' b''''"

BASE_TONE = "C"  # C4

# TONES_IN_OCTAVE = [
#     # pitch, hal line on staff
#     ["C",  0, False, 0, False],
#     ["C#", 0, True, 1, True],
#     ["D",  1, False, 1, False],
#     ["D#", 1, True, 2, True],
#     ["E",  2, False, 2, False],
#     ["F",  3, False, 3, False],
#     ["F#", 3, True, 4, True],
#     ["G",  4, False, 4, False],
#     ["G#", 4, True, 5, True],
#     ["A",  5, False, 5, False],
#     ["A#", 5, True, 6, True],
#     ["B",  6, False, 6, False]
# ]

TONES_IN_OCTAVE = [
    # pitch, SHARP: half line on staff from top, has sharp, FLAT: half line on staff from top, has flat, Hertz
    ["C",  10, False, 10, False, 261.63],
    ["C#", 10, True, 9, True, 277.18],
    ["D",  9, False, 9, False, 293.66],
    ["D#", 9, True, 8, True, 311.13],
    ["E",  8, False, 8, False, 329.66],
    ["F",  7, False, 7, False, 349.23],
    ["F#", 7, True, 6, True, 369.99],
    ["G",  6, False, 6, False, 392.00],
    ["G#", 6, True, 5, True, 415.30],
    ["A",  5, False, 5, False, 440.00],
    ["A#", 5, True, 4, True, 466.16],
    ["B",  4, False, 4, False, 493.88]
]

TEMPO = {
    "larghissimo": 24,
    "adagissimo": 32,
    "grave": 40,
    "largo": 50,
    "larghetto": 60,
    "adagio": 68,
    "adagietto": 80,
    "lento": 90,
    "adnante": 100,
    "adnantino": 95,
    "macia moderato": 70,
    "andante moderato": 110,
    "moderato": 120,
    "alegretto": 115,
    "alegro moderato": 126,
    "alegro": 140,
    "molto alegro": 150,
    "alegro vivace": 150,
    "vivace": 160,
    "vivacissimo": 180,
    "alegrisimo": 170,
    "presto": 190,
    "prestissimo": 200
}

TREBLE_CLEF = "treble_clef"
BASS_CLEF = "bass_clef"
ALTO_CLEF = "alto_clef"
TENOR_CLEF = "tenor_clef"
NEUTREL_CLEF = "neutral_clef"

FLAT = "flat"
SHARP = "sharp"
NATURAL = "natural"

T0 = "t0"
T1 = "t1"
T2 = "t2"
T3 = "t3"
T4 = "t4"
T5 = "t5"
T6 = "t6"
T7 = "t7"
T8 = "t8"
T9 = "t9"
TC = "tc"
TCI = "tci"

REST = "rest"
REST1 = "rest1"
REST2 = "rest2"
REST4 = "rest4"
REST8 = "rest8"
REST16 = "rest16"
REST32 = "rest16"
REST64 = "rest16"

HEAD1 = "head1"
HEAD2 = "head2"
HEAD4 = "head4"
STEM_UP = "stem_up"
STEM_DOWN = "stem_down"

TAIL_DOWN = "tail_down"
TAIL_UP = "tail_up"
TAIL_DOWN8 = "tail_down"
TAIL_DOWN16 = "tail_down16"
TAIL_DOWN32 = "tail_down32"
TAIL_DOWN64 = "tail_down64"
TAIL_UP8 = "tail_up8"
TAIL_UP16 = "tail_up16"
TAIL_UP32 = "tail_up32"
TAIL_UP64 = "tail_up64"

DOT = "dot"
DOT_UP = "dot_up"

MUSICAL_FILES = {
    "alto_clef": "music_alto_clef.png",
    "bass_clef": "music_bass_clef.png",
    "dot": "music_dot.png",
    "dot_up": "music_dot_up.png",
    "flat": "music_flat.png",
    "head1": "music_head1.png",
    "head2": "music_head2.png",
    "head4": "music_head4.png",
    "natural": "music_natural.png",
    "neutral_clef": "music_neutral_clef.png",
    "repeat_from": "music_repeat_from.png",
    "repeat_to": "music_repeat_to.png",
    "rest1": "music_rest1.png",
    "rest2": "music_rest2.png",
    "rest4": "music_rest4.png",
    "rest8": "music_rest8.png",
    "rest16": "music_rest16.png",
    "sharp": "music_sharp.png",
    "slur_down": "music_slur_down.png",
    "slur_up": "music_slur_up.png",
    "stem_down": "music_stem_down.png",
    "stem_up": "music_stem_up.png",
    "t0": "music_t0.png",
    "t1": "music_t1.png",
    "t2": "music_t2.png",
    "t3": "music_t3.png",
    "t4": "music_t4.png",
    "t5": "music_t5.png",
    "t6": "music_t6.png",
    "t7": "music_t7.png",
    "t8": "music_t8.png",
    "t9": "music_t9.png",
    "tail_down8": "music_tail_down8.png",
    "tail_down16": "music_tail_down16.png",
    "tail_down32": "music_tail_down32.png",
    "tail_down64": "music_tail_down64.png",
    "tail_up8": "music_tail_up8.png",
    "tail_up16": "music_tail_up16.png",
    "tail_up32": "music_tail_up32.png",
    "tail_up64": "music_tail_up64.png",
    "tc": "music_tc.png",
    "tci": "music_tci.png",
    "tenor_clef": "music_tenor_clef.png",
    "treble_clef": "music_treble_clef.png"
}

REST_TONE = -1000

SHARP_SEQ = [6, 1, 8, 3, 10]
SHARP_VISUAL_SEQ = [6 + 12, 1 + 12, 8 + 12, 3 + 12, 10]
FLAT_SEQ = [10, 3, 8, 1, 6]
FLAT_VISUAL_SEQ = [10, 3 + 12, 8, 1 + 12, 6]

DURATIONS = [1, 2, 4, 8, 16, 32, 64]

__all_tones = ALL_TONES.split(" ")
__base_tone = -1


def tone_from_string(s, base_tone="C"):
    # extracting tone

    if s == base_tone:
        return 0

    if base_tone == "":
        base = 0
    else:
        base = tone_from_string(base_tone, base_tone="")
        if base is None:
            base = 0

    tone = None
    tone_s = re.sub("[^_ABCDEFGabcdefg#]", "", s)

    if tone_s != "":
        try:
            tone = __all_tones.index(tone_s) - base
        except:
            pass

    return tone


class KeySignature:
    def __init__(self, is_sharp=True, number_of_accidentals=0):
        self.is_sharp = is_sharp
        self.number_of_accidentals = number_of_accidentals


class Meter:
    def __init__(self, upper: int = 4, lower: int = 4):
        if lower <= 1:
            raise Exception("Lower of the time signature must be positive number")
        if upper <= 1:
            raise Exception("Upper of the time signature must be positive number")
        self.upper = upper
        self.lower = lower


class NoteType(enum.Enum):
    NOTE = "note"
    PAUSE = "pause"
    SIGNATURE = "signature"
    METER = "meter"


class Note:
    def __init__(self, tone=0, duration=4, dot=False):
        self.tone = tone
        self.__duration = 0
        self.duration = duration
        self.dot = dot
        self.new_signature = None
        self.new_meter = None
        self.slur = False

    @property
    def type(self):
        if self.tone == REST_TONE:
            return NoteType.PAUSE
        if self.new_signature is not None:
            return NoteType.SIGNATURE
        if self.new_meter is not None:
            return NoteType.METER
        return NoteType.NOTE

    @property
    def duration(self):
        return self.__duration

    @duration.setter
    def duration(self, value: int):
        if value not in [1, 2, 4, 8, 16, 32, 64]:
            raise Exception("Note duration must be a power of 2: 1, 2, 4, 8, 16, 32, or 64")
        self.__duration = value

    def clone(self):
        if self.new_signature is not None:
            return Note(0, 4, False)
        else:
            return Note(self.tone, self.duration, self.dot)

class Accidental(enum.Enum):
    NONE = "none"
    SHARP = "sharp"
    FLAT = "flat"
    NATURAL = "natural"


class Music:
    def __init__(self):
        self.shifts = KeySignature()
        self.meter = Meter()
        self.notes = []
        self._all_tones = ALL_TONES.split(" ")
        try:
            self.base_tone = self._all_tones.index(BASE_TONE)
        except:
            self.base_tone = 0

    def note_from_string(self, s):
        tone = None
        pause = False
        duration = 0
        dot = False

        # extracting tone
        tone_s = re.sub("[^_ABCDEFGabcdefg#]", "", s)
        if tone_s != "":
            try:
                i = self._all_tones.index(tone_s)
                tone = i - self.base_tone
            except:
                pass

        if tone is None:
            # is it a sharp or flat? change key signature!
            sh = re.sub("[^#]", "", s)
            if len(sh) > 0:
                n = Note(0, 1, False)
                n.new_signature = KeySignature(True, len(sh))
                return n
            bm = re.sub("[^@]", "", s)
            if len(bm) > 0:
                n = Note(0, 1, False)
                n.new_signature = KeySignature(False, len(bm))
                return n
            # maybe it's a time signature?
            mt = re.sub("[ˆ123456789:]", "", s).split(":")
            if len(mt) == 2:
                n = Note(0, 1, False)
                n.new_meter = Meter(int(mt[0]), int(mt[1]))
                return n

        if re.sub("[^Pp]", "", s) != "":
            tone = REST_TONE

        dur = re.sub("[^1234567890]", "", s)
        if dur != "":
            n = int(dur)
            if n in DURATIONS:
                duration = n
            else:
                duration = 1
        else:
            duration = 1

        dot = re.sub("[^.]", "", s) != ""

        if tone is None:
            return None
        else:
            return Note(tone, duration, dot)

    def from_string(self, s, append=False):
        if not append:
            self.clear()
        self.shifts = KeySignature()
        elements = s.split(" ")
        for e in elements:
            n = self.note_from_string(e)
            if n is not None:
                self.notes.append(n)

    def string_from_note(self, note: Note):
        # check if it is a key signature
        if note.type == NoteType.SIGNATURE:
            shift_sign = "#" if note.new_signature.is_sharp else "@"
            return shift_sign * note.new_signature.number_of_accidentals
        if note.type == NoteType.METER:
            return str(note.new_meter.upper) + ":" + str(note.new_meter.lower)
        # create tone
        s = ""
        if note.type == NoteType.PAUSE or not (-self.base_tone <= note.tone < len(self._all_tones) - self.base_tone):
            s = "p"
        else:
            s = self._all_tones[note.tone + self.base_tone]
        # add dot
        s += str(note.duration)
        if note.dot:
            s += "."
        return s

    def to_string(self):
        elements = [self.string_from_note(note) for note in self.notes]
        return " ".join(elements)

    def clear(self):
        self.notes.clear()

    def clone_last(self):
        if len(self.notes) > 0:
            last_note = self.notes[-1]
            new_note = last_note.clone()
            self.notes.append(new_note)


class MusicNotationItems:
    def __init__(self):
        self.images = {}
        self._load_images()

    def _load_images(self):
        for key in MUSICAL_FILES:
            filename = MUSICAL_FILES[key]
            img = Image.open(os.path.join(IMAGE_FOLDER, filename))
            self.images[key] = img

