#!/bin/bash

# =========================================
# TCP Port Scanner Installation Script
# =========================================

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}Installing TCP Port Scanner Toolkit...${NC}"
echo

# Make scripts executable
chmod +x tcp_scanner.sh 2>/dev/null || echo -e "${YELLOW}Warning: tcp_scanner.sh not found${NC}"
chmod +x netcat_scanner.sh 2>/dev/null || echo -e "${YELLOW}Warning: netcat_scanner.sh not found${NC}"
chmod +x scanner_comparison.sh 2>/dev/null || echo -e "${YELLOW}Warning: scanner_comparison.sh not found${NC}"

# Check for required dependencies
echo -e "${BLUE}Checking dependencies...${NC}"

dependencies=("bash" "timeout" "seq")
missing=()

for dep in "${dependencies[@]}"; do
    if ! command -v $dep &> /dev/null; then
        missing+=($dep)
    fi
done

if [ ${#missing[@]} -eq 0 ]; then
    echo -e "${GREEN}✓ All required dependencies are available${NC}"
else
    echo -e "${RED}✗ Missing dependencies: ${missing[*]}${NC}"
    echo -e "${YELLOW}Please install missing dependencies and run this script again${NC}"
fi

# Check for optional dependencies
echo -e "${BLUE}Checking optional dependencies...${NC}"

optional=("nc" "netcat" "nmap" "telnet")
available=()
unavailable=()

for opt in "${optional[@]}"; do
    if command -v $opt &> /dev/null; then
        available+=($opt)
    else
        unavailable+=($opt)
    fi
done

if [ ${#available[@]} -gt 0 ]; then
    echo -e "${GREEN}✓ Available optional tools: ${available[*]}${NC}"
fi

if [ ${#unavailable[@]} -gt 0 ]; then
    echo -e "${YELLOW}○ Optional tools not installed: ${unavailable[*]}${NC}"
    echo -e "${YELLOW}  Consider installing these for additional functionality${NC}"
fi

echo
echo -e "${GREEN}Installation completed!${NC}"
echo
echo "Usage examples:"
echo -e "${CYAN}  ./tcp_scanner.sh --help${NC}"
echo -e "${CYAN}  ./tcp_scanner.sh 192.168.1.1${NC}"
echo -e "${CYAN}  ./tcp_scanner.sh -v -p 1-1000 google.com${NC}"
echo -e "${CYAN}  ./netcat_scanner.sh -v google.com 80,443${NC}"
