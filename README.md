# Import Trello Boards into Nextcloud Deck App

Simple script that can be used to import
[Trello](https://trello.com/) boards from exported JSON files into [Nextcloud](https://nextcloud.com)'s
[Deck](https://apps.nextcloud.com/apps/deck) app using Nextcloud Deck app
[API](https://github.com/nextcloud/deck/blob/master/docs/API.md).

**Requisites:**
- [Python v3](https://www.python.org/downloads/) (tested with Python 3.7)
- `python-dateutil`
- `python-scandir`


The python script reads following things from `config.json` file:
- API URL, e.g `https://nextcloud.url/index.php/apps/deck/api/v1.0/`
- Nextcloud username
- Nextcloud password (can also be app password!)

Current _batch mode_ implementation tries to parse all `json` files found from `data` sub-directory,
some make sure the files are what they should be.

Also note that Python script imports archived cards as **normal** cards.

**Known Limitations:**
- Nextcloud Deck cannot handle **multiple labels** with the **same name** (will cause the script to fail).
- Maximum character count allowed for the titles of Deck cards is **255 characters**.
- Card comments are **not** imported.
- Editing history is skipped as well (i.e. when the card was last edited).

And yes, the script is slow as molasses, but it does its job (at least for me).

**NOTE:** Original unfinished [Go](https://golang.org/) script is abandoned in favor of more complete Python implementation.

**Go script:**

- [x] Export simple example Trello board
- [x] Parse and print basic board/list/card information
- [ ] Example Deck API requests and JSON response parsing
- [ ] Add data objects for boards/lists/cards that can be marshalled into JSON that Deck API accepts
- [ ] Import board into Deck
- [ ] Import stacks (Trello list) into Deck board
- [ ] Import cards into Deck stack
- [ ] Update card description (combine trello card description and checklists)
- [ ] Set card labels

**Python script:**
- [x] Import Trello board with name
- [x] Import lists as Deck stacks with name
- [x] Import cards into respective stacks with name and markdown-formatted description
- [x] Add labels (with colors and descriptions) to the board and assign them to the correct cards
- [x] Add checklists (supports also multiple checklists in one card)
- [ ] ~~Assign users to cards~~ (abandoned)
- [x] Add due dates to cards
- [x] Added batch process of files (place exported .json files to the folder "data")
- [x] archived Trello lists and cards are skipped (not imported at all)
