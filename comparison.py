#!/usr/bin/python
import json
from os import listdir
# only god knows how this funtion works;)
def compare_calls(checker_data, target_data):
    # a list to keep track of which element is matched and which doesn't
    sequence_matched = []
    target_offset = 0
    for i in range(0,len(checker_data)):
        checker_call = checker_data[i]
        # when next_call_is_preceding is set on previous call, check to the call point by target_offset
        # if its not same then two checker and target are not having same sequence.
        if i != 0 and checker_data[i-1]['next_call_is_preceding'] == True:
            target_call = target_data[target_offset]
            target_offset = target_offset + 1;
            if checker_call['syscall'] == target_call['syscall']:
                if checker_call['check_args'] == True:
                    arg_matched = False
                    # arguments startes from 3th element in checker call
                    # change the starting value of range if you have added or removed a new tag in checker json entries
                    for k in range(3, len(checker_call)):
                        if list(checker_call.items())[k][0] in target_call:
                            # if checker's argument[i] == target's argument[i]
                            if checker_call[list(checker_call.items())[k][0]] == target_call[list(checker_call.items())[k][0]]:
                                arg_matched = True
                            else:
                                arg_matched = False
                                break
                        else:
                            arg_matched = False
                            break
                    if arg_matched == True:
                        sequence_matched.append(True)

                    else:
                        sequence_matched.append(False)
                        break
                else:
                    sequence_matched.append(True)
            else:
                sequence_matched.append(False)
                break

        else:
            for j in range(target_offset, len(target_data)):
                target_call = target_data[j]
                target_offset = target_offset + 1
                # if the calls are same
                if checker_call['syscall'] == target_call['syscall']:
                    if checker_call['check_args'] == True:
                        arg_matched = True
                        # arguments startes from 4th element in checker call
                        # change the starting value of range if you have added or removed a new tag in checker json entries
                        for k in range(3, len(checker_call)):
                            if list(checker_call.items())[k][0] in target_call:
                                # if checker's argument[i] == target's argument[i]
                                #print("ffffffffff", target_call[list(checker_call.items())[k][0]])
                                if checker_call[list(checker_call.items())[k][0]] != target_call[list(checker_call.items())[k][0]]:
                                    arg_matched = False
                                    break
                            else:
                                arg_matched = False
                                break
                        if arg_matched == True:
                            sequence_matched.append(True)
                            break
                        else:
                            # if its a last element then set sequence_matched to false
                            if target_offset == len(target_data)-1:
                                sequence_matched.append(False)
                                break
                    else:
                        sequence_matched.append(True)
                        break
                else:
                    # if we reach end of target_data list
                    if target_offset == len(target_data)-1:
                        sequence_matched.append(False)
                        break
    if False in sequence_matched:
        return False
    else:
        return True

def comparison_main():
    signatures_files = listdir("./Signatures")
    if len(signatures_files) == 0:
        print("No signatures found\n Exiting")
        exit()
    target_file = open('target_dump.json', 'r')
    target_data = json.loads(target_file.read())
    target_file.close()
    matched = False
    for i in range(0, len(signatures_files)):
        if signatures_files[i][-4:] == 'json':
            detector_file = open('Signatures/'+signatures_files[i], 'r')
            detector_data = json.loads(detector_file.read())
            detector_file.close()
            if compare_calls(detector_data, target_data):
                print("Detector ", signatures_files[i], " - Matched")
                matched = True
            else:
                print("Detector ", signatures_files[i], " - Differs")

    return matched
