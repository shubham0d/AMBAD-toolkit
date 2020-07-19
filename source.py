#!/usr/bin/python
import json
import subprocess
import sys
from os import remove

#
# will remove the blacklisted syscalls
# TODO: add comment support in blacklist file
#
def filter_blacklist(data):
    # removing the first syscall since its always execve of the process
    data.pop(0)
    # remove the last line which is the exit getstatusoutput
    data.pop(len(data)-1)
    with open('blacklist.txt') as f:
        blacklist = f.read().splitlines()
    i = 0
    while i < len(data):
        if data[i]['syscall'] in blacklist:
            data.pop(i)
            i = 0
        i = i + 1
    return data


def formatter(entry):
    no_of_args = len(entry['args'])
    i = '10'
    entry_list = {
    "syscall": entry['syscall'],
    "check_args": True,
    "next_call_is_preceding": True,
    "multi_instance": False
    }

    #Parsing the arguments
    for i in range(0, no_of_args):
        # To convert the arg of type dict in a list
        if (type(entry['args'][i]) is dict):
            # if name, value pair is present in dict
            if entry['args'][i].get('name') and entry['args'][i].get('value'):
                flag_arg = []
                for j in range(0, len(entry['args'][i]['value'])):
                    if j == 0:
                        flag_0th_string = entry['args'][i]['name']+entry['args'][i]['value'][0]
                        flag_arg.append(flag_0th_string)
                    else:
                        flag_arg.append(entry['args'][i]['value'][j])
                entry_list['argument'+str(i)] = flag_arg
            else:
                entry_list['argument'+str(i)] = entry['args'][i]
        # When arg type is int.
        # TODO: Later add support for hex arguments(current decimal)
        elif (type(entry['args'][i]) is int):
            entry_list['argument'+str(i)] = entry['args'][i]
        else:
            entry_list['argument'+str(i)] = entry['args'][i]
    #y = json.loads(x)
    #print(entry_list)
    return entry_list

def parse_strace():
    data = [json.loads(line) for line in open('input.json', 'r')]
    remove("input.json")
    data = filter_blacklist(data)
    for i in range(0, len(data)):
        data[i] = formatter(data[i])
    print(data)
    #print(data[0]['args'][1])

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
