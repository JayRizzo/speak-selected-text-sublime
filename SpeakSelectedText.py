"""SpeakSelectedText is a module built for Sublime Text 3.

This module has been expanded upon.

NOTES:
[[slnc 1000]] is used to tell Speech Synthesis how long to wait and is utilized
heavily to wrap my converted text to help annunciate or pronounce words better.

1000 = 1 Second

"""
# =============================================================================
# Built Into the Speech Syth already.
# ♠   &#9824; &spades;    BLACK SPADE SUIT
# ♣   &#9827; &clubs;     BLACK CLUB SUIT
# ♥   &#9829; &hearts;    BLACK HEART SUIT
# ♦   &#9830; &diams;     BLACK DIAMOND SUIT
# =============================================================================
import re
from subprocess import PIPE as PIPERD
from subprocess import Popen

from sublime_plugin import TextCommand


# =============================================================================
# Globals
# =============================================================================
SP_CHAR_ENDING_TIME = 200  # wait .2 second for Special chars.
LINE_ENDING_TIME = 700  # wait 0.7 seconds for new lines.


class SpeakSelectedTextCommand(TextCommand):
    """Use Speech Synthesis to read from Sublime Text 3."""

    def run(self, edit):
        """There is an Intentional Space.

    So when the Speech Synthesis is reading it is properly annunciating,
    or pausing for end of lines, elipsies, periods.  Etc.  Etcetera.
    """
        selections = self.view.sel()
        selection = self.view.substr(selections[0])

        # =====================================================================
        # CLEAN TEXT BEFORE SENDING IT THRU TERMINAL TO SPEECH!!!!!!!!!!!!!!!!!
        # =====================================================================

        # =====================================================================
        # TIMEOUT ADDED FOR LINE ENDINGS & END OF SENTENCES,
        # TO HELP THE SYNTH SEEM MORE HUMAN LIKE.
        # =====================================================================
        new_line_endings = re.compile(r'(\r\n|\n|\.|\.{3})')
        selection = new_line_endings.sub(' [[slnc {}]] '.format(
                                         LINE_ENDING_TIME),
                                         selection)

        # =====================================================================
        # BLOCK QUOTED TEXT (Python Explicit)
        # =====================================================================
        blockquote = re.compile(r'(\'{3}|"{3})')
        selection = blockquote.sub(' Block Quote [[slnc {}]] '.format(
                                   SP_CHAR_ENDING_TIME),
                                   selection)

        # =====================================================================
        # SMART QUOTES.  TIMEOUT ADDED FOR "Emphea sizeing" “QUOTED TEXT”
        # =====================================================================
        custom_open_quotes = re.compile(r'(“\w|"\w)')
        selection = custom_open_quotes.sub(' Quote [[slnc {_Wait}]] '.format(
            _Wait=SP_CHAR_ENDING_TIME * 2), selection)
        custom_end_quotes = re.compile(r'(\w”|\w")')
        selection = custom_end_quotes.sub(' [[slnc {_Wait}]] End Quote'
                                          ' [[slnc {_Wait}]]'.format(
                                              _Wait=SP_CHAR_ENDING_TIME * 2),
                                          selection)

        # =====================================================================
        # Curly Brackets/Braces
        # =====================================================================
        double_curly_brackets = re.compile(r'\{\{\s*\}\}')
        selection = double_curly_brackets.sub('{ Double Curly Brackets }',
                                              selection)

        single_curly_brackets = re.compile(r'\{\s*\}')
        selection = single_curly_brackets.sub('{ Curly Brackets }', selection)

        double_curly_braces = re.compile(r'\(\(\s*\)\)')
        selection = double_curly_braces.sub('{ Double Curly Braces }',
                                            selection)

        single_curly_brace = re.compile(r'\(\s*\)')
        selection = single_curly_brace.sub('{ Curly Brace }', selection)

        # Double Brackets must come first.
        selection = selection.replace('((', ' [[slnc {_Wait}]] Double Open Paren.. [[slnc {_Wait}]] '.format(_Wait=SP_CHAR_ENDING_TIME))  # noqa
        selection = selection.replace('))', ' [[slnc {_Wait}]] Double Close Brace [[slnc {_Wait}]] '.format(_Wait=SP_CHAR_ENDING_TIME))  # noqa
        # Single Brackets
        selection = selection.replace('(', ' [[slnc {_Wait}]] Open Brace [[slnc {_Wait}]] '.format(_Wait=SP_CHAR_ENDING_TIME))  # noqa
        selection = selection.replace(')', ' [[slnc {_Wait}]] Close Brace [[slnc {_Wait}]] '.format(_Wait=SP_CHAR_ENDING_TIME))  # noqa

        # =====================================================================
        # Symbols
        # Using: https://www.w3schools.com/html/html_symbols.asp
        # =====================================================================
        copy_right_symbol = re.compile(r'(\©|&#169;|&copy;)')
        selection = copy_right_symbol.sub('{ COPYRIGHT }', selection)

        reg_symbol = re.compile(r'(\®|&#174;|&reg;)')
        selection = reg_symbol.sub('{ REGISTERED TRADEMARK }', selection)

        reg_trade_symbol = re.compile(r'(\™|&#8482;|&trade;)')
        selection = reg_trade_symbol.sub('{ TRADEMARK }', selection)

        # =====================================================================
        # Keyboard Symbols
        # Convert symbols to text verbiage of symbol as some are reserved.
        # =====================================================================
        selection = selection.replace('`', '{ Backtick }')
        selection = selection.replace(r'|', '{ PIPE }')
        selection = selection.replace(r'\'[^s]', '{ Apostrophe }')  # ignore 's
        selection = selection.replace('\\\\\\', '{ Triple BackSlash }')
        selection = selection.replace('\\\\', '{ Double BackSlash }')
        selection = selection.replace("\\", '{ BackSlash }')
        selection = selection.replace('///', '{ Triple Forward Slash }')
        selection = selection.replace('//', '{ Double Forward Slash }')
        selection = selection.replace('/', '{ Forward Slash }')
        selection = selection.replace('"', '{ Double Quote }')
        selection = selection.replace('-', '{ Dash }')
        selection = selection.replace('_', '{ Underscore }')
        selection = selection.replace('+', '{ Plus Sign }')

        # =====================================================================
        # TODO'z
        # =====================================================================

        # TO ADD LATER
        # $20,400,257 Read the Dollar Sign AFTER the set of ints/floats (cents)
        # https://stackoverflow.com/a/2150417/1896134
        selection = selection.replace('$10B', '{ Ten Billion Dollars }')
        selection = selection.replace('$10M', '{ Ten Million Dollars }')
        selection = selection.replace('$10,000,000', '{ Ten Million Dollars }')
        selection = selection.replace('$10,000', '{ Ten Thousand Dollars }')
        selection = selection.replace('$10', ' Ten Dollars ')

        # Properly Handle Dollar Symbol to Shell as it causes issues.
        # $ has special functionality in BASH and doesn't escape.
        selection = selection.replace(r'$', r' ')

        # €   &#8364; &euro;  EURO SYMBOL
        # ←   &#8592; &larr;  LEFTWARDS ARROW
        # ↑   &#8593; &uarr;  UPWARDS ARROW
        # →   &#8594; &rarr;  RIGHTWARDS ARROW
        # ↓   &#8595; &darr;  DOWNWARDS ARROW

        # =====================================================================
        # Print End Result For Sublime's Console
        # =====================================================================
        print("End Result: {}".format(selection))

        # =====================================================================
        # Send To `SHELL` to process text by Synthesizer
        # =====================================================================
        process = Popen("ps aux | grep say | wc -l",
                        shell=True,
                        stdout=PIPERD,
                        stderr=PIPERD
                        )
        processes, error = process.communicate()
        processes = processes.strip()

        # =====================================================================
        # Run a Second time while reading to make it stop.
        # =====================================================================
        if int(processes) > 2:
            Popen("killall say",
                  shell=True,
                  stdout=PIPERD,
                  stderr=PIPERD
                  )
        else:
            Popen('say "{0}"'.format(selection),
                  shell=True,
                  stdout=PIPERD,
                  stderr=PIPERD)


# print("Selection: {}".format(selection))
