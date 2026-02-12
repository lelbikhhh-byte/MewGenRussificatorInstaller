# MewRus Installer

Учебный проект установщика русификатора для игры **Mewgenics**.

## Что делает программа

- Запускается как GUI (`MewRus.py` / `MewRus.exe`).
- Просит выбрать папку с игрой.
- По кнопке **«Установить»** копирует папку `payload` в `MewRus` внутри выбранной папки.

## Запуск из исходников

```bash
python MewRus.py
```

## Как получить `MewRus.exe` (Windows)

### Вариант 1 — в один клик

Запусти `build_windows.bat` (двойной клик или из `cmd`).

Скрипт:
1. установит/обновит PyInstaller,
2. соберёт exe,
3. покажет путь к файлу.

Готовый файл будет здесь:

```text
dist\MewRus.exe
```

### Вариант 2 — вручную

1. Установите PyInstaller:

```bash
pip install pyinstaller
```

2. Выполните сборку:

```bash
pyinstaller --noconfirm --clean --windowed --onefile --name MewRus --add-data "payload;payload" MewRus.py
```

После сборки `MewRus.exe` появится в папке `dist/`.

---

> Важно: `.exe` нужно собирать на Windows. Если собирать на Linux/macOS, получится бинарник под эту ОС, а не Windows `.exe`.
