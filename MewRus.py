from __future__ import annotations

import shutil
import sys
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

APP_TITLE = "Mewgenics Русификатор"
WINDOW_SIZE = "760x470"


def resource_path(relative: str) -> Path:
    """Return absolute path to bundled resources for source and PyInstaller modes."""
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent))
    return base / relative


class InstallerApp:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title(APP_TITLE)
        self.root.geometry(WINDOW_SIZE)
        self.root.resizable(False, False)

        self.install_dir = tk.StringVar(value="")
        self.status_text = tk.StringVar(value="Выберите папку с игрой Mewgenics")

        self._build_style()
        self._build_ui()

    def _build_style(self) -> None:
        self.root.configure(bg="#111318")
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("Main.TFrame", background="#111318")
        style.configure("Card.TFrame", background="#1b1f28")
        style.configure("Title.TLabel", background="#1b1f28", foreground="#f9f8ff", font=("Segoe UI", 23, "bold"))
        style.configure("Body.TLabel", background="#1b1f28", foreground="#c8d0ff", font=("Segoe UI", 11))
        style.configure("Path.TEntry", fieldbackground="#0d1016", foreground="#ffffff", bordercolor="#4f5ccf", padding=8)
        style.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=8)
        style.map("Accent.TButton", background=[("!disabled", "#5464ff"), ("active", "#6876ff")], foreground=[("!disabled", "#ffffff")])

    def _build_ui(self) -> None:
        wrapper = ttk.Frame(self.root, style="Main.TFrame", padding=20)
        wrapper.pack(fill="both", expand=True)

        card = ttk.Frame(wrapper, style="Card.TFrame", padding=28)
        card.pack(fill="both", expand=True)

        ttk.Label(card, text="MewRus Installer", style="Title.TLabel").pack(anchor="w")
        ttk.Label(
            card,
            text="Установка учебного русификатора для Mewgenics",
            style="Body.TLabel",
        ).pack(anchor="w", pady=(4, 20))

        ttk.Label(card, text="Папка с игрой:", style="Body.TLabel").pack(anchor="w")

        path_row = ttk.Frame(card, style="Card.TFrame")
        path_row.pack(fill="x", pady=(8, 12))

        self.path_entry = ttk.Entry(path_row, textvariable=self.install_dir, style="Path.TEntry")
        self.path_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))

        ttk.Button(path_row, text="Обзор…", style="Accent.TButton", command=self._choose_directory).pack(side="left")

        actions = ttk.Frame(card, style="Card.TFrame")
        actions.pack(fill="x", pady=8)
        ttk.Button(actions, text="Установить", style="Accent.TButton", command=self._install).pack(side="left")

        self.progress = ttk.Progressbar(card, orient="horizontal", mode="determinate", maximum=100)
        self.progress.pack(fill="x", pady=(12, 10))

        ttk.Label(card, textvariable=self.status_text, style="Body.TLabel").pack(anchor="w")


    def _choose_directory(self) -> None:
        selected = filedialog.askdirectory(title="Выберите папку с Mewgenics")
        if selected:
            self.install_dir.set(selected)
            self.status_text.set("Папка выбрана. Нажмите «Установить».")

    def _install(self) -> None:
        target = Path(self.install_dir.get().strip())
        if not target.exists() or not target.is_dir():
            messagebox.showerror("Ошибка", "Укажите корректную папку с игрой.")
            return

        payload = resource_path("payload")
        if not payload.exists():
            messagebox.showerror("Ошибка", "Папка payload не найдена рядом с программой.")
            return

        dest = target / "MewRus"
        self.progress["value"] = 10
        self.root.update_idletasks()

        try:
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(payload, dest)

            readme = dest / "README_INSTALL.txt"
            readme.write_text(
                "Русификатор установлен.\n"
                "Это учебный пример установщика.\n",
                encoding="utf-8",
            )

            self.progress["value"] = 100
            self.status_text.set("Готово! Файлы русификатора скопированы в папку игры.")
            messagebox.showinfo("Успех", f"Установка завершена.\nПуть: {dest}")
        except Exception as exc:  # pylint: disable=broad-except
            self.progress["value"] = 0
            self.status_text.set("Ошибка установки.")
            messagebox.showerror("Ошибка", f"Не удалось установить русификатор:\n{exc}")


def main() -> None:
    root = tk.Tk()
    InstallerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
