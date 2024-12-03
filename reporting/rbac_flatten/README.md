# RBAC_flatten

Flattens the RBAC results from Bloodhound to a CSV-style format

1. `go build main.go`
2. In the Bloodhound UI, use `MATCH p=(m:User)-[r:AdminTo]->(n:Computer) RETURN p` to render the graph and save the JSON. 
3. `main bh-graph.json > rbac_flattened.csv`

You can further post-process it in Excel.
