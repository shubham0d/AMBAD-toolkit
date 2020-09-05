#!/usr/bin/python
import json
import subprocess
import sys
from os import remove
import hashlib
#from pymongo import MongoClient

def savein_db(dbjson):
    myclient = MongoClient("mongodb://localhost:27017/")
    # database
    db = myclient["GFG"]
    # Created or Switched to collection
    # names: GeeksForGeeks
    Collection = db["data"]
    # Loading or Opening the json file
    with open('data.json') as file:
        file_data = json.load(file)
    # Inserting the loaded data in the Collection
    # if JSON contains data more than one entry
    # insert_many is used else inser_one is used
    if isinstance(file_data, list):
        Collection.insert_many(file_data)
    else:
        Collection.insert_one(file_data)

def generate_dbjson(filehash, json_file):
    dbjson = {
    "hash": filehash,
    "events": []
    }
    #print(dbjson)
    target_file = open(json_file, 'r')
    target_data = json.loads(target_file.read())
    target_file.close()
    for i in range(0, len(target_data)):
        if target_data[i]['syscall'] == 'openat':
            dbjson['events'].append({"source": "files", "target": target_data[i]['argument1'] \
            , "permission": target_data[i]['argument2']})
        if target_data[i]['syscall'] == 'open':
            dbjson['events'].append({"source": "files", "target": target_data[i]['argument0'] \
            , "permission": target_data[i]['argument1']})
        if target_data[i]['syscall'] == 'connect':
            if ('sin_addr' in target_data[i]['argument1']):
                dbjson['events'].append({"source": "network", "target": target_data[i]['argument1']['sin_addr']['params'][0]})
        if target_data[i]['syscall'] == 'execve':
            dbjson['events'].append({"source": "process", "target": target_data[i]['argument0']})
    print(dbjson)
    return dbjson


def findhash(filename):
    md5_hash = hashlib.md5()
    a_file = open(filename, "rb")
    content = a_file.read()
    md5_hash.update(content)
    digest = md5_hash.hexdigest()
    return digest

def banner():
    print ("Usage: python", sys.argv[0] , "<executable> <jsonfile>")

def main():
    if len(sys.argv) != 3:
        banner()
        return
    filename = sys.argv[1]
    json_file = sys.argv[2]
    filehash = findhash(filename)
    dbjson = generate_dbjson(filehash, json_file)
    #savein_db()



main()
