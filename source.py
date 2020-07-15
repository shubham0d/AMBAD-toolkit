#!/usr/bin/python
import json
import subprocess
import sys
from os import remove

#
# will remove the blacklisted syscalls
#
def filter_blacklist(data):
    # removing the first syscall since its always execve of the process
    data.pop(0)
    # remove the last line which is the exit getstatusoutput
    data.pop(len(data)-1)
    with open('blacklist.txt') as f:
        blacklist = f.read().splitlines()
    print(len(data))
    i = 0
    while i < len(data):
        if data[i]['syscall'] in blacklist:
            data.pop(i)
            i = 0
        i = i + 1

    return data


def formatter(syscall):
    x = {
    "syscall": "John",
    "age": 30,
    "married": True,
    "divorced": False,
    "children": ("Ann","Billy"),
    "pets": None,
    "cars": [
    {"model": "BMW 230", "mpg": 27.5},
    {"model": "Ford Edge", "mpg": 24.1}
    ]
    }
    print(syscall)

def parse_strace():
    data = [json.loads(line) for line in open('input.json', 'r')]
    remove("input.json")
    data = filter_blacklist(data)
    print(data)
    return
    formatter(data[0])
    print(data[0]['syscall'])

# use -f option in strace

def main():
    if len(sys.argv) == 1:
        print ("Usage: python", sys.argv[0] , "<process to execute>")
        return
    process_with_param = sys.argv[1]
    #saving the strace output in rawoutput.log
    subprocess.getstatusoutput("strace -f -o rawoutput.log " + process_with_param)
    subprocess.getstatusoutput("cat rawoutput.log |& b3 > input.json")
    parse_strace()


main()
