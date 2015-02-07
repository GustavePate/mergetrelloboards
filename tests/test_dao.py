import pytest
from dao.trellodao import TrelloBoardDAO
from datetime import datetime


conf = {}


def setup_module(module):
    pass


def test_init(conffile):
    execfile(conffile, conf)
    conf['tdao'] = TrelloBoardDAO(conf['appkey'], conf['token'], conf['testboard'])
    # drop all lists
    lists = conf['tdao'].getLists()
    for l in lists:
        conf['tdao'].closeList(l['id'])
    # create test list
    conf['tdao'].createList('test')


def test_copy(conffile):
    # listid = conf['tdao'].copyCardToList(cardid, listid
    prefix = '[prefix] '
    listid = conf['tdao'].getListId("test")
    assert listid is not None
    r = conf['tdao'].createCard(listid, "to copy", "red", True)
    r2 = conf['tdao'].copyCardIdToList(r['id'], listid, prefix, True)
    assert ''.join([prefix, r['name']]) == r2['name']


def test_setduedate(conffile):
    listid = conf['tdao'].getListId("test")
    r = conf['tdao'].createCard(listid, "duedate", "red", True)
    dt = datetime.now()
    datestr = dt.isoformat('T')
    # cut last millis
    datestr = datestr[:23]
    datestr = ''.join([datestr, 'Z'])
    print datestr
    r = conf['tdao'].setDueDate(r, datestr, True)
    assert r['due'] is not None
    assert r['due'] != 'null'


def test_getlist(conffile):
    listid = None
    listid = conf['tdao'].getListId("test")
    print "listid: ", listid
    assert listid is not None


def test_createlist(conffile):
    before = conf['tdao'].getLists()
    assert before is not None
    assert len(before) > 0

    r = conf['tdao'].createList("arg", True)
    assert r is not None
    after = conf['tdao'].getLists()
    assert after is not None
    assert len(after) == len(before) + 1


def test_getcard(conffile):
    listid = conf['tdao'].getListId("test")
    assert listid is not None
    r = conf['tdao'].createCard(listid, "to copy", "red", True)
    r2 = conf['tdao'].getCard(r['id'], True)
    assert r['id'] == r2['id']
    assert r['pos'] == r2['pos']
    assert r['name'] == r2['name']


def test_remove(conffile):
    listid = conf['tdao'].getListId("test")
    assert listid is not None
    before = conf['tdao'].getOpenCards(listid)
    assert before is not None
    conf['tdao'].deleteCard(before[0]['id'], True)
    after = conf['tdao'].getOpenCards(listid)
    assert after is not None
    assert len(after) == len(before) - 1


def test_move(conffile):

    listid = conf['tdao'].getListId("test")
    assert listid is not None
    r = conf['tdao'].createCard(listid, "my new card1", "red", True)
    initial_position = r['pos']
    assert r is not None
    # get card position
    r = conf['tdao'].moveCard(r[u'id'], 'top', True)
    final_position = r['pos']
    # compare card position
    assert final_position < initial_position


def test_opencards(conffile):
    listid = conf['tdao'].getListId("test")
    assert listid is not None
    assert conf['tdao'].getOpenCards(listid) is not None


def test_createcard(conffile):
    listid = conf['tdao'].getListId("test")
    assert listid is not None
    before = conf['tdao'].getOpenCards(listid)
    r = conf['tdao'].createCard(listid, "my new card1", "red", True)
    assert r is not None
    after = conf['tdao'].getOpenCards(listid)
    assert after is not None
    assert len(after) == len(before) + 1
