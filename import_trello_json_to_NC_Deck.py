# Python 3 script for parsing data from json and uploading the data to a NextCloud deck application via API

import requests, json
#import getpass

# Configuration from config.json
with open('config.json') as f:
    data = json.load(f)

apiUser = data['user']
apiPword = data['password']
url = data['url']

boardUrl = url + 'boards'
labelUrl = boardUrl + '/%s/labels'
stackUrl = boardUrl + '/%s/stacks'
cardUrl = boardUrl + '/%s/stacks/%s/cards'
cardLabelUrl = boardUrl + '/%s/stacks/%s/cards/%s/assignLabel'

# user = input('Username: ')
# pword = input('Password: ')
# url = input('API url: ')

# pword = getpass.getpass() Does not work for some reason.

with open('trello-data.json') as f:
    data = json.load(f)

trelloBoardName = data['name']

# Add board to Deck and retrieve the new board id
boardData = {'title': trelloBoardName, 'color': '0800fd'}
response = requests.post(boardUrl, auth=(apiUser, apiPword), data=boardData )

newboardId = json.loads(response.text)['id']
print('Board ', trelloBoardName, 'created.')

labels = {'labelId': 'newLabelId'}
for label in data['labels']:
    labelId = label['id']
    if label['name'] == '':
        labelTitle = 'Unnamed ' + label['color'] + ' label'
    else:
        labelTitle = label['name']
    if label['color'] == 'red':
        labelColor = 'ff0000'
    elif label['color'] == 'yellow':
        labelColor = 'ffff00'
    elif label['color'] == 'orange':
        labelColor = 'ff6600'
    elif label['color'] == 'green':
        labelColor = '00ff00'
    elif label['color'] == 'purple':
        labelColor = '9900ff'
    elif label['color'] == 'blue':
        labelColor = '0000ff'
    elif label['color'] == 'sky':
        labelColor = '00ccff'
    elif label['color'] == 'lime':
        labelColor = '00ff99'
    elif label['color'] == 'pink':
        labelColor = 'ff66cc'
    elif label['color'] == 'black':
        labelColor = '000000'
    else:
        labelColor = 'ffffff'
    labelData = {'title': labelTitle, 'color': labelColor}
    url = labelUrl % newboardId
    response = requests.post(url, auth=(apiUser, apiPword), data=labelData)
    newLabelId = json.loads(response.text)['id']
    labels[labelId] = newLabelId
    print('Label ', labelTitle, 'imported.')

# Add stacks to the new board
url = stackUrl % newboardId
stacks = {'listId': 'newStackId'}
order = 1
for lst in data['lists']:
    listId = lst['id']
    stackName = lst['name']
    stackData = {'title': stackName, 'order': order}
    response = requests.post(url, auth=(apiUser, apiPword), data=stackData)
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
    url = cardUrl % (newboardId, newstackId)
    response = requests.post(url, auth=(apiUser, apiPword), data=cardData)
    newcardId = json.loads(response.text)['id']
    cards[cardId] = newcardId
    print('Card', cardName, 'imported to stack number', newstackId)

    # If the card has a label assigned to it, we add it here
    for lbl in crd['labels']:
        oldLabelId = lbl['id']
        newLabelId = int(labels[oldLabelId])
        updateLabelData = {'labelId': newLabelId}
        url = cardLabelUrl % (newboardId, newstackId, newcardId)
        response = requests.put(url, auth=(apiUser, apiPword), data=updateLabelData)
        print('Label assigned to card', cardName)

#TODO: - checklists
#TODO: - users / members