# -*- coding: utf-8 -*-


# A list class containing text based cards model
class ListModel(object):
    _id = None
    _name = None
    _cards = None
    _errorcode = None
    _conf = None

    def __init__(self, id, name, conf):
        self._id = id
        self._name = name
        self._cards = {}
        self._cards[u'all'] = []
        self._conf = conf

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
                res = res + c + u"\n"
                count = count + 1
                if count >= self._conf['BY_NUMBER_COUNT']:
                    break

        return res.encode('utf-8')

    # conf['BY_COLOR'] display
    def getstrbycolor(self):
        res = self._name.upper() + u"\n"
        if self._errorcode:
            res = res + self.geterror()
        else:
            # if no filter
            if len(self._conf['COLOR_TO_DISPLAY'].keys()) == 0:
                for c in self._cards[u'all']:
                    res = res + c + u"\n"
            # color filter
            else:
                for td in self._conf['COLOR_TO_DISPLAY'].keys():
                    # cards of this color ?
                    if td in self._cards.keys():
                        for c in self._cards[td]:
                            # add prefix
                            res = res + self._conf['COLOR_TO_DISPLAY'][td]
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
