from difflib import get_close_matches
from sys import exit as sys_exit
from sys import stdout

from blessed import Terminal


class Selection:

    def __init__(self):

        pass

    pass


class SelectionPrompt:

    def __init__(self, selection, info="", prompt="> ", rows=4, current=0, cutoff=0.25):

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
        self._cutoff = cutoff

    def show(self):

        with self._term.cbreak():

            while True:

                self._render()

                open("log.txt", "a").write("\n\n")
                open("log.txt", "a").write(str(self._cursor_pos) + "\n" + str(self._written_lines))
                open("log.txt", "a").write("\n\n")

                key = self._term.inkey(timeout=5)

                if key.name == "KEY_ESCAPE":

                    self._exit()

                elif key.name == "KEY_ENTER":

                    self._flush()

                    return self._currently_shown[self._current]

                elif key.name == "KEY_DOWN":

                    self._navigate_menu(1)

                elif key.name == "KEY_UP":

                    self._navigate_menu(-1)

                elif key.name == "KEY_BACKSPACE" and \
                        self._search != "":

                    self._search = self._search[:-1]

                elif len(key) == 1 and \
                        len(self._search) < (self._term.width - len(self._prompt)) and \
                        key.name != "KEY_BACKSPACE":

                    self._search += key

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

        open("log.txt", "a").write(out + "\n")

        self._written_lines += 1 + out.count("\n")

    def _render(self):

        if self._info:
            self._print(self._info)

        self._print(self._prompt + self._search)

        if self._search != "" and True:  # TODO: Not for production | TODO Does not work

            best_matches = get_close_matches(self._search, self._selection, cutoff=self._cutoff)

            self._currently_shown = best_matches[self._current_position[0]:self._current_position[1]]

        else:

            self._currently_shown = self._selection[self._current_position[0]:self._current_position[1]]

        for pos, option in enumerate(self._currently_shown):

            option_msg = self._term.reverse(option) if pos == self._current else option
            self._print(option_msg)

        self._reset_cursor()
        self._move_cursor(len(self._prompt) + 1 * len(self._search), 0)

    def _move_cursor(self, cursor_x, cursor_y):

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

        open("log.txt", "a").write(full_write)

        stdout.write(full_write)
        stdout.flush()

        self._cursor_pos = {"x": cursor_x, "y": cursor_y}

    def _reset_cursor(self):  # TODO: Not for production  | Should be standard and before every move

        self._move_cursor(0, 0)

        self._written_lines = 0
        self._cursor_pos = None

    def _flush(self):

        self._move_cursor(0, 0)

        stdout.write(self._term.clear_eos)
        # stdout.write(self._term.clear_eol)
        stdout.flush()

        open("log.txt", "a").write(self._term.clear_eos)

        self._written_lines = 0
        self._cursor_pos = None


def select(selection, **kwargs):
    """

    """

    prompt = SelectionPrompt(selection, **kwargs)

    try:

        user_selection = prompt.show()

    except KeyboardInterrupt:

        prompt._exit()

    return user_selection
