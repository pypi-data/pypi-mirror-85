'''
Functionality to start words in Plover.
'''

from typing import List
from plover.translation import Translation
from plover.formatting import _Context, _Action

DELIM_ARGS = " | "

prefixes = (
	"", "-", "¿", "?", "(", "'", "/", "@", "\"",
	"ante", "anti", "auto", "bi", "des", "dis", "eco", "equi", "extra",
	"hidro", "in", "inter", "macro", "micro", "multi",
	"pre", "pro", "psico", "re",
	"socio", "sub", "super", "tecno", "tiflo"
)


def initial(context: _Context, args: str) -> _Action:
	'''
	Meta to start a word in Plover.

	:param context: The context of actions in Plover.
	:param args: Arguments provided to the meta as a |-delimited string.
				Piece 1: The string used when prev_attach is False.
				Piece 2: The string used when prev_attach is True.

	:return: The next action for Plover to perform.
	'''

	# Process input
	output = ''
	translations: List[Translation] = context.previous_translations[-1:]
	for translation in translations:
		actions: List[_Action] = reversed(translation.formatting)
		for action in actions:
			try:
				output = output + action.text
			except:
				output = ""

	# Create the new action
	action: _Action = context.new_action()
	for prefix in prefixes:
		if output == prefix:
			action.text = args.split(DELIM_ARGS)[0]
			return action
	if action.prev_attach and action.next_case is None:
		action.text = args.split(DELIM_ARGS)[-1]
	else:
		action.text = args.split(DELIM_ARGS)[0]
	return action
