"""
Grail GUI - Графический интерфейс
Красивое и удобное приложение для защиты данных.
Использует ваши любимые цвета: изумрудный и бордовый.
"""

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from ai_detector import RegexPIIDetector
from core import GrailVault


class GrailGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🏆 Grail - International Data Protection")
        self.root.geometry("900x700")
        
        # Цветовая схема (ваши любимые оттенки)
        self.colors = {
            'bg_primary': '#1B4332',      # Глубокий изумрудный
            'bg_secondary': '#2D0036',    # Тёмно-фиолетовый
            'accent': '#780000',          # Бордовый
            'text': '#FFFFFF',            # Белый
            'text_secondary': '#B7E4C7',  # Светло-изумрудный
            'success': '#40916C',         # Успех
            'warning': '#D4A373'          # Предупреждение
        }
        
        # Настройка основного окна
        self.root.configure(bg=self.colors['bg_secondary'])
        
        # Инициализация модулей
        self.detector = RegexPIIDetector()
        self.vault = GrailVault()
        
        # Создание интерфейса
        self.create_widgets()
    
    def create_widgets(self):
        """Создает все элементы интерфейса"""
        
        # === ЗАГОЛОВОК ===
        title_frame = tk.Frame(self.root, bg=self.colors['bg_primary'], height=80)
        title_frame.pack(fill='x', padx=10, pady=10)
        
        title_label = tk.Label(
            title_frame,
            text="🏆 GRAIL",
            font=("Helvetica", 28, "bold"),
            bg=self.colors['bg_primary'],
            fg=self.colors['text']
        )
        title_label.pack(pady=15)
        
        subtitle_label = tk.Label(
            title_frame,
            text="Ваша цифровая святыня. Неприкосновенная. Локальная. Вечная.",
            font=("Helvetica", 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary']
        )
        subtitle_label.pack()
        
        # === ОСНОВНАЯ ОБЛАСТЬ ===
        main_frame = tk.Frame(self.root, bg=self.colors['bg_secondary'])
        main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # Поле ввода текста
        input_label = tk.Label(
            main_frame,
            text="📥 Вставьте текст для защиты:",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text']
        )
        input_label.pack(anchor='w', pady=(0, 5))
        
        self.text_input = scrolledtext.ScrolledText(
            main_frame,
            height=12,
            font=("Consolas", 10),
            bg='#2D3748',
            fg='#E2E8F0',
            insertbackground='white',
            selectbackground=self.colors['accent'],
            selectforeground='white'
        )
        self.text_input.pack(fill='both', expand=True, pady=(0, 10))
        
        # === КНОПКИ ===
        button_frame = tk.Frame(main_frame, bg=self.colors['bg_secondary'])
        button_frame.pack(fill='x', pady=10)
        
        self.btn_protect = tk.Button(
            button_frame,
            text="🛡️ ЗАЩИТИТЬ ДАННЫЕ",
            font=("Helvetica", 14, "bold"),
            bg=self.colors['accent'],
            fg=self.colors['text'],
            activebackground=self.colors['success'],
            activeforeground=self.colors['text'],
            cursor="hand2",
            command=self.protect_data,
            padx=20,
            pady=10
        )
        self.btn_protect.pack(side='left', padx=5)
        
        self.btn_clear = tk.Button(
            button_frame,
            text="🗑️ ОЧИСТИТЬ",
            font=("Helvetica", 12),
            bg='#4A5568',
            fg=self.colors['text'],
            activebackground='#2D3748',
            activeforeground=self.colors['text'],
            cursor="hand2",
            command=self.clear_fields,
            padx=15,
            pady=10
        )
        self.btn_clear.pack(side='left', padx=5)
        
        # === РЕЗУЛЬТАТ ===
        result_label = tk.Label(
            main_frame,
            text="🔒 Результат защиты:",
            font=("Helvetica", 12, "bold"),
            bg=self.colors['bg_secondary'],
            fg=self.colors['text']
        )
        result_label.pack(anchor='w', pady=(10, 5))
        
        self.text_output = scrolledtext.ScrolledText(
            main_frame,
            height=10,
            font=("Consolas", 10),
            bg='#1A202C',
            fg='#48BB78',
            state='disabled',
            wrap='word'
        )
        self.text_output.pack(fill='both', expand=True)
        
        # === СТАТУС ===
        self.status_label = tk.Label(
            main_frame,
            text="✅ Готов к работе",
            font=("Helvetica", 10),
            bg=self.colors['bg_primary'],
            fg=self.colors['text_secondary'],
            pady=5
        )
        self.status_label.pack(fill='x', pady=(10, 0))
    
    def protect_data(self):
        """Обрабатывает текст и защищает данные"""
        input_text = self.text_input.get("1.0", tk.END).strip()
        
        if not input_text:
            messagebox.showwarning("Внимание", "Пожалуйста, введите текст для защиты!")
            return
        
        try:
            # Обновляем статус
            self.status_label.config(text="🔄 Обработка...", fg=self.colors['warning'])
            self.root.update()
            
            # 1. Находим PII
            found_pii = self.detector.detect_pii(input_text)
            
            # 2. Заменяем PII
            protected_text = self.detector.redact_pii(input_text, replacement="[ЗАЩИЩЕНО]")
            
            # 3. Шифруем
            encrypted_data, data_hash = self.vault.secure_process(protected_text)
            
            # Показываем результат
            result = f"""
🔍 НАЙДЕНО ЛИЧНЫХ ДАННЫХ: {len(found_pii)}

📊 ДЕТАЛИ:
"""
            for item in found_pii:
                result += f"  • {item['type']}: {item['value']}\n"
            
            result += f"""
🛡️ ЗАЩИЩЕННЫЙ ТЕКСТ:
{protected_text}

🔐 ХЭШ ЦЕЛОСТНОСТИ:
{data_hash[:32]}...

✅ Данные успешно защищены и зашифрованы!
"""
            
            self.text_output.config(state='normal')
            self.text_output.delete("1.0", tk.END)
            self.text_output.insert(tk.END, result)
            self.text_output.config(state='disabled')
            
            self.status_label.config(text="✅ Защита завершена успешно!", fg=self.colors['success'])
            
            messagebox.showinfo("Успех", f"Найдено и защищено {len(found_pii)} элементов личных данных!")
            
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {str(e)}")
            self.status_label.config(text="❌ Ошибка обработки", fg='red')
    
    def clear_fields(self):
        """Очищает все поля"""
        self.text_input.delete("1.0", tk.END)
        self.text_output.config(state='normal')
        self.text_output.delete("1.0", tk.END)
        self.text_output.config(state='disabled')
        self.status_label.config(text="✅ Готов к работе", fg=self.colors['text_secondary'])


# === ЗАПУСК ПРИЛОЖЕНИЯ ===
if __name__ == "__main__":
    root = tk.Tk()
    app = GrailGUI(root)
    root.mainloop()
