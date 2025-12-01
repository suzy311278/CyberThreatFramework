import argparse
import sys
import os

# Add src to path to allow imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.CyberThreatFramework.utils.logger import ThreatLogger
from src.CyberThreatFramework.modules.port_scanner import PortScanner
from src.CyberThreatFramework.modules.ransomware import RansomwareSimulator
from src.CyberThreatFramework.modules.brute_force import BruteForceSimulator

def main():
    parser = argparse.ArgumentParser(description="Cyber Threat Simulation Framework")
    subparsers = parser.add_subparsers(dest="command", help="Available simulations")

    # Port Scan
    scan_parser = subparsers.add_parser("scan", help="Run Port Scanner")
    scan_parser.add_argument("target", help="Target IP address")
    scan_parser.add_argument("--ports", nargs="+", type=int, default=[22, 80, 443, 8080], help="Ports to scan")

    # Ransomware
    ransom_parser = subparsers.add_parser("ransomware", help="Run Ransomware Simulation")
    ransom_parser.add_argument("directory", help="Directory to encrypt")
    ransom_parser.add_argument("--decrypt", action="store_true", help="Decrypt instead of encrypt")
    ransom_parser.add_argument("--key", help="Path to key file for decryption")

    # Brute Force
    brute_parser = subparsers.add_parser("bruteforce", help="Run SSH Brute Force")
    brute_parser.add_argument("target", help="Target IP address")
    brute_parser.add_argument("--users", nargs="+", default=["root", "admin", "user"], help="Usernames to try")
    brute_parser.add_argument("--passwords", nargs="+", default=["password", "123456", "admin"], help="Passwords to try")
    brute_parser.add_argument("--port", type=int, default=22, help="SSH Port")
    brute_parser.add_argument("--simulate", action="store_true", help="Simulate attack without real connection")

    # PLC Attack
    plc_parser = subparsers.add_parser("plc", help="Run ICS/PLC Attack Simulation")
    plc_parser.add_argument("target", help="Target IP address")

    # Visualize
    subparsers.add_parser("visualize", help="Generate visualization from logs")

    args = parser.parse_args()
    
    logger = ThreatLogger()
    
    if args.command == "scan":
        scanner = PortScanner(logger)
        print(f"Starting scan on {args.target}...")
        scanner.scan(args.target, args.ports)
        print("Scan complete. Check logs for details.")
        
    elif args.command == "ransomware":
        ransom = RansomwareSimulator(logger)
        if args.decrypt:
            if not args.key:
                print("Error: --key is required for decryption")
                return
            print(f"Decrypting {args.directory}...")
            ransom.decrypt_directory(args.directory, args.key)
        else:
            print(f"Encrypting {args.directory}...")
            ransom.encrypt_directory(args.directory)
        print("Operation complete.")
            
    elif args.command == "bruteforce":
        bf = BruteForceSimulator(logger)
        print(f"Starting brute force on {args.target}...")
        bf.ssh_brute_force(args.target, args.users, args.passwords, args.port, simulate=args.simulate)
        print("Brute force complete.")

    elif args.command == "plc":
        from src.CyberThreatFramework.modules.plc_attack import PLCAttacker
        plc = PLCAttacker(logger)
        plc.modbus_attack(args.target)

    elif args.command == "visualize":
        from src.CyberThreatFramework.utils.visualizer import ThreatVisualizer
        print("Generating visualizations...")
        viz = ThreatVisualizer()
        viz.plot_activity()
        viz.plot_attack_graph()
        
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
