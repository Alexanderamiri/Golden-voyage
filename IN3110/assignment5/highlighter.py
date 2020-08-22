import argparse
import re


def highlight_text(syntax, theme, source):
    """
    A highlighting function to highlight text
    Args:
        syntax: Syntax to look for
        theme: Theme to use on the source file with given syntax
        source: File to look into
    """
    for key, value in syntax.items():
        source = re.sub(
            r"({})".format(value),
            color_text(theme[key], r"\1"),
            source,
            flags=re.MULTILINE,
        )
    return source  # returns source instead of printing it


def color_text(color, text):
    """
    A function to color a text with a certain color
    Args:
        color: color to use
        text: text to color

    Returns:
       the colored text
    """
    start_code = "\033[{}m".format(color)
    end_code = "\033[0m"
    return start_code + text + end_code


def get_args():
    """
    A Function to allow for argparse
    Args:
        syntax: Syntax to look for
        theme: Theme to use on the source file with given syntax
        source: File to look into
    Returns:
       arguments inputed
    """
    parser = argparse.ArgumentParser(
        description="A highlighter that highlights given file"
    )
    parser.add_argument("syntax", help="This file Includes the syntax")
    parser.add_argument("theme", help="This file should tell which theme")
    parser.add_argument(
        "sourcefile", help="This is the source file to be colored"
    )
    args = parser.parse_args()
    return args


def get_dictionaries(syntax, theme):

    """
    Function to read the syntax and theme of given files
    Args:
        syntax: Syntax ofile
        theme: Theme file
    Returns:
       Syntax dict and theme dict
    """
    syntaxdict = dict()
    themedict = dict()
    for line in syntax:
        line = line.strip()
        value, key = line.split(": ")
        syntaxdict[key] = value[1:-1]
    for line in theme:
        line = line.strip()
        key, value = line.split(": ")
        themedict[key] = value
    return syntaxdict, themedict


if __name__ == "__main__":
    args = get_args()
    syntaxfile = open(args.syntax, "r")
    themefile = open(args.theme, "r")
    sourcefile = open(args.sourcefile, "r").read()
    syntax, theme = get_dictionaries(syntaxfile, themefile)

    print(highlight_text(syntax, theme, sourcefile))
