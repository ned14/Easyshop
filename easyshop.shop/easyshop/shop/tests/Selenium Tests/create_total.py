import os
import re

total = open("Total", "w")

for test_file in os.listdir("."):

    if re.search("\d", test_file) is not None:
        temp = open(test_file, "r")
        total.write("".join(temp.readlines()))
    