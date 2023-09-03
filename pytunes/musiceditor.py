import random
from tkinter import *

import musicplayer
from musicbasics import *
import instruments
import musicsheet
from PIL import Image, ImageTk
import time


TEST_MUSIC = "@ AA4 AA#4 BB4 C4 C#4 D4 D#4 E4 F4 F#4 G4 G#4 A4 A#4 B4 c4 c#4 d4 d#4 e4 f4 f#4 g4 g#4 a4 a#4 b4 cc4 cc#4 dd4 dd#4 ee4"

HOLMES_MUSIC2 = "@ F4 p8. F16 A4 c4 f16 e16 d16 e16 f4 p8 e4 d8 c16 A#16 A16 A#16 c8 c16 c16 c8 A#4 A8 A2 p2 " \
               "F4 p8. F16 A4 c4 a16 g16 f16 g16 a4 p8 g4 f8 e16 f16 g16 f16 e8 g8 e8 g8 d8 f8 e16 f16 g16 " \
               "f16 e8 g8 e8 g8 d8 f8 e8 e16 d16 c8 c16 A#16 A8 c8 f4. g8 e8. f16 f4 p4 e8. f16 e16 d16 c8 " \
               "e8 e16 f16 e16 d16 c8 e8 e16 e16 e8"

HOLMES_MUSIC = "@ F4 p8. F16 A4 c4 f16 e16 d16 e16 f4 p8 e4 d8 c16 A#16 A16 A#16 c8 c16 c16 c8 A#4 A8 A2 p2 " \
               "F4 p8. F16 A4 c4 a16 g16 f16 g16 a4 p8 g4 f8 e16 f16 g16 f16 e8 g8 e8 g8 d8 f8 e16 f16 g16 f16 " \
               "e8 g8 e8 g8 d8 f8 e8 e16 d16 c8 c16 A#16 A8 c8 f4. g8 e8. f16 f4 p4 " \
               "e8. f16 e16 d16 c8 e8 e16 f16 e16 d16 c8 e8 e16 e16 e8 g8 a4 g16 g8. " \
               "e8. f16 e16 d16 c8 g8 e8 cc8 g8 e8 e16 f16 e16 d16 c8 d4 c16 c8."


LOAD_THIS = HOLMES_MUSIC

class PageNavigator:
    def __init__(self):
        self.seleted_item = None
        self.selection_color = "#55220033"
        self.selection_box = -1
        self.selected_index = -1


class MusicEditor:

    def __init__(self, width=1200, height=1000):

        self.width = width
        self.height = height
        self.sheet = musicsheet.MusicSheet(width - instruments.INSTRUMENT_WIDTH, height)

        self.selected_index = 0
        self.window = None
        self.canvas = None
        self.canvas_image = None
        self._rendered_image = None

        self.navigator = PageNavigator()
        self.instrument = None  # Instrument
        self.instrument_x = width - instruments.INSTRUMENT_WIDTH
        self.instrument_y = 0

        self._zoom = 1
        self._invalidation_period = 0.1  # seconds
        self._invalidation_time = 0

        self.playing = False
        self.player = musicplayer.MusicPlayer()

    @property
    def music(self):
        if self.sheet is not None:
            return self.sheet.music
        else:
            return None

    @property
    def zoom(self):
        return self._zoom

    @zoom.setter
    def zoom(self, value):
        if 0.1 <= value <= 10:
            if abs(value - int(value)) < 0.01:
                # eliminating rounding error when zooming in and out
                value = int(value)
            self._zoom = value
            self.layout_changed()

    def create_window(self):
        self.window = Tk()
        self.window.title = "Music"
        self.window.geometry(str(self.width) + 'x' + str(self.height))

        self.window.bind('<KeyPress>', self.on_key_press)
        self.window.bind('<ButtonPress-1>', self.on_mouse_press)
        self.window.bind("<Configure>", self.on_window_resize)

        self.canvas = Canvas(self.window, width=self.width, height=self.height)
        self.canvas.pack(fill=BOTH, expand=YES)

        # self.instrument = instruments.Flute()
        self.instrument = instruments.Clarinet()

        # load holmes music
        self.music.from_string(LOAD_THIS)

        self.redraw()
        self.navigator.selected_index = len(self.music.notes) - 1

        self.window.mainloop()

    def erase(self):
        img_width = int(self.width / self._zoom)
        img_height = int(self.height / self._zoom)
        self.canvas_image = Image.new(mode="RGBA", size=(img_width, img_height), color="#ffeedd")
        self.canvas.delete("all")

    def update(self):
        self.canvas_image = self.canvas_image.resize((self.width, self.height))
        self._rendered_image = ImageTk.PhotoImage(self.canvas_image)
        self.canvas.create_image(0, 0, image=self._rendered_image, anchor="nw")

    def _render_selection(self):
        index = self.navigator.selected_index
        item = self.sheet.items[index]
        staff = self.sheet.staffs[item.staff_index]
        x = item.x
        w = item.width
        y = staff.y
        h = 4 * self.sheet.line_height

        col = self.navigator.selection_color
        box = Image.new("RGBA", (w, h), col)
        self.canvas_image.paste(box, (x, y), box)

    def redraw(self):
        self.erase()
        self.sheet.calculate_layout(self.sheet.music)
        self._render_selection()
        self.sheet.render(self.canvas_image, recalculate_layout=False)
        self.draw_instrument()
        self.update()

    def draw_instrument(self):
        if self.instrument is None:
            return

        note = self.sheet.music.notes[self.navigator.selected_index]

        if note.new_signature is None:
            instrument_image = self.instrument.image(note.tone, give_a_list_if_many=False)
            if instrument_image is not None:
                self.canvas_image.paste(instrument_image, (self.instrument_x, self.instrument_y), instrument_image)

    def invalidate(self):
        if self._invalidation_time == 0:
            self._invalidation_time = time.time()
        else:
            if time.time() - self._invalidation_time > self._invalidation_period:
                self._invalidation_time = 0
                self.redraw()

    def play_current_note(self):
        msec = self.player.play(self.music.notes[self.navigator.selected_index])
        self.window.after(msec, self.on_note_played)

    def on_note_played(self):
        self.player.current_sound.stop()
        if self.playing:
            note_index = self.navigator.selected_index
            if note_index >= len(self.music.notes) - 1:
                self.playing = False
            else:
                self.navigator.selected_index += 1
                self.redraw()
                self.play_current_note()

    def play(self):
        self.play_current_note()

    def layout_changed(self):
        self.instrument_x = int(self.width / self.zoom) - instruments.INSTRUMENT_WIDTH
        self.sheet.width = int(self.width / self.zoom) - instruments.INSTRUMENT_WIDTH
        self.invalidate()

    def on_window_resize(self, event):
        if event.width != self.width or event.height != self.height:
            self.width = event.width
            self.height = event.height
            self.layout_changed()

    def on_mouse_press(self, event):
        mx = int(event.x / self.zoom)
        my = int(event.y / self.zoom)
        found_item = self.sheet.item_at(mx, my)
        if found_item is not None:
            self.navigator.selected_index = found_item.order
            self.redraw()

    def on_key_press(self, event):
        print(event)
        key = event.keysym

        note = self.music.notes[self.navigator.selected_index]

        if key == "Up" and note.tone != REST_TONE and note.new_signature is None:
            note.tone += 1
            self.redraw()
        elif key == "Down" and note.tone != REST_TONE and note.new_signature is None:
            note.tone -= 1
            self.redraw()
        elif key == 'Home':
            self.navigator.selected_index = 0
            self.redraw()
        elif key == 'End':
            self.navigator.selected_index = len(self.music.notes) - 1
            self.redraw()
        elif key == "Left":
            if self.navigator.selected_index != 0:
                self.navigator.selected_index -= 1
                self.redraw()
        elif key == "Right":
            last_item = len(self.music.notes) - 1
            if self.navigator.selected_index == last_item:
                self.music.clone_last()
                self.navigator.selected_index = len(self.music.notes) - 1
                self.redraw()
            else:
                self.navigator.selected_index += 1
                self.redraw()
        elif key == "space":
            if not self.playing:
                # start playing
                self.playing = True
                self.play()
            else:
                # stop playing
                self.playing = False
        elif key == 'C':
            self.navigator.selected_index = 0
            self.music.clear()
            self.music.from_string('A8')
            self.redraw()
        elif key == '1':
            note.duration = 1
            self.redraw()
        elif key == '2':
            note.duration = 2
            self.redraw()
        elif key == '3':
            note.duration = 4
            self.redraw()
        elif key == '4':
            note.duration = 8
            self.redraw()
        elif key == '5':
            note.duration = 16
            self.redraw()
        elif key == '6':
            note.duration = 32
            self.redraw()
        elif key == '7':
            note.duration = 64
            self.redraw()
        elif key == 'p' or key == "r":
            if note.tone != REST_TONE:
                note.tone = REST_TONE
                self.redraw()
            else:
                note.tone = 12
                self.redraw()
        elif key == 'BackSpace':
            if len(self.music.notes) > 1:
                self.music.notes.remove(note)
                if self.navigator.selected_index >= len(self.music.notes):
                    self.navigator.selected_index = len(self.music.notes) - 1
                self.redraw()
            else:
                self.navigator.selected_index = 0
                self.music.clear()
                self.music.from_string('p4')
                self.redraw()
        elif key == 'equal' or key == 'plus':
            newnote = note.clone()
            self.music.notes.insert(self.navigator.selected_index, newnote)
            self.redraw()
        elif key == 'period':
            note.dot = not note.dot
            self.redraw()
        elif key == 'at':
            if note.new_signature is None:
                shift = Note()
                shift.new_signature = KeySignature(False, 1)
                self.music.notes.insert(self.navigator.selected_index, shift)
                self.redraw()
            elif note.new_signature.is_sharp:
                note.new_signature.is_sharp = False
                note.new_signature.number_of_accidentals = 1
                self.redraw()
            elif note.new_signature.number_of_accidentals < 5:
                note.new_signature.number_of_accidentals += 1
                self.redraw()
            else:
                note.new_signature.number_of_accidentals = 1
                self.redraw()
        elif key == 'numbersign':
            if note.new_signature is None:
                shift = Note()
                shift.new_signature = KeySignature(True, 1)
                self.music.notes.insert(self.navigator.selected_index, shift)
                self.redraw()
            elif not note.new_signature.is_sharp:
                note.new_signature.is_sharp = True
                note.new_signature.number_of_accidentals = 1
                self.redraw()
            elif note.new_signature.number_of_accidentals < 5:
                note.new_signature.number_of_accidentals += 1
                self.redraw()
            else:
                note.new_signature.number_of_accidentals = 1
                self.redraw()
        elif key == "T":
            # transpose up
            for note in self.music.notes:
                if note.new_signature is None and note.tone != REST_TONE:
                    note.tone += 1
            self.redraw()
        elif key == "G":
            # transpose down
            for note in self.music.notes:
                if note.new_signature is None and note.tone != REST_TONE:
                    note.tone -= 1
            self.redraw()
        elif key == "S":
            print(self.music.to_string())
        elif key == "Z":
            self.zoom *= 1.25
            self.redraw()
        elif key == "z":
            self.zoom /= 1.25
            self.redraw()






