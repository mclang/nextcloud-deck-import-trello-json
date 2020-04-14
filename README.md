# Import Trello Boards into Nextcloud Deck App

Simple [Go](https://golang.org/) and Python scripts that can be used to import Trello boards from exported JSON files
using Nextcloud [Deck](https://apps.nextcloud.com/apps/deck) app [API](https://github.com/nextcloud/deck/blob/master/docs/API.md).

**Work in Progress:**

- [x] Export simple example Trello board
- [x] Parse and print basic board/list/card information
- [ ] Example Deck API requests and JSON response parsing
- [ ] Add data objects for boards/lists/cards that can be marshalled into JSON that Deck API accepts
- [ ] Import board into Deck
- [ ] Import stacks (Trello list) into Deck board
- [ ] Import cards into Deck stack
- [ ] Update card description (combine trello card description and checklists)

**Python script:**
- [x] Import Trello board with name
- [x] Import lists as Deck stacks with name
- [x] Import cards into respective stacks with name and markdown-formatted description
- [ ] Add checklists
- [ ] Add labels

Python script reads the url of the api, username, and password from config.json file, and uses trello-data.json as source data for parsing.
