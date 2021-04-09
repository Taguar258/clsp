from difflib import get_close_matches
from sys import exit as sys_exit
from sys import stdout

from blessed import Terminal


class Selection:
    """ Selection object passed as output of Selection Prompt.
        Contains additional information.

    :attr value: User selection.
    :attr index: Index of given input list.  (TODO)
    :attr search: Search query of user.

    """

    def __init__(self, value, search=None):

        self.value = value
        self.index = None  # TODO
        self.search = search

    def __str__(self):

        return self.value

    def __repr__(self):

        return f"<Selection {self.value}>"


class SelectionPrompt:

    def __init__(self, selection, info="", prompt="> ", search="", current=0, rows=4, cutoff=0.15, highlight_color="yellow", full_exit=True):
        """ Prompt for user selection. # TODO: Go through class again and rethink + Redo comments

        Arguments
        ---------
        :arg selection (LIST): The available choices to display the user.


        Keyword Arguments
        -----------------
        :arg info (STR): Information shown above prompt. / Prompt title.
        :arg prompt (STR): Text in front of user input.
        :arg search (STR): Pre-insert text into the input prompt.
        :arg current (INT): Current item of list as default selection.
        :arg rows (INT): Amount of visible choices.
        :arg cutoff (INT): Search precision.
        :arg highlight_color (STR): Search higlight color.
        :arg full_exit (BOOL): Exit completely or pass None on KeyBoardInterrupt or ESC.

        """

        # Variables | Static variables
        self._term = Terminal()

        self._key_timeout = 5

        self._highlight_color = {"black": self._term.black, "red": self._term.red, "green": self._term.green, "yellow": self._term.yellow, "blue": self._term.blue, "magenta": self._term.magenta, "cyan": self._term.cyan, "white": self._term.white}[highlight_color]  # TODO: Find better solution

        self._default_cursor_pos = {"x": len(prompt),
                                    "y": info.count("\n") + 1 if info else 0}

        # Variables | Static User Variables
        self._selection = [str(option) for option in selection]
        self._info = info
        self._prompt = prompt
        self._rows = rows
        self._cutoff = cutoff
        self._full_exit = full_exit

        # Variables | Dynamic variables (Terminal State)
        self._cursor_pos = None
        self._written_lines = 0

        # Variables | Dynamic variables (List)
        self._reset_current_selection(self._selection, current=current)
        self.return_placeholder = None

        # Variables | Dynamic variables (Input)
        self._search = search
        self._searching = False  # TODO: Find better solution to determin end of search.

    def show(self):
        """ Entry Point | Main Loop
        """

        with self._term.cbreak():

            while True:

                self._render()

                # KEY BINDINGS
                key = self._term.inkey(timeout=self._key_timeout)

                self._key_bindings(key)

                self._flush()

                # Return value
                if self.return_placeholder is not None:

                    return self.return_placeholder

    def _exit(self):
        """ On KeyBoardInterrupt or ESC.
        """

        self._flush()

        if self._full_exit:

            sys_exit()

    def _print(self, out):
        """ Internal way of displaying content while counting all the written lines.
        """

        stdout.write(out + "\n")
        stdout.flush()

        self._written_lines += 1 + out.count("\n")

    def _flush(self):
        """ Clear the screen completely.

        Alternative would be overwriting, though it does not clear remaining characters.
        - self._reset_cursor instead of self._flush
        """

        self._reset_cursor()

        stdout.write(self._term.clear_eos)
        stdout.flush()

    def _key_bindings(self, key):
        """ Function for all the key bindings.
        """

        if key.name == "KEY_ESCAPE":

            self._exit()

        elif key.name == "KEY_ENTER":

            self._return_selection()

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

    def _move_cursor(self, cursor_x, cursor_y):  # TODO: Rework function to go back to 0, 0 and then to pos
        """ Change the cursor position.

        The x position is mostly 0 after the first stdout writes.
        Therfore we can assume x to be 0 and set y to the amount of printed lines.
        The y position is a lot more unpredictable than the x position.
        Therefore we can focus on y. (TODO: Rewrite info)
        """

        # Reset position variable if x pos not known
        if self._cursor_pos is None:

            self._cursor_pos = {"x": 0, "y": self._written_lines}

        # Calculate and move delta position
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

    def _reset_cursor(self):  # TODO: !! Should be standard and before every move
        """ Reset the cursor position and written lines.
        """

        self._move_cursor(0, 0)

        self._written_lines = 0
        self._cursor_pos = None

    def _render(self):
        """ Render the interface to the terminal.
        """

        # Display the info
        if self._info:
            self._print(self._info)

        # Display the input prompt
        self._print(self._prompt + self._search)

        # Display the list
        self._refresh_currently_shown()

        for pos, option in enumerate(self._currently_shown):

            option_msg = self._term.reverse(option) if pos + self._current_position[0] == self._current else option
            self._print(option_msg)

        # Move the cursor to the input prompt.
        self._reset_cursor()  # TODO: (Strange Issue) Cursor position changes, needs further investigation
        """
        Maybe the x does not get updated on key press but does not change anything.
        """

        self._move_cursor(self._default_cursor_pos["x"] + len(self._search), self._default_cursor_pos["y"])

    def _reset_current_selection(self, selection, current=0):

        self._current_selection = selection
        self._current = current
        self._current_position = [self._current, (self._rows + self._current)]

        # self._currently_shown = self._current_selection[self._current:(self._rows + self._current)]

    def _refresh_currently_shown(self):
        """ Update shown list.
        """

        if self._search != "":

            self.best_matches = get_close_matches(self._search, self._selection, cutoff=self._cutoff)

            best_matches_hl = [match.replace(self._search, self._highlight_color(self._search)) for match in self.best_matches]

            self._reset_current_selection(best_matches_hl)

            self._searching = True

        elif self._searching:

            self._reset_current_selection(self._selection)

            self._searching = False

        self._currently_shown = self._current_selection[self._current_position[0]:self._current_position[1]]

    def _navigate_menu(self, up_or_down):
        """ Navigates Menu one item down or up

        :arg up_or_down (INT): -1 for up and 1 for down.

        """

        # Check for list border
        if self._current == 0 and up_or_down < 0 or \
           self._current == len(self._current_selection) - 1 and up_or_down > 0:

            return

        # Change current
        if up_or_down < 0:

            self._current -= 1

        elif up_or_down > 0:

            self._current += 1

        # Change menu view point
        if self._current == self._current_position[0] - 1 and \
           up_or_down < 0:

            self._move_list_view(-1)

        elif self._current == self._current_position[1] and \
                up_or_down > 0:

            self._move_list_view(1)

    def _move_list_view(self, up_or_down):
        """ Navigates Menu view

        :arg up_or_down (INT): -1 for up and 1 for down.

        """

        self._current_position[0] += up_or_down
        self._current_position[1] += up_or_down

    def _return_selection(self):
        """ Return the user selection whilest also adding additional info.
        """

        self._flush()

        # Decolorize search output
        return_value_nhl = self._current_selection[self._current].replace(self._highlight_color(self._search), self._search)

        # Create Object
        return_value = Selection(return_value_nhl, search=self._search)  # TODO: Add index of selection

        self.return_placeholder = return_value


def select(selection, **kwargs):
    """ TODO: Add info
    """

    prompt = SelectionPrompt(selection, **kwargs)

    try:

        user_selection = prompt.show()

    except KeyboardInterrupt:

        prompt._exit()

    return user_selection
