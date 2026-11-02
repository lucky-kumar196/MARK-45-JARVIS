"""
core/platform_support.py — Platform capability detection and limit reporting.
"""
import os
import platform
import sys

def detect() -> dict:
    sys_name = platform.system()
    release = platform.release()
    is_wayland = bool(os.environ.get("WAYLAND_DISPLAY") or "wayland" in os.environ.get("XDG_SESSION_TYPE", "").lower())
    
    return {
        "system": sys_name,
        "release": release,
        "is_wayland": is_wayland,
        "is_mac": sys_name == "Darwin",
        "is_linux": sys_name == "Linux",
        "is_windows": sys_name == "Windows",
    }

def describe_for_model(caps: dict) -> list[str]:
    notes = []
    if caps.get("is_wayland"):
        notes.append("- On Linux Wayland, direct keyboard simulation or global window control may be limited by compositor security.")
    elif caps.get("is_mac"):
        notes.append("- On macOS, system automation requires Accessibility and Screen Recording permissions.")
    return notes

def describe_for_user(caps: dict) -> list[str]:
    lines = []
    sys_name = caps.get("system", "Unknown")
    rel = caps.get("release", "")
    lines.append(f"SYS: Running on {sys_name} {rel}.")
    if caps.get("is_wayland"):
        lines.append("SYS: Wayland detected. If screen capture or shortcuts fail, consider an X11 session.")
    return lines
