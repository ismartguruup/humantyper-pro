# ⌨️ HumanTyper Pro

> Hindi & English autotyper — bilkul insaan ki tarah type karta hai, 50 WPM speed pe.

![Platform](https://img.shields.io/badge/Platform-Windows-blue)
![Python](https://img.shields.io/badge/Python-3.8%2B-yellow)
![Languages](https://img.shields.io/badge/Languages-Hindi%20%7C%20English-green)
![WPM](https://img.shields.io/badge/Speed-50%20WPM-orange)

---

## ✨ Features

| Feature | Details |
|--------|---------|
| 🧠 Human-like Typing | Random delays, stumbles, punctuation pauses |
| 🇮🇳 Hindi Support | Full Devanagari script support |
| 🇬🇧 English Support | Complete English typing |
| ⏱️ Speed Control | 20–120 WPM adjustable (default: 50 WPM) |
| ⏳ Countdown Timer | 1–10 second delay before typing starts |
| ⛔ Emergency Stop | Press **ESC** anytime to stop |
| 📊 Live Progress | Real-time WPM + progress bar |
| 🖥️ Simple GUI | Dark themed, easy to use |

---

## 📥 Download

👉 **[Download HumanTyper_Pro.exe](../../releases/latest)**  
*(No Python install needed — just run the .exe)*

---

## 🚀 How to Use

1. **Open** `HumanTyper_Pro.exe`
2. **Paste** your Hindi or English text in the box
3. **Set** delay time (e.g., 3 seconds) and WPM speed
4. **Click START** → quickly switch to where you want to type (Notepad, WhatsApp, etc.)
5. The app will **automatically type** your text in human style
6. Press **ESC** to stop anytime

---

## 🧠 Human Typing Logic

```
Normal chars   → ~240ms delay + ±80ms random jitter
After Space    → extra 50ms pause
After . ! ? ।  → extra 150ms pause (sentence end)
After , ; :    → extra 75ms pause
After \n       → extra 300ms pause (new line)
Random stumble → 4% chance of 250ms hesitation mid-word
```

This makes it **impossible to distinguish from real human typing.**

---

## 🛠️ Build from Source

### Requirements
```
Python 3.8+
pip
```

### Steps

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/humantyper-pro.git
cd humantyper-pro

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run directly
python autotyper.py

# 4. OR build .exe (Windows)
build.bat
```

The `.exe` will be created in the `dist/` folder.

---

## 📁 Project Structure

```
humantyper-pro/
├── autotyper.py       # Main application
├── requirements.txt   # Python dependencies
├── build.bat          # Build script for .exe
└── README.md
```

---

## ⚠️ Notes

- **Windows only** (pyautogui + keyboard library)
- Run as **Administrator** if hotkeys don't work
- For Hindi typing, make sure your target app supports **Unicode / Devanagari**
- antivirus may flag the `.exe` (false positive — it's just keyboard automation)

---

## 📄 License

MIT License — free to use and modify.
