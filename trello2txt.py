#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
# import json
import sys
import json
from jsmin import jsmin
# from collections import OrderedDict
import argparse
import os
from collections import OrderedDict

MAX_TXT_LEN = 45

conf = {}
# A list class containing cards
import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('{asctime}  {name} {levelname:5s} {message}', style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


class __:

        def __init__(self, fmt, *args, **kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
                return self.fmt.format(*self.args, **self.kwargs)


class Card(object):
    _text = None
    _duedate = None
    _color = None

    def __init__(self, text, color, duedate):
        self._text = text
        self._duedate = duedate
        self._color = color

    def getcolor(self):
        return self._color

    def getduedate(self):
        return self._duedate

    def gettext(self):
        return self._text

    def __str__(self):
        return '{} {} {}'.format(self._text, self._color, self._duedate)


class ListModel(object):
    _id = None
    _name = None
    _cards = None
    _errorcode = None

    def __init__(self, id, name):
        self._id = id
        self._name = name
        self._cards = {}
        self._cards['all'] = []

    def __str__(self):

        res = self._name.upper() + "\n"
        for c in self._cards['all']:
            res = res + c + "\n"
        return res.encode('utf-8')

    def getcards(self):
        return self._cards

    def getname(self):
        return self._name

    # conf['BY_DATE'] display
    def getbydate(self):

        res = self._name.upper() + "\n"
        if self._errorcode:
            res = res + self.geterror()
        else:
            res = self._name.upper() + "\n"
            count = 0
            # sort cards by due date
            self._cards['all'].sort(key=lambda c: c.getduedate())
            for c in self._cards['all']:
                # order by date
                logger.debug(__("##################### {}", c))

                prefix = ''
                if (c.getcolor() in conf['COLOR_TO_DISPLAY'].keys()):
                    prefix = conf['COLOR_TO_DISPLAY'][c.getcolor()]

                res = res + prefix + c.gettext() + "\n"
                count = count + 1
                if count >= conf['BY_DATE_MAX_CARDS']:
                    break

        return res

    # conf['BY_COLOR'] display
    def getstrbycolor(self):
        res = self._name.upper() + "\n"
        if self._errorcode:
            res = res + self.geterror()
        else:
            # if no filter
            if len(conf['COLOR_TO_DISPLAY'].keys()) == 0:
                for c in self._cards['all']:
                    res = res + c + "\n"
            # color filter
            else:
                for color in conf['COLOR_TO_DISPLAY'].keys():
                    # cards of this color ?
                    logger.debug(self.getcards)
                    if color in self._cards.keys():
                        for c in self._cards[color]:
                            # add prefix
                            res = res + conf['COLOR_TO_DISPLAY'][color]
                            # add card text
                            res = res + c.gettext() + "\n"
        return res

    def geterror(self):
        return "Error HTTP " + str(self._errorcode) + '\n'

    def seterror(self, errorcode):
        self._errorcode = errorcode

    # add card text to the _card dictionnary
    # key: color, value: [card1_text, card2_text, ...]
    # special entry key: all value: list of all cards text
    def addcard(self, color, text, duedate=None):
        logger.info(__("add card {} {} {} to model".format(color, text, str(duedate))))
        c = Card(text, color, duedate)
        if color in self._cards.keys():
            self._cards[color].append(c)
        else:
            self._cards[color] = [c]
        self._cards['all'].append(c)

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

            if len(c['name']) > MAX_TXT_LEN:
                c['name'] = c[u'name'][:MAX_TXT_LEN] + "..."

            if c['labels']:
                color = c['labels'][0]['color']
            else:
                color = 'unknown'
            logger.debug(c)
            listmodel.addcard(color, c['name'], c['due'])


def exitmain(text, status):

    # open conf file
    if conf['dest']:
        tmpf = open(conf["dest"], 'w+')
        tmpf.writelines(text)
        tmpf.close()

    # cat file on sysout
    if conf['show']:
        for l in text:
            print(l)

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

    trellolists = r.json()
    # print json.dumps(lists, sort_keys=True,indent=4, separators=(',', ': '))

    # key: listname, value: ListModel
    worklist = {}

    logger.info(conf['toanalyse'].values())

    for list in trellolists:
        if list['name'] in conf['toanalyse'].keys():
            worklist[list['name']] = ListModel(list['id'], list['name'])

    # Get cards for each list
    for lm in worklist.values():
        logger.info("########## get cards for " + lm.getname() + " " + lm.getid())
        getopencards(lm)
        logger.info(__("### nb cards: {}", len(lm.getcards()["all"])))

    # Display lists

    # For each list to analyse
    for l in conf['toanalyse'].keys():
        # warn if not found
        logger.info("workin on %s", l)
        if l not in worklist.keys():
            text.append(str(l))
            text.append("WARN list not found in board")
            logger.warn(__("list {} not found in board", l))
        else:
            # print by color
            if conf['toanalyse'][l] == 'BY_COLOR':
                logger.debug("bycolor")
                text.append(worklist[l].getstrbycolor())
            # print by number
            elif conf['toanalyse'][l] == 'BY_DATE':
                logger.debug("bydate")
                text.append(worklist[l].getbydate())
            # add empty line
            text.append(" \n")

    # tolog = [l for l in text]
    # logger.info(tolog)
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
        print("configuration file  does not exist:" + args.conf)
    # else:
    #     conf_file = open(args.conf, 'r')
    #     conf_data = json.load(conf_file)
    #     conf_file.close()

    if shouldquit:
        sys.exit(1)

    with open(args.conf) as file:
        rawconf = file.read()
        tidyconf = jsmin(rawconf)
        logger.debug(tidyconf)
        conf = json.loads(tidyconf, object_pairs_hook=OrderedDict)
        file.close()

    logger.info(conf)
    # execfile(args.conf, conf)

    if args.dest:
        conf['dest'] = args.dest
    else:
        conf['dest'] = None

    conf['show'] = args.show
    main()
