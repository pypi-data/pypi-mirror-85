Plover Start words
##################

This plugin provides a meta for Plover, so we can choose the output produced deppending on the last typed text.

Usage
*****

# initial.json
{
"STROke": "{:initial:textStartingNextWord | textFollowingPreviousFragment}"

...
}


API
***

API can be manipulated via `Python dictionaries <https://github.com/benoit-pierre/plover_python_dictionary>`_

For example:

# single.py
from plover_start_words import meta

meta.prefixes = ("", "foo", "var")

LONGEST_KEY = 1


def lookup(key):
	raise KeyError


Versioning
**********

We use `SemVer <https://semver.org/>`_
