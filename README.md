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

The Network Configuration Generator is a next-generation automation tool designed to eliminate "fat-finger" errors in network deployments. By separating variable data (IPs, VLANs) from configuration logic (Command Syntax), it ensures 100% standardized, idempotent deployments across Cisco IOS and Juniper JunOS environments. Built for network administrators moving from manual CLI typing to modern Infrastructure-as-Code (IaC).

<h3>🎯 Problem It Solves</h3>

**Manual Configuration is Risky:** One typo in an IP address can take down a subnet.

**Configuration Drift:** Over time, devices deviate from the standard "Golden Image."

**Slow Deployment:** Manually typing commands for 50 switches takes hours.

**Lack of Standardization:** Different engineers use different syntax for the same task.

<h3>✨ Solution</h3>

This engine uses Jinja2 templating and YAML data models to:

- **Enforce Consistency:** Every config is generated from the same approved template.
- **Scale Instantly:** Generate 1 or 1,000 configs in milliseconds.
- **Validate Data:** Ensure all IP addresses, subnet masks, and VLAN IDs are valid before generation.
- **Multi-Vendor Support:** Switch between Cisco IOS and Juniper JunOS templates seamlessly.

<hr />

<h2>🚀 Features</h2>

| Feature | Description |
|---|---|
| 🛠️ **Template Engine** | Jinja2 decouples logic from data — supports loops, conditionals, and custom filters (e.g. `ipv4_prefix_len`). |
| 📄 **YAML Inventory** | Device variables (hostname, IP, interface, VLANs, `device_type`) stored in human-readable `routers.yaml`. |
| ✅ **Input Validation** | Pydantic models enforce valid IP addresses, subnet masks, VLAN IDs (1–4094), and supported device types before any rendering occurs. |
| 🔒 **Idempotency** | Generates the exact same configuration every time — zero drift during deployments. |
| 🌐 **Multi-Vendor** | Cisco IOS (`cisco_ios`) and Juniper JunOS (`juniper_junos`) templates included out of the box. |
| 🖥️ **CLI Interface** | `argparse`-powered CLI with `--inventory`, `--output-dir`, `--dry-run`, and `--device` flags. |
| 📋 **Dry-Run Mode** | Preview all rendered configurations in stdout without touching the filesystem. |
| 📦 **Output Directory** | Configs are saved to a dedicated `output/` folder, organized by hostname. |
| 📝 **Structured Logging** | Timestamped, leveled log output for every step of the generation pipeline. |

<hr />

<h2>📂 Project Structure</h2>

```
├── templates/
│   ├── cisco_base.j2       # Jinja2 template for Cisco IOS syntax
│   └── juniper_base.j2     # Jinja2 template for Juniper JunOS syntax
├── tests/
│   └── test_generate.py    # pytest unit tests (33 tests)
├── routers.yaml            # Source of Truth — device inventory & variables
├── generate.py             # Main engine: CLI, validation, rendering, output
├── requirements.txt        # Python dependencies
└── README.md               # Documentation
```

<hr />

<h2>⚙️ Quick Start</h2>

<h3>1. Clone the repository</h3>

```bash
git clone https://github.com/careed23/The-Network-Config-Generator.git
cd The-Network-Config-Generator
```

<h3>2. Install Dependencies</h3>

```bash
pip install -r requirements.txt
```

<h3>3. Define your Devices</h3>

Edit `routers.yaml` to add your devices. The `device_type` field selects the vendor template:

```yaml
- hostname: core-router-01
  device_type: cisco_ios          # or: juniper_junos
  interface: GigabitEthernet0/1
  ip: 192.168.10.1
  mask: 255.255.255.0
  description: Uplink to Core
  vlans:
    - id: 10
      name: DATA
    - id: 20
      name: VOICE
```

<h3>4. Generate Configs</h3>

**Generate all devices** (saved to `output/` directory):
```bash
python generate.py
```

**Preview without saving** (dry-run mode):
```bash
python generate.py --dry-run
```

**Generate a single device:**
```bash
python generate.py --device nashville-core-01
```

**Custom inventory and output directory:**
```bash
python generate.py --inventory my_devices.yaml --output-dir /etc/network/configs
```

<h3>CLI Options</h3>

| Flag | Default | Description |
|---|---|---|
| `--inventory` | `routers.yaml` | Path to the YAML device inventory |
| `--output-dir` | `output` | Directory to save generated `.cfg` files |
| `--dry-run` | `False` | Print configs to stdout, do not save files |
| `--device` | *(all)* | Only generate config for one specific hostname |

<hr />

<h2>🔍 Validation Rules</h2>

The tool validates every device record before any template is rendered:

- `ip` must be a valid IPv4 address
- `mask` must be a valid IPv4 subnet mask
- `device_type` must be `cisco_ios` or `juniper_junos`
- VLAN `id` must be in the range **1–4094**
- Any validation failure causes a clear error message and a non-zero exit code

<hr />

<h2>🧪 Running Tests</h2>

```bash
pip install pytest
python -m pytest tests/ -v
```

33 tests covering: validation, Cisco rendering, Juniper rendering, CLI flags, file output, and edge cases.

<hr />

<h2>🔧 Technology Stack</h2>

- **Python 3.10+**
- **Jinja2** — Templating engine
- **PyYAML** — YAML parsing
- **Pydantic v2** — Data validation and schema enforcement

<hr />

<p align="center">
<em>Created by <a href="https://linkedin.com/in/colten-reed-8395b6389">Colten Reed</a></em>
</p>

