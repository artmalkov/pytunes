import math
import numpy
import pygame
import musicbasics

class MusicPlayer:
    def __init__(self):
        self.bits = 16
        self.sample_rate = 44100
        self.channels = 2
        pygame.mixer.pre_init(self.sample_rate, -self.bits, self.channels)
        duration = 1.0
        self.samples = []
        self.sounds = []
        self.base_tone_index = 0
        pygame.mixer.init()
        self.generate_samples_for_all_pitches()
        self.current_sound = None

    def generate_samples_for_all_pitches(self):
        self.sounds = []
        all_tones = musicbasics.ALL_TONES.split(" ")
        i = 0
        self.base_tone_index = musicbasics.tone_from_string("C", "")
        notes_in_octave = len(musicbasics.TONES_IN_OCTAVE)
        for note in all_tones:
            index = musicbasics.tone_from_string(note, "C")
            octave = index // notes_in_octave
            tone_in_octave = index % notes_in_octave

            frequency = musicbasics.TONES_IN_OCTAVE[tone_in_octave][5] * 2 ** octave
            duration = 1.0
            max_sample = 2 ** (self.bits - 1) - 1
            sinus = [max_sample * math.sin(2.0 * math.pi * frequency * t / self.sample_rate) for t in
                     range(0, int(round(duration * self.sample_rate)))]
            sample = numpy.array([[int(p), int(p)] for p in sinus]).astype(numpy.int16)
            self.samples.append(sample)
            sound = pygame.sndarray.make_sound(sample)
            self.sounds.append(sound)
            i += 1


    def play(self, note:musicbasics.Note, tempo=120, meter_denominator=4):

        if note.type == musicbasics.NoteType.METER:
            return 0

        if note.type == musicbasics.NoteType.SIGNATURE:
            return 0

        if int(tempo) == 0:
            if tempo in musicbasics.TEMPO:
                tempo = musicbasics.TEMPO[tempo]
            else:
                tempo = 120.0

        sec_duration = 60 * meter_denominator / tempo

        if note.dot:
            sec_duration *= 1.5

        duration_milliseconds = int(1000 * sec_duration / note.duration)

        if note.type == musicbasics.NoteType.PAUSE:
            return duration_milliseconds

        if note.slur:
            duration = duration_milliseconds
        else:
            duration = int(duration_milliseconds * 0.9)

        sound = self.sounds[note.tone + self.base_tone_index]
        sound.play()
        self.current_sound = sound
        return duration_milliseconds
