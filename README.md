<h1 align="center">🌐 Network Configuration Generator</h1>

<div align="center">
<strong>An intelligent infrastructure-as-code tool that automates the generation of standardized network device configurations.</strong>
</div>

<br />

<div align="center">
<a href="#-quick-start">Quick Start</a> •
<a href="#-features">Features</a> •
<a href="#-documentation">Documentation</a>
</div>

<hr />

<h2>📊 Overview</h2>

The Network Configuration Generator is a next-generation automation tool designed to eliminate "fat-finger" errors in network deployments. By separating variable data (IPs, VLANs) from configuration logic (Command Syntax), it ensures 100% standardized, idempotent deployments across Cisco IOS and Juniper environments. Built for network administrators moving from manual CLI typing to modern Infrastructure-as-Code (IaC).

<h3>🎯 Problem It Solves</h3>

Manual Configuration is Risky: One typo in an IP address can take down a subnet.

Configuration Drift: Over time, devices deviate from the standard "Golden Image."

Slow Deployment: Manually typing commands for 50 switches takes hours.

Lack of Standardization: Different engineers use different syntax for the same task.

<h3>✨ Solution</h3>

This engine uses Jinja2 templating and YAML data models to:

Enforce Consistency: Every config is generated from the same approved template.

Scale Instantly: Generate 1 or 1,000 configs in milliseconds.

Validate Data: Ensure all IP addresses and Subnets are valid before generation.

Multi-Vendor Support: Switch between Cisco and Juniper templates seamlessly.

<hr />

<h2>🚀 Features</h2>

<h3>Core Capabilities</h3>

Feature

Description

🛠️ Template Engine

Uses Jinja2 to decouple logic from data, allowing for complex logic (loops, conditionals) within network configs.

📄 YAML Inventory

All device variables (Hostnames, IPs, Interfaces) are stored in a human-readable routers.yaml source of truth.

🔒 Idempotency

Generates the exact same configuration every time, ensuring zero drift during deployments.

⚡ High Performance

Capable of generating hundreds of device configurations in seconds using Python's optimized I/O.

<hr />

<h2>📂 Project Structure</h2>

├── templates/
│   └── cisco_ios.j2       # Jinja2 template for Cisco syntax
├── routers.yaml           # Source of Truth (Inventory & Variables)
├── generate.py            # Main Python logic script
├── requirements.txt       # Dependencies
└── README.md              # Documentation


<hr />

<h2>⚙️ How to Run</h2>

<h3>1. Clone the repository</h3>

git clone [https://github.com/careed23/The-Network-Config-Generator.git](https://github.com/careed23/The-Network-Config-Generator.git)
cd The-Network-Config-Generator


<h3>2. Install Dependencies</h3>

pip install -r requirements.txt


<h3>3. Define your Devices</h3>

Edit routers.yaml to add your device details:

- hostname: "Core-Router-01"
  interface: "GigabitEthernet0/1"
  ip_address: "192.168.10.1"
  subnet_mask: "255.255.255.0"


<h3>4. Generate Configs</h3>

Run the script:

python3 generate.py


Output configurations will print to the console or save to an /output folder (if configured).

<hr />

<h2>🔧 Technology Stack</h2>

Python 3.x

Jinja2 (Templating Engine)

YAML (Data Serialization)

<hr />

<h2>🔮 Future Improvements</h2>

[ ] Add support for Juniper Junos templates.

[ ] Integrate with Netmiko to push configs directly to devices.

[ ] Add unit tests to validate IP address formats.

<hr />

<p align="center">
<em>Created by <a href="https://www.google.com/search?q=https://linkedin.com/in/colten-reed-8395b6389">Colten Reed</a></em>
</p
