from sys import exit as sys_exit
from sys import stdout

from blessed import Terminal


class Selection:

    def __init__(self):

        pass

    pass


class SelectionPrompt:

    def __init__(self, selection, info="", prompt="> ", rows=4, current=0):

        self._term = Terminal()
        self._selection = [str(option) for option in selection]

        self._currently_shown = self._selection[:rows]
        self._current_position = [0, rows]
        self._current = current
        self._rows = rows
        self._search = ""
        self._cursor_pos = None
        self._written_lines = 0

        self._info = info
        self._prompt = prompt

    def show(self):

        with self._term.cbreak():

            while True:

                self._render()

                key = self._term.inkey(timeout=5)

                if key.name == "KEY_ESCAPE":

                    self._exit()

                elif key.name == "KEY_DOWN":

                    self._navigate_menu(1)

                elif key.name == "KEY_UP":

                    self._navigate_menu(-1)

                self._flush()

                # print(key.name)

    def _navigate_menu(self, up_or_down):

        if self._current == 0 and up_or_down == -1 or \
           self._current == len(self._selection) - 1 and up_or_down == 1:

            return

        if self._current == self._current_position[0] and \
           up_or_down < 0:

            self._current_position[0] -= 1
            self._current_position[1] -= 1
            self._currently_shown = self._selection[self._current_position[0]:self._current_position[1]]

        elif self._current == self._current_position[1] and \
                up_or_down > 0:

            self._current_position[0] += 1
            self._current_position[1] += 1
            self._currently_shown = self._selection[self._current_position[0]:self._current_position[1]]

        if up_or_down < 0:

            self._current -= 1

        elif up_or_down > 0:

            self._current += 1

    def _exit(self):

        self._flush()

        sys_exit()

    def _print(self, out):

        stdout.write(out + "\n")
        stdout.flush()

        self._written_lines += 1 + out.count("\n")

    def _render(self):

        if self._info:
            self._print(self._info)

        self._print(self._prompt + self._search)

        for pos, option in enumerate(self._currently_shown):

            option_msg = self._term.reverse(option) if pos == self._current else option
            self._print(option_msg)

        self._move_cursor(2, 0)

    def _move_cursor(self, cursor_x, cursor_y):

        # self._cursor_pos = {"x": cursor_x, "y": cursor_y}

        self._update_cursor(cursor_x, cursor_y)

    def _update_cursor(self, cursor_x, cursor_y):

        if self._cursor_pos is None:

            self._cursor_pos = {"x": 0, "y": self._written_lines}

        full_write = ""

        if self._cursor_pos["y"] < cursor_y:
            full_write += self._term.move_down * (cursor_y - self._cursor_pos["y"])

        elif self._cursor_pos["y"] > cursor_x:
            full_write += self._term.move_up * (self._cursor_pos["y"] - cursor_y)

        if self._cursor_pos["x"] < cursor_x:
            full_write += self._term.move_right * (cursor_x - self._cursor_pos["x"])

        elif self._cursor_pos["x"] > cursor_x:
            full_write += self._term.move_left * (self._cursor_pos["x"] - cursor_x)

        stdout.write(full_write)
        stdout.flush()

        self._cursor_pos = {"x": cursor_x, "y": cursor_y}

    def _flush(self):

        self._move_cursor(0, 0)

        stdout.write(self._term.clear_eos)
        # stdout.write(self._term.clear_eol)
        stdout.flush()

        self._written_lines = 0
        self._cursor_pos = None


def select(selection, **kwargs):
    """

    """

    prompt = SelectionPrompt(selection, **kwargs)

    try:

        prompt.show()

    except KeyboardInterrupt:

        prompt._exit()
