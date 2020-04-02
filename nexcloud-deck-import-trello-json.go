package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"net/url"
	"os"
)

// https://tutorialedge.net/golang/parsing-json-with-golang/
// https://www.sohamkamani.com/blog/2017/10/18/parsing-json-in-golang/

func main() {
	jsonFile, err := os.Open("trello-board-example.json")
	if err != nil {
		fmt.Println(err)
	}
	defer jsonFile.Close()

	// Read JSON as byte array
	jsonBytes, _ := ioutil.ReadAll(jsonFile)

	// Unmarshal JSON bytes as map of strings
	var result map[string]interface{}
	json.Unmarshal(jsonBytes, &result)

	trelloBoardID    := result["id"].(string)
	trelloBoardName  := result["name"].(string)
	trelloCards      := result["cards"].([]interface{})
	trelloLists      := result["lists"].([]interface{})
	trelloChecklists := result["checklists"].([]interface{})

	fmt.Println("Board Name:", trelloBoardName)
	fmt.Println("Board ID:", trelloBoardID)

	fmt.Println()
	for key, value := range trelloLists {
		data := value.(map[string]interface{})
		id   := data["id"].(string)
		name := data["name"].(string)

		fmt.Println("List number", key)
		fmt.Println("- id:  ", id)
		fmt.Println("- name:", name)
	}

	fmt.Println()
	for key, value := range trelloCards {
		data := value.(map[string]interface{})
		id   := data["id"].(string)
		name := data["name"].(string)
		desc := data["desc"].(string)
		parentBoardID := data["idBoard"].(string)
		parentListID  := data["idList"].(string)

		fmt.Println("Card number ", key)
		fmt.Println("- id:  ", id)
		fmt.Println("- name:", name)
		fmt.Printf( "- desc: '%s'\n", url.QueryEscape(desc))
		fmt.Println("- parent board id:", parentBoardID)
		fmt.Println("- parent list id: ", parentListID)
	}

	fmt.Println()
	for key, value := range trelloChecklists {
		data := value.(map[string]interface{})
		id   := data["id"].(string)
		name := data["name"].(string)
		parentBoardID := data["idBoard"].(string)
		parentCardID  := data["idCard"].(string)
		checkItems := data["checkItems"].([]interface {})

		fmt.Println("Checklist number", key)
		fmt.Println("- id:  ", id)
		fmt.Println("- name:", name)
		fmt.Println("- parent board id:", parentBoardID)
		fmt.Println("- parent card id: ", parentCardID)
		fmt.Println("- check items:", len(checkItems))
		for key, value := range checkItems {
			data := value.(map[string]interface{})
			name  := data["name"].(string)
			state := data["state"].(string)
			fmt.Printf( "    %2d: %-10s - '%s'\n", key, state, name)
		}
	}
}
