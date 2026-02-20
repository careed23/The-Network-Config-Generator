"""
Unit tests for generate.py
"""

import os
import sys
import pytest
import tempfile
import yaml
from pydantic import ValidationError

# Make sure the project root is on the path so we can import generate
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import generate  # noqa: E402


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")


@pytest.fixture
def jinja_env():
    return generate.build_jinja_env(TEMPLATES_DIR)


@pytest.fixture
def cisco_device():
    return generate.DeviceModel(
        hostname="test-router-01",
        device_type="cisco_ios",
        interface="GigabitEthernet0/1",
        ip="10.0.0.1",
        mask="255.255.255.0",
        description="Test Interface",
        vlans=[
            generate.VlanModel(id=10, name="DATA"),
            generate.VlanModel(id=20, name="VOICE"),
        ],
    )


@pytest.fixture
def juniper_device():
    return generate.DeviceModel(
        hostname="test-juniper-01",
        device_type="juniper_junos",
        interface="ge-0/0/0",
        ip="192.168.1.1",
        mask="255.255.255.252",
        description="WAN Link",
        vlans=[generate.VlanModel(id=100, name="CORP")],
    )


# ---------------------------------------------------------------------------
# Validation tests
# ---------------------------------------------------------------------------

class TestDeviceModelValidation:

    def test_valid_cisco_device(self, cisco_device):
        assert cisco_device.hostname == "test-router-01"
        assert cisco_device.device_type == "cisco_ios"

    def test_valid_juniper_device(self, juniper_device):
        assert juniper_device.device_type == "juniper_junos"

    def test_invalid_ip_raises(self):
        with pytest.raises(ValidationError):
            generate.DeviceModel(
                hostname="bad-device",
                interface="Gi0/1",
                ip="999.999.999.999",
                mask="255.255.255.0",
            )

    def test_invalid_mask_raises(self):
        with pytest.raises(ValidationError):
            generate.DeviceModel(
                hostname="bad-device",
                interface="Gi0/1",
                ip="10.0.0.1",
                mask="not-a-mask",
            )

    def test_invalid_device_type_raises(self):
        with pytest.raises(ValidationError):
            generate.DeviceModel(
                hostname="bad-device",
                interface="Gi0/1",
                ip="10.0.0.1",
                mask="255.255.255.0",
                device_type="vyos",
            )

    def test_vlan_id_out_of_range_raises(self):
        with pytest.raises(ValidationError):
            generate.VlanModel(id=5000, name="INVALID")

    def test_vlan_id_zero_raises(self):
        with pytest.raises(ValidationError):
            generate.VlanModel(id=0, name="INVALID")

    def test_default_device_type_is_cisco(self):
        device = generate.DeviceModel(
            hostname="x",
            interface="Gi0/1",
            ip="1.1.1.1",
            mask="255.255.255.0",
        )
        assert device.device_type == "cisco_ios"


# ---------------------------------------------------------------------------
# Template rendering tests
# ---------------------------------------------------------------------------

class TestCiscoRendering:

    def test_hostname_in_output(self, jinja_env, cisco_device):
        config = generate.render_config(jinja_env, cisco_device)
        assert "hostname test-router-01" in config

    def test_interface_in_output(self, jinja_env, cisco_device):
        config = generate.render_config(jinja_env, cisco_device)
        assert "interface GigabitEthernet0/1" in config

    def test_ip_address_in_output(self, jinja_env, cisco_device):
        config = generate.render_config(jinja_env, cisco_device)
        assert "ip address 10.0.0.1 255.255.255.0" in config

    def test_no_shutdown_in_output(self, jinja_env, cisco_device):
        config = generate.render_config(jinja_env, cisco_device)
        assert "no shutdown" in config

    def test_vlans_in_output(self, jinja_env, cisco_device):
        config = generate.render_config(jinja_env, cisco_device)
        assert "vlan 10" in config
        assert "name DATA" in config
        assert "vlan 20" in config
        assert "name VOICE" in config

    def test_end_statement_present(self, jinja_env, cisco_device):
        config = generate.render_config(jinja_env, cisco_device)
        assert config.strip().endswith("end")


class TestJuniperRendering:

    def test_hostname_in_output(self, jinja_env, juniper_device):
        config = generate.render_config(jinja_env, juniper_device)
        assert "host-name test-juniper-01" in config

    def test_interface_in_output(self, jinja_env, juniper_device):
        config = generate.render_config(jinja_env, juniper_device)
        assert "ge-0/0/0" in config

    def test_prefix_length_conversion(self, jinja_env, juniper_device):
        config = generate.render_config(jinja_env, juniper_device)
        # /30 for 255.255.255.252
        assert "192.168.1.1/30" in config

    def test_vlan_in_output(self, jinja_env, juniper_device):
        config = generate.render_config(jinja_env, juniper_device)
        assert "vlan-id 100" in config
        assert "corp" in config  # lowercase vlan name


# ---------------------------------------------------------------------------
# ipv4_prefix_len filter
# ---------------------------------------------------------------------------

class TestIpv4PrefixLen:

    def test_slash_24(self):
        assert generate._ipv4_prefix_len("255.255.255.0") == 24

    def test_slash_30(self):
        assert generate._ipv4_prefix_len("255.255.255.252") == 30

    def test_slash_16(self):
        assert generate._ipv4_prefix_len("255.255.0.0") == 16

    def test_slash_32(self):
        assert generate._ipv4_prefix_len("255.255.255.255") == 32


# ---------------------------------------------------------------------------
# load_inventory tests
# ---------------------------------------------------------------------------

class TestLoadInventory:

    def test_loads_valid_yaml(self):
        data = [{"hostname": "r1", "interface": "Gi0/1", "ip": "1.1.1.1", "mask": "255.255.255.0"}]
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as fh:
            yaml.dump(data, fh)
            path = fh.name
        try:
            result = generate.load_inventory(path)
            assert result[0]["hostname"] == "r1"
        finally:
            os.unlink(path)

    def test_missing_file_exits(self):
        with pytest.raises(SystemExit):
            generate.load_inventory("/tmp/does_not_exist_xyz.yaml")

    def test_non_list_yaml_exits(self):
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yaml", delete=False) as fh:
            yaml.dump({"key": "value"}, fh)
            path = fh.name
        try:
            with pytest.raises(SystemExit):
                generate.load_inventory(path)
        finally:
            os.unlink(path)


# ---------------------------------------------------------------------------
# write_config / output dir tests
# ---------------------------------------------------------------------------

class TestWriteConfig:

    def test_writes_file(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = generate.write_config(tmpdir, "my-router", "! config content\n")
            assert os.path.isfile(path)
            with open(path) as fh:
                assert fh.read() == "! config content\n"

    def test_filename_matches_hostname(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = generate.write_config(tmpdir, "edge-01", "x")
            assert os.path.basename(path) == "edge-01.cfg"


# ---------------------------------------------------------------------------
# CLI / main() integration tests
# ---------------------------------------------------------------------------

class TestMain:

    def test_dry_run_returns_zero(self, capsys):
        rc = generate.main(["--inventory", os.path.join(SCRIPT_DIR, "routers.yaml"), "--dry-run"])
        assert rc == 0

    def test_dry_run_outputs_cisco_config(self, capsys):
        generate.main(["--inventory", os.path.join(SCRIPT_DIR, "routers.yaml"), "--dry-run"])
        captured = capsys.readouterr()
        assert "hostname nashville-core-01" in captured.out

    def test_dry_run_outputs_juniper_config(self, capsys):
        generate.main(["--inventory", os.path.join(SCRIPT_DIR, "routers.yaml"), "--dry-run"])
        captured = capsys.readouterr()
        assert "host-name atlanta-core-01" in captured.out

    def test_device_filter(self, capsys):
        generate.main([
            "--inventory", os.path.join(SCRIPT_DIR, "routers.yaml"),
            "--dry-run",
            "--device", "memphis-edge-01",
        ])
        captured = capsys.readouterr()
        assert "memphis-edge-01" in captured.out
        assert "nashville" not in captured.out

    def test_unknown_device_returns_nonzero(self):
        rc = generate.main([
            "--inventory", os.path.join(SCRIPT_DIR, "routers.yaml"),
            "--device", "nonexistent-device",
        ])
        assert rc != 0

    def test_file_output_creates_cfg_files(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            generate.main([
                "--inventory", os.path.join(SCRIPT_DIR, "routers.yaml"),
                "--output-dir", tmpdir,
            ])
            files = os.listdir(tmpdir)
            assert "nashville-core-01.cfg" in files
            assert "memphis-edge-01.cfg" in files
            assert "atlanta-core-01.cfg" in files
