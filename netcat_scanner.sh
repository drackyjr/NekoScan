#!/bin/bash

# =========================================
# Simple Netcat Port Scanner
# =========================================
# A lightweight alternative using netcat for port scanning

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default settings
TIMEOUT=3
VERBOSE=false

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] <target> <port_range>"
    echo "Options:"
    echo "  -v      Verbose output"
    echo "  -t <n>  Timeout in seconds (default: 3)"
    echo "  -h      Show this help"
    echo
    echo "Examples:"
    echo "  $0 192.168.1.1 1-100"
    echo "  $0 -v -t 2 google.com 80,443,8080"
}

# Parse arguments
while getopts "vt:h" opt; do
    case $opt in
        v) VERBOSE=true ;;
        t) TIMEOUT=$OPTARG ;;
        h) show_usage; exit 0 ;;
        *) show_usage; exit 1 ;;
    esac
done
shift $((OPTIND-1))

# Validate arguments
if [ $# -ne 2 ]; then
    echo "Error: Invalid arguments"
    show_usage
    exit 1
fi

TARGET=$1
PORT_RANGE=$2

# Check if netcat is available
if ! command -v nc &> /dev/null; then
    echo -e "${RED}Error: netcat (nc) is not installed${NC}"
    exit 1
fi

# Function to scan ports with netcat
scan_with_netcat() {
    local target=$1
    local ports=$2

    echo -e "${BLUE}[*] Scanning $target with netcat...${NC}"
    echo -e "${BLUE}[*] Port range: $ports${NC}"
    echo -e "${BLUE}[*] Timeout: ${TIMEOUT}s${NC}"
    echo

    # Use netcat to scan ports
    if [[ $ports == *-* ]]; then
        # Range format (e.g., 1-100)
        IFS='-' read -ra RANGE <<< "$ports"
        start=${RANGE[0]}
        end=${RANGE[1]}

        echo -e "${YELLOW}Scanning ports $start to $end...${NC}"

        for port in $(seq $start $end); do
            if nc -z -v -w$TIMEOUT "$target" "$port" 2>&1 | grep -q "succeeded"; then
                echo -e "${GREEN}[+] Port $port/tcp is open${NC}"
            elif [[ $VERBOSE == true ]]; then
                echo -e "${RED}[-] Port $port/tcp is closed${NC}"
            fi
        done
    elif [[ $ports == *,* ]]; then
        # Comma-separated format (e.g., 80,443,8080)
        IFS=',' read -ra PORT_LIST <<< "$ports"

        echo -e "${YELLOW}Scanning specific ports...${NC}"

        for port in "${PORT_LIST[@]}"; do
            if nc -z -v -w$TIMEOUT "$target" "$port" 2>&1 | grep -q "succeeded"; then
                echo -e "${GREEN}[+] Port $port/tcp is open${NC}"
            elif [[ $VERBOSE == true ]]; then
                echo -e "${RED}[-] Port $port/tcp is closed${NC}"
            fi
        done
    else
        # Single port
        if nc -z -v -w$TIMEOUT "$target" "$ports" 2>&1 | grep -q "succeeded"; then
            echo -e "${GREEN}[+] Port $ports/tcp is open${NC}"
        else
            echo -e "${RED}[-] Port $ports/tcp is closed${NC}"
        fi
    fi

    echo
    echo -e "${BLUE}[*] Scan completed!${NC}"
}

# Perform the scan
scan_with_netcat "$TARGET" "$PORT_RANGE"
