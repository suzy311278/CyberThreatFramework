
ATTACK_CATALOG = [
    {
        "id": "T1046", 
        "name": "Network Service Scanning", 
        "tactic": "Discovery", 
        "description": "Adversaries may attempt to get a listing of services running on remote hosts.", 
        "tool": "scan",
        "compromise": "The attacker identifies open ports (doors) on your server. This reveals what services are running (e.g., SSH, Web, Database) and helps them choose the right exploit.",
        "mitigation": "1. Use a Firewall to block unused ports.\n2. Implement Port Knocking.\n3. Use IDS/IPS to detect scanning activity."
    },
    {
        "id": "T1110", 
        "name": "Brute Force", 
        "tactic": "Credential Access", 
        "description": "Adversaries may use brute force techniques to gain access to accounts.", 
        "tool": "bruteforce",
        "compromise": "The attacker guesses thousands of password combinations until one works. Once successful, they have full access to the user's account.",
        "mitigation": "1. Enforce strong, complex passwords.\n2. Implement Account Lockout policies after N failed attempts.\n3. Use Multi-Factor Authentication (MFA)."
    },
    {
        "id": "T1486", 
        "name": "Data Encrypted for Impact", 
        "tactic": "Impact", 
        "description": "Adversaries may encrypt data on target systems to interrupt availability.", 
        "tool": "ransomware",
        "compromise": "The attacker runs a malicious script that encrypts your files with a secret key. You lose access to your data unless you have the key.",
        "mitigation": "1. Maintain offline backups.\n2. Use Endpoint Detection and Response (EDR).\n3. Restrict file permissions."
    },
    {
        "id": "T0831", 
        "name": "Manipulation of Control", 
        "tactic": "Impact (ICS)", 
        "description": "Adversaries may manipulate control logic or values to disrupt industrial processes.", 
        "tool": "plc",
        "compromise": "The attacker sends Modbus/TCP commands to a PLC (Programmable Logic Controller) to overwrite safety limits (e.g., max temperature), causing physical damage.",
        "mitigation": "1. Segregate ICS/SCADA networks from the internet (Air Gap).\n2. Use Deep Packet Inspection (DPI) for Modbus.\n3. Implement Read-Only permissions on critical registers."
    },
    {"id": "T1566", "name": "Phishing", "tactic": "Initial Access", "description": "Adversaries may send phishing messages to gain access to victim systems.", "tool": "phishing", "compromise": "User clicks a malicious link.", "mitigation": "User training and Email filtering."},
    {"id": "T1498", "name": "Network Denial of Service", "tactic": "Impact", "description": "Adversaries may perform DoS attacks to degrade availability.", "tool": "dos", "compromise": "Flooding the network with traffic.", "mitigation": "Rate limiting and CDNs."}
]

THREAT_ACTORS = [
    {"name": "APT28 (Fancy Bear)", "origin": "Russia", "targets": ["Government", "Military", "Security"], "description": "Known for using phishing and zero-day exploits."},
    {"name": "APT29 (Cozy Bear)", "origin": "Russia", "targets": ["Government", "Think Tanks"], "description": "Stealthy actor focusing on long-term intelligence gathering."},
    {"name": "Lazarus Group", "origin": "North Korea", "targets": ["Financial", "Media"], "description": "Responsible for the Sony hack and WannaCry ransomware."},
    {"name": "Equation Group", "origin": "USA", "targets": ["Government", "Telecom"], "description": "Highly sophisticated actor linked to Stuxnet."},
    {"name": "OilRig", "origin": "Iran", "targets": ["Energy", "Government"], "description": "Focuses on Middle Eastern targets using social engineering."},
    {"name": "Sandworm", "origin": "Russia", "targets": ["Energy", "ICS"], "description": "Known for attacks on Ukrainian power grid (BlackEnergy)."}
]
