# ⚡ Keyboard Rage Detector

A real-time typing hostility analyzer that measures how aggressively you are hitting your keyboard. It calculates a dynamic **Rage Score (0–100%)**, visualizes your current fury with animated gauges and screen-shaking effects, produces reactive Web Audio sounds, and delivers witty, sarcastic commentary.

![Rage Meter Preview](https://img.shields.io/badge/Rage_Status-Active-critical?style=for-the-badge)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-success?style=for-the-badge)

---

## 🌟 Features

- **Dynamic Rage Meter (0–100%)**:
  - Smooth semi-circular neon gauge reacting instantly to your typing cadence.
- **5 Tier Classifications**:
  1. 🌿 **Zen Monk (0–18%)**: Calm, rhythmic, peaceful keystrokes.
  2. ☕ **Mildly Irritated (19–38%)**: Subtle sigh, passive-aggressive emails.
  3. ⚡ **Simmering Salt (39–62%)**: Punchy typing, audible nose-exhales, CSS struggles.
  4. 🔥 **High Voltage Rage (63–84%)**: Keycaps flying, heavy breathing, spacebar abuse.
  5. 💀 **DEFCON 1: Obliteration (85–100%)**: Maximum annihilation, keyboard emergency!
- **Reactive Sensory Effects**:
  - **Screen Shake**: Physical viewport tremors scaling from subtle vibration to cataclysmic screen quake at DEFCON 1.
  - **Procedural Sound Engine**: Built entirely with the Web Audio API (synthesized mechanical key clicks, tension hums, emergency sirens, and calming chords — zero external audio downloads).
- **Multi-Factor Heuristics Engine**:
  - **Burst Velocity**: Keys Per Second (CPS) & estimated WPM.
  - **Backspace Fury**: Tracks rapid consecutive deletions and regret ratios.
  - **Mash / Slam Detection**: Identifies repeated character spam (`aaaaaa`) and home-row fist mashes (`asdfghjk`).
  - **Caps Shouting**: Detects uppercase text and furious punctuation marks (`!?!11!`).
  - **Dwell Time**: Measures keypress hold duration (heavy angry presses).
- **Witty Contextual Comments**:
  - Scores of situational quotes tailored to your exact typing trauma.
- **Sensitivity Slider & Preset Rage Scenarios**:
  - Easily test scenarios like "Salty Email", "Broken Code", and "Office Chaos".

---

## 🚀 How to Run

### Option 1: Web Application (Recommended)
No installation, package managers, or server setup required!

1. Open `index.html` directly in your favorite browser (Chrome, Edge, Firefox, Safari):
   ```powershell
   # In Windows PowerShell:
   Start-Process index.html
   ```
2. Or start a simple local server if you prefer:
   ```powershell
   python -m http.server 8000
   # Then open http://localhost:8000
   ```

### Option 2: Python Terminal Edition
A zero-dependency CLI version using Python's built-in `msvcrt` on Windows:

```powershell
python desktop_detector.py
```
- Real-time colored ANSI bar meter
- Live mood commentary
- Keystroke counter & Peak rage tracker
- Press `ESC` or `Ctrl+C` to exit

---

## 📁 Project Structure

```
keyboard-rage-detector/
├── index.html           # Main user interface & interactive typing arena
├── style.css            # Cyberpunk/arcade styling, gauge layout, screen-shake keyframes
├── engine.js            # Algorithmic scoring engine & rolling-window event listener
├── comments.js          # Tiered commentary library & situational callout triggers
├── audio.js             # Web Audio API procedural sound synthesizer
├── desktop_detector.py  # Standalone Python CLI edition for terminal lovers
└── README.md            # Documentation & setup guide
```

---

## 💡 Calibration & Tips
- **Adjust Sensitivity**: Use the slider on the web app (0.5x to 2.0x) to tune the detector for your keyboard switch type (e.g. heavy tactile switches vs light laptop chiclets).
- **Audio Permission**: Modern browsers require an initial click or keystroke to start Web Audio playback.
- **Cooling Down**: Stop typing or type gentle rhythmic sentences to watch your rage score naturally decay back to Zen.
