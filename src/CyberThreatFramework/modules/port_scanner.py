from scapy.all import IP, TCP, sr1, ICMP
import socket
import time

class PortScanner:
    def __init__(self, logger):
        self.logger = logger

    def scan(self, target_ip, ports):
        self.logger.log_event("PortScanner", "Start", f"Scanning {target_ip} ports {ports}")
        print(f"[*] Starting Port Scan on {target_ip}")
        print(f"[*] Target identified. Enumerating {len(ports)} ports...")
        time.sleep(1)
        
        results = {}
        
        # Try Scapy first (might fail without root)
        try:
            for port in ports:
                print(f"  > Probing port {port}/TCP...", end=" ", flush=True)
                time.sleep(0.5) # Cinematic delay
                
                # Simple SYN scan
                self.logger.log_event("PortScanner", "Attempt", f"Scapy scanning port {port}")
                pkt = IP(dst=target_ip)/TCP(dport=port, flags="S")
                resp = sr1(pkt, timeout=1, verbose=0)
                
                state = "Closed"
                if resp:
                    if resp.haslayer(TCP):
                        if resp.getlayer(TCP).flags == 0x12: # SYN-ACK
                            state = "Open"
                            # Send RST to close connection
                            sr1(IP(dst=target_ip)/TCP(dport=port, flags="R"), timeout=1, verbose=0)
                        elif resp.getlayer(TCP).flags == 0x14: # RST-ACK
                            state = "Closed"
                
                results[port] = state
                self.logger.log_event("PortScanner", "Result", f"Port {port} is {state}")
                
                if state == "Open":
                    print(f"\033[92m[OPEN]\033[0m") # Green text
                else:
                    print(f"\033[91m[CLOSED]\033[0m") # Red text
                
        except Exception as e:
            print(f"\n[!] Scapy scan failed: {e}. Falling back to Socket.")
            self.logger.log_event("PortScanner", "Error", f"Scapy scan failed/impaired: {e}. Falling back to Socket.", status="WARNING")
            results = self.socket_scan(target_ip, ports)
            
        print("[*] Scan Complete.")
        return results

    def socket_scan(self, target_ip, ports):
        results = {}
        for port in ports:
            print(f"  > Connecting to port {port}...", end=" ", flush=True)
            time.sleep(0.3)
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    results[port] = "Open"
                    print(f"\033[92m[OPEN]\033[0m")
                else:
                    results[port] = "Closed"
                    print(f"\033[91m[CLOSED]\033[0m")
                sock.close()
                self.logger.log_event("PortScanner", "Result", f"Port {port} is {results[port]} (Socket)")
            except Exception as e:
                print(f"[ERROR] {e}")
                self.logger.log_event("PortScanner", "Error", f"Socket scan error on port {port}: {e}", status="ERROR")
                results[port] = "Error"
        return results
