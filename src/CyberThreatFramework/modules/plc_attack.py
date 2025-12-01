import time
import random

class PLCAttacker:
    def __init__(self, logger):
        self.logger = logger

    def modbus_attack(self, target_ip, port=502):
        self.logger.log_event("PLC_Attack", "Start", f"Targeting PLC at {target_ip}:{port}")
        print(f"[*] Initializing Industrial Protocol Attack on {target_ip}:{port}")
        print("[*] Protocol: Modbus/TCP")
        time.sleep(1)

        # 1. Recon - Identify Device
        print(f"  > Sending Device ID Request...", end=" ", flush=True)
        time.sleep(0.8)
        print(f"\033[92m[ACK]\033[0m")
        print(f"    [+] Device Found: Siemens S7-1200 (Simulated)")
        self.logger.log_event("PLC_Attack", "Recon", "Identified Siemens S7-1200")
        
        # 2. Scan Registers
        print(f"  > Scanning Holding Registers (40001-40100)...")
        for i in range(5):
            reg = 40001 + i*10
            val = random.randint(0, 65535)
            print(f"    - Register {reg}: {val}")
            time.sleep(0.2)
            
        # 3. The Attack - Overwrite Critical Values
        print(f"[*] \033[91mINJECTING MALICIOUS PAYLOAD\033[0m")
        target_registers = [40005, 40006, 40010] # Temperature, Pressure, Safety Cutoff
        
        for reg in target_registers:
            print(f"  > Overwriting Register {reg} (Safety Limit)...", end=" ", flush=True)
            time.sleep(0.6)
            print(f"\033[91m[SUCCESS]\033[0m")
            self.logger.log_event("PLC_Attack", "Exploit", f"Overwrote Register {reg} with unsafe value")
            
        # 4. Impact
        print(f"[*] \033[91mCRITICAL ALERT: TURBINE OVERSPEED DETECTED\033[0m")
        print(f"[*] \033[91mSAFETY SYSTEMS DISABLED\033[0m")
        self.logger.log_event("PLC_Attack", "Impact", "Safety systems disabled, turbine overspeed")
        
        print("[*] Attack Complete. Process disrupted.")
