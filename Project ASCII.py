import tkinter as tk
from tkinter import ttk, messagebox
from art import text2art

POPULAR_FONTS = [
    "block",
    "standard",
    "slant",
    "banner",
    "isometric1",
    "letters",
    "alligator",
    "bubble",
    "digital",
    "lean",
    "shadow",
    "cyberlarge",
    "cybermedium",
    "caligraphy",
    "starwars"
]

PLATFORMS = [
    "WhatsApp",
    "Instagram",
    "X (Twitter)",
    "Discord"
]

def format_output(art_text, target):
    lines = [line.rstrip() for line in art_text.splitlines() if line.strip()]
    if not lines:
        return ""

    if target == "WhatsApp":
        return f"```{chr(10).join(lines)}```"

    if target == "Instagram":
        max_len = max(len(l) for l in lines)
        padded = [l.ljust(max_len).replace(" ", "⠀") for l in lines]
        return "\n.\n".join(padded)

    if target == "X (Twitter)":
        return "\n".join(lines)

    if target == "Discord":
        return f"```text\n{chr(10).join(lines)}\n```"

    return "\n".join(lines)

def generate_art():
    text = text_entry.get().strip()
    font = font_combo.get().strip() or "block"
    target = platform_combo.get().strip() or "WhatsApp"

    if not text:
        messagebox.showwarning("Input Missing", "Please enter some text to convert.")
        return

    try:
        raw_art = text2art(text, font=font)
        formatted = format_output(raw_art, target)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, formatted)
        status_label.config(text=f"Ready to copy formatted for {target} ({font})", fg="#38bdf8")
    except Exception as e:
        messagebox.showerror("Error", f"Failed with font '{font}':\n{e}")

def copy_to_clipboard():
    content = output_text.get("1.0", tk.END).strip()
    if not content:
        messagebox.showinfo("Clipboard", "No art generated yet to copy.")
        return

    r.clipboard_clear()
    r.clipboard_append(content)
    r.update()
    status_label.config(text=f"✓ Copied format for {platform_combo.get()} to clipboard!", fg="#4ade80")

r = tk.Tk()
r.title("ASCII Art Studio")
r.geometry("860x620")
r.minsize(680, 480)
r.configure(bg="#0f172a")

style = ttk.Style()
style.theme_use("clam")

style.configure("TCombobox",
                fieldbackground="#1e293b",
                background="#334155",
                foreground="#38bdf8",
                darkcolor="#1e293b",
                lightcolor="#1e293b",
                selectbackground="#334155",
                selectforeground="#ffffff",
                arrowcolor="#38bdf8")

style.map("TCombobox",
          fieldbackground=[("readonly", "#1e293b")],
          selectbackground=[("readonly", "#334155")],
          selectforeground=[("readonly", "#ffffff")],
          foreground=[("readonly", "#f8fafc")])

header_frame = tk.Frame(r, bg="#0f172a", pady=12)
header_frame.pack(fill=tk.X)

tk.Label(header_frame, text="ASCII Art Generator", font=("Segoe UI", 18, "bold"), fg="#f8fafc", bg="#0f172a").pack()
tk.Label(header_frame, text="Generate and copy format-ready ASCII for your favorite apps", font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a").pack(pady=2)

controls_card = tk.Frame(r, bg="#1e293b", padx=16, pady=14, highlightbackground="#334155", highlightthickness=1)
controls_card.pack(fill=tk.X, padx=20, pady=(0, 10))

tk.Label(controls_card, text="TEXT INPUT", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#1e293b").grid(row=0, column=0, sticky="w", padx=6, pady=(0, 2))
tk.Label(controls_card, text="FONT SELECTION", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#1e293b").grid(row=0, column=1, sticky="w", padx=6, pady=(0, 2))
tk.Label(controls_card, text="TARGET PLATFORM", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#1e293b").grid(row=0, column=2, sticky="w", padx=6, pady=(0, 2))

text_entry = tk.Entry(controls_card, font=("Segoe UI", 11), bg="#0f172a", fg="#f8fafc", insertbackground="#38bdf8", relief="flat", highlightbackground="#475569", highlightthickness=1)
text_entry.grid(row=1, column=0, sticky="ew", padx=6, pady=4, ipady=4)
text_entry.insert(0, "PYTHON")

font_combo = ttk.Combobox(controls_card, values=POPULAR_FONTS, font=("Segoe UI", 10), state="readonly")
font_combo.grid(row=1, column=1, sticky="ew", padx=6, pady=4, ipady=3)
font_combo.set("block")

platform_combo = ttk.Combobox(controls_card, values=PLATFORMS, font=("Segoe UI", 10), state="readonly")
platform_combo.grid(row=1, column=2, sticky="ew", padx=6, pady=4, ipady=3)
platform_combo.set("WhatsApp")

btn_generate = tk.Button(controls_card, text="Generate", command=generate_art, font=("Segoe UI", 10, "bold"), bg="#0284c7", fg="#ffffff", activebackground="#0369a1", activeforeground="#ffffff", relief="flat", padx=14, pady=4, cursor="hand2")
btn_generate.grid(row=1, column=3, padx=(10, 6), pady=4)

font_combo.bind("<<ComboboxSelected>>", lambda _: generate_art())
platform_combo.bind("<<ComboboxSelected>>", lambda _: generate_art())
text_entry.bind("<Return>", lambda _: generate_art())

controls_card.columnconfigure(0, weight=3)
controls_card.columnconfigure(1, weight=2)
controls_card.columnconfigure(2, weight=2)

output_card = tk.Frame(r, bg="#1e293b", highlightbackground="#334155", highlightthickness=1)
output_card.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))

output_toolbar = tk.Frame(output_card, bg="#1e293b", padx=10, pady=8)
output_toolbar.pack(fill=tk.X)

tk.Label(output_toolbar, text="PREVIEW CANVAS", font=("Segoe UI", 8, "bold"), fg="#94a3b8", bg="#1e293b").pack(side=tk.LEFT)

btn_copy = tk.Button(output_toolbar, text="📋 Copy Output", command=copy_to_clipboard, font=("Segoe UI", 9, "bold"), bg="#10b981", fg="#ffffff", activebackground="#059669", activeforeground="#ffffff", relief="flat", padx=12, pady=3, cursor="hand2")
btn_copy.pack(side=tk.RIGHT)

editor_container = tk.Frame(output_card, bg="#0b0f19")
editor_container.pack(fill=tk.BOTH, expand=True, padx=1, pady=1)

output_text = tk.Text(editor_container, wrap=tk.NONE, font=("Consolas", 10), bg="#0b0f19", fg="#22c55e", insertbackground="#38bdf8", selectbackground="#334155", selectforeground="#ffffff", relief="flat", padx=12, pady=12)
output_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

scroll_y = ttk.Scrollbar(editor_container, orient=tk.VERTICAL, command=output_text.yview)
scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
output_text.config(yscrollcommand=scroll_y.set)

scroll_x = ttk.Scrollbar(output_card, orient=tk.HORIZONTAL, command=output_text.xview)
scroll_x.pack(fill=tk.X)
output_text.config(xscrollcommand=scroll_x.set)

status_bar = tk.Frame(r, bg="#0f172a", padx=20, pady=6)
status_bar.pack(fill=tk.X)

status_label = tk.Label(status_bar, text="Ready.", font=("Segoe UI", 9), fg="#94a3b8", bg="#0f172a")
status_label.pack(side=tk.LEFT)

generate_art()

r.mainloop()
