#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
# import json
import sys
# from collections import OrderedDict
import argparse
import os
from dao.trellodao import TrelloBoardDAO


conf = {}
# A list class containing cards


class ListModel(object):
    _id = None
    _name = None
    _cards = None
    _errorcode = None

    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._cards = {}
        self._cards[u'all'] = []

    def __str__(self):

        res = self._name.upper() + u"\n"
        for c in self._cards[u'all']:
            res = res + c + u"\n"
        return res.encode('utf-8')

    # conf['BY_NUMBER'] display
    def getfirst(self):

        res = self._name.upper() + u"\n"
        if self._errorcode:
            res = res + self.geterror()
        else:
            res = self._name.upper() + u"\n"
            count = 0
            for c in self._cards[u'all']:
                for td in conf['COLOR_TO_DISPLAY'].keys():
                    if self._cards[td] is not None:
                        if c in self._cards[td]:
                            res = res + conf['COLOR_TO_DISPLAY'][td]
                res = res + c + u"\n"
                count = count + 1
                if count >= conf['BY_NUMBER_COUNT']:
                    break

        return res.encode('utf-8')

    # conf['BY_COLOR'] display
    def getstrbycolor(self):
        res = self._name.upper() + u"\n"
        if self._errorcode:
            res = res + self.geterror()
        else:
            # if no filter
            if len(conf['COLOR_TO_DISPLAY'].keys()) == 0:
                for c in self._cards[u'all']:
                    res = res + c + u"\n"
            # color filter
            else:
                for td in conf['COLOR_TO_DISPLAY'].keys():
                    # cards of this color ?
                    if td in self._cards.keys():
                        for c in self._cards[td]:
                            # add prefix
                            res = res + conf['COLOR_TO_DISPLAY'][td]
                            # add card text
                            res = res + c + u"\n"

        return res.encode('utf-8')

    def geterror(self):
        return "Error HTTP " + str(self._errorcode) + u'\n'

    def seterror(self, errorcode):
        self._errorcode = errorcode

    # add card text to the _card dictionnary
    # key: color, value: [card1_text, card2_text, ...]
    # special entry key: all value: list of all cards text
    def addcard(self, color, text):
        if color in self._cards.keys():
            self._cards[color].append(text)
        else:
            self._cards[color] = [text]
        self._cards[u'all'].append(text)

    def getid(self):
        return self._id

# get open cards of a list


def getopencards(listmodel):
    r = requests.get(''.join(['https://api.trello.com/1/lists/',
                              listmodel.getid(),
                              '/cards?&key=',
                              conf['appkey'],
                              '&token=',
                              conf['token']]))

    if r.status_code != 200:
        listmodel.seterror(r.status_code)
    else:
        cards = r.json()

        for c in cards:
            if c[u'labels']:
                color = c[u'labels'][0][u'color']
            else:
                color = u'unknown'
            listmodel.addcard(color, c[u'name'])


def exitmain(text, status):

    # open conf file
    if conf['dest']:
        tmpf = open(conf["dest"], 'w+')
        tmpf.writelines(text)
        tmpf.close()

    # cat file on sysout
    if conf['show']:
        for l in text:
            print l

    sys.exit(status)


def main():

    text = []

    # get all lists
    r = requests.get(''.join(['https://api.trello.com/1/boards/',
                              conf['board'],
                              '/lists/open?&key=',
                              conf['appkey'],
                              '&token=',
                              conf['token']]))
    if r.status_code != 200:
        text.append("GENERAL ERROR unable to fetch board lists:" + str(r.status_code) + u'\n')
        exitmain(text, 1)

    lists = r.json()
    # print json.dumps(lists, sort_keys=True,indent=4, separators=(',', ': '))

    # key: listname, value: ListModel
    worklist = {}

    for list in lists:
        if list['name'] in conf['toanalyse'].keys():
            worklist[list['name']] = ListModel(list['id'], list['name'])

    # Get cards for each list
    for wl in worklist.values():
        getopencards(wl)

    # Display lists

    # For each list to analyse
    for l in conf['toanalyse'].keys():
        # warn if not found
        if l not in worklist.keys():
            text.append(l)
            text.append("WARN list not found in board")
        else:
            # print by color
            if conf['toanalyse'][l] == conf['BY_COLOR']:
                text.append(worklist[l].getstrbycolor())
            # print by number
            elif conf['toanalyse'][l] == conf['BY_NUMBER']:
                text.append(worklist[l].getfirst())
            # add empty line
            text.append(" \n")
    exitmain(text, 0)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Output a trello board to text " +
                                                  "with some filtering available"))
    parser.add_argument('conf', help='configuration file', type=str)
    parser.add_argument('--dest', '-d', help='destination file', type=str)
    parser.add_argument('--show', '-s', help='show result on stdout', action="store_true")
    args = parser.parse_args()
    shouldquit = False

    if not os.path.exists(args.conf):
        shouldquit = True
        print "configuration file  does not exist:" + args.conf
    # else:
    #     conf_file = open(args.conf, 'r')
    #     conf_data = json.load(conf_file)
    #     conf_file.close()

    if shouldquit:
        sys.exit(1)

    execfile(args.conf, conf)
    if args.dest:
        conf['dest'] = args.dest
    else:
        conf['dest'] = None

    conf['show'] = args.show
    main()
