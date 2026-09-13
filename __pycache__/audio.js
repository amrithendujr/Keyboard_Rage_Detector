/**
 * Keyboard Rage Detector - Web Audio API Sound Generator
 * Generates dynamic, zero-external-asset sound effects reacting to typing hostility.
 */

class RageAudioEngine {
    constructor() {
        this.ctx = null;
        this.isMuted = false;
        this.alarmInterval = null;
        this.lastRageTier = 'ZEN';
    }

    init() {
        if (!this.ctx) {
            const AudioContext = window.AudioContext || window.webkitAudioContext;
            this.ctx = new AudioContext();
        }
        if (this.ctx && this.ctx.state === 'suspended') {
            this.ctx.resume();
        }
    }

    setMuted(muted) {
        this.isMuted = muted;
        if (muted && this.alarmInterval) {
            clearInterval(this.alarmInterval);
            this.alarmInterval = null;
        }
    }

    playKeyClick(rageLevel) {
        if (this.isMuted) return;
        this.init();

        try {
            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            // Rage scales pitch and aggression
            const baseFreq = 300 + (rageLevel * 8); // 300Hz up to ~1100Hz
            osc.type = rageLevel > 60 ? 'sawtooth' : 'triangle';
            osc.frequency.setValueAtTime(baseFreq, now);
            osc.frequency.exponentialRampToValueAtTime(50, now + 0.04);

            const vol = Math.min(0.25, 0.05 + (rageLevel / 100) * 0.2);
            gain.gain.setValueAtTime(vol, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.04);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now);
            osc.stop(now + 0.05);
        } catch (e) {
            // Audio context safely ignored if browser blocks autoplay
        }
    }

    playAlarm() {
        if (this.isMuted) return;
        this.init();

        try {
            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();

            osc.type = 'sawtooth';
            // Two-tone warble
            osc.frequency.setValueAtTime(880, now);
            osc.frequency.setValueAtTime(440, now + 0.1);
            osc.frequency.setValueAtTime(880, now + 0.2);

            gain.gain.setValueAtTime(0.2, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.28);

            osc.connect(gain);
            gain.connect(this.ctx.destination);

            osc.start(now);
            osc.stop(now + 0.3);
        } catch (e) {}
    }

    playCalmSound() {
        if (this.isMuted) return;
        this.init();
        try {
            const now = this.ctx.currentTime;
            const freqs = [523.25, 659.25, 783.99]; // C5, E5, G5 soothing chime
            freqs.forEach((freq, idx) => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now + idx * 0.08);
                gain.gain.setValueAtTime(0.08, now + idx * 0.08);
                gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.9 + idx * 0.08);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start(now + idx * 0.08);
                osc.stop(now + 1.0 + idx * 0.08);
            });
        } catch (e) {}
    }

    playBeepSound() {
        if (this.isMuted) return;
        this.init();
        try {
            const now = this.ctx.currentTime;
            // Crisp double-pip notification beep
            [720, 920].forEach((freq, idx) => {
                const osc = this.ctx.createOscillator();
                const gain = this.ctx.createGain();
                osc.type = 'sine';
                osc.frequency.setValueAtTime(freq, now + idx * 0.11);
                gain.gain.setValueAtTime(0.12, now + idx * 0.11);
                gain.gain.exponentialRampToValueAtTime(0.001, now + 0.08 + idx * 0.11);
                osc.connect(gain);
                gain.connect(this.ctx.destination);
                osc.start(now + idx * 0.11);
                osc.stop(now + 0.09 + idx * 0.11);
            });
        } catch (e) {}
    }

    playRageSound() {
        if (this.isMuted) return;
        this.init();
        try {
            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sawtooth';
            osc.frequency.setValueAtTime(280, now);
            osc.frequency.linearRampToValueAtTime(360, now + 0.18);
            gain.gain.setValueAtTime(0.18, now);
            gain.gain.exponentialRampToValueAtTime(0.001, now + 0.32);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + 0.33);
        } catch (e) {}
    }

    playDangerSound() {
        if (this.isMuted) return;
        this.init();
        try {
            const now = this.ctx.currentTime;
            const osc = this.ctx.createOscillator();
            const gain = this.ctx.createGain();
            osc.type = 'sawtooth';
            // Emergency 2-tone klaxon warble
            osc.frequency.setValueAtTime(980, now);
            osc.frequency.setValueAtTime(640, now + 0.12);
            osc.frequency.setValueAtTime(980, now + 0.24);
            osc.frequency.setValueAtTime(640, now + 0.36);
            gain.gain.setValueAtTime(0.25, now);
            gain.gain.exponentialRampToValueAtTime(0.01, now + 0.52);
            osc.connect(gain);
            gain.connect(this.ctx.destination);
            osc.start(now);
            osc.stop(now + 0.53);
        } catch (e) {}
    }

    updateRageState(rage) {
        let currentBracket = null;
        if (rage < 30) currentBracket = "calm";
        else if (rage < 50) currentBracket = "beep";
        else if (rage < 85) currentBracket = "rage";
        else currentBracket = "danger";

        if (currentBracket !== this.lastSoundBracket) {
            if (currentBracket === "calm") this.playCalmSound();
            else if (currentBracket === "beep") this.playBeepSound();
            else if (currentBracket === "rage") this.playRageSound();
            else if (currentBracket === "danger") this.playDangerSound();
            this.lastSoundBracket = currentBracket;
        }
    }
}

// Global instance
window.rageAudio = new RageAudioEngine();
