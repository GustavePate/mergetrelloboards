from collections import OrderedDict

# ########### GLOBAL CONFIGURATION ############

# appkey and token (see trello api doc to get yours)

# CHANGE THIS !!!!! (otherwise you will see my fantastic TodoList)
appkey = u'64842214ed1b16224ee8742f8db14aoh'
secret = u'a2f1445f1bf434bc8a551308ddb26fdd5a2c1a4b520231156cb0ff55aef46ac2'
token = u'156a31cab6a59a86345ce34f283e9546506d859a7b21b0caf8d9e47ead75aed'

# ########### trello2txt CONFIGURATION ############

# Board id (see Trello url)
# CHANGE THIS !!!!!
board = u'GKibRtoN'

# Possible behaviour
BY_COLOR = 0
BY_NUMBER = 1

# list here the name of  lists to be monitored and the desired behaviour for each list
# list all = BY_COLOR with no color filter specified
# CHANGE THIS !!!!!
toanalyse = OrderedDict()
toanalyse[u'List1_name'] = BY_COLOR
toanalyse[u'List2_name'] = BY_COLOR
toanalyse[u'List3_name'] = BY_NUMBER

# IF you choose a by number behaviour, the number of cards to retrieve
BY_NUMBER_COUNT = 10

# color filter
# List the card colors you wan't to display
# the dic value is a prefix added to the card text in the rendered list
# set an empty dic to display all cards
COLOR_TO_DISPLAY = {}
COLOR_TO_DISPLAY['red'] = '!'
COLOR_TO_DISPLAY['orange'] = ""
# COLOR_TO_DISPLAY[u'yellow']=""
# COLOR_TO_DISPLAY[u'green']=""

# ########### trellomerge CONFIGURATION ############

masterboard = u'y79lF0eI'
slaveboard = u'yh8jqhba'
testboard = u'HCqmI3Sb'

# prefix to add to cards copied from the master list
slavecardsprefix = '[kr] '

# theses slave lists will be sorted by due date and not by priority [default behaviour]
orderbyduedate = ['Calendar']
