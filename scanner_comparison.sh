#!/bin/bash

# =========================================
# Port Scanner Comparison Tool
# =========================================
# Compare results between different scanning methods

show_banner() {
    echo "┌─────────────────────────────────────────┐"
    echo "│        Port Scanner Comparison          │"
    echo "└─────────────────────────────────────────┘"
}

compare_scanners() {
    local target=$1
    local ports=$2

    echo "Comparing scanning methods for $target on ports $ports"
    echo

    # Method 1: /dev/tcp
    echo "=== Method 1: /dev/tcp ==="
    time {
        for port in $(echo $ports | tr ',' ' '); do
            (echo >/dev/tcp/$target/$port) &>/dev/null && echo "Port $port: OPEN"
        done
    }

    echo

    # Method 2: netcat (if available)
    if command -v nc &> /dev/null; then
        echo "=== Method 2: netcat ==="
        time {
            echo $ports | tr ',' '\n' | while read port; do
                nc -z -w1 $target $port 2>/dev/null && echo "Port $port: OPEN"
            done
        }
        echo
    fi

    # Method 3: telnet (if available)
    if command -v telnet &> /dev/null; then
        echo "=== Method 3: telnet ==="
        time {
            echo $ports | tr ',' '\n' | while read port; do
                timeout 1 telnet $target $port </dev/null 2>/dev/null | grep -q "Connected" && echo "Port $port: OPEN"
            done
        }
        echo
    fi
}

# Main execution
if [ $# -ne 2 ]; then
    show_banner
    echo "Usage: $0 <target> <ports>"
    echo "Example: $0 google.com 80,443,8080"
    exit 1
fi

show_banner
compare_scanners $1 $2
