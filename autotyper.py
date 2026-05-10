import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import pyautogui
import time
import random
import threading
import keyboard

# ─── Human Typing Config ─────────────────────────────────────────────────────
WPM_TARGET       = 50          # words per minute
AVG_CPM          = WPM_TARGET * 5          # ~250 chars/min
BASE_DELAY       = 60 / AVG_CPM           # seconds per char (~0.24s)
VARIANCE         = 0.08                   # ±80ms natural jitter
SPACE_PAUSE      = 0.05                   # extra pause after space
PUNCT_PAUSE      = 0.15                   # extra pause after . , ! ? etc
WORD_STUMBLE     = 0.04                   # chance of tiny stumble mid-word
STUMBLE_DELAY    = 0.25                   # stumble pause duration
HOTKEY_STOP      = "esc"                  # press Esc to stop
# ─────────────────────────────────────────────────────────────────────────────

class AutoTyper:
    def __init__(self, root):
        self.root = root
        self.root.title("HumanTyper Pro — Hindi & English")
        self.root.geometry("680x560")
        self.root.resizable(False, False)
        self.root.configure(bg="#0f0f13")

        self.typing = False
        self.stop_flag = False
        self.typed_chars = 0
        self.total_chars = 0
        self.start_time = None

        pyautogui.FAILSAFE = True
        self._build_ui()
        self._bind_hotkeys()

    # ── UI ──────────────────────────────────────────────────────────────────
    def _build_ui(self):
        # Title bar
        title_frame = tk.Frame(self.root, bg="#0f0f13")
        title_frame.pack(fill="x", pady=(18, 0))

        tk.Label(title_frame, text="⌨  HumanTyper Pro",
                 font=("Segoe UI", 18, "bold"), fg="#e0c97f",
                 bg="#0f0f13").pack()
        tk.Label(title_frame, text="Hindi & English  •  50 WPM  •  Human Style",
                 font=("Segoe UI", 9), fg="#666", bg="#0f0f13").pack()

        # Language selector
        lang_frame = tk.Frame(self.root, bg="#0f0f13")
        lang_frame.pack(fill="x", padx=24, pady=(14, 0))

        tk.Label(lang_frame, text="Language:", font=("Segoe UI", 10),
                 fg="#aaa", bg="#0f0f13").pack(side="left")

        self.lang_var = tk.StringVar(value="auto")
        langs = [("🔄 Auto Detect", "auto"),
                 ("🇮🇳 Hindi", "hi"),
                 ("🇬🇧 English", "en")]
        for text, val in langs:
            tk.Radiobutton(lang_frame, text=text, variable=self.lang_var,
                           value=val, font=("Segoe UI", 10),
                           fg="#ccc", bg="#0f0f13", selectcolor="#1e1e2e",
                           activebackground="#0f0f13",
                           activeforeground="#e0c97f").pack(side="left", padx=10)

        # Text area
        txt_frame = tk.Frame(self.root, bg="#1a1a24", bd=0,
                             highlightthickness=1, highlightbackground="#333")
        txt_frame.pack(fill="both", expand=True, padx=24, pady=12)

        self.text_area = scrolledtext.ScrolledText(
            txt_frame, wrap="word", font=("Noto Sans", 11),
            bg="#1a1a24", fg="#e8e8e8", insertbackground="#e0c97f",
            relief="flat", padx=12, pady=12,
            selectbackground="#3a3a5c")
        self.text_area.pack(fill="both", expand=True)
        self.text_area.insert("1.0",
            "यहाँ अपना टेक्स्ट लिखें या paste करें...\n"
            "Type or paste your text here (Hindi / English)...")
        self.text_area.bind("<FocusIn>", self._clear_placeholder)

        # Settings row
        settings = tk.Frame(self.root, bg="#0f0f13")
        settings.pack(fill="x", padx=24)

        tk.Label(settings, text="Delay before start (sec):",
                 font=("Segoe UI", 9), fg="#888", bg="#0f0f13").pack(side="left")
        self.delay_var = tk.IntVar(value=3)
        delay_spin = ttk.Spinbox(settings, from_=1, to=10,
                                 textvariable=self.delay_var, width=4,
                                 font=("Segoe UI", 10))
        delay_spin.pack(side="left", padx=(4, 20))

        tk.Label(settings, text="Speed (WPM):",
                 font=("Segoe UI", 9), fg="#888", bg="#0f0f13").pack(side="left")
        self.wpm_var = tk.IntVar(value=50)
        wpm_spin = ttk.Spinbox(settings, from_=20, to=120,
                               textvariable=self.wpm_var, width=5,
                               font=("Segoe UI", 10))
        wpm_spin.pack(side="left", padx=(4, 0))

        # Status bar
        status_frame = tk.Frame(self.root, bg="#141420")
        status_frame.pack(fill="x", padx=24, pady=(8, 0))

        self.status_var = tk.StringVar(value="Ready  •  Press START then switch to target window")
        tk.Label(status_frame, textvariable=self.status_var,
                 font=("Segoe UI", 9), fg="#777", bg="#141420",
                 anchor="w").pack(side="left")

        self.progress = ttk.Progressbar(status_frame, length=160,
                                        mode="determinate")
        self.progress.pack(side="right", pady=4)

        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0f0f13")
        btn_frame.pack(pady=(8, 16))

        self.start_btn = tk.Button(btn_frame, text="▶  START",
                                   font=("Segoe UI", 11, "bold"),
                                   bg="#2a7a4f", fg="white",
                                   activebackground="#1e5c3a",
                                   relief="flat", padx=24, pady=8,
                                   cursor="hand2",
                                   command=self.start_typing)
        self.start_btn.pack(side="left", padx=8)

        self.stop_btn = tk.Button(btn_frame, text="■  STOP  (ESC)",
                                  font=("Segoe UI", 11, "bold"),
                                  bg="#7a2a2a", fg="white",
                                  activebackground="#5c1e1e",
                                  relief="flat", padx=24, pady=8,
                                  cursor="hand2",
                                  state="disabled",
                                  command=self.stop_typing)
        self.stop_btn.pack(side="left", padx=8)

        tk.Button(btn_frame, text="🗑  Clear",
                  font=("Segoe UI", 10), bg="#222230", fg="#aaa",
                  activebackground="#2a2a3e", relief="flat",
                  padx=14, pady=8, cursor="hand2",
                  command=self.clear_text).pack(side="left", padx=8)

    def _bind_hotkeys(self):
        keyboard.add_hotkey("esc", self.stop_typing)

    def _clear_placeholder(self, event=None):
        current = self.text_area.get("1.0", "end-1c")
        if "यहाँ अपना" in current or "Type or paste" in current:
            self.text_area.delete("1.0", "end")

    # ── Core Logic ──────────────────────────────────────────────────────────
    def start_typing(self):
        text = self.text_area.get("1.0", "end-1c").strip()
        if not text or "यहाँ अपना" in text:
            messagebox.showwarning("Empty!", "Pehle text daalein / Please enter text first.")
            return

        self.typing = True
        self.stop_flag = False
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.text_area.config(state="disabled")
        self.typed_chars = 0
        self.total_chars = len(text)
        self.progress["value"] = 0
        self.progress["maximum"] = self.total_chars

        thread = threading.Thread(target=self._type_thread, args=(text,), daemon=True)
        thread.start()

    def _type_thread(self, text):
        delay = self.delay_var.get()
        for i in range(delay, 0, -1):
            self._set_status(f"⏳ Starting in {i}s — Switch to target window now!")
            time.sleep(1)
            if self.stop_flag:
                self._reset_ui()
                return

        # Recalculate based on current WPM setting
        wpm = self.wpm_var.get()
        cpm = wpm * 5
        base = 60 / cpm

        self._set_status("⌨  Typing... Press ESC to stop")
        self.start_time = time.time()

        i = 0
        while i < len(text) and not self.stop_flag:
            ch = text[i]
            pyautogui.typewrite(ch, interval=0)

            # Human delay calculation
            delay_ms = base + random.uniform(-VARIANCE, VARIANCE)

            if ch == " ":
                delay_ms += SPACE_PAUSE
            elif ch in ".!?।":
                delay_ms += PUNCT_PAUSE + random.uniform(0, 0.1)
            elif ch in ",;:":
                delay_ms += PUNCT_PAUSE * 0.5
            elif ch == "\n":
                delay_ms += PUNCT_PAUSE * 2

            # Occasional human stumble
            if random.random() < WORD_STUMBLE and ch not in " \n":
                delay_ms += STUMBLE_DELAY

            time.sleep(max(delay_ms, 0.04))

            self.typed_chars += 1
            i += 1

            # Update progress every 5 chars
            if i % 5 == 0:
                self._update_progress()

        elapsed = time.time() - self.start_time
        actual_wpm = round((self.typed_chars / 5) / (elapsed / 60)) if elapsed > 0 else 0

        if not self.stop_flag:
            self._set_status(f"✅ Done! {self.typed_chars} chars typed at ~{actual_wpm} WPM")
        else:
            self._set_status(f"⛔ Stopped at char {self.typed_chars}/{self.total_chars}")

        self._reset_ui()

    def _update_progress(self):
        pct = (self.typed_chars / self.total_chars) * 100 if self.total_chars else 0
        elapsed = time.time() - self.start_time if self.start_time else 0
        wpm_live = round((self.typed_chars / 5) / (elapsed / 60)) if elapsed > 0 else 0
        self.root.after(0, lambda: self._set_progress(pct, wpm_live))

    def _set_progress(self, pct, wpm):
        self.progress["value"] = self.typed_chars
        self._set_status(f"⌨  Typing... {self.typed_chars}/{self.total_chars} chars  •  ~{wpm} WPM  •  ESC=Stop")

    def _set_status(self, msg):
        self.root.after(0, lambda: self.status_var.set(msg))

    def stop_typing(self):
        self.stop_flag = True
        self.typing = False

    def _reset_ui(self):
        def _do():
            self.start_btn.config(state="normal")
            self.stop_btn.config(state="disabled")
            self.text_area.config(state="normal")
        self.root.after(0, _do)

    def clear_text(self):
        if not self.typing:
            self.text_area.config(state="normal")
            self.text_area.delete("1.0", "end")
            self.progress["value"] = 0
            self._set_status("Ready  •  Press START then switch to target window")


# ── Entry Point ───────────────────────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = AutoTyper(root)

    # Style ttk widgets
    style = ttk.Style()
    style.theme_use("clam")
    style.configure("TProgressbar", troughcolor="#1e1e2e",
                    background="#e0c97f", thickness=8)
    style.configure("TSpinbox", fieldbackground="#1e1e2e",
                    foreground="#eee", background="#1e1e2e")

    root.mainloop()
