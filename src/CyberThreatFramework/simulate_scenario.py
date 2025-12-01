import subprocess
import time
import os
import sys

# Ensure we are in the repo root
REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
os.chdir(REPO_ROOT)

PYTHON_EXEC = "/home/suzy/Python_Malwares_Repo/venv/bin/python"
MAIN_SCRIPT = "/home/suzy/Python_Malwares_Repo/src/CyberThreatFramework/main.py"
TARGET_SCRIPT = "/home/suzy/Python_Malwares_Repo/src/CyberThreatFramework/utils/dummy_target.py"

def run_command(cmd):
    print(f"\n>>> Running: {cmd}")
    subprocess.run(cmd, shell=True)
    time.sleep(1)

def main():
    print("=== Starting Full Attack Chain Simulation ===")
    
    # 1. Start Dummy Target
    print("\n[Step 1] Setting up Vulnerable Target...")
    target_proc = subprocess.Popen([PYTHON_EXEC, TARGET_SCRIPT], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    time.sleep(2) # Wait for it to start
    
    try:
        # 2. Reconnaissance
        print("\n[Step 2] Reconnaissance: Port Scanning")
        print("Attacker is scanning the target to find open doors...")
        # Scan localhost on the dummy ports
        run_command(f"{PYTHON_EXEC} {MAIN_SCRIPT} scan 127.0.0.1 --ports 2222 8080 9090")
        
        # 3. Initial Access
        print("\n[Step 3] Initial Access: Brute Force")
        print("Attacker found SSH on port 2222. Attempting to crack credentials...")
        # Use simulation mode to show success
        run_command(f"{PYTHON_EXEC} {MAIN_SCRIPT} bruteforce 127.0.0.1 --port 2222 --users admin root --passwords pass123 secret --simulate")
        
        # 4. Impact
        print("\n[Step 4] Impact: Ransomware")
        print("Attacker has gained access. Deploying ransomware...")
        # Create dummy data
        if not os.path.exists("victim_data"):
            os.makedirs("victim_data")
            with open("victim_data/financials.xls", "w") as f: f.write("Confidential Data")
            with open("victim_data/passwords.txt", "w") as f: f.write("MySecretPass")
            
        run_command(f"{PYTHON_EXEC} {MAIN_SCRIPT} ransomware victim_data")
        
        # 5. Analysis
        print("\n[Step 5] Analysis & Visualization")
        print("Generating reports...")
        run_command(f"{PYTHON_EXEC} {MAIN_SCRIPT} visualize")
        
    finally:
        print("\n[Cleanup] Stopping Vulnerable Target...")
        target_proc.terminate()
        
    print("\n=== Simulation Complete ===")
    print("Check the Dashboard at http://127.0.0.1:5002 to see the results!")

if __name__ == "__main__":
    main()
