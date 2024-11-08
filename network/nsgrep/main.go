package main

import (
        "bufio"
        "fmt"
        "net"
        "os"
        "strings"
)

func main() {
        var f *os.File
        if len(os.Args) > 1 {
                var err error
                // Read from file
                f, err = os.Open(os.Args[1])
                if err != nil {
                        panic(fmt.Sprintf("Error opening file: %s", os.Args[1]))
                }
        } else {
                // Read from stdin
                f = os.Stdin
        }

        scanner := bufio.NewScanner(f)
        for scanner.Scan() {
                target := scanner.Text()
                // Filter input
                sanitized, err := sanitizeInput(target)
                if err != nil {
                        fmt.Fprintln(os.Stderr, fmt.Sprintf("%s: Error occurred: %s", target, err.Error()))
                }

                _, err = net.LookupIP(sanitized)
                if err != nil {
                        continue
                }
                fmt.Println(sanitized)

        }
        if err := scanner.Err(); err != nil {
                fmt.Fprintln(os.Stderr, fmt.Sprintf("Error occurred reading input: %s", err.Error()))
        }

}

// sanitizeInput does some rudimentary input checking
func sanitizeInput(s string) (string, error) {
        // Remove trailing spaces
        trimmed := strings.TrimSpace(s)

        // Each domain should at least contain a dot, so do this as final check
        if strings.Contains(trimmed, ".") {
                return trimmed, nil
        }
        return "", fmt.Errorf("Invalid name: %s", s)
}
