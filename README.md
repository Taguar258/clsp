# CLSP

<img src="https://img.shields.io/badge/Version-1.4-orange"> <img src="https://img.shields.io/badge/Linux-yes-green"> <img src="https://img.shields.io/badge/MacOS-yes-green"> <img src="https://img.shields.io/badge/Windows-yes-green"><!-- <img src="https://img.shields.io/badge/FreeBSD-yes-green">-->

CLSP short for **C**ommand **L**ine **S**election **P**rompt, is a by fzf inspired, minimalistic, and fast to navigate single choice prompt.


```python
from clsp import select


user_choice = select([1, 2, 3], info="Please pick a number:")

print("You selected:")
print(user_choice)
```

![Preview](https://raw.githubusercontent.com/Taguar258/clsp/main/docs/preview.gif)

CLSP is designed to be user-friendly, minimal, and very easy to understand.

Due to it's search function, it supports large lists and spares the end-user unnecessary frustration.

It's especially useful if you'd like the user to choose between files, numbers, country codes, and much more.


## Documentation


```python
# CLSP can be easily imported using:
from clsp import select

# You can then show the actual prompt by calling the select function while passing a list type as the positional argument.

user_choice = select(["Choose me!", "Dare to choose me!"])

# You can navigate using the arrow key up and the arrow key down while pressing enter to confirm your selection.
```

You can provide additional key arguments for further configuration:

|      Name       | Type  |                                  Description                                        |
| --------------- | ----- | ----------------------------------------------------------------------------------- |
| title           | STR   | Information shown above the prompt.                                                 |
| prompt          | STR   | Text in front of user input.                                                        |
| search          | STR   | Pre-insert text into the input prompt.                                              |
| current         | INT   | Index as the default selection.                                                     |
| rows            | INT   | Amount of choices at a time.                                                        |
| cutoff          | FLOAT | Precision of search. (0 < x < 1).                                                   |
| amount_results  | INT   | The maximum amount of search results to return.                                     |
| highlight_color | STR   | Highlight color for search (black, red, green, yellow, blue, magenta, cyan, white). |
| full_exit       | BOOL  | Exit completely or pass None on KeyBoardInterrupt or ESC.                           |
| ignore_warnings | BOOL  | Ignore warnings.                                                                    |

```python
# The function 'select' will return a Selection object which holds following attributes:

print(f"Selected value: {user_choice.value}")
# > "Choose me!" or "Dare to choose me!"

print(f"Index: {user_choice.index}")
# > 0 or 1

if user_choice.search:

	print(f"Search-Query: {user_choice.search}")
	# > For example 'Dare'

	print(f"Search Result: {user_choice.search_result}")
	# > For example ["Dare to chose me!"]
```

