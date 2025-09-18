#Nekoscan TCP Port Scanner 

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
