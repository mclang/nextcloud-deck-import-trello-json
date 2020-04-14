# Python 3 script for parsing data from json and uploading the data to a NextCloud deck application via API

import requests, json
#import getpass

# Configuration from config.json
with open('config.json') as f:
    data = json.load(f)

user = data['user']
pword = data['password']
url = data['url']

boardurl = url + 'boards'
stackurl = boardurl + '/%s/stacks'
cardurl = boardurl + '/%s/stacks/%s/cards'

# user = input('Username: ')
# pword = input('Password: ')
# url = input('API url: ')

# pword = getpass.getpass() Does not work for some reason.

with open('trello-data.json') as f:
    data = json.load(f)

trelloBoardID = data['id']
trelloBoardName = data['name']
trelloCards = data['cards']
trelloLists = data['lists']
#trelloChecklists = data['checklists']

print('Trello board id:', trelloBoardID)
print('Trello board name: ', trelloBoardName)
print('')
# print(json.dumps(trelloCards, indent = 4))

# Add board to Deck and retrieve the new board id
boardData = {'title': trelloBoardName, 'color': '0800fd'}
response = requests.post(boardUrl, auth = (user, pword), data=boardData )

newboardId = json.loads(response.text)['id']
print('Board ', trelloBoardName, 'created.')


# Add stacks to the new board
url = stackurl % newboardId
stacks = {'listId': 'newStackId'}
order = 1
for lst in data['lists']:
    listId = lst['id']
    stackName = lst['name']
    stackData = {'title': stackName, 'order': order}
    response = requests.post(url, auth=(user, pword), data=stackData)
    newstackId = json.loads(response.text)['id']
    stacks[listId] = newstackId
    order = order + 1
    print('New stack imported:', stackName)

# Go through the cards and assign them to the correct lists
cards = {'cardId': 'newCardId'}

for crd in data['cards']:
    cardId = crd['id']
    cardName = crd['name']
    cardDesc = crd['desc']
    newstackId = stacks[crd['idList']]
    cardOrder = crd['idShort']
    cardData = {'title': cardName, 'type': 'plain', 'order': cardOrder, 'description': cardDesc}
    #cardDue = crd['due'] Let's first test without due dates
    #cardData = {'title': cardName, 'type': 'plain', 'order': cardOrder, 'description': cardDesc, 'duedate': cardDue}
    url = cardurl % (newboardId, newstackId)
    response = requests.post(url, auth=(user, pword), data=cardData)
    newcardId = json.loads(response.text)['id']
    cards[cardId] = newcardId
    print('Card', cardName, 'imported to stack number', newstackId)

    #TO DO: if-loop for checking checklists

# TO DO: labels
