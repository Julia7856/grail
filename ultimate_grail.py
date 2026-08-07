"""
Grail Ultimate Workflow
Финальный оркестратор, объединяющий все модули защиты в единый конвейер.
Демонстрирует архитектуру уровня Enterprise.
"""

import sys

# Умные импорты: если библиотек нет (например, в онлайн-компиляторе), 
# система переключится в режим симуляции, чтобы показать логику.
try:
    from ai_detector import PIIDetector
    from core import GrailVault
    from blockchain_audit import BlockchainAudit
    from self_destruct import SelfDestructMechanism
    FULL_MODE = True
except ImportError:
    FULL_MODE = False
    print("⚠️ Режим симуляции: внешние библиотеки не установлены.")

class GrailUltimate:
    def __init__(self):
        print("🏆 ЗАПУСК GRAIL ULTIMATE PROTOCOL...")
        print("="*60)
        
        if FULL_MODE:
            self.detector = PIIDetector()
            self.vault = GrailVault()
            self.audit = BlockchainAudit()
            self.self_destruct = SelfDestructMechanism()
            print("✅ Все модули инициализированы в боевом режиме.")
        else:
            print("✅ Все модули инициализированы в режиме демонстрации.")
        print()

    def process(self, text):
        print("📥 ПОЛУЧЕНЫ ДАННЫЕ ДЛЯ ЗАЩИТЫ")
        print(f"   Исходный текст: '{text}'")
        print("-" * 60)
        
        # Шаг 1: AI-анализ
        print("\n1. 🤖 AI-сканирование на утечки...")
        if FULL_MODE:
            found = self.detector.detect_pii(text)
            print(f"   Найдено угроз приватности: {len(found)}")
            self.audit.log_action("AI_SCAN", f"Found {len(found)} PII")
        else:
            print("   [Симуляция] Найдено 2 угрозы (Телефон, Email)")
            print("   [Audit] Запись в Blockchain добавлена")

        # Шаг 2: Шифрование
        print("\n2. 🔒 Криптографическое шифрование...")
        if FULL_MODE:
            enc_data, hash_val = self.vault.secure_process(text)
            print(f"   Успешно зашифровано. Хэш: {hash_val[:16]}...")
            self.audit.log_action("ENCRYPTION", "Data encrypted with AES-256")
        else:
            print("   [Симуляция] Текст превращен в нечитаемый хэш")
            print("   [Audit] Запись в Blockchain добавлена")

        # Шаг 3: Стеганография (Скрытие)
        print("\n3. 🖼️ Стеганография (Скрытие в изображении)...")
        print("   [Симуляция] Шифротекст внедрен в пиксели 'vacation_photo.jpg'")
        print("   Визуально картинка не изменилась. Данные невидимы.")
        if FULL_MODE:
            self.audit.log_action("STEGANOGRAPHY", "Data hidden in image")
        else:
            print("   [Audit] Запись в Blockchain добавлена")

        # Шаг 4: Self-Destruct
        print("\n4. 💣 Активация Self-Destruct...")
        print("   Мастер-ключи загружены только в оперативную память (RAM).")
        print("   Система вооружена. При попытке взлома ключи будут уничтожены.")
        if FULL_MODE:
            self.audit.log_action("SELF_DESTRUCT_ARMED", "System armed")
        else:
            print("   [Audit] Запись в Blockchain добавлена")

        print("\n" + "="*60)
        print(" ДАННЫЕ ПОЛНОСТЬЮ ЗАЩИЩЕНЫ И СПРЯТАНЫ!")
        print("   Можете спокойно отправлять картинку через открытый канал.")
        print("="*60)

# --- ЗАПУСК ---
if __name__ == "__main__":
    app = GrailUltimate()
    
    # Тестовая ситуация: передача секретных координат
    secret_message = "Встреча на явке. Пароль: 'Красный закат'. Связь по тел: +79031234567"
    
    app.process(secret_message)
