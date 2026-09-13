#!/usr/bin/env python3
"""
Keyboard Rage Detector - Terminal Edition
Measures typing aggression and calculates a real-time Rage Score with humorous commentary.
Zero external dependencies required (uses standard library and Windows msvcrt).
"""

import time
import sys
import os
import random
from collections import deque

# Ensure utf-8 encoding for Windows console output
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# Check for Windows msvcrt
try:
    import msvcrt
    HAS_MSVCRT = True
except ImportError:
    HAS_MSVCRT = False

# Enable ANSI escape sequences on Windows
if os.name == 'nt':
    os.system('')

# Tier definitions with hilarious titles and emoji roasts
TIERS = [
    (18, "🧘‍♂️ CHILLAXED BUDDHA", "\033[92m", [  # Green
        "Namaste bro 🧘‍♂️ You're typing like you're rubbing essential oils on the keys 🍵",
        "Zero hostility detected 🌱 Are you typing in a lavender field with flute music? 🪈",
        "Your keyboard feels safe, loved, and emotionally validated 💖⌨️",
        "Bro is typing in lowercase whisper mode... shhh don't wake the switches 🤫☁️"
    ]),
    (38, "☕ PASSIVE-AGGRESSIVE INTERN", "\033[96m", [  # Cyan
        "We detect a subtle brow furrow 👁️👄👁️ 'Per my previous email' incoming...",
        "A tiny vein just popped on your forehead 🤏😡 Take a sip of water, bestie 🧃",
        "You just aggressively clicked your mouse wheel didn't you? 🐁👀",
        "Slight finger tension detected. Someone scheduled an 8:30 AM status sync 📅🤡"
    ]),
    (62, "🧂 CHIEF SALT OFFICER", "\033[93m", [  # Yellow
        "Warning: That backspace key didn't steal your lunch money, chill! 💀🥪",
        "Are you coding or playing Street Fighter combos on the home row?! 🕹️🥋",
        "Bro is cooking minute rice in 54 seconds with that finger friction! 🍚🔥",
        "You just sighed audibly through your nose like a disappointed dragon 🐉💨"
    ]),
    (84, "🦍 ANGRY GORILLA MODE", "\033[91m", [  # Red
        "WOAH! Keycaps are holding on for dear life! Ease off the throttle! 🪂💥",
        "Your spacebar just filed an emergency restraining order with HR 📜🚨",
        "You're typing like the keyboard owes you 50 bucks and lunch! 💸🥊",
        "Cherry MX switches are screaming in lowercase 'help us' 😭🍒"
    ]),
    (100, "💀 KEYBOARD EXTINCTION EVENT", "\033[95m\033[1m", [  # Bold Magenta / Red
        "🚨 CODE RED! THE DESK IS SHAKING, THE CAT IS HIDING, CALL 911! 🐈💨🚑",
        "NUCLEAR MELTDOWN DETECTED! BRO IS TYPING WITH SLEDGEHAMMERS! 🌋🔨",
        "ARE YOU TYPING WITH A FOREHEAD ROLL?! STEP AWAY FROM THE PLASTIC! 🤦‍♂️💥",
        "KEYBOARD REPLACEMENT: $150. ANGER MANAGEMENT: STRONGLY RECOMMENDED 🛋️🧠"
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
        "ALL CAPS DETECTED! We can hear your scream through the fiber optic cables! 📡😱"
    ],
    "mash": [
        "DID A GOBLIN SMASH ITS HEAD ON YOUR HOME ROW?! 👺💥⌨️",
        "A wild keyboard smash appeared! 'asdfghjk' is not a real word, bro! 🐾🤯",
        "Total unbridled mash! You literally just donkey-kong punched your desk! 🦍🍌"
    ]
}

class RageDetector:
    def __init__(self, window_sec=3.0, sensitivity=1.0):
        self.window_sec = window_sec
        self.sensitivity = sensitivity
        self.events = deque()  # stores (timestamp, char, is_backspace, is_caps)
        self.current_rage = 0.0
        self.peak_rage = 0.0
        self.total_keystrokes = 0
        self.last_comment = "Start typing to detect your rage level..."
        self.last_comment_time = 0

    def add_key(self, char):
        now = time.time()
        is_backspace = (char in ('\x08', '\x7f', 'backspace'))
        is_caps = False
        if isinstance(char, str) and len(char) == 1 and not is_backspace:
            is_caps = char.isupper() or char in '!@#$%^&*()_+{}|:"<>?'

        self.events.append((now, char, is_backspace, is_caps))
        self.total_keystrokes += 1
        self.prune(now)
        self.calculate_rage(now)

    def prune(self, now):
        cutoff = now - self.window_sec
        while self.events and self.events[0][0] < cutoff:
            self.events.popleft()

    def calculate_rage(self, now):
        count = len(self.events)
        if count == 0:
            self.current_rage = max(0.0, self.current_rage - 3.0)
            return

        # 1. Velocity (Keys per second)
        span = max(0.4, now - self.events[0][0])
        cps = count / span

        # 2. Backspace ratio
        backspaces = sum(1 for e in self.events if e[2])
        backspace_ratio = backspaces / count

        # 3. Caps / Exclamation ratio
        caps_count = sum(1 for e in self.events if e[3])
        caps_ratio = caps_count / count

        # 4. Mash count
        mash_score = 0
        ev_list = list(self.events)
        for i in range(1, len(ev_list)):
            prev_t, prev_c, _, _ = ev_list[i - 1]
            curr_t, curr_c, _, _ = ev_list[i]
            dt = curr_t - prev_t
            if prev_c == curr_c and dt < 0.12:
                mash_score += 3
            elif dt < 0.05:
                mash_score += 2

        # Subscores
        v_score = min(35.0, max(0.0, (cps - 3.0) * 4.5)) if cps > 3.0 else 0
        b_score = min(30.0, backspace_ratio * 40.0)
        m_score = min(30.0, mash_score * 3.5)
        c_score = min(20.0, caps_ratio * 25.0)

        raw = (v_score + b_score + m_score + c_score) * self.sensitivity
        target = max(0.0, min(100.0, raw))

        # Smooth interpolation
        alpha = 0.5 if target > self.current_rage else 0.15
        self.current_rage += (target - self.current_rage) * alpha

        if self.current_rage > self.peak_rage:
            self.peak_rage = self.current_rage

        # Update comments if tier changes or every 2.0s
        current_tier_name, _ = self.get_tier_info()
        tier_changed = getattr(self, '_last_tier_name', None) != current_tier_name
        self._last_tier_name = current_tier_name

        if tier_changed or (now - self.last_comment_time > 2.0) or abs(target - self.current_rage) > 20:
            self.last_comment = self.pick_comment(backspace_ratio, caps_ratio, mash_score)
            self.last_comment_time = now

    def pick_comment(self, b_ratio, c_ratio, mash):
        rage = self.current_rage
        if rage > 40:
            if c_ratio > 0.6:
                return random.choice(SPECIAL_COMMENTS["caps"])
            if b_ratio > 0.4:
                return random.choice(SPECIAL_COMMENTS["backspace"])
            if mash > 5:
                return random.choice(SPECIAL_COMMENTS["mash"])

        for limit, name, color, comments in TIERS:
            if rage <= limit:
                return random.choice(comments)
        return TIERS[-1][3][0]

    def get_tier_info(self):
        for limit, name, color, comments in TIERS:
            if self.current_rage <= limit:
                return name, color
        return TIERS[-1][1], TIERS[-1][2]

    def render_bar(self, width=28):
        filled = int((self.current_rage / 100.0) * width)
        empty = width - filled
        name, color = self.get_tier_info()
        reset = "\033[0m"
        fill_char = '#'
        empty_char = '-'
        try:
            # Try smooth block characters
            fill_char = '█'
            empty_char = '░'
            test_encode = fill_char.encode(sys.stdout.encoding or 'utf-8')
        except Exception:
            fill_char = '#'
            empty_char = '-'
        bar = f"{color}[{fill_char * filled}{empty_char * empty}]{reset}"
        return f"{bar} {color}{int(self.current_rage):3d}% - {name}{reset}"

def run_cli():
    detector = RageDetector()
    print("\033[2J\033[H", end="") # Clear screen
    print("=" * 65)
    print("   ⚡ KEYBOARD RAGE DETECTOR (Terminal Edition)")
    print("   Type freely below. Press Ctrl+C or ESC to exit.")
    print("=" * 65)

    if not HAS_MSVCRT:
        print("\nNote: Standard interactive mode requires Windows msvcrt.")
        print("Running in simulated typing demonstration mode...\n")
        demo_sequences = [
            ("Zen writing: Hello, world. How are you today? Everything is calm.", 0.12),
            ("Mild frustration: As per my last email, please fix this.", 0.07),
            ("Salty mash: AAAAAAA WHY IS THIS NOT WORKING?!?!?!", 0.04),
            ("Extinction rage: WHAT ARE YOU DOING??????!!!!!!!!!!!", 0.02),
            ("\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08\x08", 0.03),
            ("Cooling down slowly... taking deep breaths...", 0.15)
        ]
        for phrase, delay in demo_sequences:
            for ch in phrase:
                detector.add_key(ch)
                now = time.time()
                detector.calculate_rage(now)
                bar = detector.render_bar()
                sys.stdout.write(f"\r{bar} | Peak: {int(detector.peak_rage)}%\nComment: {detector.last_comment}\033[F")
                sys.stdout.flush()
                time.sleep(delay)
        print("\n\nDemo finished.")
        return

    # Interactive Windows terminal loop
    typed_buffer = []
    last_draw = 0

    try:
        while True:
            now = time.time()

            # Check if key was pressed
            if msvcrt.kbhit():
                ch = msvcrt.getwch()
                if ch == '\x1b':  # ESC key
                    break
                detector.add_key(ch)
                if ch == '\x08':  # Backspace
                    if typed_buffer:
                        typed_buffer.pop()
                elif ch == '\r':
                    typed_buffer.clear()
                elif len(ch) == 1 and ch.isprintable():
                    typed_buffer.append(ch)
                    if len(typed_buffer) > 40:
                        typed_buffer.pop(0)

            # Natural rage decay calculation
            detector.prune(now)
            detector.calculate_rage(now)

            # Redraw UI at ~20 FPS
            if now - last_draw > 0.05:
                bar = detector.render_bar()
                buffer_str = "".join(typed_buffer)
                
                # ANSI formatting
                sys.stdout.write("\033[H") # Move to top home
                print("=" * 65)
                print("   ⚡ KEYBOARD RAGE DETECTOR (Terminal Edition)")
                print("   Type freely below. Press ESC to quit.")
                print("=" * 65)
                print(f" Meter : {bar}")
                print(f" Peak  : {int(detector.peak_rage)}%  |  Keystrokes: {detector.total_keystrokes}")
                print(f" Mood  : \"{detector.last_comment}\"\033[K")
                print("-" * 65)
                print(f" Input : {buffer_str}\033[K")
                print("=" * 65)
                sys.stdout.flush()
                last_draw = now

            time.sleep(0.015)

    except KeyboardInterrupt:
        pass

    print("\n\nSession finished.")
    print(f"Total Keystrokes: {detector.total_keystrokes}")
    print(f"Highest Rage Achieved: {int(detector.peak_rage)}%")

if __name__ == "__main__":
    run_cli()
