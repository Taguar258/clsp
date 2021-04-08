from difflib import get_close_matches
from sys import exit as sys_exit
from sys import stdout

from blessed import Terminal


class Selection:  # TODO: Return this object instead of item

    def __init__(self):

        pass

    pass


class SelectionPrompt:

    def __init__(self, selection, info="", prompt="> ", current=0, rows=4, cutoff=0.15, highlight_color="yellow"):
        """ Prompt for user selection.

        Arguments
        ---------
        :arg selection (LIST): The available choices to display the user.


        Keyword Arguments
        -----------------
        :arg info (STR): Information shown above prompt. / Prompt title.
        :arg prompt (STR): Text in front of user input.
        :arg current (INT): Current item of list as default selection.
        :arg rows (INT): Amount of visible choices.
        :arg cutoff (INT): Search precision.
        :arg highlight_color (STR): Search higlight color.
        :arg full_exit (BOOL): (TODO: Not implemented yet) Exit completely or pass None on KeyBoardInterrupt or ESC.

        """

        # Variables | Static variables
        self._term = Terminal()

        self._key_timeout = 5

        self._highlight_color = {"black": self._term.black, "red": self._term.red, "green": self._term.green, "yellow": self._term.yellow, "blue": self._term.blue, "magenta": self._term.magenta, "cyan": self._term.cyan, "white": self._term.white}[highlight_color]  # TODO: Find better solution

        # Variables | Static User Variables
        self._selection = [str(option) for option in selection]
        self._info = info
        self._prompt = prompt
        self._rows = rows
        self._cutoff = cutoff

        # Variables | Dynamic variables (Terminal State)
        self._cursor_pos = None
        self._written_lines = 0

        # Variables | Dynamic variables (List)
        self._current = current
        self._currently_shown = self._selection[:rows]  # TODO Interfiers with user current option
        self._current_position = [0, rows]

        # Variables | Dynamic variables (Input)
        self._search = ""

    def show(self):
        """ Entry Point | Main Loop
        """

        with self._term.cbreak():

            while True:

                self._render()

                # KEY BINDINGS
                key = self._term.inkey(timeout=self._key_timeout)

                if key.name == "KEY_ESCAPE":

                    self._exit()

                elif key.name == "KEY_ENTER":

                    return self._return_selection()

                elif key.name == "KEY_DOWN":

                    self._navigate_menu(1)

                elif key.name == "KEY_UP":

                    self._navigate_menu(-1)

                elif key.name == "KEY_BACKSPACE" and \
                        self._search != "":  # On Backspace

                    self._search = self._search[:-1]

                elif len(key) == 1 and key.name is None and \
                        len(self._search) < (self._term.width - len(self._prompt)):  # On Key except special keys

                    self._search += key

                self._flush()

    def _navigate_menu(self, up_or_down):  # TODO: Highlighted does not work with higher list len
        """ Navigates Menu one item down or up

        :arg up_or_down (INT): -1 for up and 1 for down.

        """

        # Check for list border
        if self._current == 0 and up_or_down == -1 or \
           self._current == len(self._selection) - 1 and up_or_down == 1:

            return

        # Change menu view point
        if self._current == self._current_position[0] and \
           up_or_down < 0:

            self._move_list_view(-1)

        elif self._current == self._current_position[1] and \
                up_or_down > 0:

            self._move_list_view(1)

        # Change current
        if up_or_down < 0:

            self._current -= 1

        elif up_or_down > 0:

            self._current += 1

    def _move_list_view(self, up_or_down):
        """ Navigates Menu view

        :arg up_or_down (INT): -1 for up and 1 for down.

        """

        self._current_position[0] += up_or_down
        self._current_position[1] += up_or_down

        self._currently_shown = self._selection[self._current_position[0]:self._current_position[1]]

    def _exit(self):
        """On KeyBoardInterrupt or ESC.
        """

        self._flush()

        sys_exit()

    def _print(self, out):

        stdout.write(out + "\n")
        stdout.flush()

        self._written_lines += 1 + out.count("\n")

    def _return_selection(self):

        self._flush()

        return self._currently_shown[self._current]

    def _render(self):

        if self._info:
            self._print(self._info)

        self._print(self._prompt + self._search)

        if self._search != "" and True:  # TODO: Not for production

            best_matches = get_close_matches(self._search, self._selection, cutoff=self._cutoff)

            for pos, match in enumerate(best_matches):

                best_matches[pos] = match.replace(self._search, self._highlight_color(self._search))  # TODO: Passes object with color

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
