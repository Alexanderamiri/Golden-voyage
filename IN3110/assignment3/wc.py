import sys, glob


def wordcount(x):
    a = 0
    c = 0
    file = open(x)
    list = []
    for line in file:
        word = line.split(" ")
        list = word
        c += len(line)
        a += 1
    wc = len(list)
    print(a, wc, c, x)


p = sys.argv
if p[1] == "*":
    k = []
    for file in glob.glob("*.txt"):
        k.append(file)
    p = k
    for i in p:
        wordcount(i)
else:
    for i in p[1:]:
        wordcount(i)
