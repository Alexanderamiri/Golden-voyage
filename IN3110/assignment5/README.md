# **Coloring and highlighting**

## Highlighter.py
This file contains the highlighting module to highlight a given text with a color
### Usage
``` 
> python highlighter.py naython.syntax naython.theme hello.ny
```
```
A highlighting function to highlight text
Args:
    syntax: Syntax to look for
    theme: Theme to use on the source file with given syntax
    source: File to look into
   Print the source
```


## Grep.py
```
Function to look for given pattern and color the pattern:
This program open a file and reads the whole thing then colors it
Args:
    File: File to check pattern for
    Pattern: Pattern to look for
    highlight: Variable to check if pattern was found
Returns:
   None
```
### Usage
```
 python grep.py --highlight demo_grep.txt somepattern somepat2 sompat3
```

## diff.py
    '''
    Function to write a new file
    Args:
        differences: Changes made between the two file
    Returns:
       None
    '''
### Usage
```
python diff.py original.txt otherfile.txt
```