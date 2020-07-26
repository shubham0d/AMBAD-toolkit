#!/usr/bin/python
import json
import subprocess
import sys
from os import remove
from comparison import comparison_main
from time import sleep
#
# will remove the blacklisted syscalls
# TODO: add comment support in blacklist file
#
def filter_data(data):
    # removing the first syscall since its always execve of the process
    data.pop(0)
    # remove the last line which is the exit getstatusoutput
    data.pop(len(data)-1)
    # remove the non SYSCALL type data
    i = 0
    while i < len(data):
        if data[i]['type'] != "SYSCALL":
            data.pop(i)
            i = 0
        i = i + 1
    # remove the syscall present in blacklist
    with open('blacklist.txt') as f:
        blacklist = f.read().splitlines()
    f.close()
    i = 0
    while i < len(data):
        if data[i]['syscall'] in blacklist:
            data.pop(i)
            i = 0
        i = i + 1
    return data


def formatter(entry):
    no_of_args = len(entry['args'])

    if sys.argv[1] == "checker":
        entry_list = {
        "syscall": entry['syscall'],
        "check_args": True,
        "next_call_is_preceding": False
        }
    else:
        entry_list = {
        "syscall": entry['syscall']
        }

    #Parsing the arguments
    for i in range(0, no_of_args):
        # To convert the arg of type dict in a list
        if (type(entry['args'][i]) is dict):
            # if name, value pair is present in dict
            if entry['args'][i].get('name') and entry['args'][i].get('value'):
                flag_arg = []
                print(type(entry['args'][i]['value']))
                # TODO: fix the issue when value type is int
                if type(entry['args'][i]['value']) is list:
                    for j in range(0, len(entry['args'][i]['value'])):
                        if j == 0:
                            flag_0th_string = entry['args'][i]['name']+entry['args'][i]['value'][0]
                            flag_arg.append(flag_0th_string)
                        else:
                            flag_arg.append(entry['args'][i]['value'][j])
                #elif if type(entry['args'][i]['value']) is int:
                    #flag_arg.append(entry['args'][i]['value'])
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

def save_json_output(data):
    if sys.argv[1] == "checker":
        file_handle = open('checker.json', 'w')
    else:
        file_handle = open('target_dump.json', 'w')
    #json.loads(s, kwds)
    #checker_file.write(json.dumps(data, indent=1))
    file_handle.write(json.dumps(data, indent=0))
    file_handle.close()
    return



def parse_strace():
    data = [json.loads(line) for line in open('input.json', 'r')]
    remove("input.json")
    data = filter_data(data)
    #print(data[0])
    for i in range(0, len(data)):
        data[i] = formatter(data[i])
    #print(json.dumps(data, indent=1))
    save_json_output(data)
    #print(data[0]['args'][1])




def banner():
    print ("Usage: python", sys.argv[0] , "<checker|target> <cmd inside quotes>")

def main():
    if len(sys.argv) != 3:
        banner()
        return
    process_with_param = sys.argv[2]
    if(sys.argv[1] not in ['checker', 'target']):
        banner()
        return
    #saving the strace output in rawoutput.log
    subprocess.getstatusoutput("strace -f -o rawoutput.log " + process_with_param)
    print("System calls captured!!")
    sleep(2)
    # for ubuntu use following
    # subprocess.Popen(["/bin/bash", "-c" , "cat rawoutput.log |& b3 > input.json"])
    subprocess.getstatusoutput("cat rawoutput.log |& b3 > input.json")
    print("System calls saved!!")
    sleep(2)
    parse_strace()
    if (sys.argv[1] == 'target'):
        result = comparison_main()
        if result == True:
            print('Target Matched!!')
        else:
            print('Target differs!!')
    else:
        print('checker.json generated')

main()
