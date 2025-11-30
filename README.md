Network Configuration Generator 🛠️

A Python-based infrastructure-as-code tool that automates the generation of standardized network device configurations (Cisco IOS / Juniper Junos) using YAML data models and Jinja2 templating.

Why this exists: Manual configuration of network devices is prone to human error ("fat-fingering" IP addresses) and inconsistency. This tool solves Configuration Drift by decoupling the data (IPs, VLANs, Hostnames) from the logic (Command Syntax).

🚀 Key Features

Separation of Concerns: Keeps variable data in routers.yaml and logic in templates/.

Multi-Vendor Ready: Designed to support multiple template styles (currently focused on Cisco IOS).

Idempotency: Generates consistent output every time, reducing deployment risks.

Scalable: Can generate 1 config or 100 configs in seconds.

📂 Project Structure

├── templates/
│   └── cisco_ios.j2       # Jinja2 template for Cisco syntax
├── routers.yaml           # Source of Truth (Inventory & Variables)
├── generate.py            # Main Python logic script
├── requirements.txt       # Dependencies
└── README.md              # Documentation


⚙️ How to Run

1. Clone the repository

git clone [https://github.com/careed23/The-Network-Config-Generator.git](https://github.com/careed23/The-Network-Config-Generator.git)
cd The-Network-Config-Generator


2. Install Dependencies

pip install -r requirements.txt


3. Define your Devices

Edit routers.yaml to add your device details:

- hostname: "Core-Router-01"
  interface: "GigabitEthernet0/1"
  ip_address: "192.168.10.1"
  subnet_mask: "255.255.255.0"


4. Generate Configs

Run the script:

python3 generate.py


Output configurations will print to the console or save to an /output folder (if configured).

🔧 Technology Stack

Python 3.x

Jinja2 (Templating Engine)

YAML (Data Serialization)

🔮 Future Improvements

[ ] Add support for Juniper Junos templates.

[ ] Integrate with Netmiko to push configs directly to devices.

[ ] Add unit tests to validate IP address formats.

Created by Colten Reed
