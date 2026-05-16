import platform
import re
import subprocess
from dataclasses import dataclass
from typing import Optional


@dataclass
class WiFiInfo:
    ssid: str = "Unknown"
    state: str = "Unknown"
    signal_percent: Optional[int] = None
    rssi_dbm: Optional[float] = None
    radio_type: str = "Unknown"
    channel: Optional[int] = None
    frequency_ghz: float = 2.4
    message: str = ""


def quality_percent_to_dbm(signal_percent: int) -> float:
    signal_percent = max(0, min(100, int(signal_percent)))
    return round((signal_percent / 2.0) - 100.0, 2)


def classify_signal(signal_dbm: float) -> str:
    if signal_dbm >= -50:
        return "Excellent"
    if signal_dbm >= -60:
        return "Good"
    if signal_dbm >= -70:
        return "Fair"
    if signal_dbm >= -80:
        return "Poor"
    return "Very Poor"


def optimization_tips(signal_dbm: float) -> list[str]:
    if signal_dbm >= -60:
        return [
            "Signal is strong. Current router placement is suitable.",
            "Keep router away from metal objects for stable performance.",
        ]

    if signal_dbm >= -70:
        return [
            "Signal is usable, but can be improved.",
            "Move closer to the router or reduce physical obstacles.",
            "Place router at a higher and more central location.",
        ]

    if signal_dbm >= -80:
        return [
            "Signal is weak. Internet speed may become unstable.",
            "Reduce walls between device and router.",
            "Avoid placing router near microwave ovens or thick concrete walls.",
            "Try changing WiFi channel from router settings.",
        ]

    return [
        "Signal is very weak. Connection drops may happen.",
        "Move the device much closer to the router.",
        "Use a WiFi extender or mesh router.",
        "Place router in an open central area.",
        "Use 2.4 GHz band for longer range.",
    ]


def _parse_windows_netsh_output(output: str) -> WiFiInfo:
    def find_value(label: str) -> str:
        pattern = rf"^\s*{re.escape(label)}\s*:\s*(.+)$"
        match = re.search(pattern, output, flags=re.MULTILINE | re.IGNORECASE)
        return match.group(1).strip() if match else ""

    state = find_value("State") or "Unknown"

    ssid = "Unknown"
    for line in output.splitlines():
        stripped = line.strip()

        if stripped.lower().startswith("ssid") and not stripped.lower().startswith("bssid"):
            parts = stripped.split(":", 1)

            if len(parts) == 2 and parts[1].strip():
                ssid = parts[1].strip()
                break

    signal_text = find_value("Signal")
    signal_percent = None
    rssi_dbm = None

    if signal_text:
        match = re.search(r"(\d+)", signal_text)

        if match:
            signal_percent = int(match.group(1))
            rssi_dbm = quality_percent_to_dbm(signal_percent)

    radio_type = find_value("Radio type") or "Unknown"

    channel_text = find_value("Channel")
    channel = None

    if channel_text:
        match = re.search(r"(\d+)", channel_text)

        if match:
            channel = int(match.group(1))

    frequency_ghz = 2.4

    if channel is not None and channel > 14:
        frequency_ghz = 5.0
    elif "802.11ac" in radio_type.lower() or "802.11a" in radio_type.lower():
        frequency_ghz = 5.0

    return WiFiInfo(
        ssid=ssid,
        state=state,
        signal_percent=signal_percent,
        rssi_dbm=rssi_dbm,
        radio_type=radio_type,
        channel=channel,
        frequency_ghz=frequency_ghz,
        message="",
    )


def get_wifi_info_windows() -> WiFiInfo:
    try:
        completed = subprocess.run(
            ["netsh", "wlan", "show", "interfaces"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=8,
        )

        output = completed.stdout

        if completed.returncode != 0 or not output.strip():
            return WiFiInfo(message="Unable to read WiFi information using netsh.")

        return _parse_windows_netsh_output(output)

    except Exception as exc:
        return WiFiInfo(message=f"Windows WiFi reading failed: {exc}")


def get_wifi_info_linux() -> WiFiInfo:
    try:
        completed = subprocess.run(
            ["iwconfig"],
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="ignore",
            timeout=8,
        )

        output = completed.stdout + completed.stderr

        ssid_match = re.search(r'ESSID:"([^"]+)"', output)
        ssid = ssid_match.group(1) if ssid_match else "Unknown"

        signal_match = re.search(r"Signal level=(-?\d+)\s*dBm", output)
        rssi_dbm = float(signal_match.group(1)) if signal_match else None

        signal_percent = None

        if rssi_dbm is not None:
            signal_percent = int(max(0, min(100, 2 * (rssi_dbm + 100))))

        freq_match = re.search(r"Frequency:(\d+\.\d+)", output)
        frequency_ghz = float(freq_match.group(1)) if freq_match else 2.4

        return WiFiInfo(
            ssid=ssid,
            state="Connected" if ssid != "Unknown" else "Unknown",
            signal_percent=signal_percent,
            rssi_dbm=rssi_dbm,
            frequency_ghz=5.0 if frequency_ghz >= 5 else 2.4,
            message="",
        )

    except Exception as exc:
        return WiFiInfo(message=f"Linux WiFi reading failed: {exc}")


def get_wifi_info_pywifi() -> WiFiInfo:
    try:
        import pywifi

        wifi = pywifi.PyWiFi()
        interfaces = wifi.interfaces()

        if not interfaces:
            return WiFiInfo(message="No WiFi adapter found by pywifi.")

        iface = interfaces[0]
        iface.scan()
        results = iface.scan_results()

        if not results:
            return WiFiInfo(message="No scan results found by pywifi.")

        strongest = max(results, key=lambda item: item.signal)

        return WiFiInfo(
            ssid=strongest.ssid or "Unknown",
            state="Visible",
            signal_percent=None,
            rssi_dbm=float(strongest.signal),
            frequency_ghz=2.4,
            message="",
        )

    except Exception as exc:
        return WiFiInfo(message=f"pywifi reading failed: {exc}")


def get_wifi_info() -> WiFiInfo:
    system_name = platform.system().lower()

    if "windows" in system_name:
        info = get_wifi_info_windows()

        if info.rssi_dbm is not None:
            return info

    if "linux" in system_name:
        info = get_wifi_info_linux()

        if info.rssi_dbm is not None:
            return info

    return get_wifi_info_pywifi()


def estimate_distance_from_rssi(rssi_dbm: float) -> float:
    if rssi_dbm >= -45:
        return 2.0
    if rssi_dbm >= -55:
        return 5.0
    if rssi_dbm >= -65:
        return 10.0
    if rssi_dbm >= -75:
        return 18.0
    if rssi_dbm >= -85:
        return 28.0
    return 40.0