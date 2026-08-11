"""
Grail GUI - "The Gutsy Little Guardian"
One-click data protection: PII redaction + AES-256-GCM encryption.
Password vault (PBKDF2), clipboard, .grail file save/load,
best-effort key wipe on close.

Grail GUI - «Удаленький защитник»
Защита данных в один клик: поиск PII + шифрование AES-256-GCM.
Парольное хранилище (PBKDF2), буфер обмена, сохранение/загрузка .grail-файлов,
стирание ключей при закрытии (best effort).
"""

import os
import tkinter as tk
from tkinter import scrolledtext, messagebox, filedialog
from ai_detector import RegexPIIDetector
from core import GrailVault, SecurityError

MAGIC = b'GRAIL1\n'  # File format marker / Маркер формата файла


class GrailGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏆 Grail — The Gutsy Little Guardian / Удаленький защитник")
        self.root.geometry("900x780")

        # Color scheme (emerald & burgundy) / Цветовая схема (изумрудный и бордовый)
        self.colors = {
            'bg_primary': '#1B4332',      # Deep emerald / Глубокий изумрудный
            'bg_secondary': '#2D0036',    # Dark violet / Тёмно-фиолетовый
            'accent': '#780000',          # Burgundy / Бордовый
            'text': '#FFFFFF',            # White / Белый
            'text_secondary': '#B7E4C7',  # Light emerald / Светло-изумрудный
            'success': '#40916C',         # Success / Успех
            'warning': '#D4A373'          # Warning / Предупреждение
        }

        self.root.configure(bg=self.colors['bg_secondary'])

        # Module initialization / Инициализация модулей
        self.detector = RegexPIIDetector()
        self.vault = GrailVault()  # ephemeral key / эфемерный ключ
        self.last_protected = None  # last protected text / последний защищённый текст

        self.create_widgets()

        # Best-effort key wipe on close / Стирание ключей при закрытии (best effort)
        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def create_widgets(self):
        """Creates all UI elements / Создает все элементы интерфейса"""

        # === HEADER / ЗАГОЛОВОК ===
        title_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=80)
        title_frame.pack(fill='x', padx=10, pady=10)

        tk.Label(
            title_frame,
            text="🏆 GRAIL",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text']
        ).pack(pady=(15, 0))

        tk.Label(
            title_frame,
            text="Your digital sanctuary / Ваша цифровая святыня. Неприкосновенная. Локальная. Вечная.",
            font=("Helvetica", 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        ).pack()

        # === MAIN AREA / ОСНОВНАЯ ОБЛАСТЬ ===
        main_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)

        # Input field / Поле ввода текста
        tk.Label(
            main_frame,
            text="📥 Paste text to protect / Вставьте текст для защиты:",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(0, 5))

        self.text_input = scrolledtext.ScrolledText(
            main_frame,
            height=9,
            font=("Consolas", 10),
            bg='#2D3748',
            fg='#E2E8F0',
            insertbackground='white',
            selectbackground=self.colors['accent'],
            selectforeground='white'
        )
        self.text_input.pack(fill='both', expand=True, pady=(0, 10))

        # Password field / Поле пароля
        pw_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'])
        pw_frame.pack(fill='x', pady=(0, 5))

        tk.Label(
            pw_frame,
            text="🔑 Password / Пароль (PBKDF2, 600k):",
            font=("Helvetica", 11, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text']
        ).pack(side='left')

        self.password_entry = tk.Entry(
            pw_frame,
            show="*",
            font=("Consolas", 11),
            bg='#2D3748',
            fg='#E2E8F0',
            insertbackground='white',
            width=30
        )
        self.password_entry.pack(side='left', padx=10)

        # === BUTTONS / КНОПКИ ===
        # Row 1: protect & clear / Строка 1: защита и очистка
        row1 = tk.Frame(main_frame, bg=self.colors['bg_secondary'])
        row1.pack(fill='x', pady=5)

        self.btn_protect = tk.Button(
            row1,
            text="🛡️ PROTECT / ЗАЩИТИТЬ",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            activebackground=self.colors['success'],
            activeforeground=self.colors['text'],
            cursor="hand2",
            command=self.protect_data,
            padx=20,
            pady=8
        )
        self.btn_protect.pack(side='left', padx=5)

        tk.Button(
            row1,
            text="🗑️ CLEAR / ОЧИСТИТЬ",
            font=("Helvetica", 12),
            bg='#4A5568',
            fg=self.colors['text'],
            cursor="hand2",
            command=self.clear_fields,
            padx=15,
            pady=8
        ).pack(side='left', padx=5)

        # Row 2: file vault / Строка 2: файловое хранилище
        row2 = tk.Frame(main_frame, bg=self.colors['bg_secondary'])
        row2.pack(fill='x', pady=5)

        tk.Button(
            row2,
            text="💾 SAVE .grail / СОХРАНИТЬ",
            font=("Helvetica", 12),
            bg=self.colors['bg_primary'],
            fg=self.colors['text'],
            cursor="hand2",
            command=self.save_to_file,
            padx=15,
            pady=8
        ).pack(side='left', padx=5)

        tk.Button(
            row2,
            text="📂 LOAD .grail / ЗАГРУЗИТЬ",
            font=("Helvetica", 12),
            bg=self.colors['bg_primary'],
            fg=self.colors['text'],
            cursor="hand2",
            command=self.load_from_file,
            padx=15,
            pady=8
        ).pack(side='left', padx=5)

        # Row 3: clipboard / Строка 3: буфер обмена
        row3 = tk.Frame(main_frame, bg=self.colors['bg_secondary'])
        row3.pack(fill='x', pady=5)

        tk.Button(
            row3,
            text="📋 PASTE / ВСТАВИТЬ ИЗ БУФЕРА",
            font=("Helvetica", 11),
            bg='#4A5568',
            fg=self.colors['text'],
            cursor="hand2",
            command=self.paste_from_clipboard,
            padx=12,
            pady=6
        ).pack(side='left', padx=5)

        tk.Button(
            row3,
            text="📄 COPY RESULT / СКОПИРОВАТЬ",
            font=("Helvetica", 11),
            bg='#4A5568',
            fg=self.colors['text'],
            cursor="hand2",
            command=self.copy_result,
            padx=12,
            pady=6
        ).pack(side='left', padx=5)

        # === RESULT / РЕЗУЛЬТАТ ===
        tk.Label(
            main_frame,
            text="🔒 Result / Результат защиты:",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text']
        ).pack(anchor='w', pady=(10, 5))

        self.text_output = scrolledtext.ScrolledText(
            main_frame,
            height=8,
            font=("Consolas", 10),
            bg='#1A202C',
            fg='#48BB78',
            state='disabled',
            wrap='word'
        )
        self.text_output.pack(fill='both', expand=True)

        # === STATUS / СТАТУС ===
        self.status_label = tk.Label(
            main_frame,
            text="✅ Ready / Готов к работе",
            font=("Helvetica", 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary'],
            pady=5
        )
        self.status_label.pack(fill='x', pady=(10, 0))

    def protect_data(self):
        """Detects PII, redacts and encrypts / Находит PII, скрывает и шифрует"""
        input_text = self.text_input.get("1.0", tk.END).strip()

        if not input_text:
            messagebox.showwarning("Grail", "Enter text first / Сначала введите текст!")
            return

        try:
            self.status_label.config(text="🔄 Processing / Обработка...", fg=self.colors['warning'])
            self.root.update()

            # 1. Detect PII / Находим PII
            found_pii = self.detector.detect_pii(input_text)

            # 2. Redact PII / Заменяем PII
            protected_text = self.detector.redact_pii(input_text, replacement="[ЗАЩИЩЕНО]")

            # 3. Encrypt / Шифруем
            encrypted_data, data_hash = self.vault.secure_process(protected_text)
            self.last_protected = protected_text

            result = f"\n🔍 PII FOUND / НАЙДЕНО ЛИЧНЫХ ДАННЫХ: {len(found_pii)}\n\n📊 DETAILS / ДЕТАЛИ:\n"
            for item in found_pii:
                result += f"  • {item['type']}: {item['value']}\n"

            result += f"""
🛡️ PROTECTED TEXT / ЗАЩИЩЕННЫЙ ТЕКСТ:
{protected_text}

🔐 INTEGRITY HASH / ХЭШ ЦЕЛОСТНОСТИ:
{data_hash[:32]}...

✅ Encrypted with AES-256-GCM! / Зашифровано AES-256-GCM!
💾 Enter password and press SAVE to store as .grail file
💾 Введите пароль и нажмите СОХРАНИТЬ для записи в .grail-файл
"""

            self.text_output.config(state='normal')
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, result)
            self.text_output.config(state='disabled')

            self.status_label.config(text="✅ Protected / Защита завершена!", fg=self.colors['success'])

        except Exception as e:
            messagebox.showerror("Grail", f"Error / Ошибка: {e}")
            self.status_label.config(text="❌ Error / Ошибка обработки", fg='red')

    def save_to_file(self):
        """Saves protected text into a password-protected .grail file.
        Сохраняет защищённый текст в .grail-файл с парольной защитой."""
        if not self.last_protected:
            messagebox.showwarning("Grail", "Protect data first / Сначала защитите данные")
            return

        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Grail", "Enter password to save / Введите пароль для сохранения")
            return

        path = filedialog.asksaveasfilename(
            defaultextension=".grail",
            filetypes=[("Grail vault / Файлы Grail", "*.grail")])
        if not path:
            return

        try:
            vault_pw = GrailVault(password=password)
            packed, data_hash = vault_pw.secure_process(self.last_protected)

            with open(path, 'wb') as f:
                f.write(MAGIC)
                f.write(vault_pw.salt.hex().encode() + b'\n')
                f.write(data_hash.encode() + b'\n')
                f.write(packed)

            self.status_label.config(text=f"💾 Saved / Сохранено: {path}", fg=self.colors['success'])
            messagebox.showinfo("Grail", f"Saved / Сохранено: {path}")
        except Exception as e:
            messagebox.showerror("Grail", f"Save error / Ошибка сохранения: {e}")

    def load_from_file(self):
        """Loads and decrypts a .grail file with password.
        Загружает и расшифровывает .grail-файл по паролю."""
        password = self.password_entry.get()
        if not password:
            messagebox.showwarning("Grail", "Enter password to load / Введите пароль для загрузки")
            return

        path = filedialog.askopenfilename(
            filetypes=[("Grail vault / Файлы Grail", "*.grail")])
        if not path:
            return

        try:
            with open(path, 'rb') as f:
                magic = f.readline()
                if magic != MAGIC:
                    raise ValueError("Not a Grail file / Не файл Grail")
                salt = bytes.fromhex(f.readline().strip().decode())
                data_hash = f.readline().strip().decode()
                packed = f.read()

            vault_pw = GrailVault(password=password, salt=salt)
            text = vault_pw.verify_and_decrypt(packed, data_hash)

            self.text_output.config(state='normal')
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, "🔓 DECRYPTED / РАСШИФРОВАНО:\n\n" + text)
            self.text_output.config(state='disabled')

            self.status_label.config(text="✅ Loaded / Загружено", fg=self.colors['success'])
        except SecurityError:
            messagebox.showerror("Grail",
                "Wrong password or corrupted file / Неверный пароль или повреждённый файл")
        except Exception as e:
            messagebox.showerror("Grail", f"Load error / Ошибка загрузки: {e}")

    def paste_from_clipboard(self):
        """Inserts clipboard content / Вставляет содержимое буфера обмена"""
        try:
            text = self.root.clipboard_get()
            self.text_input.delete("1.0", tk.END)
            self.text_input.insert(tk.END, text)
            self.status_label.config(text="📋 Pasted / Вставлено из буфера", fg=self.colors['success'])
        except tk.TclError:
            messagebox.showwarning("Grail", "Clipboard is empty / Буфер обмена пуст")

    def copy_result(self):
        """Copies result to clipboard / Копирует результат в буфер обмена"""
        text = self.text_output.get("1.0", tk.END).strip()
        if not text:
            return
        self.root.clipboard_clear()
        self.root.clipboard_append(text)
        self.status_label.config(text="📋 Copied / Скопировано", fg=self.colors['success'])

    def clear_fields(self):
        """Clears all fields / Очищает все поля"""
        self.text_input.delete("1.0", tk.END)
        self.password_entry.delete(0, tk.END)
        self.text_output.config(state='normal')
        self.text_output.delete("1.0", tk.END)
        self.text_output.config(state='disabled')
        self.last_protected = None
        self.status_label.config(text="✅ Ready / Готов к работе", fg=self.colors['text_secondary'])

    def on_close(self):
        """Best-effort key wipe on close / Стирание ключей при закрытии (best effort).
        Honest limitation: Python cannot guarantee full RAM wipe.
        Честное ограничение: Python не может гарантировать полное стирание RAM."""
        try:
            if self.vault is not None and getattr(self.vault, 'key', None):
                self.vault.key = os.urandom(32)  # overwrite reference / перезаписываем ссылку
            self.vault = None
            self.last_protected = None
        except Exception:
            pass
        self.root.destroy()


# === APP LAUNCH / ЗАПУСК ПРИЛОЖЕНИЯ ===
if __name__ == "__main__":
    root = tk.Tk()
    app = GrailGUI(root)
    root.mainloop()
