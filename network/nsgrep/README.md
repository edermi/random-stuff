# nsgrep

Small go tool that filters out hostnames that aren't resolvable. 
Just `cat allhosts.txt | nsgrep > resolvable_hosts.txt``. 

Faster than a dig for-loop. Also, prints the hostnames and not the resolved addresses.

Building should be as easy as `go build`.
