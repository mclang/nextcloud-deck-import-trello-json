# Python 3 script for parsing data from json and uploading the data to a NextCloud deck application via API

import json
import requests
import os
from dateutil import parser

# Configuration from config.json
with open('config.json') as f:
    data = json.load(f)

apiUser = data['user']
apiPword = data['password']
url = data['url']

# Specify the location of data here (the script will try to go through all .json-files in the folder
directory = './data/'

# Define function for making POST requests
def api_post(api_data, api_url):
    response = requests.post(api_url, auth=(apiUser, apiPword), data=api_data)
    if response:
        print('Imported successfully ' + '"' + api_data['title'] + '"')
        return json.loads(response.text)['id']
    elif response.status_code == 400:
        print('Importing failed: ' + '"' + api_data['title'] + '"')
        print(response)
        print('Bad request. Parameter missing?')
        return ''
    elif response.status_code == 403:
        print('Importing failed: ' + '"' + api_data['title'] + '"')
        print(response)
        print('Permission denied, check credentials.')
        return ''
    elif response.status_code == 404:
        print('Importing failed: ' + '"' + api_data['title'] + '"')
        print(response)
        print('Server not found.')
        return ''
    else:
        print('Importing failed: ' + '"' + api_data['title'] + '"')
        print('Something weird happened.')
        print(response)
        return ''


# Functions for formulating the text strings for checklists
def checklist_item(item):
    if item['state'] == 'incomplete':
        string_start = '[ ]'
    else:
        string_start = '[x]'
    check_item_string = string_start + ' ' + item['name']
    return check_item_string


def formulate_checklist_text(checklist):
    checklist_string = '\n\n## ' + checklist['name'] + '\n'
    for item in checklist['checkItems']:
        checklist_item_string = checklist_item(item)
        checklist_string = checklist_string + '\n' + checklist_item_string
    return checklist_string


# This convert the duedate from Trello-format to Deck format (they both are ISO 8601, but signify timezone differently)
def convert_date(trellodate):
    date = parser.isoparse(trellodate)
    deckdate = date.replace(microsecond=0).isoformat()
    return deckdate


# Define urls for api requests
boardUrl = url + 'boards'
labelUrl = boardUrl + '/%s/labels'
stackUrl = boardUrl + '/%s/stacks'
cardUrl = boardUrl + '/%s/stacks/%s/cards'
cardLabelUrl = boardUrl + '/%s/stacks/%s/cards/%s/assignLabel'


# NB: Maximum number of characters allowed in Deck is 250 (import will of a card fail if this is exceeded)
for filename in os.scandir(directory):
    if filename.path.endswith('.json'):
        print('\nProcessing file: %s \n' % filename.path)

        with open(filename.path, encoding='utf-8') as f:
            data = json.load(f)

        # Add board to Deck and retrieve the new board id
        trelloBoardName = data['name']
        boardData = {'title': trelloBoardName, 'color': '0800fd'}
        newboardId = api_post(boardData, boardUrl)


        # Import labels
        labels = {'labelId': 'newLabelId'}

        print('')
        print('Importing labels...')
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
            newLabelId = api_post(labelData, url)
            labels[labelId] = newLabelId


        # Save checklist content into a library
        checklists = {'checklistId': 'Checklist string'}
        for checkl in data['checklists']:
            checklistText = formulate_checklist_text(checkl)
            checklists[checkl['id']] = checklistText


        # Add stacks to the new board
        print('')
        print('Importing stacks...')
        url = stackUrl % newboardId
        stacks = {'listId': 'newStackId'}
        order = 1
        for lst in data['lists']:
            listId = lst['id']
            stackName = lst['name']
            stackData = {'title': stackName, 'order': order}
            newstackId = api_post(stackData, url)
            stacks[listId] = newstackId
            order = order + 1


        # Go through the cards and assign them to the correct lists
        print('')
        print('Importing cards...')
        cards = {'cardId': 'newCardId'}
        for crd in data['cards']:
            cardId = crd['id']
            cardName = crd['name']
            stringEnd = ''
            for checkl in crd['idChecklists']:
                # find the respective checklist string from the library that was generated earlier
                stringEnd = checklists[checkl]
            cardDesc = crd['desc'] + stringEnd
            newstackId = stacks[crd['idList']]
            cardOrder = crd['idShort']
            # Here we check whether the card has a due date, if not, run the first one, if yes, convert the date to ISO 8601
            if crd['due'] is None:
                cardData = {'title': cardName, 'type': 'plain', 'order': cardOrder, 'description': cardDesc}
            else:
                cardDue = convert_date(crd['due'])
                cardData = {'title': cardName, 'type': 'plain', 'order': cardOrder, 'description': cardDesc, 'duedate': cardDue}
            url = cardUrl % (newboardId, newstackId)
            newcardId = api_post(cardData, url)
            cards[cardId] = newcardId

            # If the card has a label assigned to it, we add it here
            for lbl in crd['labels']:
                oldLabelId = lbl['id']
                newLabelId = int(labels[oldLabelId])
                updateLabelData = {'labelId': newLabelId}
                url = cardLabelUrl % (newboardId, newstackId, newcardId)
                labelResponse = requests.put(url, auth=(apiUser, apiPword), data=updateLabelData)
                if labelResponse:
                    print('Label assigned to card', cardName)
                else:
                    print('Assigning label failed to card:', cardName)
    else:
        continue
