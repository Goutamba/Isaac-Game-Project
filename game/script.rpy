# =========================================================
# CORE CONFIG
# =========================================================

define config.rollback_enabled = False
define config.window_auto_hide = ["scene", "show", "hide"]

# Placeholders so the game doesn't crash if images are missing
image bg room = "#2c2c2c" # Dark grey background
image eileen neutral = Placeholder("girl")
image eileen sad = Placeholder("girl")
image eileen happy = Placeholder("girl")
image eileen angry = Placeholder("girl")

# =========================================================
# CHARACTERS
# =========================================================

define i = Character("Isaac", what_color="#e6e6e6")
define f = Character("Fiona", what_color="#c8ffd4")
define j = Character("Jack", what_color="#ff4b4b", what_italic=True)
define n = Character(None)

# =========================================================
# PSYCHOLOGICAL VARIABLES
# =========================================================

default hope = 35
default pressure = 45
default dissociation = 10
default seen = 0
default jack_control = 0
default memory_fragments = []

# =========================================================
# TEXT EFFECTS
# =========================================================

transform tremble:
    linear 0.05 xoffset -4
    linear 0.05 xoffset 4
    repeat

# =========================================================
# GAME START
# =========================================================

label start:
    scene black
    window hide

    centered "HE WILL LAUGH"
    pause 2.0

    centered "A story about existing when you feel optional."
    pause 2.0

    jump content_warning

# =========================================================
# CONTENT WARNING
# =========================================================

label content_warning:
    window show
    n "This story explores emotional distress, intrusive thoughts, and despair."
    n "Nothing here glorifies self-harm."
    n "You are allowed to stop."

    menu:
        "Continue":
            pass
        "Leave":
            return

    jump chapter_zero

# =========================================================
# CHAPTER 0 — BEFORE
# =========================================================

label chapter_zero:
    scene bg room
    show eileen neutral at center

    i "Some people are born loud."
    i "I was born useful."

    $ pressure += 5

    menu:
        "Get up":
            $ hope += 5
        "Wait":
            $ dissociation += 5

    jump chapter_one

# =========================================================
# CHAPTER 1 — EXPECTATION
# =========================================================

label chapter_one:
    show eileen sad

    n "Expectation doesn’t scream."
    n "It whispers until you obey."

    i "If I fail, they’ll be disappointed."
    i "If I succeed… they’ll want more."

    if pressure > 50:
        j "You already know you’ll never be enough."
        $ jack_control += 1

    menu:
        "Talk to Fiona":
            jump fiona_path
        "Say nothing":
            jump silence_path

# =========================================================
# FIONA PATH
# =========================================================

label fiona_path:
    show eileen happy

    f "You look like you’re carrying something heavy."

    menu:
        "Tell her":
            $ seen += 2
            $ hope += 10
        "Deflect":
            $ dissociation += 5

    n "Being seen is not always comforting."
    n "Sometimes it feels dangerous."

    jump memory_unlock

# =========================================================
# SILENCE PATH
# =========================================================

label silence_path:
    show eileen angry

    j "Good choice."
    j "Silence keeps you safe."

    $ jack_control += 2
    $ pressure += 10

    jump memory_unlock

# =========================================================
# MEMORY FRAGMENT SYSTEM
# =========================================================

label memory_unlock:
    if "childhood" not in memory_fragments:
        $ memory_fragments.append("childhood")
        n "A memory surfaced."

    jump mid_state_check

# =========================================================
# MID STATE CHECK
# =========================================================

label mid_state_check:
    if jack_control >= 3:
        jump jack_route
    elif seen >= 3:
        jump witness_route
    else:
        jump hollow_route

# =========================================================
# HOLLOW ROUTE
# =========================================================

label hollow_route:
    show eileen neutral
    i "If I feel nothing… I can survive anything."
    $ dissociation += 15
    jump collapse_check

# =========================================================
# JACK ROUTE
# =========================================================

label jack_route:
    scene black
    window hide
    j "Let me think for you."
    j "You’re tired."
    $ jack_control += 2
    $ pressure += 15
    pause 1.5
    jump collapse_check

# =========================================================
# WITNESS ROUTE
# =========================================================

label witness_route:
    show eileen happy
    f "You don’t disappear when I look at you."
    i "That terrified me."
    $ hope += 25
    $ seen += 2
    jump collapse_check

# =========================================================
# COLLAPSE CHECK
# =========================================================

label collapse_check:
    if dissociation >= 20:
        jump dissociation_event
    else:
        jump ending_gate

# =========================================================
# DISSOCIATION EVENT (UI BREAK)
# =========================================================

label dissociation_event:
    window hide
    show eileen neutral at tremble
    centered "{size=+10}Why do you feel distant?{/size}"
    pause 2.0
    $ dissociation += 5
    jump ending_gate

# =========================================================
# ENDING GATE
# =========================================================

label ending_gate:
    if hope >= 70 and seen >= 4:
        jump true_ending
    elif jack_control >= 4:
        jump jack_ending
    else:
        jump hollow_ending

# =========================================================
# ENDINGS
# =========================================================

label true_ending:
    scene black
    window hide
    centered "Seven minutes."
    pause 1.0
    centered "That’s how long it took."
    pause 1.0
    centered "Not to fix his life."
    pause 1.0
    centered "But to finally want it."
    pause 1.5
    centered "For the first time—"
    pause 1.0
    centered "Isaac laughed."
    pause 1.5
    centered "And it didn’t hurt."
    return

label hollow_ending:
    scene black
    n "Isaac lived."
    n "The world called that enough."
    return

label jack_ending:
    scene black
    n "Jack kept his promise."
    pause 1.0
    n "There was peace."
    pause 1.0
    n "There was no Isaac."
    returns