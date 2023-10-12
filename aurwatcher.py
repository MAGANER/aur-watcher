#!/usr/bin/env python3
#Usage example: aurwatcher p=emacs

import requests
import json
import sys
from functools import reduce


def print_help():
    options = '''
    aurwatcher looks for packages in AUR.\n\n
    
    available options:\n
    p - package\n
    d - description\n
    m - maintainer\n
    n - name\n\n

    Usage example: aurwatcher p=emacs d=plugin\n
    Finds every package which name contains emacs and description contains plugin as substring.\n
    '''
    print(options)
    

def parse_arguments():
    '''returns the hash-table of arguments'''
    
    #at least there is only one argument - the script name
    if len(sys.argv) == 1:
        print("error: not enough arguments")
        print_help()
        exit(0)
    
    table = {} #key is argument name, value is key's value

    #p - package
    #d - description
    #m - maintainer
    #n - name
    available_keys = "pdmn"

    for arg in sys.argv[1:]:
        #try to parse argument
        try:
            left, right = arg.split("=")
        except ValueError:
            print("incorrect format of argument! it should be a=b")
            print_help()
            exit(-1)

        #key should exist as available key and it must not be added already
        if left in available_keys and left not in table.keys():
            table[left] = right
        else:
            print("key is used already or doesn't exist!")
            print_help()
            exit(-1)
    
    return table
    
def sort_response(response,args):    
    #switch key from args to correct key that is contained within repsonse
    switcher = {
        "d":"Description",
        "m":"Maintainer",
        "n":"Name"
    }

    sorted = []

    keys = list(args.keys())
    keys.remove("p")#this key isn't used

    counter = 0
    for element in response["results"]:
        for a in keys:
            right_option = switcher[a]
            value_to_find = args[a]

            check_value = element[right_option]
            if check_value is not None and value_to_find in check_value:
                counter+=1

        if counter == len(keys): sorted.append(element)
        counter = 0

    return sorted


args = parse_arguments()
if "p" not in args.keys():
    print("no package to look for...")
    exit(-1)


request = "https://aur.archlinux.org/rpc/?v=5&type=search&arg={}".format(args["p"])
response = requests.get(request)

if response.status_code != 200:
    print("can not access AUR...")
    exit(0)

response = dict(json.loads(response.text))


#if there is only one key then it's p, because p is required key, other ones are optional
#so just pass all results, otherwise sort it
if len(args.keys()) != 1:
    response = sort_response(response,args)
else:
    response = response["results"]

if not response:
    print("nothing was found...")


for id,item in enumerate(response):
    print("found item #{}".format(id))
    print("-"*40)
    for k in item.keys():
        print("{}:{}".format(k,item[k]))
    print("-"*40)
