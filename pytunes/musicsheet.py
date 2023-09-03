from pytunes.musicbasics import *
from PIL import Image, ImageDraw

# space for the note the page
NOTE_WIDTH = [0, 120, 100, 0, 90, 0, 0, 0, 80, 0, 0, 0, 0, 0, 0, 0, 60, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 55,
              0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 55]

SIGN_CENTER_X = 40
SIGN_CENTER_Y = 80
SIGN_WIDTH = 80
SIGN_HEIGHT = 160
CLEF_WIDTH = 80
SHARP_OFFSET = -40
ACCIDENTAL_WIDTH = 20
DOT_WIDTH = 15

ZERO_LINE = 5  # C line starting from 0
EXTENDED_LINE_LENGTH = 30  # extra lines below or above line block


class Staff:
    def __init__(self, index=0, key=TREBLE_CLEF, width=1000):
        self.index = index
        self.key = key
        self.inherit_signature = None
        self.inherit_meter = None
        self.x = 0
        self.y = 0
        self.width = width
        self.items = []


class LayoutItem:
    def __init__(self):
        self.type = "note"
        self.staff_index = 0
        self.order = 0
        self.order_on_staff = 0
        self.x = 0
        self.y = 0
        self.note = None
        self.note_halfline_from_top = 0
        self.accidental: Accidental = Accidental.NONE
        self.width = 0
        self.image_x = 0
        self.image_y = 0
        self.right_x = 0
        self.current_signature = None
        self.current_meter = None
        self.previous_item = None
        self.previous_item_on_staff = None
        self.selected = False
        self.signature_layout = None


class LayoutIterator:
    def __init__(self):
        self.staff_index = -1
        self.item_index = 0
        self.item_on_staff = 0
        self.last_x_on_staff = 0
        self.current_signature = None
        self.current_meter = None
        self.previous_item = None


class MusicSheet:
    def __init__(self, width, height):
        self.music = Music()

        self.width = width
        self.height = height

        self.line_height = 16
        self.padding_top = 64
        self.padding_left = 32
        self.padding_right = 32
        self.line_block_height = 128
        self.note_y_step = 60
        self.accidental_x_step = 30

        self.show_all_accidentals = True

        self.staffs = []
        self.items = []

        self.output_image = None  # canvas image of the editor
        self.notation_items = MusicNotationItems()

    def _draw(self, symbol: str, x, y):
        self.output_image.paste(self.notation_items.images[symbol], (x - SIGN_CENTER_X, y - SIGN_CENTER_Y),
                                self.notation_items.images[symbol])

    def render(self, output=None, recalculate_layout=True):
        if output is not None:
            self.output_image = output

        if self.output_image is None:
            raise Exception("Output is not defined")

        if recalculate_layout:
            width = self.width - self.padding_left - self.padding_right
            self.calculate_layout(self.music, width)

        for staff in self.staffs:
            self.draw_staff(staff)

    def _calculate_note_halfline_from_top(self, tone, signature: KeySignature):
        if tone == REST_TONE:
            return 4

        octave = tone // OCTAVE_TONES
        tone_in_octave = tone % OCTAVE_TONES

        if signature.is_sharp:
            halfline = TONES_IN_OCTAVE[tone_in_octave][1]
        else:
            halfline = TONES_IN_OCTAVE[tone_in_octave][3]

        return halfline - octave * OCTAVE

    def _calculate_note_y(self, tone, shifts: KeySignature):
        line = self._calculate_note_halfline_from_top(tone, shifts)
        return line * self.line_height // 2

    def has_accidental_deprecated(self, tone, signature: KeySignature):
        # deprecated
        sharp = signature.is_sharp
        number_of_accidentals = signature.number_of_accidentals
        tone_in_octave = tone % OCTAVE_TONES
        if sharp:
            try:
                index = SHARP_SEQ.index(tone_in_octave)
                return self.show_all_accidentals or index >= number_of_accidentals
            except ValueError:
                return False
        else:
            try:
                index = FLAT_SEQ.index(tone_in_octave)
                return self.show_all_accidentals or index >= number_of_accidentals
            except ValueError:
                return False

    def has_natural_deprecated(self, tone, signature: KeySignature):
        # deprecated
        if signature.is_sharp:
            tone_in_octave = (tone + 1) % OCTAVE_TONES
            try:
                index = SHARP_SEQ.index(tone_in_octave)
                return index < signature.number_of_accidentals
            except ValueError:
                return False
        else:
            tone_in_octave = (tone - 1) % OCTAVE_TONES
            try:
                index = FLAT_SEQ.index(tone_in_octave)
                return index < signature.number_of_accidentals
            except ValueError:
                return False

    def _tone_accidental_order(self, tone_in_octave, signature: KeySignature):
        if signature.is_sharp:
            try:
                index = SHARP_SEQ.index(tone_in_octave)
                return index
            except ValueError:
                return 100  # more than 5
        else:
            try:
                index = FLAT_SEQ.index(tone_in_octave)
                return index
            except ValueError:
                return 100  # more than 5

    def accidental_of(self, tone, signature: KeySignature):
        number_of_accidentals = signature.number_of_accidentals
        tone_in_octave = tone % OCTAVE_TONES
        if signature.is_sharp:
            # SHARP NOTATION
            tone_has_sharp = TONES_IN_OCTAVE[tone_in_octave][2]

            if tone_has_sharp:
                # my tone has sharp, let's check if it is already in the current signature
                signature_has_my_sharp = \
                    self._tone_accidental_order(tone_in_octave, signature) < number_of_accidentals
                if (not signature_has_my_sharp) or self.show_all_accidentals:
                    return Accidental.SHARP
                else:
                    return Accidental.NONE
            else:
                # my tone has no sharp, let's check if current signature has sharp for my halfline, then need natural
                plus_one_tone = (tone + 1) % OCTAVE_TONES
                my_halfline_has_sharp = \
                    self._tone_accidental_order(plus_one_tone, signature) < number_of_accidentals
                if my_halfline_has_sharp:
                    return Accidental.NATURAL
                else:
                    return Accidental.NONE
        else:
            # FLAT NOTATION
            tone_has_flat = TONES_IN_OCTAVE[tone_in_octave][4]

            if tone_has_flat:
                # my tone has flat, let's check if it is already in the current signature
                signature_has_my_flat = \
                    self._tone_accidental_order(tone_in_octave, signature) < number_of_accidentals
                if (not signature_has_my_flat) or self.show_all_accidentals:
                    return Accidental.FLAT
                else:
                    return Accidental.NONE
            else:
                # my tone has no flat, let's check if current signature has flat for my halfline, then need natural
                minus_one_tone = (tone - 1) % OCTAVE_TONES
                my_halfline_has_flat = \
                    self._tone_accidental_order(minus_one_tone, signature) < number_of_accidentals
                if my_halfline_has_flat:
                    return Accidental.NATURAL
                else:
                    return Accidental.NONE

    def draw_signature(self, x0, y0, signature: KeySignature, signature_layouts):
        for i in range(len(signature_layouts)):
            x, y = signature_layouts[i]
            x += x0
            y += y0
            if signature.is_sharp:
                self._draw(SHARP, x, y)
            else:
                self._draw(FLAT, x, y)

    def layout_signature(self, signature: KeySignature):
        signature_layouts = []
        is_sharp = signature.is_sharp
        count = signature.number_of_accidentals
        for i in range(count):
            x = i * ACCIDENTAL_WIDTH + ACCIDENTAL_WIDTH
            if is_sharp:
                y = self._calculate_note_y(SHARP_VISUAL_SEQ[i], signature)
            else:
                y = self._calculate_note_y(FLAT_VISUAL_SEQ[i], signature)
            point = (x, y)
            signature_layouts.append(point)
        return signature_layouts

    def signature_width(self, signature: KeySignature):
        return signature.number_of_accidentals * ACCIDENTAL_WIDTH + 2 * ACCIDENTAL_WIDTH

    def new_staff(self, x0, y0, width, index, signature, meter):
        block = Staff()
        block.x = x0
        block.y = y0
        block.width = width
        block.index = index
        block.inherit_signature = signature
        block.inherit_meter = meter
        return block

    def calculate_layout(self, music, staff_width=0):

        self.staffs.clear()
        self.items.clear()
        iterator = LayoutIterator()
        iterator.staff_index = 0
        iterator.item_index = 0
        iterator.item_on_staff = 0

        if staff_width == 0:
            staff_width = self.width - self.padding_left - self.padding_right

        staff = self.new_staff(self.padding_left, self.padding_top, staff_width, 0, music.shifts, music.meter)
        self.staffs.append(staff)

        iterator.last_x_on_staff = CLEF_WIDTH
        iterator.current_signature = music.shifts
        iterator.current_meter = music.meter
        iterator.previous_item = None

        self.iterate(music, iterator)

        return self.staffs

    def prepare_item(self, music: Music, iterator: LayoutIterator):
        note = music.notes[iterator.item_index]
        item = LayoutItem()
        item.previous_item = iterator.previous_item
        item.note = note
        item.order = iterator.item_index

        if note.new_signature is None:
            # normal note (or pause)
            item.accidental = self.accidental_of(note.tone, iterator.current_signature)

            # item.signature = self.has_accidental(note.tone, iterator.current_signature)
            # item.shift_is_sharp = iterator.current_signature.is_sharp
            # item.natural = self.has_natural(note.tone, iterator.current_signature)

            item.note_halfline_from_top = self._calculate_note_halfline_from_top(note.tone, iterator.current_signature)

            item.width = NOTE_WIDTH[note.duration]
            if note.duration > 4:
                # if item.signature:
                #     item.width += ACCIDENTAL_WIDTH * 3 // 2
                # if item.natural:
                #     item.width += ACCIDENTAL_WIDTH * 3 // 2
                if note.dot:
                    item.width += DOT_WIDTH
                item.image_x = 0  # - (item.width - SIGN_WIDTH) // 2
            else:
                item.image_x = 0
            item.y = self._calculate_note_y(note.tone, iterator.current_signature)
        else:
            # new signature item
            iterator.current_signature = note.new_signature
            item.signature_layout = self.layout_signature(note.new_signature)
            item.width = self.signature_width(note.new_signature)
        return item

    def iterate(self, music: Music, iterator: LayoutIterator):
        staff = self.staffs[len(self.staffs) - 1]
        while iterator.item_index < len(music.notes):
            item = self.prepare_item(music, iterator)

            # calculate the x position of the item
            if staff.width < iterator.last_x_on_staff + item.width:
                # create new staff and place the item there
                prev_block = staff
                iterator.staff_index += 1
                staff = self.new_staff(prev_block.x, prev_block.y + self.line_block_height,
                                       prev_block.width, iterator.staff_index,
                                       iterator.current_signature, iterator.current_meter)
                self.staffs.append(staff)

                # put item into staff
                iterator.item_on_staff = 0
                item.previous_item_on_staff = None

            # check if this item is going to be first in the staff
            if iterator.item_on_staff == 0:
                if item.note.new_signature is not None:
                    # this is a first item in the staff, and it is a shifts item
                    iterator.current_signature = item.note.new_signature
                    staff.inherit_signature = None
                    iterator.last_x_on_staff = CLEF_WIDTH
                else:
                    # this is a first item in the staff, but it is not new
                    # so we automatically create inherited shifts
                    staff.inherit_signature = iterator.current_signature
                    iterator.last_x_on_staff = CLEF_WIDTH + self.signature_width(iterator.current_signature)

                # check if the staff is too narrow for this first item
                if staff.width < iterator.last_x_on_staff + item.width:
                    raise Exception("The item width " + str(item.width) +
                                    " does not fit the width of the staff " + str(staff.width))

            # set location-based values to the item
            item.current_signature = iterator.current_signature
            item.x = iterator.last_x_on_staff
            item.right_x = item.x + item.width
            item.image_y = 0  # shift of the image as compared to the item.x
            item.staff_index = iterator.staff_index
            item.order_on_staff = iterator.item_on_staff

            # update iterator
            iterator.last_x_on_staff += item.width
            iterator.item_on_staff += 1
            iterator.item_index += 1

            # add items to the storage
            staff.items.append(item)
            self.items.append(item)

        return self.staffs

    def calculate_layout_from_index(self, item_index, music, staff_width=1000):

        raise Exception("This method is not yet tested")

        if len(self.staffs) == 0:
            # if empty run the whole process
            return self.calculate_layout(music, staff_width)

        previous_item_on_staff = None
        previous_item = None

        print("redrawing from", item_index)

        # find block with the item
        if item_index < len(self.items):
            item = self.items[item_index]
            previous_item_on_staff = item.previous_item_on_staff
            previous_item = item.previous_item
            block_index = item.block_index
            block = self.staffs[block_index]

            # remove blocks and items after this item
            self.items = self.items[:item_index]  # removing the last item from the list
            self.staffs = self.staffs[:block_index + 1]
            block.items = block.items[:item.order_in_block]
        else:
            # starting from the last item
            item_index = len(self.items)
            if item_index > 0:
                previous_item = self.items[item_index - 1]
                previous_item_on_staff = previous_item
            block_index = len(self.staffs) - 1
            block = self.staffs[block_index]

        iterator = LayoutIterator()
        iterator.staff_index = block_index
        iterator.item_index = item_index
        iterator.item_on_staff = len(block.items)

        if previous_item_on_staff is not None:
            iterator.last_x_on_staff = previous_item_on_staff.right_x
        else:
            iterator.last_x_on_staff = CLEF_WIDTH

        iterator.previous_item = previous_item
        if previous_item is not None:
            iterator.current_signature = previous_item.current_shifts
        else:
            iterator.current_signature = music.shifts

        self.iterate(music, iterator)

        return self.staffs

    def item_at(self, x, y):

        valid_xy = True
        y -= self.padding_top - self.line_height
        block_index = y // self.line_block_height

        if block_index < 0:
            valid_xy = False
        if block_index >= len(self.staffs):
            valid_xy = False

        if y % self.line_block_height > 6 * self.line_height:
            valid_xy = False

        if not valid_xy:
            return

        found_item = None
        block = self.staffs[block_index]

        for item in block.items:
            if item.x <= x <= item.x + item.width:
                found_item = item

        return found_item

    def draw_staff(self, staff: Staff):

        # drawing lines
        x0 = staff.x
        x1 = staff.width
        y0 = staff.y
        y1 = staff.y + 4 * self.line_height

        lines_img = Image.new("RGBA", (x1 - x0 + 2, y1 - y0 + 2))
        draw = ImageDraw.Draw(lines_img)
        draw.rectangle(((0, 0), (x1 - x0 + 1, y1 - y0 + 1)), fill=None, outline="black", width=2)

        for i in range(3):
            draw.line((0, (i + 1) * self.line_height, x1 - x0, (i + 1) * self.line_height), fill="#000000", width=2)

        self.output_image.paste(lines_img, (x0, y0), lines_img)

        # draw key
        self._draw(TREBLE_CLEF, staff.x + CLEF_WIDTH // 2, staff.y + 2 * self.line_height)

        # draw shifts
        if staff.inherit_signature is not None:
            self.draw_signature(staff.x + CLEF_WIDTH, staff.y, staff.inherit_signature, self.layout_signature(staff.inherit_signature))

        for item in staff.items:
            self.draw_item(staff.x, staff.y, item)

    def draw_item(self, x0, y0, item: LayoutItem):

        if item.note.type == NoteType.SIGNATURE:
            # draw a sharp change item and quit
            self.draw_signature(x0 + item.x, y0, item.note.new_signature, item.signature_layout)
            return

        x = x0 + item.x + item.image_x
        y = y0 + item.y + item.image_y

        # signature = item.signature
        # is_sharp = item.signature.is_sharp
        # natural = item.natural
        accidental = item.accidental

        note_on_line = item.note_halfline_from_top
        note = item.note

        if note.tone == REST_TONE:
            self._draw("rest" + str(note.duration), x, y)

        else:
            if note.duration == 1:
                self._draw(HEAD1, x, y)
            elif note.duration == 2:
                self._draw(HEAD2, x, y)
            elif note.duration > 2:
                self._draw(HEAD4, x, y)
            if note.duration != 1:
                if note.tone >= 12:
                    self._draw(STEM_DOWN, x, y)
                    if note.duration >= 8:
                        self._draw(TAIL_DOWN + str(note.duration), x, y)
                else:
                    self._draw(STEM_UP, x, y)
                    if note.duration >= 8:
                        self._draw(TAIL_UP + str(note.duration), x, y)
            if accidental == Accidental.SHARP:
                self._draw(SHARP, x, y)
            elif accidental == Accidental.FLAT:
                self._draw(FLAT, x, y)
            elif accidental == Accidental.NATURAL:
                self._draw(NATURAL, x, y)

            # if signature:
            #     if signature.is_sharp:
            #         self._draw(SHARP, x, y)
            #     else:
            #         self._draw(FLAT, x, y)
            # if natural:
            #     self._draw(NATURAL, x, y)

        if note.dot:
            if note_on_line % 2 == 0:
                self._draw(DOT_UP, x, y)
            else:
                self._draw(DOT, x, y)

        draw = ImageDraw.Draw(self.output_image)

        if note_on_line >= 10:
            l = EXTENDED_LINE_LENGTH
            lines = note_on_line
            yy = y
            if note_on_line % 2 == 1:
                lines -= 1
                yy -= self.line_height // 2
            while lines >= 10:
                draw.line((x - l//2, yy, x + l//2, yy), width=2, fill="black")
                lines -= 2
                yy -= self.line_height

        if note_on_line <= -2:
            l = EXTENDED_LINE_LENGTH
            lines = note_on_line
            yy = y
            if note_on_line % 2 == 1:
                lines += 1
                yy += self.line_height // 2
            while lines <= -2:
                draw.line((x - l//2, yy, x + l//2, yy), width=2, fill="black")
                lines += 2
                yy += self.line_height