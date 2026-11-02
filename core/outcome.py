"""
core/outcome.py — Result formatting and content wrapping for tools.

Provides standardized markers (done, unverified, failed, ask, started) and
untrusted-content wrapping so external data (web pages, search results) is safely
delimited from model instructions.
"""
import re

WRAPPER_START = "<<<EXTERNAL_UNTRUSTED_CONTENT>>>"
WRAPPER_END   = "<<</EXTERNAL_UNTRUSTED_CONTENT>>>"

_WRAP_RE = re.compile(
    re.escape(WRAPPER_START) + r"(.*?)" + re.escape(WRAPPER_END),
    re.DOTALL
)

def wrap(content: str) -> str:
    """Wrap untrusted external data (e.g. web search results, external files)."""
    if not content:
        return ""
    safe = str(content).replace(WRAPPER_END, "[END_MARKER_DEFANGED]")
    return f"{WRAPPER_START}\n{safe}\n{WRAPPER_END}"

def unwrap(content: str) -> str:
    """Strip untrusted wrapper markers before showing content to the user."""
    if not content:
        return ""
    s = str(content)
    s = s.replace(WRAPPER_START, "").replace(WRAPPER_END, "")
    s = s.replace("[END_MARKER_DEFANGED]", "")
    return s.strip()

def done(message: str = "Done.") -> str:
    return f"[DONE] {message}"

def unverified(message: str) -> str:
    return f"[UNVERIFIED] {message}"

def failed(message: str) -> str:
    return f"[FAILED] {message}"

def ask(message: str) -> str:
    return f"[ASK] {message}"

def started(message: str) -> str:
    return f"[STARTED] {message}"
