#!/usr/bin/env python3
"""
Keyboard Rage Detector - Floating Desktop Overlay HUD (Emoji Edition)
An always-on-top, draggable, transparent widget that monitors typing hostility
across all laptop apps with rich emojis, animated emoji particle bursts,
large reactive mascot emoji, and 4-tier procedural audio:
  - < 30 : Calm Sound (Soothing meditative chord chime)
  - < 50 : Rage Sound (Distorted angry harmonic buzz)
  - < 85 : Racing Car Sound (Engine rev sweep 80→380Hz)
  - 85+  : Danger Alarm (Emergency klaxon siren)
"""

import time
import sys
import os
import random
import threading
import io
import wave
import struct
import math
from collections import deque
import tkinter as tk

# Global keyboard listener
try:
    from pynput import keyboard
    HAS_PYNPUT = True
except ImportError:
    HAS_PYNPUT = False

# Sound on Windows
try:
    import winsound
    HAS_WINSOUND = True
except ImportError:
    HAS_WINSOUND = False


class ProceduralAudioEngine:
    """Zero-dependency, in-memory 4-tier procedural audio synthesizer."""
    def __init__(self):
        self.muted = False
        self.rate = 22050
        self.sounds = {}
        self.lock = threading.Lock()
        self._generate_all_sounds()

    def _make_wav(self, samples):
        buf = io.BytesIO()
        w = wave.open(buf, 'wb')
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(self.rate)
        raw = b''.join(struct.pack('<h', max(-32767, min(32767, int(s)))) for s in samples)
        w.writeframes(raw)
        w.close()
        return buf.getvalue()

    def _generate_all_sounds(self):
        # 1. Calm Sound (< 30): Gentle, soothing C-E-G ambient chord chime
        calm_samples = []
        duration = int(self.rate * 0.95)
        for i in range(duration):
            t = i / self.rate
            env = math.exp(-t * 3.8)
            s = (
                math.sin(2 * math.pi * 523.25 * t) +       # C5
                0.8 * math.sin(2 * math.pi * 659.25 * t) + # E5
                0.6 * math.sin(2 * math.pi * 783.99 * t)   # G5
            ) * 7500 * env
            calm_samples.append(s)
        self.sounds["calm"] = self._make_wav(calm_samples)

        # 2. Rage Sound (< 50): Distorted angry buzz with rich harmonic crunch
        rage_samples = []
        duration = int(self.rate * 0.35)
        for i in range(duration):
            t = i / self.rate
            env = math.exp(-t * 2.2)
            s = (
                math.sin(2 * math.pi * 280 * t) +
                0.65 * math.sin(2 * math.pi * 560 * t) +
                0.40 * math.sin(2 * math.pi * 840 * t)
            ) * 18000 * env
            rage_samples.append(s)
        self.sounds["rage"] = self._make_wav(rage_samples)

        # 3. Racing Car Sound (< 85): Engine rev sweep with harmonics + noise
        racing_samples = []
        duration = int(self.rate * 0.65)
        for i in range(duration):
            t = i / self.rate
            # Rising fundamental: 80Hz → 380Hz over duration (power curve)
            freq = 80 + (300 * (t / 0.65) ** 1.5)
            # Sawtooth wave (engine timbre)
            saw = 2 * ((freq * t) % 1.0) - 1
            # Harmonic overtones
            harm1 = 0.5 * (2 * ((freq * 2 * t) % 1.0) - 1)
            harm2 = 0.25 * (2 * ((freq * 3 * t) % 1.0) - 1)
            # Mechanical noise component
            noise = (random.random() * 2 - 1) * 0.15
            # Attack + slight decay envelope
            env = min(1.0, t * 8) * (1 - (t / 0.65) * 0.3)
            s = (saw + harm1 + harm2 + noise) * 14000 * env
            racing_samples.append(s)
        self.sounds["racing"] = self._make_wav(racing_samples)

        # 4. Danger Sound (85+): Emergency siren klaxon warble
        danger_samples = []
        duration = int(self.rate * 0.55)
        for i in range(duration):
            t = i / self.rate
            freq = 980 if int(t * 8) % 2 == 0 else 640
            s = math.sin(2 * math.pi * freq * t) * 20000
            danger_samples.append(s)
        self.sounds["danger"] = self._make_wav(danger_samples)

    def play(self, sound_name):
        if self.muted or not HAS_WINSOUND:
            return
        data = self.sounds.get(sound_name)
        if not data:
            return

        def _worker():
            with self.lock:
                try:
                    winsound.PlaySound(data, winsound.SND_MEMORY)
                except Exception:
                    pass

        threading.Thread(target=_worker, daemon=True).start()


# Tier database with roasts and emojis
TIERS = [
    (18, "🧘‍♂️ CHILLAXED BUDDHA", "#10b981", "🧘‍♂️", [
        "Namaste bro 🧘‍♂️ Typing like you're rubbing essential oils on the keys 🍵",
        "Zero hostility detected 🌱 Are you typing in a lavender field with flute music? 🪈",
        "Your keyboard feels safe, loved, and emotionally validated 💖⌨️",
        "Bro is typing in lowercase whisper mode... shhh 🤫☁️"
    ]),
    (38, "☕ PASSIVE-AGGRESSIVE INTERN", "#3b82f6", "☕", [
        "We detect a subtle brow furrow 👁️👄👁️ 'Per my previous email' incoming...",
        "A tiny vein just popped on your forehead 🤏😡 Take a sip of water, bestie 🧃",
        "You just aggressively clicked your mouse wheel didn't you? 🐁👀",
        "Slight finger tension. Someone scheduled an 8:30 AM sync 📅🤡"
    ]),
    (62, "🧂 CHIEF SALT OFFICER", "#f59e0b", "🧂", [
        "Warning: That backspace key didn't steal your lunch money, chill! 💀🥪",
        "Are you coding or playing Street Fighter combos on the home row?! 🕹️🥋",
        "Bro is cooking minute rice in 54 seconds with that finger friction! 🍚🔥",
        "You just sighed audibly through your nose like a disappointed dragon 🐉💨"
    ]),
    (84, "🦍 ANGRY GORILLA MODE", "#ef4444", "🦍", [
        "WOAH! Keycaps are holding on for dear life! Ease off the throttle! 🪂💥",
        "Your spacebar just filed an emergency restraining order with HR 📜🚨",
        "You're typing like the keyboard owes you 50 bucks and child support! 💸🥊",
        "Cherry MX switches are screaming in lowercase 'help us' 😭🍒"
    ]),
    (100, "💀 KEYBOARD EXTINCTION EVENT", "#dc2626", "💀", [
        "🚨 CODE RED! THE DESK IS SHAKING, THE CAT IS HIDING, CALL 911! 🐈💨🚑",
        "NUCLEAR MELTDOWN DETECTED! BRO IS TYPING WITH SLEDGEHAMMERS! 🌋🔨",
        "ARE YOU TYPING WITH A FOREHEAD ROLL?! STEP AWAY FROM THE PLASTIC! 🤦‍♂️💥",
        "KEYBOARD REPLACEMENT: $150. ANGER MANAGEMENT: HIGHLY RECOMMENDED 🛋️🧠"
    ])
]

SPECIAL_COMMENTS = {
    "backspace": [
        "BACKSPACE SPEEDRUN ANY% NO GLITCHES! 🏃‍♂️💨 Rewinding life choices!",
        "Bro just erased an entire novel in 0.3 seconds! Regret level: OVER 9000 💀⏪",
        "The delete key is begging for ice water and an ambulance! 🚑🧯"
    ],
    "caps": [
        "LOUD NOISES! 🗣️📢 WHY ARE WE SCREAMING AT THE CLOUDS?! 🦖⚡",
        "CAPS LOCK DOESN'T MAKE YOUR CODE RUN, IT JUST MAKES IT SCARY! 👹🔥",
        "ALL CAPS DETECTED! We can hear your scream through the fiber cables! 📡😱"
    ],
    "mash": [
        "DID A GOBLIN SMASH ITS HEAD ON YOUR HOME ROW?! 👺💥⌨️",
        "A wild keyboard smash appeared! 'asdfghjk' is not a real word, bro! 🐾🤯",
        "Total unbridled mash! You literally just donkey-kong punched your desk! 🦍🍌"
    ]
}

RAGE_BURST_EMOJIS = ['🔥', '💀', '💥', '💢', '🚨', '🦖', '🦍', '🪓', '🧂', '🥪', '🤡', '😱', '🌋', '💣']


class RageScorer:
    def __init__(self, window_sec=3.0, sensitivity=1.0):
        self.window_sec = window_sec
        self.sensitivity = sensitivity
        self.events = deque()
        self.current_rage = 0.0
        self.peak_rage = 0.0
        self.total_keystrokes = 0
        self.last_comment = "Start typing anywhere on your PC to detect rage..."
        self.last_comment_time = 0
        self.press_times = {}

        self.last_metrics = {
            "cps": 0.0,
            "wpm": 0,
            "backspace_rate": 0.0,
            "caps_ratio": 0.0,
            "mash_index": 0
        }

    def record_press(self, key_str):
        now = time.time()
        self.press_times[key_str] = now

        is_backspace = (key_str in ('Key.backspace', 'Key.delete', '\x08', '\x7f'))
        is_caps = False
        if len(key_str) == 1 and not is_backspace:
            is_caps = key_str.isupper() or key_str in '!@#$%^&*()_+{}|:"<>?'

        self.events.append((now, key_str, is_backspace, is_caps))
        self.total_keystrokes += 1
        self.prune(now)
        self.calculate(now)

    def record_release(self, key_str):
        if key_str in self.press_times:
            del self.press_times[key_str]

    def prune(self, now):
        cutoff = now - self.window_sec
        while self.events and self.events[0][0] < cutoff:
            self.events.popleft()

    def calculate(self, now):
        count = len(self.events)
        if count == 0:
            self.current_rage = max(0.0, self.current_rage - 2.8)
            return

        span = max(0.4, now - self.events[0][0])
        cps = count / span
        wpm = int((cps * 60) / 5)

        backspaces = sum(1 for e in self.events if e[2])
        backspace_rate = backspaces / count

        caps_count = sum(1 for e in self.events if e[3])
        caps_ratio = caps_count / count

        mash_score = 0
        ev_list = list(self.events)
        for i in range(1, len(ev_list)):
            prev_t, prev_c, _, _ = ev_list[i - 1]
            curr_t, curr_c, _, _ = ev_list[i]
            dt = curr_t - prev_t
            if prev_c == curr_c and dt < 0.13:
                mash_score += 2.5
            elif dt < 0.05:
                mash_score += 1.8

        v_score = min(35.0, max(0.0, (cps - 3.0) * 4.5)) if cps > 3.0 else 0
        b_score = min(30.0, backspace_rate * 35.0)
        m_score = min(30.0, mash_score * 3.2)
        c_score = min(20.0, caps_ratio * 25.0)

        target = max(0.0, min(100.0, (v_score + b_score + m_score + c_score) * self.sensitivity))

        alpha = 0.45 if target > self.current_rage else 0.15
        self.current_rage += (target - self.current_rage) * alpha

        if self.current_rage > self.peak_rage:
            self.peak_rage = self.current_rage

        self.last_metrics = {
            "cps": round(cps, 1),
            "wpm": wpm,
            "backspace_rate": round(backspace_rate, 2),
            "caps_ratio": round(caps_ratio, 2),
            "mash_index": int(mash_score)
        }

        current_tier_name, _, _ = self.get_tier_info()
        tier_changed = getattr(self, '_last_tier_name', None) != current_tier_name
        self._last_tier_name = current_tier_name

        if tier_changed or (now - self.last_comment_time > 2.2) or abs(target - self.current_rage) > 22:
            self.last_comment = self.pick_comment(backspace_rate, caps_ratio, mash_score)
            self.last_comment_time = now

    def pick_comment(self, b_rate, c_ratio, mash):
        rage = self.current_rage
        if rage > 35:
            if c_ratio > 0.65: return random.choice(SPECIAL_COMMENTS["caps"])
            if b_rate > 0.4: return random.choice(SPECIAL_COMMENTS["backspace"])
            if mash > 4: return random.choice(SPECIAL_COMMENTS["mash"])

        for limit, name, color, mascot, comments in TIERS:
            if rage <= limit:
                return random.choice(comments)
        return TIERS[-1][4][0]

    def get_tier_info(self):
        for limit, name, color, mascot, comments in TIERS:
            if self.current_rage <= limit:
                return name, color, mascot
        return TIERS[-1][1], TIERS[-1][2], TIERS[-1][3]


class RageOverlayHUD:
    def __init__(self, root):
        self.root = root
        self.scorer = RageScorer()
        self.audio = ProceduralAudioEngine()
        self.is_compact = False

        # Sound Bracket Tracker (<30: calm, <50: beep, <85: rage, 85<: danger)
        self.last_sound_bracket = None
        self.last_sound_time = 0

        # Floating emoji particles: list of dicts [id, vx, vy, life]
        self.particles = []

        # Drag coordinates
        self.drag_x = 0
        self.drag_y = 0

        # Window configuration
        self.root.title("Keyboard Rage Detector HUD")
        self.root.overrideredirect(True)
        self.root.wm_attributes("-topmost", True)
        self.root.wm_attributes("-alpha", 0.94)
        self.root.config(bg="#0a0d14")

        # Position: top-right corner
        screen_w = self.root.winfo_screenwidth()
        self.pos_x = screen_w - 430
        self.pos_y = 35
        self.base_pos_x = self.pos_x
        self.base_pos_y = self.pos_y
        self.root.geometry(f"410x245+{self.pos_x}+{self.pos_y}")

        self.setup_ui()
        self.bind_drag_events()
        self.start_keyboard_listener()
        self.update_loop()

    def setup_ui(self):
        # Outer border container
        self.outer_frame = tk.Frame(self.root, bg="#0a0d14", highlightbackground="#10b981", highlightthickness=2)
        self.outer_frame.pack(fill="both", expand=True, padx=2, pady=2)

        # Draggable title bar
        self.title_bar = tk.Frame(self.outer_frame, bg="#121826")
        self.title_bar.pack(fill="x", padx=6, pady=(6, 2))

        self.lbl_title = tk.Label(
            self.title_bar,
            text="⚡ RAGE DETECTOR OVERLAY 💻🔥",
            font=("Segoe UI", 9, "bold"),
            fg="#9ca3af",
            bg="#121826"
        )
        self.lbl_title.pack(side="left", padx=4)

        # Buttons: Close, Minimize/Compact, Sound Mute
        self.btn_close = tk.Label(self.title_bar, text="❌", font=("Segoe UI Emoji", 9), fg="#9ca3af", bg="#121826", cursor="hand2")
        self.btn_close.pack(side="right", padx=3)
        self.btn_close.bind("<Button-1>", lambda e: self.quit_app())

        self.btn_compact = tk.Label(self.title_bar, text="🗕", font=("Segoe UI", 9, "bold"), fg="#9ca3af", bg="#121826", cursor="hand2")
        self.btn_compact.pack(side="right", padx=4)
        self.btn_compact.bind("<Button-1>", lambda e: self.toggle_compact())

        self.btn_sound = tk.Label(self.title_bar, text="🔊", font=("Segoe UI Emoji", 9), fg="#9ca3af", bg="#121826", cursor="hand2")
        self.btn_sound.pack(side="right", padx=4)
        self.btn_sound.bind("<Button-1>", lambda e: self.toggle_sound())

        # Main Score + Large Mascot Emoji + Badge Row
        self.score_frame = tk.Frame(self.outer_frame, bg="#0a0d14")
        self.score_frame.pack(fill="x", padx=10, pady=2)

        # Big Animated Mascot Emoji
        self.lbl_mascot = tk.Label(
            self.score_frame,
            text="🧘‍♂️",
            font=("Segoe UI Emoji", 26),
            bg="#0a0d14"
        )
        self.lbl_mascot.pack(side="left", padx=(0, 4))

        self.lbl_rage_num = tk.Label(
            self.score_frame,
            text="0%",
            font=("Segoe UI", 26, "bold"),
            fg="#10b981",
            bg="#0a0d14"
        )
        self.lbl_rage_num.pack(side="left", padx=(0, 8))

        self.lbl_tier_badge = tk.Label(
            self.score_frame,
            text="🧘‍♂️ CHILLAXED BUDDHA",
            font=("Segoe UI", 9, "bold"),
            fg="#10b981",
            bg="#141e2e",
            padx=8,
            pady=3
        )
        self.lbl_tier_badge.pack(side="left", pady=4)

        # Sound mode indicator pill
        self.lbl_sound_mode = tk.Label(
            self.score_frame,
            text="🎵 CALM",
            font=("Segoe UI", 7, "bold"),
            fg="#10b981",
            bg="#0a0d14"
        )
        self.lbl_sound_mode.pack(side="right", padx=4, pady=4)

        # Progress bar
        self.canvas_bar = tk.Canvas(self.outer_frame, height=8, bg="#1e293b", highlightthickness=0)
        self.canvas_bar.pack(fill="x", padx=12, pady=(4, 1))
        self.bar_fill = self.canvas_bar.create_rectangle(0, 0, 0, 8, fill="#10b981", width=0)

        # Emoji Milestones Track under the bar
        self.lbl_milestones = tk.Label(
            self.outer_frame,
            text="🌿 Zen      ☕ Peeved      🧂 Salty      🦍 Gorilla      💀 Meltdown",
            font=("Segoe UI", 7),
            fg="#64748b",
            bg="#0a0d14"
        )
        self.lbl_milestones.pack(fill="x", padx=12, pady=(0, 2))

        # Floating Emoji Particle Canvas
        self.canvas_particles = tk.Canvas(self.outer_frame, height=24, bg="#0a0d14", highlightthickness=0)
        self.canvas_particles.pack(fill="x", padx=10, pady=0)

        # Reactive Comment Box
        self.lbl_comment = tk.Label(
            self.outer_frame,
            text="Start typing anywhere on your PC to detect rage...",
            font=("Segoe UI", 9),
            fg="#e2e8f0",
            bg="#0f172a",
            wraplength=375,
            justify="left",
            padx=8,
            pady=5
        )
        self.lbl_comment.pack(fill="x", padx=10, pady=(2, 4))

        # Telemetry footer with emojis
        self.lbl_telemetry = tk.Label(
            self.outer_frame,
            text="🏎️💨 0.0 CPS  |  ⏪🤦‍♂️ 0% Regret  |  🥊🦍 0 Mash  |  🏆💀 0% Peak",
            font=("Segoe UI", 8),
            fg="#64748b",
            bg="#0a0d14"
        )
        self.lbl_telemetry.pack(fill="x", padx=10, pady=(0, 6))

    def spawn_emoji_particle(self, rage):
        if rage < 30 and random.random() > 0.15:
            return
        emoji_char = random.choice(RAGE_BURST_EMOJIS)
        w = self.canvas_particles.winfo_width()
        if w < 10:
            w = 380
        x = random.randint(30, max(40, w - 30))
        y = 20
        item = self.canvas_particles.create_text(
            x, y, text=emoji_char, font=("Segoe UI Emoji", 12), fill="#ffffff"
        )
        vx = (random.random() - 0.5) * 2.5
        vy = -random.uniform(1.2, 2.8)
        self.particles.append({"id": item, "vx": vx, "vy": vy, "life": 16})

    def toggle_compact(self):
        self.is_compact = not self.is_compact
        if self.is_compact:
            self.lbl_milestones.pack_forget()
            self.canvas_particles.pack_forget()
            self.lbl_comment.pack_forget()
            self.lbl_telemetry.pack_forget()
            self.root.geometry(f"360x95+{self.pos_x}+{self.pos_y}")
            self.btn_compact.config(text="🗖")
        else:
            self.lbl_milestones.pack(fill="x", padx=12, pady=(0, 2))
            self.canvas_particles.pack(fill="x", padx=10, pady=0)
            self.lbl_comment.pack(fill="x", padx=10, pady=(2, 4))
            self.lbl_telemetry.pack(fill="x", padx=10, pady=(0, 6))
            self.root.geometry(f"410x245+{self.pos_x}+{self.pos_y}")
            self.btn_compact.config(text="🗕")

    def toggle_sound(self):
        self.audio.muted = not self.audio.muted
        self.btn_sound.config(text="🔇" if self.audio.muted else "🔊")

    def bind_drag_events(self):
        for widget in (self.title_bar, self.lbl_title, self.outer_frame):
            widget.bind("<ButtonPress-1>", self.on_drag_start)
            widget.bind("<B1-Motion>", self.on_drag_motion)

    def on_drag_start(self, event):
        self.drag_x = event.x_root - self.root.winfo_x()
        self.drag_y = event.y_root - self.root.winfo_y()

    def on_drag_motion(self, event):
        self.pos_x = event.x_root - self.drag_x
        self.pos_y = event.y_root - self.drag_y
        self.base_pos_x = self.pos_x
        self.base_pos_y = self.pos_y
        self.root.geometry(f"+{self.pos_x}+{self.pos_y}")

    def start_keyboard_listener(self):
        if not HAS_PYNPUT:
            return

        def on_press(key):
            try:
                k_str = key.char if hasattr(key, 'char') and key.char else str(key)
                self.scorer.record_press(k_str)
                # Spawn floating emoji particle on keystroke!
                self.spawn_emoji_particle(self.scorer.current_rage)
            except Exception:
                pass

        def on_release(key):
            try:
                k_str = key.char if hasattr(key, 'char') and key.char else str(key)
                self.scorer.record_release(k_str)
            except Exception:
                pass

        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
        listener.daemon = True
        listener.start()

    def update_loop(self):
        now = time.time()
        self.scorer.prune(now)
        self.scorer.calculate(now)

        rage = int(self.scorer.current_rage)
        tier_name, tier_color, mascot_emoji = self.scorer.get_tier_info()
        metrics = self.scorer.last_metrics

        # 1. Update text, Mascot Emoji & colors
        self.lbl_rage_num.config(text=f"{rage}%", fg=tier_color)
        self.lbl_tier_badge.config(text=tier_name, fg=tier_color)
        self.lbl_mascot.config(text=mascot_emoji)
        self.outer_frame.config(highlightbackground=tier_color)

        if not self.is_compact:
            self.lbl_comment.config(text=self.scorer.last_comment)
            self.lbl_telemetry.config(
                text=f"🏎️💨 {metrics['cps']} CPS  |  ⏪🤦‍♂️ {int(metrics['backspace_rate']*100)}% Regret  |  🥊🦍 {metrics['mash_index']} Mash  |  🏆💀 {int(self.scorer.peak_rage)}% Peak"
            )

        # 2. Update Progress Bar
        bar_w = self.canvas_bar.winfo_width()
        if bar_w > 1:
            fill_len = int((rage / 100.0) * bar_w)
            self.canvas_bar.coords(self.bar_fill, 0, 0, fill_len, 8)
            self.canvas_bar.itemconfig(self.bar_fill, fill=tier_color)

        # 3. Animate Floating Emoji Particles
        surviving_particles = []
        for p in self.particles:
            self.canvas_particles.move(p["id"], p["vx"], p["vy"])
            p["life"] -= 1
            if p["life"] > 0:
                surviving_particles.append(p)
            else:
                self.canvas_particles.delete(p["id"])
        self.particles = surviving_particles

        # Extra spontaneous burst at DEFCON 1!
        if rage >= 85 and random.random() < 0.25:
            self.spawn_emoji_particle(rage)

        # 4. Physical Screen Shake on Overlay
        if rage >= 85:
            dx = random.randint(-7, 7)
            dy = random.randint(-5, 5)
            self.root.geometry(f"+{self.base_pos_x + dx}+{self.base_pos_y + dy}")
        elif rage >= 63:
            dx = random.randint(-3, 3)
            dy = random.randint(-2, 2)
            self.root.geometry(f"+{self.base_pos_x + dx}+{self.base_pos_y + dy}")
        else:
            self.root.geometry(f"+{self.base_pos_x}+{self.base_pos_y}")

        # 5. EFFECTIVE 4-TIER SOUND SYSTEM:
        current_bracket = None
        bracket_label = ""
        bracket_color = "#10b981"

        if rage < 30:
            current_bracket = "calm"
            bracket_label = "🎵 CALM"
            bracket_color = "#10b981"
        elif rage < 50:
            current_bracket = "rage"
            bracket_label = "😤 RAGE"
            bracket_color = "#3b82f6"
        elif rage < 85:
            current_bracket = "racing"
            bracket_label = "🏎️ RACING"
            bracket_color = "#f59e0b"
        else:
            current_bracket = "danger"
            bracket_label = "🚨 DANGER"
            bracket_color = "#dc2626"

        self.lbl_sound_mode.config(text=bracket_label, fg=bracket_color)

        bracket_changed = (current_bracket != self.last_sound_bracket)
        time_since_sound = now - self.last_sound_time

        if bracket_changed and time_since_sound > 0.8:
            self.audio.play(current_bracket)
            self.last_sound_bracket = current_bracket
            self.last_sound_time = now
        elif current_bracket == "danger" and time_since_sound > 1.6 and metrics["cps"] > 3.0:
            self.audio.play("danger")
            self.last_sound_time = now
        elif current_bracket == "calm" and bracket_changed:
            self.audio.play("calm")
            self.last_sound_bracket = current_bracket
            self.last_sound_time = now

        self.root.after(40, self.update_loop)

    def quit_app(self):
        self.root.destroy()
        sys.exit(0)


def main():
    root = tk.Tk()
    app = RageOverlayHUD(root)
    root.mainloop()


if __name__ == "__main__":
    main()
