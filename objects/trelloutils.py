# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from datetime import datetime
from datetime import timedelta
import logging


class __:

        def __init__(self, fmt, *args, **kwargs):
            self.fmt = fmt
            self.args = args
            self.kwargs = kwargs

        def __str__(self):
            return self.fmt.format(*self.args, **self.kwargs)


class TrelloUtils(object):

    _dao = None

    def __init__(self, trello_dao):
        self._dao = trello_dao

    def redSoonDueDate(self, listid):
        cards = self._dao.getOpenCards(listid)
        today = datetime.today().date()
        td = timedelta(days=2)
        near_futur = today + td

        for c in cards:
            duestr = c['due']
            if duestr is not None and duestr != 'null':
                duedate = datetime.strptime(duestr, "%Y-%m-%dT%H:%M:%S.%fZ").date()
                # logging.info("due date: " + duestr
                # logging.info("due date: " + str(duedate)
                if duedate < near_futur:
                    # make it red
                    # logging.info("make it red"
                    # logging.info(str(c)
                    self._dao.setLabel(c, 'red')

    def reorderListByPriority(self, listid, labels_order_by_priority_asc):

        cards = self._dao.getOpenCards(listid)
        ignorelist = []
        toreorder = [sc for sc in cards if sc['labels'] != []]
        for p in labels_order_by_priority_asc:
            for sc in toreorder:
                colors = sc['labels']
                colorpresence = None
                colorpresence = [label for label in colors if label['color'] == p]
                if colorpresence != []:
                    logging.info(__("** {} has a label {} ", sc['name'], p))
                    if sc['id'] not in ignorelist:
                        self._dao.moveCard(sc['id'], 'top')
                        logging.info(__("** {} moved to top ", sc['name']))
                        ignorelist.append(sc['id'])

    def reorderListByDueDate(self, listid):
        cards = self._dao.getOpenCards(listid)
        toreorder = [sc for sc in cards if sc['due'] != 'null']
        neworder = sorted(toreorder, key=lambda x: x['due'], reverse=True)
        for c in neworder:
            try:
                logging.info(__("** {} has a due date {}", c['name'],  c['due']))
                self._dao.moveCard(c['id'], 'top')
                logging.info(__("** {} moved to top ", c['name']))
            except Exception as e:
                logging.error(e)
