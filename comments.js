/**
 * Keyboard Rage Detector - Commentary Database
 * Packed with hilarious roasts, unhinged emojis, and situation-aware keyboard sympathy.
 */

const RAGE_TIERS = {
    ZEN: {
        name: "Zen Monk",
        min: 0,
        max: 18,
        color: "#10b981", // Emerald green
        badge: "🧘‍♂️ CHILLAXED BUDDHA",
        comments: [
            "Namaste bro 🧘‍♂️ You're typing like you're rubbing essential oils on the keys 🍵",
            "Zero hostility detected 🌱 Are you typing in a lavender field with flute music? 🪈",
            "Your keyboard feels safe, loved, and emotionally validated 💖⌨️",
            "Bro is typing in lowercase whisper mode... shhh don't wake the switches 🤫☁️",
            "Smooth, dignified, and serene. You definitely drink chamomile tea while reading docs 🍵✨",
            "Typing cadence as gentle as raindrops on a sleeping kitten's nose 🐾🌧️",
            "Are you floating right now? Because your keys barely felt that touch 🪶✨"
        ]
    },
    MILD: {
        name: "Mildly Irritated",
        min: 19,
        max: 38,
        color: "#3b82f6", // Blue/cyan
        badge: "☕ PASSIVE-AGGRESSIVE INTERN",
        comments: [
            "We detect a subtle brow furrow 👁️👄👁️ 'Per my previous email' incoming...",
            "A tiny vein just popped on your forehead 🤏😡 Take a sip of water, bestie 🧃",
            "Typing briskly. Did someone reply-all with 'Please remove me from this thread'?! 💀✉️",
            "You just aggressively clicked your mouse wheel didn't you? 🐁👀",
            "Slight finger tension detected. Someone scheduled an 8:30 AM status sync 📅🤡",
            "Polite corporate smile on the outside, eye-twitch on the inside 🙃💼",
            "Typing speed increased by 40%. The salt is starting to crystallize 🧂👀"
        ]
    },
    SIMMERING: {
        name: "Simmering Frustration",
        min: 39,
        max: 62,
        color: "#f59e0b", // Amber/orange
        badge: "🧂 CHIEF SALT OFFICER",
        comments: [
            "Warning: That backspace key didn't steal your lunch money, chill! 💀🥪",
            "Are you coding or playing Street Fighter combos on the home row?! 🕹️🥋",
            "Bro is cooking minute rice in 54 seconds with that finger friction! 🍚🔥",
            "You just sighed audibly through your nose like a disappointed dragon 🐉💨",
            "Your spacebar is whispering 'Please have mercy on me' 🥺⌨️",
            "One more missing semicolon and someone is getting thrown out the window 🪟🏃‍♂️",
            "The keys are heating up! Someone get this person an iced boba tea stat! 🧋🧊"
        ]
    },
    RAGING: {
        name: "High Voltage Rage",
        min: 63,
        max: 84,
        color: "#ef4444", // Crimson red
        badge: "🦍 ANGRY GORILLA MODE",
        comments: [
            "WOAH! Keycaps are holding on for dear life! Ease off the throttle! 🪂💥",
            "Your spacebar just filed an emergency restraining order with HR 📜🚨",
            "You're typing like the keyboard owes you 50 bucks and child support! 💸🥊",
            "Neighbors think you're jackhammering the floorboards! 🏗️🔊",
            "Cherry MX switches are screaming in lowercase 'help us' 😭🍒",
            "Bro is attacking the plastic like it personally insulted his grandmother 👵🪓",
            "High impact detected! Plastic fatigue is imminent! Put the hammer down! 🔨🚨"
        ]
    },
    DEFCON1: {
        name: "DEFCON 1: OBLITERATION",
        min: 85,
        max: 100,
        color: "#dc2626", // Flashing Red/Neon Violet
        badge: "💀 KEYBOARD EXTINCTION EVENT",
        comments: [
            "🚨 CODE RED! THE DESK IS SHAKING, THE CAT IS HIDING, CALL 911! 🐈💨🚑",
            "NUCLEAR MELTDOWN DETECTED! BRO IS TYPING WITH SLEDGEHAMMERS! 🌋🔨",
            "ARE YOU TYPING WITH A FOREHEAD ROLL?! STEP AWAY FROM THE PLASTIC! 🤦‍♂️💥",
            "MAXIMUM UNHINGED ANNIHILATION! RIP MECHANICAL SWITCHES 🪦👻",
            "KEYBOARD REPLACEMENT: $150. ANGER MANAGEMENT: STRONGLY RECOMMENDED 🛋️🧠",
            "EMERGENCY: YOUR KEYCAPS JUST FILED FOR WORKERS' COMP! 📋🤕",
            "CATACLYSMIC IMPACT! HIDE THE MONITORS BEFORE THEY GET THROWN OUT THE WINDOW! 🖥️🪟💥"
        ]
    }
};

// Specialized situational callouts
const SPECIAL_COMMENTS = {
    backspaceFury: [
        "BACKSPACE SPEEDRUN ANY% NO GLITCHES! 🏃‍♂️💨 Rewinding life choices!",
        "Bro just erased an entire novel in 0.3 seconds! Regret level: OVER 9000 💀⏪",
        "The delete key is begging for ice water and an ambulance! 🚑🧯",
        "Hitting backspace like it's a drum pedal at an Iron Maiden concert 🥁🔥"
    ],
    capsRage: [
        "LOUD NOISES! 🗣️📢 WHY ARE WE SCREAMING AT THE CLOUDS?! 🦖⚡",
        "CAPS LOCK DOESN'T MAKE YOUR CODE RUN, IT JUST MAKES IT TERRIFYING! 👹🔥",
        "ALL CAPS DETECTED! We can hear your scream through the fiber optic cables! 📡😱",
        "CRUISE CONTROL FOR RAGE ENGAGED! FULL SPEED INTO THE VOLCANO! 🌋🏎️💨"
    ],
    keyMash: [
        "DID A GOBLIN SMASH ITS HEAD ON YOUR HOME ROW?! 👺💥⌨️",
        "A wild keyboard smash appeared! 'asdfghjk' is not a valid emotional dialect, bro! 🐾🤯",
        "Total unbridled mash! You literally just donkey-kong punched your desk! 🦍🍌",
        "Did a cat walk across your keyboard or did CSS flexbox break your spirit?! 🐈💥"
    ],
    heavyDwell: [
        "Heavy finger press detected! Are you trying to push that key to China?! 🌏⛏️",
        "Dwell time off the charts! Stop grinding the keycaps into fine seasoning! 🧂💥"
    ]
};

/**
 * Selects an appropriate comment based on rage level and telemetry metrics.
 */
function getRageFeedback(rage, metrics = {}) {
    if (rage > 35) {
        if (metrics.capsRatio > 0.65 && Math.random() < 0.5) {
            const list = SPECIAL_COMMENTS.capsRage;
            return buildFeedback(rage, list[Math.floor(Math.random() * list.length)]);
        }
        if (metrics.backspaceRate > 0.4 && Math.random() < 0.55) {
            const list = SPECIAL_COMMENTS.backspaceFury;
            return buildFeedback(rage, list[Math.floor(Math.random() * list.length)]);
        }
        if (metrics.mashIndex > 5 && Math.random() < 0.6) {
            const list = SPECIAL_COMMENTS.keyMash;
            return buildFeedback(rage, list[Math.floor(Math.random() * list.length)]);
        }
    }

    let tier = RAGE_TIERS.ZEN;
    if (rage >= RAGE_TIERS.DEFCON1.min) tier = RAGE_TIERS.DEFCON1;
    else if (rage >= RAGE_TIERS.RAGING.min) tier = RAGE_TIERS.RAGING;
    else if (rage >= RAGE_TIERS.SIMMERING.min) tier = RAGE_TIERS.SIMMERING;
    else if (rage >= RAGE_TIERS.MILD.min) tier = RAGE_TIERS.MILD;

    const comments = tier.comments;
    const comment = comments[Math.floor(Math.random() * comments.length)];
    return {
        tier: tier.name,
        badge: tier.badge,
        color: tier.color,
        comment: comment
    };
}

function buildFeedback(rage, comment) {
    let tier = RAGE_TIERS.ZEN;
    if (rage >= RAGE_TIERS.DEFCON1.min) tier = RAGE_TIERS.DEFCON1;
    else if (rage >= RAGE_TIERS.RAGING.min) tier = RAGE_TIERS.RAGING;
    else if (rage >= RAGE_TIERS.SIMMERING.min) tier = RAGE_TIERS.SIMMERING;
    else if (rage >= RAGE_TIERS.MILD.min) tier = RAGE_TIERS.MILD;

    return {
        tier: tier.name,
        badge: tier.badge,
        color: tier.color,
        comment: comment
    };
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = { RAGE_TIERS, SPECIAL_COMMENTS, getRageFeedback };
}
