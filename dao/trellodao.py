# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import requests
import json

# A trello mapper

conf = {}


class TrelloBoardDAO(object):
    _token = None
    _appkey = None
    _boardid = None

    def __init__(self, appkey, token, boardid):
        self._token = token
        self._appkey = appkey
        self._boardid = boardid

    def getLists(self, verbose=None):
        res = None
        # get all lists
        url = ''.join(['https://api.trello.com/1/boards/',
                       self._boardid,
                       '/lists/open?&key=',
                       self._appkey,
                       '&token=',
                       self._token])
        r = requests.get(url)

        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)

        if r.status_code != 200:
            print "GENERAL ERROR unable to fetch board lists:" + str(r.status_code) + r.text + u'\n'
            raise Exception("getLists:" + str(r.status_code))
        else:
            res = r.json()

        # print json.dumps(lists, sort_keys=True,indent=4, separators=(',', ': '))
        return res

    def createList(self, listname, verbose=None):
        res = None
        url = ''.join(['https://api.trello.com/1/boards/',
                       self._boardid,
                       '/lists',
                       '?&key=',
                       self._appkey,
                       '&token=',
                       self._token,
                       '&name=',
                       listname
                       ])
        r = requests.post(url)

        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)

        if r.status_code != 200:
            print "GENERAL ERROR createList:" + str(r.status_code) + r.text + u'\n'
            raise Exception("createList:" + str(r.status_code))
        else:
            res = r.json()
        return res

    def closeList(self, listid, verbose=None):
        res = None
        url = ''.join(['https://api.trello.com/1/lists/',
                       listid,
                       '/closed?&key=',
                       self._appkey,
                       '&token=',
                       self._token,
                       '&value=',
                       'true'])
        r = requests.put(url)

        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)

        if r.status_code != 200:
            print "GENERAL ERROR unable to move card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("closeList:" + str(r.status_code))
        else:
            res = r.json()
        return res

    def openList(self, listid, verbose=None):
        res = None
        url = ''.join(['https://api.trello.com/1/lists/',
                       listid,
                       '/closed?&key=',
                       self._appkey,
                       '&token=',
                       self._token,
                       '&value=',
                       'false'])
        r = requests.put(url)

        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)

        if r.status_code != 200:
            print "GENERAL ERROR unable to move card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("closeList:" + str(r.status_code))
        else:
            res = r.json()
        return res

    def getListId(self, listname):
        res = None
        lists = self.getLists()
        for l in lists:
            if l[u'name'] == listname:
                res = l[u'id']
        if not(res):
            print "ERROR LIST NOT FOUND"
        return res

    def moveCard(self, cardid, pos, verbose=None):
        res = None
        url = ''.join(['https://api.trello.com/1/cards/',
                       cardid,
                       '/pos?&key=',
                       self._appkey,
                       '&token=',
                       self._token,
                       '&value=',
                       pos])
        r = requests.put(url)

        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)

        if r.status_code != 200:
            print "GENERAL ERROR unable to move card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("moveCard:" + str(r.status_code))
        else:
            res = r.json()
        return res

    def createCard(self, listid, cardtext, desc, verbose=None):
        res = None
        url = ''.join(['https://api.trello.com/1/lists/',
                       listid,
                       '/cards?&key=',
                       self._appkey,
                       '&token=',
                       self._token,
                       '&name=',
                       cardtext,
                       '&desc=',
                       desc,
                       '&pos=',
                       '7',
                       '&labels=',
                       u'green'])

        r = requests.post(url)
        if r.status_code != 200:
            print "GENERAL ERROR unable to create card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("createCard:" + str(r.status_code))
        else:
            res = r.json()

        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)
        return res

    def deleteCard(self, cardid, verbose=None):
        res = None
        url = ''.join(['https://api.trello.com/1/cards/',
                       cardid,
                       '?&key=',
                       self._appkey,
                       '&token=',
                       self._token])
        r = requests.delete(url)

        if r.status_code != 200:
            print "GENERAL ERROR unable to delete card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("deletecard:" + str(r.status_code))
        else:
            res = r.json()
        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)
        return res

        pass

    # get open cards of a list
    def getOpenCards(self, listid, verbose=None):
        res = None
        url = ''.join(['https://api.trello.com/1/lists/',
                       listid,
                       '/cards?&key=',
                       self._appkey,
                       '&token=',
                       self._token])
        r = requests.get(url)

        if r.status_code != 200:
            print "GENERAL ERROR unable to get open card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("getopencards:" + str(r.status_code))
        else:
            res = r.json()
            # for c in cards:
            #     if c[u'labels']:
            #         color = c[u'labels'][0][u'color']
            #     else:
            #         color = u'unknown'
            #     res[c[u'name']] = color
        if verbose:
            print url
            print 'encoding: ', r.encoding
            print json.dumps(r.json(), sort_keys=True, indent=4)
        return res

    def getCard(self, cardid, verbose=None):
        res = None
        url = ''.join(['https://api.trello.com/1/cards/',
                       cardid,
                       '?&key=',
                       self._appkey,
                       '&token=',
                       self._token])
        r = requests.get(url)

        if r.status_code != 200:
            print "GENERAL ERROR unable to get card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("getCard:" + str(r.status_code))
        else:
            res = r.json()
        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)
        return res

    def setDueDate(self, card, duedate='null', verbose=None):
        res = card
        url = ''
        if (duedate is not None) and (duedate != 'null'):
            res = None
            url = ''.join(['https://api.trello.com/1/cards/',
                           card['id'],
                           '/due?&key=',
                           self._appkey,
                           '&token=',
                           self._token,
                           '&value=',
                           duedate])
            r = requests.put(url)

            if r.status_code != 200:
                print "GENERAL ERROR unable to get card:" + str(r.status_code) + r.text + u'\n'
                raise Exception("setDueDate:" + str(r.status_code))
            else:
                res = r.json()
        if verbose:
            print 'url: ', url
            print json.dumps(r.json(), sort_keys=True, indent=4)
        return res

    def setLabel(self, card, label='red', verbose=None):
        res = card
        url = ''
        res = None
        url = ''.join(['https://api.trello.com/1/cards/',
                       card['id'],
                       '/labels?&key=',
                       self._appkey,
                       '&token=',
                       self._token,
                       '&value=',
                       label])
        r = requests.put(url)

        if r.status_code != 200:
            print "GENERAL ERROR unable to get card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("setLabel:" + str(r.status_code))
        else:
            res = r.json()

        if verbose:
            print 'url: ', url
            print json.dumps(r.json(), sort_keys=True, indent=4)
        return res

    def copyCardToList(self, card, listid, prefix, verbose=None):
        res = None
        res = self.copyCardIdToList(card['id'], listid, prefix, verbose)
        if card['due'] != 'null':
            res = self.setDueDate(res, card['due'])
        return res

    def copyCardIdToList(self, cardid, listid, prefix, verbose=None):
        res = None

        url = ''.join(['https://api.trello.com/1/cards',
                       '?&key=',
                       self._appkey,
                       '&token=',
                       self._token,
                       '&due=',
                       'null',
                       '&idList=',
                       listid,
                       '&urlSource=',
                       'null',
                       '&idCardSource=',
                       cardid])
        r = requests.post(url)

        if r.status_code != 200:
            print "GENERAL ERROR unable to get card to copy:" + str(r.status_code) + r.text + u'\n'
            raise Exception("copyCardToList:" + str(r.status_code))

        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)

        newcard = r.json()

        # rename card
        url = ''.join(['https://api.trello.com/1/cards/',
                       newcard['id'],
                       '/name',
                       '?&key=',
                       self._appkey,
                       '&token=',
                       self._token,
                       '&value=',
                       ''.join([prefix, newcard['name']])
                       ])
        r = requests.put(url)

        if r.status_code != 200:
            print "GENERAL ERROR unable to copy card:" + str(r.status_code) + r.text + u'\n'
            raise Exception("copyCardToList:" + str(r.status_code))
        else:
            res = r.json()
        if verbose:
            print url
            print json.dumps(r.json(), sort_keys=True, indent=4)
        return res
