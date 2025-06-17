import socket
import threading
import time
import os
from queue import Queue
from colorama import init, Fore, Style
from termcolor import colored

# === INIT COLORAMA ===
init(autoreset=True)

# === CONFIGURATION ===
start_port = 1
end_port = 65000
threads = 1000
queue = Queue()
open_ports = []
scan_done = False

# === COLORFUL CAT FRAMES ===
frames = [
f"""
{Fore.GREEN}     /\\_/\\  
    ( -.- )  < Scanning
     > ^ <  
""",
f"""
{Fore.CYAN}     /\\_/\\  
    ( o.o )  < Scanning.
     > ^ <  
""",
f"""
{Fore.YELLOW}     /\\_/\\  
    ( O_O )  < Scanning..
     > ^ <  
""",
f"""
{Fore.MAGENTA}     /\\_/\\  
    ( ^.^ )  < Scanning...
     > ^ <  
"""
]

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def animate_cat():
    while not scan_done:
        for frame in frames:
            if scan_done:
                break
            clear()
            print(frame)
            print(colored("NekoScan - Port Scanner", "yellow", attrs=["bold"]))
            print(colored("by Dracky Jr\n", "cyan"))
            print(colored(f"[*] Open ports so far: {len(open_ports)}", "cyan"))
            time.sleep(0.4)

    # Final display after scanning is done
    clear()
    print(frames[-1])
    print(colored("NekoScan - Port Scanner", "yellow", attrs=["bold"]))
    print(colored("by Dracky Jr\n", "cyan"))
    print(colored("[✔] Scanning complete.\n", "green"))

    if open_ports:
        print(colored("[+] Open Ports Found:\n", "green", attrs=["bold"]))
        print(f"{'PORT':<8}{'PROTO':<8}{'SERVICE':<15}{'BANNER'}")
        print("-" * 60)
        for port, banner in sorted(open_ports):
            try:
                service = socket.getservbyport(port)
            except:
                service = "unknown"
            port_str = colored(f"{port:<8}", "yellow")
            proto_str = colored("TCP", "cyan")
            service_str = colored(f"{service:<15}", "magenta")
            banner_str = colored(banner, "white")
            print(f"{port_str}{proto_str:<8}{service_str}{banner_str}")
    else:
        print(colored("[-] No open ports found.", "red"))

def resolve_target(target):
    try:
        ip = socket.gethostbyname(target)
        return ip
    except socket.gaierror:
        print(colored("[-] Invalid domain or IP.", "red"))
        exit()

def scan_port(ip, port):
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(0.5)
        result = sock.connect_ex((ip, port))
        if result == 0:
            try:
                banner = sock.recv(1024).decode(errors="ignore").strip()
            except:
                banner = "No Banner"
            open_ports.append((port, banner if banner else "No Banner"))
        sock.close()
    except:
        pass

def worker(ip):
    while not queue.empty():
        port = queue.get()
        scan_port(ip, port)
        queue.task_done()

def run_scanner(ip):
    for port in range(start_port, end_port + 1):
        queue.put(port)

    for _ in range(threads):
        t = threading.Thread(target=worker, args=(ip,))
        t.daemon = True
        t.start()

    queue.join()
    global scan_done
    scan_done = True

# === MAIN ENTRY POINT ===
if __name__ == "__main__":
    clear()
    print(colored("="*50, "magenta", attrs=["bold"]))
    print(colored("NekoScan - Port Scanner", "yellow", attrs=["bold"]))
    print(colored("by Dracky Jr", "cyan"))
    print(colored("="*50 + "\n", "magenta", attrs=["bold"]))

    target = input(colored("Enter target domain or IP: ", "cyan")).strip()
    ip = resolve_target(target)

    anim_thread = threading.Thread(target=animate_cat)
    anim_thread.start()

    run_scanner(ip)

    anim_thread.join()

