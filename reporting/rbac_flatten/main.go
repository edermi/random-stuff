package main

import (
	"encoding/json"
	"fmt"
	"os"
	"time"
)

// Define structs to match JSON structure
type Data struct {
	Nodes map[string]Node `json:"nodes"`
	Edges []Edge          `json:"edges"`
}

type Node struct {
	Label      string    `json:"label"`
	Kind       string    `json:"kind"`
	ObjectID   string    `json:"objectId"`
	IsTierZero bool      `json:"isTierZero"`
	LastSeen   time.Time `json:"lastSeen"`
}

type Edge struct {
	Source   string    `json:"source"`
	Target   string    `json:"target"`
	Label    string    `json:"label"`
	Kind     string    `json:"kind"`
	LastSeen time.Time `json:"lastSeen"`
}

type JSONData struct {
	Data Data `json:"data"`
}

func main() {
	if len(os.Args) != 2 {
		printHelp()
		os.Exit(1)
	}

	f, err := os.Open(os.Args[1])
	if err != nil {
		fmt.Fprintf(os.Stderr, "Error opening file: %v\n", err)
		os.Exit(1)
	}
	defer f.Close()

	var data JSONData
	if err := json.NewDecoder(f).Decode(&data); err != nil {
		fmt.Fprintf(os.Stderr, "Error unmarshalling JSON: %v\n", err)
		os.Exit(1)
	}

	nodeMap := make(map[string]string)
	for id, node := range data.Data.Nodes {
		nodeMap[id] = node.Label
	}

	fmt.Println("Account,Computer")
	for _, edge := range data.Data.Edges {
		sourceLabel, sourceExists := nodeMap[edge.Source]
		targetLabel, targetExists := nodeMap[edge.Target]
		if !sourceExists || !targetExists {
			continue // Optionally log this error to stderr or a log file
		}
		fmt.Printf("%s,%s\n", sourceLabel, targetLabel)
	}
}

func printHelp() {
	fmt.Fprintln(os.Stderr, "Usage: rbac_flatten <input.json>")
}
