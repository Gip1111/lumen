import subprocess
import re
from typing import List, Dict

class DriverManager:
    """Manages hardware detection and driver recommendations."""
    
    def scan_pci(self) -> List[Dict[str, str]]:
        """Scans PCI bus for hardware."""
        try:
            result = subprocess.run(['lspci', '-nn'], capture_output=True, text=True)
            devices = []
            for line in result.stdout.splitlines():
                # Format: 00:02.0 VGA compatible controller [0300]: Intel Corporation ... [8086:9b41]
                match = re.search(r'^(.*?) (.*?): (.*?) \[(.*?)\]', line)
                if match:
                    devices.append({
                        "slot": match.group(1),
                        "type": match.group(2),
                        "name": match.group(3),
                        "ids": match.group(4)
                    })
            return devices
        except FileNotFoundError:
            return [{"error": "lspci not found"}]

    def scan_usb(self) -> List[Dict[str, str]]:
        """Scans USB bus for hardware."""
        try:
            result = subprocess.run(['lsusb'], capture_output=True, text=True)
            devices = []
            for line in result.stdout.splitlines():
                # Format: Bus 002 Device 001: ID 1d6b:0003 Linux Foundation 3.0 root hub
                match = re.search(r'ID (.*?):(.*?) (.*)', line)
                if match:
                    devices.append({
                        "vendor_id": match.group(1),
                        "product_id": match.group(2),
                        "name": match.group(3)
                    })
            return devices
        except FileNotFoundError:
            return [{"error": "lsusb not found"}]

    def get_recommendations(self) -> List[Dict[str, str]]:
        """Returns recommended drivers based on scan."""
        devices = self.scan_pci()
        recommendations = []
        
        for dev in devices:
            if "VGA" in dev.get("type", ""):
                if "NVIDIA" in dev.get("name", ""):
                    recommendations.append({"device": dev["name"], "driver": "nvidia", "status": "proprietary"})
                elif "AMD" in dev.get("name", "") or "ATI" in dev.get("name", ""):
                    recommendations.append({"device": dev["name"], "driver": "mesa / amdgpu", "status": "open-source"})
                elif "Intel" in dev.get("name", ""):
                    recommendations.append({"device": dev["name"], "driver": "mesa / i915", "status": "open-source"})
        
        return recommendations

    def install_driver(self, driver_name: str) -> Dict[str, str]:
        """Installs a driver using pkexec pacman."""
        # Map driver names to actual packages
        package_map = {
            "nvidia": ["nvidia", "nvidia-utils", "nvidia-settings"],
            "mesa / amdgpu": ["mesa", "xf86-video-amdgpu"],
            "mesa / i915": ["mesa", "xf86-video-intel"]
        }
        
        packages = package_map.get(driver_name)
        if not packages:
            return {"error": f"Unknown driver: {driver_name}"}
        
        try:
            # pkexec will trigger a polkit authentication dialog
            cmd = ['pkexec', 'pacman', '-S', '--noconfirm'] + packages
            subprocess.run(cmd, check=True)
            return {"success": True, "message": f"Installed {driver_name}"}
        except subprocess.CalledProcessError as e:
            return {"error": f"Installation failed: {e}"}
        except FileNotFoundError:
            return {"error": "pkexec or pacman not found"}

driver_manager = DriverManager()
