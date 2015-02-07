#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import sys
import argparse
import os
import json


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=("Connectivity test with trello"))
    parser.add_argument('conf', help='configuration file', type=str)
    args = parser.parse_args()
    shouldquit = False

    if not os.path.exists(args.conf):
        print "configuration file  does not exist:" + args.conf
        sys.exit(1)
    conf = {}
    execfile(args.conf, conf)

    url = ''.join(['https://api.trello.com/1/boards/',
                   conf['testboard'],
                   '/lists/open?&key=',
                   conf['appkey'],
                   '&token=',
                   conf['token']])
    r = requests.get(url)

    print url
    print r.status_code

    if r.status_code != 200:
        print "GENERAL ERROR unable to fetch board lists:" + str(r.status_code) + r.text + u'\n'
        raise Exception("getLists:" + str(r.status_code))
    else:
        print json.dumps(r.json(), sort_keys=True, indent=4)
