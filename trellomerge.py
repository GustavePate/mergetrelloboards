#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
# import json
import sys
# from collections import OrderedDict
import argparse
import os
from jsmin import jsmin
import json
from collections import OrderedDict
from dao.trellodao import TrelloBoardDAO
from objects.trelloutils import TrelloUtils
from objects.trelloutils import __

conf = {}

import logging

logger = logging.getLogger()
handler = logging.StreamHandler()
formatter = logging.Formatter('{asctime}  {name} {levelname:5s} {message}', style='{')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)


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

    slavedao = TrelloBoardDAO(conf['appkey'], conf['token'], conf['MERGE']['slaveboard'])
    masterdao = TrelloBoardDAO(conf['appkey'], conf['token'], conf['MERGE']['masterboard'])
    prefix = '[kr]'

    # get master lists
    masterlists = masterdao.getLists()

    # create (or reopen) list in slave if not exists
    slavelists = slavedao.getLists()

    # cards that have been synced while computing masterlist
    syncslavecards = []

    # for each master list
    for ml in masterlists:

        logger.info(ml)
        logger.info("---------------------------------------")
        logger.info(__("compute master list: {} ", ml['name']))
        logger.info("---------------------------------------")

        # if list exists in slave ?
        slavelist = listexists(ml['name'], slavelists)
        if slavelist is not None:
            logger.info(__("* {} exists in slaveboard", ml['name']))

            # if it's not open
            if slavelist[u'closed']:
                logger.info(__("* {} is closed in slaveboard", ml['name']))
                # open it
                slavedao.openList(slavelist['id'])
                logger.info(__("* {} is now open in slaveboard", ml['name']))
        else:
            logger.info(__("* {} does not exists in slaveboard", ml['name']))
            # else create it
            slavelist = slavedao.createList(ml[u'name'])
            logger.info(__("* {} is now created in slaveboard", ml['name']))

        # for each open card in master list
        mastercards = masterdao.getOpenCards(ml[u'id'])
        slavecards = slavedao.getOpenCards(slavelist[u'id'])
        for mc in mastercards:
            logger.info(__("compute mastercard: {} --", mc['name']))

            # if not exists in slave
            sc = cardexists(mc, slavecards, prefix)
            if sc is None:
                logger.info(__("** {} does not exist in slaveboard", mc['name']))

                # create it
                sc = slavedao.copyCardToList(mc, slavelist[u'id'], prefix)
                logger.info(__("** {} is now created in slaveboard", mc['name']))
            # if exists in slave
            else:
                logger.info(__("** {} exists in slaveboard", mc['name']))
                # compare last modification date
                # if master fresher than slave
                if mc['dateLastActivity'] > sc['dateLastActivity']:
                    logger.info(__("** {} needs to be refreshed from master", mc['name']))

                    # delete slave card
                    slavedao.deleteCard(sc['id'])
                    logger.info(__("** {} has been deleted", mc['name']))
                    # recreate it
                    sc = slavedao.copyCardToList(mc, slavelist['id'], prefix)
                    logger.info(__("** {} has been recreated", mc['name']))

            syncslavecards.append(sc['id'])

    logger.info(__("******** sync ok: {}", str(syncslavecards)))

    # For each slave list remove master synced close cards
    slavelists = slavedao.getLists()
    for sl in slavelists:
        logger.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        logger.info(__("compute slave list: {}", sl['name']))
        logger.info("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
        slavecards = slavedao.getOpenCards(sl['id'])
        for sc in slavecards:
            if sc['name'].startswith(prefix):
                logger.info(__("* created from master: {}", sc['name']))
                if sc['id'] not in syncslavecards:
                    logger.info(__("* no longer exists in master: {} {}", sc['name'], sc['id']))
                    slavedao.deleteCard(sc['id'])
                    logger.info(__("* {} has been deleted", sc['name']))

        # reordrer cards
        logger.info(__("* reorder cards: {}", sl['name']))
        priority = ['green', 'yellow', 'orange', 'red']
        tu = TrelloUtils(slavedao)
        if sl['name'] in conf['MERGE']['orderbyduedate']:
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
        logger.info("configuration file  does not exist:" + args.conf.encode('utf-8'))

    if shouldquit:
        sys.exit(1)

    with open(args.conf) as file:
        rawconf = file.read()
        tidyconf = jsmin(rawconf)
        logger.debug(tidyconf)
        conf = json.loads(tidyconf, object_pairs_hook=OrderedDict)
        file.close()

    main()
