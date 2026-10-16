import tkinter as tk
import random

# Simple "love quiz" GUI with a playful fake-alert screen.
# Improvements:
# - Removed offensive text
# - Stagger heart lifetimes and animate them upward
# - Safer Toplevel handling (esc to close)
# - Minor refactor and PEP8-style names

BG = "#090711"
PINK = "#ff48dc"
ACCENT = "#d900ad"
DARK = "#24142f"


def show_hack(parent):
    """Show a playful full-screen 'SYSTEM ALERT' window (can be closed with Escape)."""
    hack = tk.Toplevel(parent)
    hack.title("SYSTEM ALERT")
    hack.configure(bg="black")
    # Try to make it full-screen but allow user to close with Escape
    try:
        hack.attributes("-fullscreen", True)
    except Exception:
        # fallback: maximize window if fullscreen attribute not supported
        hack.state("zoomed")

    title = tk.Label(
        hack,
        text="⚠ SYSTEM HACKED ⚠",
        font=("Courier New", 32, "bold"),
        fg="red",
        bg="black",
    )
    title.pack(pady=30)

    status = tk.Label(
        hack,
        text="ОБНАРУЖЕН ВИРУС",
        font=("Courier New", 15, "bold"),
        fg="#ff3333",
        bg="black",
    )
    status.pack(pady=10)

    code = tk.Label(
        hack,
        text="",
        font=("Courier New", 12),
        fg="#39ff88",
        bg="black",
        justify="left",
    )
    code.pack(pady=15)

    joke = tk.Label(
        hack,
        text="Это шутка — всё в порядке",
        font=("Courier New", 20, "bold"),
        fg="#ff1744",
        bg="black",
    )
    joke.pack(pady=15)

    lines = [
        "Подключение к серверу...",
        "Поиск Liebe...",
        "Ошибка: слишком много отказов.",
        "Загрузка сердечек...",
        "Процесс завершён — это шутка"
    ]

    def generate_code():
        return "\n".join(
            "".join(random.choice("01") for _ in range(38)) for _ in range(8)
        )

    def animate():
        # If window was closed externally, stop animation
        if not hack.winfo_exists():
            return

        status.config(text=random.choice(lines))
        code.config(text=generate_code())
        title.config(fg=random.choice(["red", "#ff1744", "#ff5555"]))
        hack.after(400, animate)

    def close_hack(event=None):
        if hack.winfo_exists():
            hack.destroy()

    close_button = tk.Button(
        hack,
        text="Закрыть (это шутка)",
        font=("Arial", 16, "bold"),
        fg="white",
        bg="#8b0000",
        command=close_hack,
    )
    close_button.pack(pady=20)

    hack.bind("<Escape>", close_hack)
    hack.protocol("WM_DELETE_WINDOW", close_hack)

    animate()


def say_yes(root, message_label):
    """Show message and spawn a bunch of hearts that float up and disappear."""
    message_label.config(text="Я знал(а), что ты меня любишь 🥺🩵")

    root.update_idletasks()
    max_x = root.winfo_width() - 40
    max_y = root.winfo_height() - 40

    def animate_heart(heart, steps=30, delay=30):
        def step(i=0):
            if not heart.winfo_exists():
                return
            # move up and optionally slightly left/right
            x, y = heart.winfo_x(), heart.winfo_y()
            heart.place(x=x + random.randint(-2, 2), y=y - 6)
            if i < steps:
                heart.after(delay, step, i + 1)
            else:
                heart.destroy()

        step()

    for i in range(15):
        x = random.randint(10, max(10, max_x))
        y = random.randint(180, max(180, max_y))
        heart = tk.Label(root, text="🩵", font=("Arial", 20), bg=BG, fg=PINK)
        heart.place(x=x, y=y)
        # stagger starts so hearts don't all vanish at once
        root.after(50 * i, animate_heart, heart)


def main():
    root = tk.Tk()
    root.title("Вопрос жизни и смерти")
    root.geometry("600x500")
    root.configure(bg=BG)

    title = tk.Label(root, text="Liebe", font=("Arial", 28, "bold"), fg=PINK, bg=BG)
    title.pack(pady=25)

    question = tk.Label(
        root,
        text="Ты меня любишь?",
        font=("Arial", 22, "bold"),
        fg="white",
        bg=BG,
    )
    question.pack(pady=10)

    arena = tk.Frame(root, bg=BG, height=130, width=500)
    arena.pack(pady=20)
    arena.pack_propagate(False)

    yes_btn = tk.Button(
        arena,
        text="конечно 🥺",
        font=("Arial", 16, "bold"),
        bg=ACCENT,
        fg="white",
        command=lambda: say_yes(root, message),
    )
    yes_btn.place(x=90, y=35, width=130, height=50)

    no_btn = tk.Button(
        arena,
        text="Неa",
        font=("Arial", 16, "bold"),
        bg=DARK,
        fg="white",
        command=lambda: show_hack(root),
    )
    no_btn.place(x=280, y=35, width=130, height=50)

    message = tk.Label(
        root,
        text="Вопрос жизни и смерти",
        font=("Arial", 16),
        fg="#c7a1ff",
        bg=BG,
    )
    message.pack(pady=15)

    root.mainloop()


if __name__ == "__main__":
    main()
