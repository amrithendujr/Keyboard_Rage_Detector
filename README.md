# ⚡ Keyboard Rage Detector

A real-time typing hostility analyzer that measures how aggressively you are hitting your keyboard. It calculates a dynamic **Rage Score (0–100%)**, visualizes your current fury with animated gauges and screen-shaking effects, produces reactive Web Audio sounds, and delivers witty, sarcastic commentary.

<<<<<<< HEAD
![Rage Meter Preview](https://img.shields.io/badge/Rage_Status-Active-critical?style=for-the-badge)
![Zero Dependencies](https://img.shields.io/badge/Dependencies-Zero-success?style=for-the-badge)
=======

# [Keyboard Rage Detector] 🎯


## Basic Details
### Team Name: [Name]


### Team Members
- Team Lead: [Amrithendu J R] - [SOE CUSAT]
  

### Project Description
[Keyboard rage detector is a software project that monitors keyboard activity detects unusual or aggressive typing patterns. It analyses factors such as rapid key presses, repeated key presses, and excessive backspace or space usage to estimate the user's frustration or rage level. When the detected activity crosses a predefined threshold, the application displays a warning and a visual indication with sound. The project can run in the background while the user works, studies, codes or play games.]

### The Problem (that doesn't exist)
[People sometimes become frustrated while studying, programing, gaming or typing. During these moments they may repeatedly hit keys, press keys fast or aggressively use backspace. There is no simple system that humorously detects these keyboard patterns and tell the user.]

### The Solution (that nobody asked for)
[I created a keyboard rage detector that continuously observes the keyboard activity and create a Rage Score.
The system can detect patterns such as:
. Extremely fast key presses
. Many keys pressed within a short period
. Repeating pressing of the same key
. Excessive space/enter presses
. Excessive backspace presses

And the application displays a funny warning according to your rage score.
Example: 
     Rage level: 80%
     "Angry Gorilla Mode"]

## Technical Details
### Technologies/Components Used
For Software:
- [Python]
- [pynput - keyboard event mnitoring]
- [pySide6 / PyQt6 - graphical user interface]
- [time - timing keyboard events]
- [collections - storing recent keyboard events]
- [threading - running keyboard monitoring without freezing the GUI]
- [statistics / mathematics - calculating rage score]

For Hardware:
- [No additional hardware is required]

### Implementation
For Software:
# Installation
[commands]

# Run
[commands]

### Project Documentation
For Software:

# Screenshots (Add at least 3)
![Screenshot1](Add screenshot 1 here with proper name)
*Add caption explaining what this shows*

![Screenshot2](Add screenshot 2 here with proper name)
*Add caption explaining what this shows*

![Screenshot3](Add screenshot 3 here with proper name)
*Add caption explaining what this shows*

# Diagrams
![Workflow](Add your workflow/architecture diagram here)
*Add caption explaining your workflow*

For Hardware:

# Schematic & Circuit
![Circuit](Add your circuit diagram here)
*Add caption explaining connections*

![Schematic](Add your schematic diagram here)
*Add caption explaining the schematic*

# Build Photos
![Components](Add photo of your components here)
*List out all components shown*

![Build](Add photos of build process here)
*Explain the build steps*

![Final](Add photo of final product here)
*Explain the final build*

### Project Demo
# Video
[Add your demo video link here]
*Explain what the video demonstrates*

# Additional Demos
[Add any extra demo materials/links]

## Team Contributions
- [Name 1]: [Specific contributions]
>>>>>>> 88bd0e2820392b698cfb590b51c01ce481911e31

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
