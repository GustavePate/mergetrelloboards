Trello utilities
==================

* [Trellomerge: synchronize your trello boards](#trellomerge)
* [Trello2txt: dump your boards to text](#trello2txt)


## Requirements

Theses utilities use standard libray python module and the request module

On debian/ubuntu:

    sudo apt-get install python-requests

or

    [sudo] pip install requests

## Installation

    git clone https://github.com/GustavePate/mergetrelloboards


Trellomerge
===========

Trellomerge allows you to merge a master in a slave board.

Theses requirements will be applied in order to synchronize trello boards:

* Lists from the master board will be created in the slave board
* Cards from the master board will be created in the slave board
* Cards from the slave board will be untouched
* Lists from the slave board will be untouched
* Cards coming from the master board are prefixed in the slave board.
* Slave lists are reordered by labels (red first, green last)
* You can specify to sort some slave board lists by due date

Use crontab to keep your trello boards synchronized.

## Configuration

Run

    vim /path/to/mergetrelloboards/conf.py

Change the configuration, you will need:
- a trello api developper key [here](https://trello.com/docs/).
- a trello api developper token [here](https://trello.com/docs/).
- your master and slave board id (see the url in your webbrowser when you're connected to trello)

## Usage

    python /path/to/mergetrelloboards/trellomerge.py /path/to/trello2txt/conf.py

Trello2txt
==========

Fetch trello cards from a board and output their text in stdout. Notable use case: use it with conky !

## Context

While improving my workflow, I was searching to have my trello tasks quickly accessible.
Then I lokk at my conky dashboard ;)
All I needed was a trello2txt tool. Here it is !

## Configuration


Run

    vim /path/to/mergetrelloboards/conf.py

Change the configuration, you will need:
- a trello api developper key [here](https://trello.com/docs/).
- a trello api developper token [here](https://trello.com/docs/).
- your board id (see the url in your webbrowser when you're connected to trello)
- the name of the lists you wan't to dump to text

Adjust the filters to your needs (by default only cards with orange and red labels will be display)

## Usage

Just run:

    python /path/to/mergetrelloboards/trello2txt.py /path/to/trello2txt/conf.py -s

or to create a local file:

    python /path/to/mergetrelloboards/trello2txt.py /path/to/trello2txt/conf.py -s -d /tmp/trello.txt

Enjoy !

## Use it with conky

First make sure you completed the installation section !

There is a conky template to display your trello list on your desktop.
Edit it first, you'll have to change the path to the trello2txt.py, conf.py and to the stored todolist file.

>I'm currently not happy with it's line by line implementation. I'll be glad if you send me an improvement !

Then:

    conky -d -c /path/to/mergetrelloboards/trelloconkyrc

Wait up to 10 minutes to ensure the list is updated.

Tada !

A screenshot of my desktop with trello2txt/conky:

![screenshot of conky and trello2txt(https://raw.github.com/GustavePate/mergetrelloboards/master/pics/trello+conky.png "Conky + Trello screenshot")

