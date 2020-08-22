import argparse, re
import highlighter as h


def search_pattern(file, pattern, highlight):
    """
    Function to look for given pattern and color the pattern:
    This program open a file and reads the whole thing then colors it
    Args:
        File: File to check pattern for
        Pattern: Pattern to look for
        highlight: Variable to check if pattern was found
    Returns:
       None
    """
    text = open(file, "r")
    all_matches = []
    lines = {}
    line_id = 0
    for line in text:
        pat_match = []
        for pat in pattern:
            match = re.match(r".*{}.*(?:$|\n)".format(pat), line)
            if match != None:
                pat_match.append(match.group())
                lines[line_id] = line
                line_id += 1
        if pat_match:
            all_matches.append(pat_match)

    # print("\nMatches: ", all_matches)
    lines_text = "".join(lines.values())
    if highlight:
        syntax_dict = dict()
        theme_dict = dict()
        i = 31
        for pat in pattern:
            value = "({}).*?".format(pat)
            syntax_dict[pat] = value
            theme_dict[pat] = "0;{}".format(i)
            i += 1
        print(h.highlight_text(syntax_dict, theme_dict, lines_text))


def get_args():
    """
    Function to look for given pattern and color the pattern:
    This program open a file and reads the whole thing then colors it
    Args:
        File: File to check pattern for
        Pattern: Pattern to look for
        highlight: Variable to check if pattern was found
    Returns:
       Args
    """
    parser = argparse.ArgumentParser(description="A grep algorithm")
    parser.add_argument("file", help="Source file to look for pattern")
    parser.add_argument("pattern", nargs="+", help="Pattern to look for")
    parser.add_argument(
        "--highlight", action="store_true", default=False, help=" Highlighter"
    )
    args = parser.parse_args()
    return args


if __name__ == "__main__":
    args = get_args()
    search_pattern(
        args.file, args.pattern, args.highlight
    )  # changed from args.filename to args.file
