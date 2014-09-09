#!/usr/bin/env python

import re
import os
import sys


def splitter(file):
    base = os.path.splitext(file)[0]
    categorized = [
        open(base + "_0.txt", "w"),
        open(base + "_1.txt", "w"),
        open(base + "_2.txt", "w"),
        open(base + "_3.txt", "w"),
        open(base + "_4.txt", "w"),
    ]
    # http://effbot.org/zone/readline-performance.htm
    with open(file, "r") as f:
        while 1:
            lines = f.readlines(1000000)
            if not lines:
                break
            for line in lines:
                matches = re.match(r'(\d+)\t(\d+)\t([^\t]+)\t(\d)', line)
                if matches:
                    categorized[int(matches.group(4))].write(matches.group(3) + "\n")

    categorized[0].close()
    categorized[1].close()
    categorized[2].close()
    categorized[3].close()
    categorized[4].close()

if __name__ == '__main__':
    splitter(sys.argv[1])
