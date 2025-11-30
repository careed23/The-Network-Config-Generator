🌐 Network Configuration Generator

An intelligent infrastructure-as-code tool that automates the generation of standardized network device configurations.

Quick Start • Features • Documentation

📊 Overview

The Network Configuration Generator is a next-generation automation tool designed to eliminate "fat-finger" errors in network deployments. By separating variable data (IPs, VLANs) from configuration logic (Command Syntax), it ensures 100% standardized, idempotent deployments across Cisco IOS and Juniper environments. Built for network administrators moving from manual CLI typing to modern Infrastructure-as-Code (IaC).

🎯 Problem It Solves

Manual Configuration is Risky: One typo in an IP address can take down a subnet.

Configuration Drift: Over time, devices deviate from the standard "Golden Image."

Slow Deployment: Manually typing commands for 50 switches takes hours.

Lack of Standardization: Different engineers use different syntax for the same task.

✨ Solution

This engine uses Jinja2 templating and YAML data models to:

Enforce Consistency: Every config is generated from the same approved template.

Scale Instantly: Generate 1 or 1,000 configs in milliseconds.

Validate Data: Ensure all IP addresses and Subnets are valid before generation.

Multi-Vendor Support: Switch between Cisco and Juniper templates seamlessly.

🚀 Features

Core Capabilities

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
