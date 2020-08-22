import argparse, re
import highlighter as h


def difference(original, otherfile):
    '''
    Function to look for differences in two given files
    This program open a file compares to files and looks for the changes. either removed or added code and colors it
    Args:
        original: File to compare to otherfile
        otherfile: file that is an edited version of original
    Returns:
       the changes
    '''
    result = ''
    i = 0
    j = 0
    while i < len(original) or j < len(otherfile):
        if j >= len(otherfile):
            org_line = original[i]
            result += "- " + org_line + "\n"
            i +=  1
        elif i >= len(original):
            mod_line = otherfile[j]
            result += "+ " + mod_line + "\n"
        else:
            org_line = original[i]
            mod_line = otherfile[j]
            if org_line == mod_line:
                result +=  "0 " + org_line + "\n"
            else:
                if org_line in otherfile:
                    result +=  "+ " + mod_line + "\n"
                    i -= 1
                elif org_line not in otherfile:
                    result +=  "- " + org_line + "\n"
                    j -= 1
                else:
                    result += "- " + org_line + "\n"
                    result += "+ " + mod_line + "\n"
        i += 1
        j += 1
    return result 


def get_lines(filename):
    '''
    Function that splits each of the lines in a file into a list
    Args:
        Filename: File to check pattern for
    Returns:
       file_lines: List of file lines
    '''
    file = open(filename,"r").read()
    file_lines = re.split(r"\n", file)
    return file_lines


def make_file(differences):
    '''
    Function to write a new file
    Args:
        differences: Changes made between the two file
    Returns:
       None
    '''

    output = open("output_diff.txt", 'w')
    output.write(differences)
    output.close()


def get_args():
    '''
    A Function to allow for argparse
    Args:
        original: File to compare to otherfile
        otherfile: file that is an edited version of original
    Returns:
       Args
    '''
    parser = argparse.ArgumentParser(description='A program that takes two files as input and outputs a file containing all changes made on the first file to get second file')
    parser.add_argument('original', help='The original version of the file')
    parser.add_argument('otherfile', help='The file that the original file should be otherfile to')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    original = get_lines(args.original)
    otherfile = get_lines(args.otherfile)
    diff = difference(original, otherfile)
    print(diff)
    make_file(diff)