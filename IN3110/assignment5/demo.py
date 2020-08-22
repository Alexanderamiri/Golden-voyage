import sys
from matplotlib.pyplot import plot
from mnist import *
import numpy as np
import re


class Demo:
    def __init__(self, age, name=None):
        # This is a comment
        self.age = age
        self.name = name
        self.has_name = True

    def print_info(self):
        print("hello")
        print("Name:", self.name)
        print("Age:", self.age)

    def is_adult(self, other):
        dud = False

        while self.has_name:
            if (other.age == self.age) and (other.name == self.name):
                if self.age > 18:
                    print("Good luck with taxes")
                    dud = True
                    break
                else:
                    print("You're not an adult dude")
        return dud
