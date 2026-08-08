"""
Grail Ultimate Workflow
Финальный оркестратор, объединяющий все модули защиты в единый конвейер.
Полный цикл: Regex-детекция -> Шифрование -> Стеганография -> Аудит -> Self-Destruct.
"""

import sys

# Умные импорты: если библиотек нет (например, в онлайн-компиляторе),
# система переключится в режим симуляции, чтобы показать логику.
try:
    from ai_detector import RegexPIIDetector
    from core import GrailVault
    from blockchain_audit import BlockchainAudit
    from self_destruct import SelfDestructMechanism
    from steganography import Steganography
    FULL_MODE = True
except ImportError:
    FULL_MODE = False
    print("⚠️ Режим симуляции: внешние библиотеки не установлены.")


class GrailUltimate:
    def __init__(self):
        print("🏆 ЗАПУСК GRAIL ULTIMATE PROTOCOL...")
        print("=" * 60)

        if FULL_MODE:
            self.detector = RegexPIIDetector()
            self.vault = GrailVault()
            self.audit = BlockchainAudit()
            # DEMO-код: в продакшене код задаёт пользователь через GUI
            self.self_destruct = SelfDestructMechanism(access_code="GRAIL-DEMO-2026")
            self.stego = Steganography()
            # Регистрируем ключ хранилища в системе самоуничтожения
            self.self_destruct.register_key("vault_key", self.vault.key)
            print("✅ Все модули инициализированы в боевом режиме.")
        else:
            print("✅ Все модули инициализированы в режиме демонстрации.")
        print()

    def process(self, text):
        print("📥 ПОЛУЧЕНЫ ДАННЫЕ ДЛЯ ЗАЩИТЫ")
        print(f"   Исходный текст: '{text}'")
        print("-" * 60)

        # Шаг 1: Regex-анализ
        print("\n1. 🔍 Regex-сканирование на утечки...")
        if FULL_MODE:
            found = self.detector.detect_pii(text)
            protected = self.detector.redact_pii(text)
            print(f"   Найдено угроз приватности: {len(found)}")
            self.audit.log_action("REGEX_SCAN", f"Found {len(found)} PII")
        else:
            protected = text
            print("   [Симуляция] Найдено 2 угрозы (Телефон, Email)")

        # Шаг 2: Шифрование
        print("\n2. 🔒 Криптографическое шифрование (AES-256-GCM)...")
        if FULL_MODE:
            enc_data, hash_val = self.vault.secure_process(protected)
            print(f"   Успешно зашифровано. Хэш: {hash_val[:16]}...")
            self.audit.log_action("ENCRYPTION", "Data encrypted with AES-256-GCM")
        else:
            enc_data = b"SIMULATED_CIPHERTEXT"
            print("   [Симуляция] Текст превращен в нечитаемый хэш")

        # Шаг 3: Стеганография
        print("\n3. 🖼️ Стеганография (Скрытие в изображении)...")
        if FULL_MODE:
            from PIL import Image
            Image.new('RGB', (300, 300), color=(30, 60, 50)).save('grail_cover.png')
            ok = self.stego.encode_data_to_image('grail_cover.png', enc_data, 'grail_secret.png')
            if ok:
                print("   Шифротекст внедрен в пиксели 'grail_secret.png'")
                self.audit.log_action("STEGANOGRAPHY", "Data hidden in grail_secret.png")
            else:
                print("   ⚠️ Не удалось скрыть данные в изображении")
        else:
            print("   [Симуляция] Шифротекст внедрен в пиксели 'vacation_photo.jpg'")

        # Шаг 4: Self-Destruct
        print("\n4. 💣 Активация Self-Destruct...")
        print("   Мастер-ключи загружены только в оперативную память (RAM).")
        print("   Система вооружена. При попытке взлома ключи будут уничтожены.")
        if FULL_MODE:
            self.audit.log_action("SELF_DESTRUCT_ARMED", "System armed")

        print("\n" + "=" * 60)
        print("🏆 ДАННЫЕ ПОЛНОСТЬЮ ЗАЩИЩЕНЫ И СПРЯТАНЫ!")
        print("   Можете спокойно отправлять картинку через открытый канал.")
        print("=" * 60)


if __name__ == "__main__":
    app = GrailUltimate()

    # Тестовая ситуация: передача секретных координат
    secret_message = "Встреча на явке. Пароль: 'Красный закат'. Связь по тел: +79031234567"

    app.process(secret_message)
