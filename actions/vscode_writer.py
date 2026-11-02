"""
actions/vscode_writer.py — Direct Code Generation & Writing into VS Code.

Enables JARVIS to generate code using Gemini and either:
1. Save it to a file and automatically open/display it in VS Code (mode='file')
2. Focus the active VS Code window, open a new editor tab, and paste the code live (mode='active_window')
"""

import os
import re
import sys
import time
import platform
import subprocess
from pathlib import Path

try:
    from core import gemini
except Exception:
    gemini = None

try:
    from core import outcome
except Exception:
    outcome = None

try:
    import pyperclip
    _HAS_PYPERCLIP = True
except Exception:
    _HAS_PYPERCLIP = False

try:
    import pyautogui
    _HAS_PYAUTOGUI = True
except Exception:
    _HAS_PYAUTOGUI = False


def _clean_code(text: str) -> str:
    """Strips markdown code blocks, backticks, and extraneous explanations."""
    text = text.strip()
    text = re.sub(r"^```[a-zA-Z0-9_-]*\n?", "", text)
    text = re.sub(r"\n?```$", "", text)
    return text.strip()


def _get_os() -> str:
    s = platform.system().lower()
    if "windows" in s:
        return "windows"
    if "darwin" in s:
        return "mac"
    return "linux"


def _focus_vscode() -> bool:
    """Bring Visual Studio Code to the foreground."""
    os_name = _get_os()
    title = "Visual Studio Code"

    if os_name == "windows":
        try:
            script = f'(New-Object -ComObject WScript.Shell).AppActivate("{title}")'
            res = subprocess.run(
                ["powershell", "-NoProfile", "-NonInteractive", "-Command", script],
                capture_output=True, timeout=5
            )
            time.sleep(0.4)
            return b"True" in res.stdout or res.returncode == 0
        except Exception:
            return False

    elif os_name == "mac":
        script = (
            f'tell application "System Events" to '
            f'set frontmost of (first process whose name contains "Code") to true'
        )
        try:
            subprocess.run(["osascript", "-e", script], capture_output=True, timeout=5)
            time.sleep(0.4)
            return True
        except Exception:
            return False

    elif os_name == "linux":
        try:
            res = subprocess.run(["wmctrl", "-a", "Visual Studio Code"], capture_output=True, timeout=5)
            if res.returncode == 0:
                time.sleep(0.4)
                return True
        except Exception:
            pass
        try:
            res = subprocess.run(["xdotool", "search", "--name", "Visual Studio Code", "windowactivate"], capture_output=True, timeout=5)
            if res.returncode == 0:
                time.sleep(0.4)
                return True
        except Exception:
            pass

    return False


def _launch_vscode(path_to_open: Path = None) -> bool:
    """Launch VS Code using the 'code' CLI or standard paths."""
    os_name = _get_os()
    candidates = ["code"]
    
    if os_name == "windows":
        user_name = Path.home().name
        candidates.extend([
            rf"C:\Users\{user_name}\AppData\Local\Programs\Microsoft VS Code\bin\code.cmd",
            r"C:\Program Files\Microsoft VS Code\bin\code.cmd",
            rf"C:\Users\{user_name}\AppData\Local\Programs\Microsoft VS Code\Code.exe",
            r"C:\Program Files\Microsoft VS Code\Code.exe",
        ])
    elif os_name == "mac":
        candidates.extend([
            "/Applications/Visual Studio Code.app/Contents/Resources/app/bin/code",
            str(Path.home() / "Applications/Visual Studio Code.app/Contents/Resources/app/bin/code")
        ])
    elif os_name == "linux":
        candidates.extend(["/usr/bin/code", "/snap/bin/code"])

    args = []
    if path_to_open:
        args.append(str(path_to_open))

    for cmd in candidates:
        try:
            cmd_args = [cmd] + args
            subprocess.Popen(
                cmd_args,
                shell=(os_name == "windows"),
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            time.sleep(1.2)
            return True
        except Exception:
            continue

    return False


def _generate_code(prompt: str, language: str) -> str:
    """Ask Gemini to generate clean, self-contained source code."""
    sys_instruction = (
        f"You are a professional software engineer. "
        f"Write complete, working, high-quality {language} code for the user's request. "
        f"Output ONLY the raw code. Do NOT wrap in markdown backticks. "
        f"Do NOT include conversational filler, preamble, or explanations. "
        f"Include helpful inline comments inside the code."
    )
    
    full_prompt = f"{sys_instruction}\n\nTask: {prompt}\nLanguage: {language}"
    
    if gemini is not None:
        try:
            if hasattr(gemini, "text"):
                raw = gemini.text(full_prompt, tier=getattr(gemini, "SMART", "smart"), timeout_ms=60000)
                if raw:
                    return _clean_code(raw)
        except Exception:
            pass

        try:
            if hasattr(gemini, "call"):
                resp = gemini.call(full_prompt, tier=getattr(gemini, "SMART", "smart"), timeout_ms=60000)
                if resp:
                    text = getattr(resp, "text", str(resp))
                    return _clean_code(text)
        except Exception as e:
            raise RuntimeError(f"Gemini code generation failed: {e}")

    return ""


def _default_filename(language: str, prompt: str) -> str:
    """Generate a clean filename from prompt and language."""
    ext_map = {
        "python": ".py", "py": ".py",
        "javascript": ".js", "js": ".js", "node": ".js",
        "typescript": ".ts", "ts": ".ts",
        "html": ".html", "htm": ".html",
        "css": ".css",
        "c++": ".cpp", "cpp": ".cpp", "c": ".c",
        "java": ".java",
        "c#": ".cs", "csharp": ".cs",
        "go": ".go", "golang": ".go",
        "rust": ".rs",
        "json": ".json",
        "sql": ".sql",
        "bash": ".sh", "shell": ".sh",
    }
    ext = ext_map.get(language.lower().strip(), ".txt")
    
    words = re.findall(r"[a-zA-Z0-9]+", prompt.lower())
    words = [w for w in words if w not in ("write", "code", "create", "make", "in", "a", "an", "the", "for", "me", "vscode", "vs")]
    slug = "_".join(words[:3]) if words else "script"
    return f"{slug}{ext}"


def vscode_write_action(parameters: dict, player=None, session_memory=None) -> str:
    prompt = parameters.get("prompt") or parameters.get("description") or parameters.get("code_task")
    if not prompt or not str(prompt).strip():
        return "Sir, please specify what code you would like me to write in VS Code."

    prompt = str(prompt).strip()
    language = str(parameters.get("language", "python")).strip()
    mode = str(parameters.get("mode", "file")).lower().strip()
    custom_filename = parameters.get("filename")

    if player and hasattr(player, "write_log"):
        player.write_log(f"DEV: Generating {language} code for '{prompt[:45]}'...")

    # Step 1: Generate code
    try:
        code = _generate_code(prompt, language)
    except Exception as e:
        msg = f"Sir, I could not generate the code: {e}"
        if player and hasattr(player, "write_log"):
            player.write_log(f"ERR: {msg}")
        return msg

    if not code:
        return "Sir, the code generation returned an empty result."

    # Step 2: Handle active_window mode (Live Typing / Paste in active tab)
    if mode == "active_window" and _HAS_PYPERCLIP and _HAS_PYAUTOGUI:
        focused = _focus_vscode()
        if not focused:
            _launch_vscode()
            time.sleep(2.0)
            _focus_vscode()

        time.sleep(0.3)
        # Open a new tab in VS Code: Ctrl+N or Cmd+N
        mod_key = "command" if _get_os() == "mac" else "ctrl"
        try:
            pyautogui.hotkey(mod_key, "n")
            time.sleep(0.4)
            # Copy and Paste code
            pyperclip.copy(code)
            time.sleep(0.1)
            pyautogui.hotkey(mod_key, "v")
            time.sleep(0.3)

            msg = f"Sir, I have written and pasted the {language} code for '{prompt}' directly into your VS Code editor."
            if player and hasattr(player, "write_log"):
                player.write_log(f"DEV: Pasted {language} code into VS Code editor.")
            return msg
        except Exception:
            pass

    # Step 3: Default mode — Create file on disk and open directly in VS Code
    filename = custom_filename or _default_filename(language, prompt)
    
    desktop_dir = Path.home() / "Desktop"
    target_dir = desktop_dir if desktop_dir.exists() else Path.home()
    target_path = target_dir / filename

    try:
        target_path.write_text(code, encoding="utf-8")
    except Exception as e:
        return f"Sir, failed to save code file to {target_path}: {e}"

    # Launch or bring up in VS Code
    opened = _launch_vscode(target_path)
    if not opened:
        _focus_vscode()

    msg = f"Sir, I have created '{filename}' and opened it in VS Code for you."
    if player and hasattr(player, "write_log"):
        player.write_log(f"DEV: Created {filename} and opened in VS Code.")
        
    return msg


TOOL = {
    "name": "vscode_writer",
    "description": (
        "Writes, types, or generates code directly into Visual Studio Code (VS Code). "
        "Call this whenever the user asks to write code, generate a script, create a program, "
        "or type code in VS Code (Python, HTML, JS, C++, etc.). "
        "It generates complete code, creates the file, and automatically opens it in VS Code, "
        "or pastes it live into the editor."
    ),
    "parameters": {
        "type": "OBJECT",
        "properties": {
            "prompt": {
                "type": "STRING",
                "description": "What code or program to write (e.g. 'snake game in python', 'HTML login page', 'binary search in C++')"
            },
            "language": {
                "type": "STRING",
                "description": "Programming language (e.g. python, javascript, html, cpp, java). Default: python"
            },
            "mode": {
                "type": "STRING",
                "description": "'file' (creates file and opens it in VS Code) or 'active_window' (pastes directly into active VS Code editor). Default: file"
            },
            "filename": {
                "type": "STRING",
                "description": "Optional filename to create (e.g. 'game.py', 'index.html')"
            }
        },
        "required": ["prompt"]
    },
    "handler": vscode_write_action,
}
