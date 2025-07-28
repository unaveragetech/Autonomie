
# 🧬 Autonomie – The Digital You

[![Build Status](https://img.shields.io/github/actions/workflow/status/unaveragetech/autonomie/python-app.yml?branch=main)](https://github.com/unaveragetech/autonomie/actions)
[![License: SDUC](https://img.shields.io/badge/license-SDUC-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.9%2B-blue.svg)](https://www.python.org/)
[![Open Issues](https://img.shields.io/github/issues/unaveragetech/autonomie)](https://github.com/unaveragetech/autonomie/issues)

---

## 🧠 What Is Autonomie?

**Autonomie** is a self-hosted system that watches how you interact with your computer and slowly learns to act on your behalf.

It doesn't ask you to write scripts or hardcode macros.  
It watches, remembers, and *evolves* based on how **you** use your machine.

> Autonomie's goal is simple: **your PC should already know what you were going to do.**

This is not traditional automation. This is the beginning of a **digital self** — your second set of eyes, hands, and intent living inside your OS.

---

## 🌍 Why Autonomie Matters

### 🏭 The Problem

Today, all advanced user modeling is controlled by corporations:

- They predict what you’ll click — but only to sell you something.
- They record your behavior — but never share what they learn.
- They build personal AI — but it's *not yours*.

You’re being studied by your machine, yet **you have no access to the brain behind the glass**.

---

### 🧑‍💻 Our Belief

You deserve the same power — on your terms.

Autonomie empowers you with a system that:

- Observes your real behaviors (no manual programming)
- Learns visually from what you see
- Remembers your interactions
- Evolves your preferences
- Lives *locally* and *only learns from you*

This is about **freedom, agency, and control** in your digital life.

---

## 🎯 Our Vision: A Digital Human Interface

Autonomie is a step toward building the first true **digital human interface** — a machine that mimics your real interactions in every sense.

It’s not just automation. It’s a replication of **how** and **why** you interact.

| Human Trait            | Autonomie Counterpart                                      |
|------------------------|-------------------------------------------------------------|
| Vision                 | Screenshot analysis + object detection + OCR               |
| Memory                 | Visual memory graph with element IDs and frequency         |
| Touch / Movement       | Mouse path simulation, wheel scrolling, timing variance    |
| Attention              | Top-down screen parsing and UI relevance heuristics        |
| Decision Making        | Action prediction based on past behavior (in development)  |
| Emotion/Bias           | Weighted action preference by time of day, hesitation, etc |

> The computer shouldn't just run tasks. It should run *your intent*.

---

## 🧩 CAPTCHA, Authenticity & Human Simulation

Avoiding CAPTCHA is **not the goal**, but it is a **necessary obstacle** for truly human interfaces.

Autonomie avoids API-level "captcha solvers" because they:

- Compromise your data
- Violate terms of service
- Use third-party behavioral data

Instead, Autonomie achieves authenticity by **actually behaving like a human**:

### ✅ Human Simulation Techniques

- **Top-down visual scanning**
- **Scroll wheel behavior with irregular timing**
- **Mouse movement that includes acceleration, wobble, and pauses**
- **Click hesitation** and **overshoot correction**
- **Response to visible elements only**, just like human vision
- **Live OCR** to mimic reading text, not querying metadata

If all else fails, Autonomie uses **vision + interaction delay** to legitimately pass human checks — not because it's faking, but because it's behaving naturally enough to **be treated like you.**

> If a CAPTCHA can’t tell the difference, maybe there *isn’t* one.

---

## ✨ Features

### ✅ Core

- **UI Object Detection** – Detect buttons, labels, checkboxes, and more using OpenCV.
- **Text Recognition (OCR)** – Read visible screen text with Tesseract.
- **Visual Memory System** – Recognize elements across sessions with hashed visual IDs.
- **Live CLI** – Pause/resume/inspect engine state in real-time.

### 🧪 Experimental

- **Behavior Logging** – Record user behavior for pattern analysis (non-invasive).
- **Scroll Logic** – Dynamic wheel behavior with noise functions.
- **Mouse Movement Simulation** – Realistic pathing and speed variability.

### 🛣 Planned

- **Intent Modeling** – Learn patterns like “what I usually do after I open this app.”
- **Task Recognition** – Notice and offer to automate common behavior chains.
- **Autonomous Response** – Let the system take action when confidence is high.
- **Neural Agent Mode** – Use lightweight LLMs to ask: *“What would you do here?”*

---

## 🛠 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/unaveragetech/autonomie.git
cd autonomie
````

### 2. Run the Setup Script

This installs required Python packages and prepares the local environment:

```bash
bash setup.sh
```

### 3. Install Tesseract OCR

* [Official Install Instructions](https://github.com/tesseract-ocr/tesseract)
* [Mirror Download via SourceForge](https://sourceforge.net/projects/tesseract-ocr.mirror/)

### 4. Add Tesseract to PATH

* **Windows**: Add install path to Environment Variables.
* **Linux/macOS**:

```bash
export PATH=$PATH:/path/to/tesseract
```

---

## ▶️ Running the Engine

Start the main interface:

```bash
python main.py
```

---

## ⌨️ CLI Commands

| Command          | Description                                 |
| ---------------- | ------------------------------------------- |
| `exit`           | Safely shuts down the engine                |
| `pause`          | Temporarily stops activity without quitting |
| `resume`         | Continues activity after a pause            |
| `status`         | Prints current engine state                 |
| `toggle_logging` | Enable/disable console action logs          |
| `clear_logs`     | Clears the CLI output for easier reading    |
| `help`           | Lists all available commands                |

---

## 🤝 Contributing

This project is early-stage but ambitious. We’re building a prototype of the future — and we want **you** to help shape it.

Ways to contribute:

* ⭐ Star the repo to support visibility
* 🐛 Report bugs or feature requests
* 🔧 Submit PRs with improvements or integrations
* 📣 Share the vision with others in open-source, privacy, and AI communities

Want to help design the UI layer?
Or plug in your own vision model?
Or build the first plugin system?

> This is your invitation. Let’s build *you* — in code.

---

## 📜 License

This project is licensed under the **SDUC License** (Self-Directed Use & Contribution). See [LICENSE](LICENSE) for terms.

---

## 📢 Final Note

**Autonomie** is not a tool. It's a statement:

> You should own the system that learns you.

If corporations build AI to predict your every move, you should have that power too — on your desktop, with your data, and under your control.

Let’s build the digital self.
One screen, one mouse movement, one learned habit at a time.

