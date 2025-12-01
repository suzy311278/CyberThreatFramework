# Cyber Threat Simulation Framework

**Developed by:** Sushant Kumar Tiwari

A professional, modular Cyber Threat Simulation Framework designed to model, execute, and visualize cyber attacks in a controlled environment. This tool helps security professionals and students understand attack vectors, validate defense mechanisms, and analyze attack chains through a real-time dashboard.

![Dashboard Preview](https://via.placeholder.com/800x400?text=Cyber+Threat+Simulation+Dashboard)

## 🚀 Features

*   **Interactive Dashboard:** A professional Red/White themed web interface to control simulations.
*   **Attack Modules:**
    *   **Network Scanning (T1046):** Simulates port scanning and service discovery.
    *   **SSH Brute Force (T1110):** Simulates credential access attacks.
    *   **Ransomware (T1486):** Simulates file encryption (safely in a dummy directory).
    *   **ICS/PLC Manipulation (T0831):** Simulates attacks on Industrial Control Systems (Modbus).
*   **Real-time Visualization:**
    *   **Attack Chain Graph:** Dynamically generated flowcharts showing the step-by-step execution of attacks.
    *   **Timeline:** Visual history of events.
*   **MITRE ATT&CK Integration:** All attacks are mapped to their respective MITRE T-codes with direct links to the knowledge base.
*   **Interactive Guide:** Built-in tour to walk users through the application features.

## 🛠️ Installation & Usage

### Option 1: Docker (Recommended for Render/Deployment)

This application is containerized and ready for deployment on platforms like Render.com.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/suzy311278/CyberThreatFramework.git
    cd CyberThreatFramework
    ```

2.  **Build and Run:**
    ```bash
    docker build -t threat-framework .
    docker run -p 5002:5002 threat-framework
    ```

3.  Access the dashboard at `http://localhost:5002`.

### Option 2: Local Python Environment

1.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

2.  **Run the Dashboard:**
    ```bash
    python src/CyberThreatFramework/dashboard.py
    ```

## 📂 Project Structure

```
CyberThreatFramework/
├── api/                    # Vercel entry point
├── src/
│   └── CyberThreatFramework/
│       ├── dashboard.py    # Main Flask Web Server
│       ├── main.py         # Attack Engine Entry Point
│       ├── data.py         # MITRE ATT&CK Data
│       ├── modules/        # Attack Scripts (Ransomware, PLC, etc.)
│       ├── templates/      # HTML Dashboard
│       └── utils/          # Visualizer, Logger, etc.
├── Dockerfile              # Container Configuration
├── requirements.txt        # Python Dependencies
└── vercel.json             # Vercel Configuration
```

## ⚠️ Disclaimer

This tool is for **EDUCATIONAL PURPOSES ONLY**. It is designed to simulate attacks in a safe, controlled environment (e.g., localhost, dummy directories). Do not use this tool against targets you do not have explicit permission to test. The developer is not responsible for any misuse of this software.

## 📄 License

MIT License