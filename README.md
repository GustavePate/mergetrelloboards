Trello utilities
==================

* [Trellomerge: synchronize your Trello boards](#trellomerge)
* [Trello2txt: dump your boards to text](#trello2txt)


## Requirements

These utilities use standard library python modules, and the `requests` module.

On debian/ubuntu:

    sudo apt-get install python-requests

or

    [sudo] pip install requests

## Installation

    git clone https://github.com/GustavePate/mergetrelloboards


Trellomerge
===========

Trellomerge allows you to merge a _master_ to a _slave_ board.

These steps will be applied in order to synchronize Trello boards:

* Lists from the master board will be created in the slave board
* Cards from the master board will be created in the slave board
* Cards from the slave board will be untouched
* Lists from the slave board will be untouched
* Cards coming from the master board are prefixed in the slave board.
* Slave lists are reordered by labels (red first, green last)
* You can specify to sort some slave board lists by due date

Use `crontab` to keep your Trello boards synchronized.

## Configuration

Run

    vim /path/to/mergetrelloboards/conf.py

Change the configuration. You will need:
- a Trello API developer key [here](https://tello.com/docs/).
- a Trello API developer token [here](https://trello.com/docs/).
- your master and slave board id (see the URL in your webbrowser when you're connected to Trello).

## Usage

    python /path/to/mergetrelloboards/trellomerge.py /path/to/trello2txt/conf.py

Trello2txt
==========

Fetch Trello cards from a board and output their text to `stdout`. Notable use case: use it with conky !

## Context

While improving my workflow, I wanted to have my Trello tasks quickly accessible.
Then I looked at my conky dashboard ;)
All I needed was a `trello2txt` tool. Here it is !

## Configuration

Run

    vim /path/to/mergetrelloboards/conf.py

Change the configuration; you will need:
- a Trello API developer key [here](https://trello.com/docs/),
- a Trello API developer token [here](https://trello.com/docs/),
- your board id (see the URL in your webbrowser when you're connected to Trello),
- the name of the lists you want to dump to text.

Adjust the filters to your needs (by default only cards with orange and red labels will be displayed).

## Usage

Just run:

    python /path/to/mergetrelloboards/trello2txt.py /path/to/trello2txt/conf.py -s

or to create a local file:

    python /path/to/mergetrelloboards/trello2txt.py /path/to/trello2txt/conf.py -s -d /tmp/trello.txt

Enjoy !

## Use it with conky

First make sure you completed the installation section !

There is a conky template to display your Trello list on your desktop.
Edit it first: you'll have to change the paths to the `trello2txt.py`, `conf.py` and to the stored `todolist` files.

>I'm currently not happy with its line by line implementation. I'll be glad if you send me an improvement !

Then:

    conky -d -c /path/to/mergetrelloboards/trelloconkyrc

Wait up to 10 minutes to ensure the list is updated.

Tada !

A screenshot of my desktop with `trello2txt/conky`:

![screenshot of conky and trello2txt(https://raw.github.com/GustavePate/mergetrelloboards/master/pics/trello+conky.png "Conky + Trello screenshot")

