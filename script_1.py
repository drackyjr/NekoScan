# Create a simple netcat-based port scanner as an alternative
netcat_scanner = '''#!/bin/bash

# =========================================
# Simple Netcat Port Scanner
# =========================================
# A lightweight alternative using netcat for port scanning

# Color codes
RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m' # No Color

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
'''

# Create a port scanner comparison tool
comparison_tool = '''#!/bin/bash

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
            echo $ports | tr ',' '\\n' | while read port; do
                nc -z -w1 $target $port 2>/dev/null && echo "Port $port: OPEN"
            done
        }
        echo
    fi
    
    # Method 3: telnet (if available)
    if command -v telnet &> /dev/null; then
        echo "=== Method 3: telnet ==="
        time {
            echo $ports | tr ',' '\\n' | while read port; do
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
'''

# Create an installation and setup script
install_script = '''#!/bin/bash

# =========================================
# TCP Port Scanner Installation Script
# =========================================

RED='\\033[0;31m'
GREEN='\\033[0;32m'
YELLOW='\\033[1;33m'
BLUE='\\033[0;34m'
NC='\\033[0m'

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
'''

# Create a comprehensive README
readme_content = '''# Advanced TCP Port Scanner Toolkit

A comprehensive collection of bash-based TCP port scanning tools designed for network analysis, security assessment, and system administration.

## Features

### 🚀 Advanced TCP Scanner (`tcp_scanner.sh`)
- **Multiple Scan Modes**: Quick scan (common ports), full scan (all 65535 ports), custom ranges
- **Parallel Processing**: Configurable thread count for high-speed scanning
- **Stealth Mode**: Less detectable scanning with controlled timing
- **Flexible Input**: Support for IP addresses, hostnames, and CIDR notation
- **Comprehensive Output**: Colored terminal output with detailed results
- **Service Detection**: Automatic identification of common services
- **Export Functionality**: Save results to file for analysis
- **Signal Handling**: Graceful interruption and cleanup

### 🔧 Netcat Scanner (`netcat_scanner.sh`)
- Lightweight alternative using netcat
- Simple command-line interface
- Timeout controls
- Verbose output options

### 📊 Scanner Comparison (`scanner_comparison.sh`)
- Compare different scanning methods
- Performance benchmarking
- Multiple technique evaluation

## Installation

1. **Download the toolkit:**
   ```bash
   # If you have the scripts, make them executable
   chmod +x *.sh
   
   # Or run the installation script
   ./install.sh
   ```

2. **Verify dependencies:**
   - `bash` (version 4.0+)
   - `timeout` command
   - `netcat` (optional, for netcat scanner)

## Usage

### Basic Examples

```bash
# Scan common ports on a target
./tcp_scanner.sh 192.168.1.1

# Verbose scan with 5-second timeout
./tcp_scanner.sh -v -t 5 google.com

# Full port scan with results saved to file
./tcp_scanner.sh -f -o results.txt 10.0.0.1

# Stealth scan of specific ports
./tcp_scanner.sh -s -p 22,80,443,8080 example.com

# Quick scan with netcat
./netcat_scanner.sh -v google.com 80,443
```

### Advanced Examples

```bash
# High-speed scan with 100 threads
./tcp_scanner.sh -T 100 -p 1-10000 target.com

# Comprehensive scan with all options
./tcp_scanner.sh -v -c -t 3 -T 50 -o comprehensive_scan.txt target.com

# Compare scanning methods
./scanner_comparison.sh google.com 80,443,8080
```

## Command-Line Options

### tcp_scanner.sh Options

| Option | Description | Default |
|--------|-------------|---------|
| `-h, --help` | Show help message | - |
| `-v, --verbose` | Enable verbose output | false |
| `-t, --timeout <sec>` | Connection timeout | 3 |
| `-T, --threads <num>` | Number of parallel threads | 50 |
| `-o, --output <file>` | Output results to file | - |
| `-s, --stealth` | Enable stealth mode | false |
| `-c, --closed` | Show closed ports | false |
| `-q, --quick` | Quick scan (common ports) | - |
| `-f, --full` | Full scan (all 65535 ports) | - |
| `-p, --ports <range>` | Custom port range | common ports |

### Port Range Formats

- **Single port**: `80`
- **Port list**: `22,80,443,8080`
- **Port range**: `1-1000`
- **Mixed**: `22,80,443,8000-8100`

## Technical Details

### Scanning Methods

1. **TCP Connect Scan**: Uses bash's `/dev/tcp` pseudo-device
2. **Parallel Processing**: Background job management for speed
3. **Timeout Control**: Prevents hanging on unresponsive ports
4. **Stealth Techniques**: Controlled timing to avoid detection

### Performance Considerations

- **Thread Count**: Balance between speed and system resources
- **Timeout Values**: Shorter timeouts = faster scans, potential false negatives
- **Network Conditions**: Adjust settings based on network latency
- **Target Responsiveness**: Some targets may require longer timeouts

### Security and Ethics

⚠️ **Important**: This tool is for authorized testing only. 

- Only scan systems you own or have explicit permission to test
- Respect network policies and rate limiting
- Be aware of legal implications in your jurisdiction
- Use stealth mode responsibly to minimize network impact

## Output Examples

### Standard Output
```
┌─────────────────────────────────────────────────────────┐
│              Advanced TCP Port Scanner                  │
│          Fast, Efficient Network Analysis Tool         │
└─────────────────────────────────────────────────────────┘

Scanning target: google.com
Port range: 10 ports
Timeout: 3s
Threads: 50
Stealth mode: false

[*] Starting TCP port scan...
[+] Port 80/tcp is open
[+] Port 443/tcp is open

=== SCAN RESULTS ===
Target: google.com
Scan Duration: 2s
Total Ports Scanned: 10
Open Ports: 2

OPEN PORTS:
Port    Service
----    -------
80/tcp  http
443/tcp https

[*] Scan completed!
```

### File Output
```
TCP Port Scan Results
====================
Target: google.com
Scan Date: Thu Sep 18 13:35:00 IST 2025
Total Ports Scanned: 10
Open Ports Found: 2

OPEN PORTS:
Port    Service
----    -------
80/tcp  http
443/tcp https
```

## Troubleshooting

### Common Issues

1. **Permission Denied**
   ```bash
   chmod +x tcp_scanner.sh
   ```

2. **Timeout Command Not Found**
   ```bash
   # Install coreutils package
   sudo apt-get install coreutils  # Ubuntu/Debian
   sudo yum install coreutils      # CentOS/RHEL
   ```

3. **Slow Scanning**
   - Reduce thread count: `-T 10`
   - Increase timeout: `-t 5`
   - Use stealth mode: `-s`

4. **False Negatives**
   - Increase timeout value
   - Try different scanning methods
   - Check network connectivity

### Performance Tuning

- **Fast Networks**: Use higher thread counts (100-200)
- **Slow Networks**: Lower thread counts (10-25), higher timeouts
- **Stealth Requirements**: Use stealth mode with lower thread counts
- **Large Ranges**: Consider breaking into smaller chunks

## Contributing

Feel free to contribute improvements, bug fixes, or additional features:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This toolkit is provided for educational and authorized testing purposes. Use responsibly and in accordance with applicable laws and regulations.

## Acknowledgments

- Inspired by nmap and other professional scanning tools
- Built using standard Unix/Linux utilities
- Community feedback and contributions

---

**Disclaimer**: This tool is for authorized security testing and network administration only. Users are responsible for ensuring they have proper authorization before scanning any networks or systems.
'''

# Write all the files
with open('netcat_scanner.sh', 'w') as f:
    f.write(netcat_scanner)

with open('scanner_comparison.sh', 'w') as f:
    f.write(comparison_tool)

with open('install.sh', 'w') as f:
    f.write(install_script)

with open('README.md', 'w') as f:
    f.write(readme_content)

print("Complete TCP Port Scanner Toolkit created!")
print("\nFiles created:")
print("1. tcp_scanner.sh - Advanced multi-threaded scanner")
print("2. netcat_scanner.sh - Simple netcat-based scanner") 
print("3. scanner_comparison.sh - Method comparison tool")
print("4. install.sh - Installation and setup script")
print("5. README.md - Comprehensive documentation")
print("6. usage_examples.txt - Quick usage reference")

print("\nTo get started:")
print("1. Run: chmod +x *.sh")
print("2. Run: ./install.sh") 
print("3. Try: ./tcp_scanner.sh --help")