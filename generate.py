"""
Network Configuration Generator
================================
Generates standardized network device configurations from a YAML inventory
using Jinja2 templates.  Supports Cisco IOS and Juniper JunOS.

Usage:
    python generate.py [OPTIONS]

Options:
    --inventory   Path to the YAML device inventory  (default: routers.yaml)
    --output-dir  Directory to write generated configs (default: output)
    --dry-run     Render configs to stdout without saving files
    --device      Only generate config for a specific hostname
"""

import argparse
import ipaddress
import logging
import os
import sys
from typing import Any

import yaml
from jinja2 import Environment, FileSystemLoader, TemplateNotFound
from pydantic import BaseModel, field_validator, ValidationError

# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s  %(levelname)-8s  %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.INFO,
)
log = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Template map:  device_type  ->  Jinja2 template filename
# ---------------------------------------------------------------------------
TEMPLATE_MAP: dict[str, str] = {
    "cisco_ios": "cisco_base.j2",
    "juniper_junos": "juniper_base.j2",
}
DEFAULT_DEVICE_TYPE = "cisco_ios"

# ---------------------------------------------------------------------------
# Pydantic models – validate every device record before rendering
# ---------------------------------------------------------------------------

class VlanModel(BaseModel):
    id: int
    name: str

    @field_validator("id")
    @classmethod
    def vlan_id_range(cls, v: int) -> int:
        if not 1 <= v <= 4094:
            raise ValueError(f"VLAN id {v} is outside the valid range 1-4094")
        return v


class DeviceModel(BaseModel):
    hostname: str
    interface: str
    ip: str
    mask: str
    device_type: str = DEFAULT_DEVICE_TYPE
    description: str = "Uplink"
    vlans: list[VlanModel] = []

    @field_validator("ip")
    @classmethod
    def validate_ip(cls, v: str) -> str:
        try:
            ipaddress.ip_address(v)
        except ValueError:
            raise ValueError(f"'{v}' is not a valid IP address")
        return v

    @field_validator("mask")
    @classmethod
    def validate_mask(cls, v: str) -> str:
        try:
            ipaddress.ip_address(v)
        except ValueError:
            raise ValueError(f"'{v}' is not a valid subnet mask")
        return v

    @field_validator("device_type")
    @classmethod
    def validate_device_type(cls, v: str) -> str:
        if v not in TEMPLATE_MAP:
            raise ValueError(
                f"Unknown device_type '{v}'. Supported: {list(TEMPLATE_MAP)}"
            )
        return v


# ---------------------------------------------------------------------------
# Core functions
# ---------------------------------------------------------------------------

def load_inventory(path: str) -> list[dict[str, Any]]:
    """Load and parse the YAML device inventory."""
    if not os.path.isfile(path):
        log.error("Inventory file not found: %s", path)
        sys.exit(1)
    with open(path) as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, list):
        log.error("Inventory must be a YAML list of device records.")
        sys.exit(1)
    return data


def validate_devices(raw_devices: list[dict[str, Any]]) -> list[DeviceModel]:
    """Validate each device record; exit on first error."""
    validated: list[DeviceModel] = []
    for i, record in enumerate(raw_devices):
        try:
            validated.append(DeviceModel(**record))
        except ValidationError as exc:
            log.error("Validation failed for device #%d (%s):\n%s",
                      i + 1, record.get("hostname", "<unknown>"), exc)
            sys.exit(1)
    return validated


def _ipv4_prefix_len(mask: str) -> int:
    """Jinja2 filter: convert dotted-decimal mask to prefix length (e.g. '255.255.255.0' -> 24)."""
    return ipaddress.IPv4Network(f"0.0.0.0/{mask}").prefixlen


def build_jinja_env(templates_dir: str) -> Environment:
    """Return a configured Jinja2 environment with custom filters."""
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        trim_blocks=True,
        lstrip_blocks=True,
    )
    env.filters["ipv4_prefix_len"] = _ipv4_prefix_len
    return env


def render_config(env: Environment, device: DeviceModel) -> str:
    """Render the Jinja2 template for a single device."""
    template_name = TEMPLATE_MAP[device.device_type]
    try:
        template = env.get_template(template_name)
    except TemplateNotFound:
        log.error("Template '%s' not found in templates directory.", template_name)
        sys.exit(1)
    return template.render(device=device)


def ensure_output_dir(path: str) -> None:
    """Create the output directory if it does not exist."""
    os.makedirs(path, exist_ok=True)


def write_config(output_dir: str, hostname: str, config: str) -> str:
    """Write a rendered config to disk; returns the file path."""
    filename = os.path.join(output_dir, f"{hostname}.cfg")
    with open(filename, "w") as fh:
        fh.write(config)
    return filename


# ---------------------------------------------------------------------------
# CLI entry point
# ---------------------------------------------------------------------------

def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate network device configurations from a YAML inventory.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument(
        "--inventory", default="routers.yaml",
        help="Path to the YAML device inventory file.",
    )
    parser.add_argument(
        "--output-dir", default="output",
        help="Directory where generated .cfg files will be saved.",
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Print generated configs to stdout without writing files.",
    )
    parser.add_argument(
        "--device",
        help="Only generate config for the device with this hostname.",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    args = parse_args(argv)

    # Resolve template directory relative to this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    templates_dir = os.path.join(script_dir, "templates")

    log.info("Loading inventory from: %s", args.inventory)
    raw_devices = load_inventory(args.inventory)

    log.info("Validating %d device(s)...", len(raw_devices))
    devices = validate_devices(raw_devices)

    if args.device:
        devices = [d for d in devices if d.hostname == args.device]
        if not devices:
            log.error("No device found with hostname '%s'.", args.device)
            return 1

    jinja_env = build_jinja_env(templates_dir)

    if not args.dry_run:
        ensure_output_dir(args.output_dir)

    generated = 0
    for device in devices:
        log.info("[%s] Rendering config (type=%s)...", device.hostname, device.device_type)
        config = render_config(jinja_env, device)

        if args.dry_run:
            separator = "=" * 60
            print(f"\n{separator}")
            print(f"  Device: {device.hostname}  |  Type: {device.device_type}")
            print(separator)
            print(config)
        else:
            path = write_config(args.output_dir, device.hostname, config)
            log.info("[%s] Saved -> %s", device.hostname, path)

        generated += 1

    if args.dry_run:
        log.info("Dry-run complete. %d config(s) rendered.", generated)
    else:
        log.info("Done. %d config(s) saved to '%s'.", generated, args.output_dir)

    return 0


if __name__ == "__main__":
    sys.exit(main())

