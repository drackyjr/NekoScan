
# 🐾 NekoScan - Port Scanner

**NekoScan** is a fast, colorful, and fun terminal-based **TCP port scanner** with animated ASCII cats and live port discovery.  
Built with love by **Dracky Jr**, this tool combines performance with a playful interface — perfect for developers, cybersecurity students, and enthusiasts.

---

## ✨ Features

- ⚡ Ultra-fast multithreaded TCP scanning (1000 threads by default)
- 🐱 Cute animated cat frames during scanning
- 🎨 Color-coded, real-time terminal output
- 🔍 Live tracking of discovered open ports
- 📡 Banner grabbing from open services
- 🔒 Works on Linux, Windows, and macOS

---

## 📸 Preview

```

```
 /\_/\
( ^.^ )  < Scanning...
 > ^ <
```

NekoScan - Port Scanner
by Dracky Jr

\[\*] Open ports so far: 8

````

---

## 🚀 Getting Started

### 📦 Requirements

- Python 3.6 or higher
- Install dependencies:

```bash
pip install colorama termcolor
````

---

### ▶️ How to Use

1. Clone the repository:

```bash
git clone https://github.com/drackyjr/NekoScan.git
cd NekoScan
```

2. Run the scanner:

```bash
python NekoScan.py
```

3. Enter the target IP address or domain when prompted:

```
Enter target domain or IP: 192.168.1.1
```

---

## ⚙️ Configuration

You can modify these parameters in `NekoScan.py` to suit your needs:

```python
start_port = 1       # Starting port
end_port = 10000     # Ending port
threads = 1000       # Number of concurrent threads
```

---

## 📁 Sample Output

Once scanning is done, NekoScan will display open ports like this:

```
[+] Open Ports Found:

PORT    PROTO   SERVICE        BANNER
------------------------------------------------------------
22      TCP     ssh            OpenSSH 7.6p1 Ubuntu
80      TCP     http           Apache/2.4.29 (Ubuntu)
443     TCP     https          nginx
```

---

## 🧠 Notes

* NekoScan performs **TCP connect scans**.
* Intended for **educational and ethical use only**.
* No logging or saving is done — everything is terminal-based.

---

## 🧑‍💻 Author

**Dracky Jr**
🔗 GitHub: [dracky](https://github.com/drackyjr)


---




