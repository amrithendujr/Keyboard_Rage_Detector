/**
 * Keyboard Rage Detector - Algorithmic Scoring Engine
 * Analyzes real-time typing dynamics to measure frustration, mash, speed, and hostility.
 */

class RageEngine {
    constructor(options = {}) {
        this.sensitivity = options.sensitivity || 1.0;
        this.windowMs = options.windowMs || 3000; // 3-second rolling window
        this.keyEvents = [];
        this.keyDownTimes = new Map();

        this.currentRage = 0;
        this.targetRage = 0;
        this.peakRage = 0;
        this.totalKeystrokes = 0;
        this.rageKeystrokes = 0;

        this.activeComment = "Start typing below to analyze your keyboard aggression...";
        this.activeBadge = "🌿 ZEN";
        this.activeColor = "#10b981";
        this.lastCommentUpdate = 0;

        this.listeners = [];
        this.animationFrameId = null;
        this.decayInterval = null;

        this.lastMetrics = {
            cps: 0,
            wpm: 0,
            backspaceRate: 0,
            capsRatio: 0,
            mashIndex: 0,
            avgDwellMs: 80,
            totalKeys: 0
        };

        this.startLoop();
    }

    setSensitivity(val) {
        this.sensitivity = Math.max(0.2, Math.min(2.5, val));
    }

    onUpdate(fn) {
        this.listeners.push(fn);
    }

    handleKeyDown(event) {
        const now = performance.now();
        const key = event.key;
        const code = event.code;

        // Record keydown timestamp for dwell time
        if (!this.keyDownTimes.has(code)) {
            this.keyDownTimes.set(code, now);
        }

        const isBackspace = (key === 'Backspace' || key === 'Delete');
        const isCaps = !isBackspace && key.length === 1 && key.toUpperCase() === key && key.toLowerCase() !== key;
        const isAngryPunctuation = ['!', '?', '#', '$', '%', '@', '^', '&', '*'].includes(key);

        this.keyEvents.push({
            time: now,
            key: key,
            code: code,
            isBackspace: isBackspace,
            isCaps: isCaps || isAngryPunctuation,
            dwell: 80 // Default estimate until keyup
        });

        this.totalKeystrokes++;
        this.pruneOldEvents(now);
        this.evaluateRage(now);
    }

    handleKeyUp(event) {
        const now = performance.now();
        const code = event.code;

        if (this.keyDownTimes.has(code)) {
            const downTime = this.keyDownTimes.get(code);
            const dwell = now - downTime;
            this.keyDownTimes.delete(code);

            // Update matching recent event dwell time
            for (let i = this.keyEvents.length - 1; i >= 0; i--) {
                if (this.keyEvents[i].code === code) {
                    this.keyEvents[i].dwell = dwell;
                    break;
                }
            }
        }
    }

    pruneOldEvents(now) {
        const cutoff = now - this.windowMs;
        while (this.keyEvents.length > 0 && this.keyEvents[0].time < cutoff) {
            this.keyEvents.shift();
        }
    }

    evaluateRage(now) {
        const count = this.keyEvents.length;
        if (count === 0) {
            this.targetRage = 0;
            return;
        }

        // 1. Keystroke Frequency (CPS - Keys Per Second)
        const windowDurationSec = Math.max(0.5, (now - this.keyEvents[0].time) / 1000);
        const cps = count / windowDurationSec;
        const wpm = Math.round((cps * 60) / 5);

        // 2. Backspace & Delete Hostility
        const backspaces = this.keyEvents.filter(e => e.isBackspace).length;
        const backspaceRate = backspaces / count;

        // Count consecutive backspaces
        let maxConsecutiveBackspaces = 0;
        let currConsecutive = 0;
        for (const e of this.keyEvents) {
            if (e.isBackspace) {
                currConsecutive++;
                if (currConsecutive > maxConsecutiveBackspaces) {
                    maxConsecutiveBackspaces = currConsecutive;
                }
            } else {
                currConsecutive = 0;
            }
        }

        // 3. Caps Lock & Screaming Punctuation
        const capsCount = this.keyEvents.filter(e => e.isCaps).length;
        const capsRatio = capsCount / count;

        // 4. Repeated Mash Index (e.g. "aaaaa", "asdfasdf", "jjjjj")
        let mashCounter = 0;
        for (let i = 1; i < this.keyEvents.length; i++) {
            const prev = this.keyEvents[i - 1];
            const curr = this.keyEvents[i];
            // Identical key repeated in rapid succession (<120ms)
            if (prev.key === curr.key && (curr.time - prev.time) < 140) {
                mashCounter += 2;
            }
            // Rapid keystroke burst (<60ms) indicating hand/fist smash
            if ((curr.time - prev.time) < 55) {
                mashCounter += 1.5;
            }
        }

        // 5. Average Key Dwell Time (Hard smashing tends to sustain longer contact)
        const totalDwell = this.keyEvents.reduce((acc, e) => acc + (e.dwell || 80), 0);
        const avgDwellMs = totalDwell / count;

        // --- RAGE SCORING MODEL ---
        // Velocity: 0-35 points (starts ramping over 4 CPS, peaks around 12 CPS)
        let velocityScore = 0;
        if (cps > 3.5) {
            velocityScore = Math.min(38, Math.pow((cps - 3.5) / 8, 1.3) * 38);
        }

        // Backspace Fury: 0-30 points
        let backspaceScore = 0;
        if (backspaceRate > 0.15) {
            backspaceScore = Math.min(30, (backspaceRate * 25) + (maxConsecutiveBackspaces * 3));
        }

        // Mash Factor: 0-30 points
        let mashScore = Math.min(32, mashCounter * 3.2);

        // Caps & Screaming: 0-20 points
        let capsScore = 0;
        if (capsRatio > 0.25) {
            capsScore = Math.min(22, capsRatio * 25);
        }

        // Dwell / Heavy Impact Factor: 0-15 points
        let dwellScore = 0;
        if (avgDwellMs > 160) {
            dwellScore = Math.min(15, ((avgDwellMs - 160) / 120) * 15);
        }

        // Combine subscores and apply user sensitivity
        let totalCalculated = (velocityScore + backspaceScore + mashScore + capsScore + dwellScore) * this.sensitivity;

        // Hard clamp between 0 and 100
        this.targetRage = Math.max(0, Math.min(100, Math.round(totalCalculated)));

        if (this.targetRage > this.peakRage) {
            this.peakRage = this.targetRage;
        }

        this.lastMetrics = {
            cps: parseFloat(cps.toFixed(1)),
            wpm: wpm,
            backspaceRate: parseFloat(backspaceRate.toFixed(2)),
            capsRatio: parseFloat(capsRatio.toFixed(2)),
            mashIndex: Math.round(mashCounter),
            avgDwellMs: Math.round(avgDwellMs),
            totalKeys: this.totalKeystrokes
        };
    }

    startLoop() {
        let lastTick = performance.now();

        const tick = (now) => {
            const dt = (now - lastTick) / 1000;
            lastTick = now;

            // Prune events continuously
            this.pruneOldEvents(now);
            if (this.keyEvents.length === 0) {
                // If idle, rapidly cool down target rage
                this.targetRage = Math.max(0, this.targetRage - (35 * dt));
            } else {
                this.evaluateRage(now);
            }

            // Smoothly interpolate currentRage toward targetRage (spring/lerp)
            const speed = this.targetRage > this.currentRage ? 8 : 3.5; // Fast attack, smooth decay
            this.currentRage += (this.targetRage - this.currentRage) * Math.min(1, speed * dt);

            const displayRage = Math.round(this.currentRage);

            // Update comments if tier changes or every 2.5 seconds when active
            if (now - this.lastCommentUpdate > 2500 || Math.abs(this.currentRage - this.targetRage) > 20) {
                if (typeof getRageFeedback === 'function') {
                    const feedback = getRageFeedback(displayRage, this.lastMetrics);
                    this.activeComment = feedback.comment;
                    this.activeBadge = feedback.badge;
                    this.activeColor = feedback.color;
                    if (window.rageAudio) {
                        window.rageAudio.updateRageState(displayRage);
                    }
                }
                this.lastCommentUpdate = now;
            }

            // Notify UI listeners
            const payload = {
                rage: displayRage,
                targetRage: this.targetRage,
                peakRage: this.peakRage,
                badge: this.activeBadge,
                color: this.activeColor,
                comment: this.activeComment,
                metrics: this.lastMetrics
            };

            for (const fn of this.listeners) {
                fn(payload);
            }

            this.animationFrameId = requestAnimationFrame(tick);
        };

        this.animationFrameId = requestAnimationFrame(tick);
    }

    reset() {
        this.keyEvents = [];
        this.keyDownTimes.clear();
        this.currentRage = 0;
        this.targetRage = 0;
        this.peakRage = 0;
        this.totalKeystrokes = 0;
        this.activeComment = "Start typing below to analyze your keyboard aggression...";
        this.activeBadge = "🌿 ZEN";
        this.activeColor = "#10b981";
    }
}

// Global instance
window.rageEngine = new RageEngine();
