#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
# import json
import sys
# from collections import OrderedDict
import argparse
import os
from dao.trellodao import TrelloBoardDAO
from objects.trelloutils import TrelloUtils

conf = {}


def listexists(listname, lists):
    res = None
    for l in lists:
        if l[u'name'] == listname:
            res = l
            break
    return res


def cardexists(card, cardlist, prefix):
    res = None
    for c in cardlist:
        if c[u'name'] == ''.join([prefix, card[u'name']]):
            res = c
            break
    return res


def main():

    slavedao = TrelloBoardDAO(conf[u'appkey'], conf[u'token'], conf[u'slaveboard'])
    masterdao = TrelloBoardDAO(conf[u'appkey'], conf[u'token'], conf[u'masterboard'])
    prefix = u'[kr]'

    # get master lists
    masterlists = masterdao.getLists()

    # create (or reopen) list in slave if not exists
    slavelists = slavedao.getLists()

    # cards that have been synced while computing masterlist
    syncslavecards = []

    # for each master list
    for ml in masterlists:
        print u"\n---------------------------------------"
        print u"compute master list:", ml[u'name'].encode('utf-8')
        print u"---------------------------------------"

        # if list exists in slave ?
        slavelist = listexists(ml[u'name'], slavelists)
        if slavelist is not None:
            print u"* ", ml[u'name'].encode('utf-8'), u" exists in slaveboard"

            # if it's not open
            if slavelist[u'closed']:
                print "* ", ml[u'name'].encode('utf-8'), u" is closed in slaveboard"
                # open it
                slavedao.openList(slavelist[u'id'])
                print "* ", ml[u'name'].encode('utf-8'), u" is now open in slaveboard"
        else:
            print u"* ", ml[u'name'].encode('utf-8'), u" does not exists in slaveboard"
            # else create it
            slavelist = slavedao.createList(ml[u'name'])
            print u"* ", ml[u'name'].encode('utf-8'), u" is now created in slaveboard"

        # for each open card in master list
        mastercards = masterdao.getOpenCards(ml[u'id'])
        slavecards = slavedao.getOpenCards(slavelist[u'id'])
        for mc in mastercards:
            print u"compute master card:", mc[u'name'].encode('utf-8'), u"--"

            # if not exists in slave
            sc = cardexists(mc, slavecards, prefix)
            if sc is None:
                print u"** ", mc[u'name'].encode('utf-8'), u"does not exist in slave board"

                # create it
                sc = slavedao.copyCardToList(mc, slavelist[u'id'], prefix)
                print u"** ", mc[u'name'].encode('utf-8'), u"is now created in slave board"
            # if exists in slave
            else:
                print u"** ", mc[u'name'].encode('utf-8'), u"exists in slave board"
                # compare last modification date
                # if master fresher than slave
                if mc[u'dateLastActivity'] > sc[u'dateLastActivity']:
                    print u"** ", mc[u'name'].encode('utf-8'), u"needs to be refresh from master"

                    # delete slave card
                    slavedao.deleteCard(sc['id'])
                    print "** ", mc['name'].encode('utf-8'), "has been deleted"
                    # recreate it
                    sc = slavedao.copyCardToList(mc, slavelist['id'], prefix)
                    print "** ", mc['name'].encode('utf-8'), "has been recreated"

            syncslavecards.append(sc['id'])

    print "******** sync ok: ", str(syncslavecards)

    # For each slave list remove master synced close cards
    slavelists = slavedao.getLists()
    for sl in slavelists:
        print "\n~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        print "compute slave list:", sl['name'].encode('utf-8')
        print "~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~"
        slavecards = slavedao.getOpenCards(sl['id'])
        for sc in slavecards:
            if sc['name'].startswith(prefix):
                print "* created from master:", sc['name'].encode('utf-8')
                if sc['id'] not in syncslavecards:
                    print "* no longer exists in master:", sc['name'].encode('utf-8'), sc['id'].encode('utf-8')
                    slavedao.deleteCard(sc['id'])
                    print "* ", sc['name'].encode('utf-8'), "has been deleted"

        # reordrer cards
        print "* reorder cards:", sl['name'].encode('utf-8')
        priority = ['green', 'yellow', 'orange', 'red']
        tu = TrelloUtils(slavedao)
        if sl['name'] in conf['orderbyduedate']:
            tu.reorderListByDueDate(sl['id'])
            tu.redSoonDueDate(sl['id'])
        else:
            tu.reorderListByPriority(sl['id'], priority)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("synchronize 2 trello boards "))
    parser.add_argument('conf', help='configuration file', type=str)
    args = parser.parse_args()
    shouldquit = False

    if not os.path.exists(args.conf):
        shouldquit = True
        print "configuration file  does not exist:" + args.conf.encode('utf-8')

    if shouldquit:
        sys.exit(1)

    execfile(args.conf, conf)
    main()
