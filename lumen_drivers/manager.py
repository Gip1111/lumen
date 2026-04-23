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

driver_manager = DriverManager()
