from ast import arg
import os.path
import subprocess
import time
import re
import argparse


def importData():
    cmd = ["lastlog"]
    text = []
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    lines = proc.stdout

    # parsing data
    for line in lines:
        entry = str(line)
        entry = entry.replace("b\'", "")
        entry = entry.replace("\\n\'", "")
        entry = entry.replace("\s+", ",")
        text.append(entry)

    # dictionary to populate data
    dict = {}

    # creating dictionary containing users and attributes
    for entry in text:
        # making a list of all words
        lst = entry.split(" ")

        # removing blanks
        lst = [i for i in lst if i]

        # first item in lst is user
        user = lst[0]

        # removing unwanted characters
        for i in range(len(lst)):
            lst[i] = re.sub(r'[^a-zA-Z0-9.:+_/]+', '', lst[i])

        # list of everything after username
        user_items = lst[1:]
        # adding list to user
        dict[user] = user_items

    # refining dictionary to define attributes
    for key in dict:
        value = dict[key]
        temp_dict = {}

        # for entries that have never logged in
        if('Never' in value):
            temp_dict['logged_in'] = False
            temp_dict['latest'] = 'Never logged in'
            dict[key] = temp_dict.copy()
            continue

        # adding tags to relevant information
        temp_dict['logged_in'] = True
        temp_dict['port'] = value[0]
        temp_dict['from'] = value[1]
        temp_dict['latest'] = value[2:]
        dict[key] = temp_dict.copy()

    # return populated dicitonary
    print(dict)
    return dict


def output(dict):
    print()


def args():
    # Parsing script arguments
    parser = argparse.ArgumentParser(
        description='Report script to retrieve Unity user logs')
    parser.add_argument(
        '-m', '--month', help='Enter month of operation as three letter non-spaced letters (Works only with  --admin)', action='store_true')
    parser.add_argument(
        '-y', '--year', help='Enter year of operation as a non-spaced integer (Works only with  --admin)', action='store_true')
    parser.add_argument('--dryrun', action='store_true',
                        help='Test the script with the dryrun method')
    parser.add_argument('--driver', action='store_true',
                        help='Run the script. Final Step.')
    parser.add_argument('--admin', action='store_true',
                        help='Sends user stats to the admin')

    args = parser.parse_args()
    # Defining argument behavior
    # if (args.dryrun):
    #     dryrun()

    # if (args.driver):
    #     driver()

    # if (args.admin):
    #     if(args.month):
    #         admin('month')
    #     elif (args.year):
    #         admin('year')
    #     else:
    #         admin('month')


def main():
    print('Hello')
    # args()
    output(importData())


if __name__ == "__main__":
    main()

    # Username         Port     From             Latest
    # aryamanagraw_umass_edu pts/81   128.119.202.15   Tue Feb 15 16:29:58 +0000 2022

    # ['pts81', '12811920215', 'Tue', 'Feb', '15', '162958', '0000', '2022']
    # Username         Port     From             Latest
