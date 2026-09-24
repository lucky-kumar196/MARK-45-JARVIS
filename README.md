# ✨ MARK-45-JARVIS — SRJ Web Sto Assistant

**Created & Maintained by:** Lucky  
**Organization:** SRJ Web Sto

MARK-45-JARVIS is the flagship release where the **SRJ Web Sto Assistant** gets a face.

A holographic head sits at the center of the HUD and speaks your assistant's words with real lip-sync — using actual mouth shapes derived from speech formants and transcripts.

It ships with **zero extra dependencies** and a single **25 KB asset**. The face uses real measured human geometry; everything else — the skull, rig, and lighting — is generated at startup and rendered entirely in software, ensuring identical performance on both high-end systems and legacy laptops with zero GPU driver overhead.

---

## 🎨 System Architecture & Functional Layout

```text
+-----------------------------------------------------------------------------------+
|  1. VISUAL AVATAR ENGINE                                                         |
|     Holographic Head • Viseme Lip-Sync • Software QPainter • Status Indicators   |
+-----------------------------------------------------------------------------------+
|  2. INTELLIGENT CORE & MEMORY                                                    |
|     Recallable Memory • Reversible Safety Undo • Live Runtime Self-Knowledge      |
+-----------------------------------------------------------------------------------+
|  3. CONTROL & HARDWARE UTILITIES                                                 |
|     Push-to-Talk (PTT) • Self-Echo Guard • Physical UI Confirmation • Device Picker|
+-----------------------------------------------------------------------------------+
|  4. AUTOMATION & EXTENSION ENGINE                                                |
|     Gemini 3.1 Flash Live • Self-Describing Plugins • Modular Action Handlers    |
+-----------------------------------------------------------------------------------+
```

---

## 🚀 Key Capabilities

| Domain | Feature | Details |
|---|---|---|
| **Visual Avatar** | 🧑‍🎤 **Holographic Head** | Real-time software-rendered human head HUD interface. |
| **Visual Avatar** | 👄 **Viseme Lip-Sync** | Formants and transcripts drive ~50 mouth shapes per second. |
| **Visual Avatar** | 🌍 **Universal Script** | Articulation via Unicode reduction for Latin, Cyrillic, Greek, Hindi, etc. |
| **Visual Avatar** | 😐 **Face as Status** | Glances away when thinking, engages eye contact when listening, and sleeps when idle. |
| **Core Memory** | 🧠 **Recallable Memory** | Local JSON lookup engine with unlimited capacity and zero silent deletions. |
| **Core Memory** | 👁️ **Memory Panel** | View every stored fact and remove entries in a single click. |
| **Core Memory** | ↩️ **Safety Undo** | Instant reversion of file modifications, moves, creations, and system settings. |
| **User Control** | 🎚️ **Push-to-Talk** | Global `Ctrl+Space` chord activation for precise microphone management. |
| **User Control** | 🔇 **Self-Echo Guard** | Subtracts assistant voice output from microphone input without muting. |
| **User Control** | ⚠️ **Physical Confirmation** | Hard gates for shutdown, restart, and Wi-Fi toggles via explicit UI button presses. |
| **Automation** | ⚡ **Instant Acknowledgment** | Speaks immediate task status before long-running background tasks begin. |
| **Automation** | 🧩 **Plugin Architecture** | Self-describing `.py` drop-in architecture for rapid skill expansion. |
| **Automation** | 🚀 **Live Voice Engine** | Ultra-low-latency voice responses powered by Gemini 3.1 Flash Live. |

---

## 📋 Requirements & System Compatibility

| Requirement | Details |
|---|---|
| **Operating System** | Windows 10/11, macOS, or Linux |
| **Python Version** | Python 3.11, 3.12, or 3.13 |
| **Audio I/O** | Microphone and speakers required for voice interaction |
| **API Integration** | Gemini API Key configured in `config/api_keys.json` |
| **GPU Requirement** | **Not Required** — all avatar visual features render via software |

---

## 🗂️ Project Directory Layout


```text
Mark LIV/
├── main.py                   # Core loop — Gemini Live session, audio I/O, viseme extraction, tool dispatch
├── ui.py                     # PyQt6 HUD — avatar canvas, waveform, log panel, settings drawer, camera feed
├── setup.py                  # OS-aware installer (skips wrong-OS dependencies, checks your Python)
├── .gitignore                # Keeps your API key, TLS key and memories out of the repository
├── plugins/
│   ├── quiz.py               # Interactive quiz — JARVIS writes the questions, you answer on screen
│   ├── document_review.py    # Contracts and policies in plain language, ordered by what matters
│   ├── _google_core.py       # Shared OAuth for the Gmail/Calendar plugins (not a plugin itself)
│   ├── _printer_core.py      # Shared printer connectivity (not a plugin itself)
│   ├── _template.py          # Copy this to write a new plugin — one file, drop in, done
│   └── ...                   # Drop-in skills (each self-describes via a PLUGIN dict + run())
├── actions/                  # Bundled skills — each self-describes via a TOOL dict + handler
│   ├── web_search.py         # Gemini + DDG parallel search (news, research, price, compare)
│   ├── screen_processor.py   # Screen & webcam capture for vision
│   ├── background_monitor.py # User-configured topic watching — daily DDG check
│   ├── proactive.py          # Proactive 2.0 — time/context/rotation-aware check-ins
│   ├── reminder.py           # OS-native scheduled notifications
│   ├── system_monitor.py     # CPU / RAM / GPU / temperature telemetry
│   ├── computer_settings.py  # Volume, brightness, WiFi, power (per-OS)
│   ├── computer_control.py   # Keyboard shortcuts, mouse, window management
│   ├── open_app.py           # Application launcher (per-OS name map)
│   ├── browser_control.py    # Web browser control
│   ├── file_controller.py    # File system operations
│   ├── file_processor.py     # Document reading and summarization
│   ├── send_message.py       # Messaging integration
│   ├── weather_report.py     # Live weather data
│   ├── flight_finder.py      # Flight search
│   ├── youtube_video.py      # YouTube playback control
│   ├── game_updater.py       # Game update management (Steam / Epic)
│   ├── code_helper.py        # Code review and generation
│   ├── dev_agent.py          # Developer task agent
│   └── desktop.py            # Desktop and taskbar control
├── memory/
│   ├── memory_manager.py     # Load/save long_term.json — sessions, monitors, identity
│   ├── config_manager.py     # api_keys.json access — key, OS, name, voice, colour, toggles
│   └── long_term.json        # Persistent store — created on first run
├── core/
│   ├── prompt.txt            # All prompt wording — {tokens} are filled from the live system at startup
│   ├── avatar.py             # Avatar renderer — lighting, pose, expression, mouth (QPainter)
│   ├── avatar_mesh.py        # Head geometry — loads the face, generates skull/neck/rigs
│   ├── face_model.obj        # The face itself (MediaPipe canonical model, Apache-2.0, 25 KB)
│   ├── viseme.py             # Transcript → mouth shapes, fused with the audio's timing
│   ├── echo.py               # Tells your voice from the assistant's own echo; self-calibrating
│   ├── hotkey.py             # Push-to-talk chord — global on Windows, windowed fallback elsewhere
│   ├── undo.py               # One shared undo stack — actions register how to reverse themselves
│   ├── confirm.py            # Irreversible-action gate — the token is issued by the UI, not the model
│   ├── audio_devices.py      # Microphone / speaker list — filtered, measured, resolved by name
│   ├── plugin_loader.py      # Plugin engine — discovery, validation, crash isolation
│   ├── action_loader.py      # Bundled-action engine — the built-in twin of plugin_loader
│   └── wake_word.py          # Local "Hey Jarvis" detector — own thread, offline, opt-in
└── config/
    ├── api_keys.json         # API key, name, voice, colour, toggles — created on first launch (git-ignored)
    └── certs/                # Self-signed TLS pair for the phone dashboard — generated locally (git-ignored)
```

---

## ⚡ Quick Start & Deployment

### 1. Clone the repository

```bash
git clone https://github.com/lucky-kumar196/MARK-45-JARVIS.git
cd MARK-45-JARVIS
```

### 2. Run the OS-aware environment setup

```bash
python setup.py
```

### 3. Launch MARK-45-JARVIS

```bash
python main.py
```

---

## 🔒 SRJ Web Sto Data Privacy & Security

| Data Asset | Storage Location | Privacy Standard |
|---|---|---|
| **Long-Term Memory** | `memory/long_term.json` | 100% local retention — never leaves your system. |
| **API Keys & Credentials** | `config/api_keys.json` | Stored locally and kept git-ignored for safety. |
| **Voice Streaming** | Gemini Live API | Directly encrypted TLS connection without intermediate servers. |

> **Security Note:** Keep `config/api_keys.json` private and never commit API credentials to a public repository.

---

## 🧠 Architecture Overview

MARK-45-JARVIS is organized into four primary layers:

### 1. Visual Avatar Engine
Handles the holographic head, software rendering, facial status states, and real-time viseme animation.

### 2. Intelligent Core & Memory
Provides local long-term memory, runtime self-knowledge, and reversible actions through an undo history.

### 3. Control & Hardware Utilities
Provides Push-to-Talk activation, microphone echo protection, device selection, and physical confirmation gates for sensitive system actions.

### 4. Automation & Extension Engine
Connects the assistant to Gemini Live and exposes modular plugins and action handlers that can be expanded without changing the core architecture.

---

## 🔌 Plugin Architecture

MARK-45-JARVIS uses a modular plugin system designed around self-describing Python (`.py`) skills.

Plugins can be added to the:

```text
plugins/
```

directory and can expose additional assistant capabilities without requiring changes to the main assistant architecture.

---

## 🎙️ Voice Interaction

MARK-45-JARVIS supports real-time voice interaction through the Gemini Live engine.

The interaction pipeline is designed around:

```text
Microphone
    ↓
Voice Input
    ↓
Gemini Live
    ↓
Assistant Response
    ↓
Voice Output
    ↓
Viseme / Facial Animation
```

The Self-Echo Guard helps prevent the assistant from interpreting its own voice output as new user input.

---

## 👁️ Avatar Behavior

The avatar is designed to communicate system state visually:

| Assistant State | Avatar Behavior |
|---|---|
| **Idle** | Face enters a sleeping/resting state |
| **Listening** | Maintains eye contact |
| **Thinking** | Glances away while processing |
| **Speaking** | Animates mouth shapes using viseme synchronization |

---

## ↩️ Safety & Reversible Actions

MARK-45-JARVIS includes an action history system designed to make supported operations reversible.

The undo layer can track supported:

- File modifications
- File moves
- File creations
- System setting changes

This allows actions to be reverted when supported by the underlying action handler.

---

## 🛡️ Security Principles

MARK-45-JARVIS follows several core security principles:

- 🔐 Keep API credentials local.
- 🚫 Do not commit secrets to Git.
- 🧩 Use modular action handlers.
- ⚠️ Require explicit UI confirmation for sensitive physical/system controls.
- ↩️ Preserve an action history for supported reversible operations.
- 🏠 Keep long-term memory stored locally.

---

## 💻 Hardware Philosophy

The avatar renderer is intentionally software-based.

### GPU

**No dedicated GPU is required.**

The avatar's visual features are rendered using software rendering, allowing the application to operate across a broad range of hardware, including legacy laptops.

### Required Hardware

- Microphone
- Speakers

---

## 🌟 Project Highlights

- 🧑‍🎤 Software-rendered holographic avatar
- 👄 Real-time viseme lip-sync
- 🧠 Local long-term memory
- ↩️ Reversible action system
- 🎚️ Global Push-to-Talk
- 🔇 Self-Echo Guard
- ⚠️ Physical confirmation gates
- 🧩 Self-describing plugin architecture
- 🚀 Gemini Live voice interaction
- 🌍 Multi-script articulation support
- 💻 No dedicated GPU requirement
- 📦 Minimal asset footprint

---


---

## 👨‍💻 Author

**Lucky**  
**SRJ Web Sto(srjwebsto.site.je)**

Developed and maintained as the **MARK-45-JARVIS — SRJ Web Sto Assistant**.

---

<div align="center">

### ✨ MARK-45-JARVIS

**Your assistant. Your system. Your control.**

**Developed & Maintained by Lucky · SRJ Web Sto**

</div>
