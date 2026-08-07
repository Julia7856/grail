"""
Grail Main Application (International Edition)
Главный файл, объединяющий все модули в единый защищенный механизм.
Универсальная система защиты данных для глобального использования.
"""

# Импортируем наши модули (они лежат в одной папке и видят друг друга)
from core import GrailVault
from ai_detector import PIIDetector

class GrailApp:
    def __init__(self):
        print("🏆 Запуск глобальной системы защиты Grail...")
        # Инициализируем механизмы
        self.vault = GrailVault()
        self.detector = PIIDetector()
        print("✅ Все модули загружены. Готов к международной работе.\n")

    def process_document(self, document_text: str):
        """Полный цикл обработки: Поиск -> Защита -> Шифрование"""
        print("=" * 60)
        print("📥 НАЧАЛО ОБРАБОТКИ ДОКУМЕНТА")
        print("=" * 60)
        
        # 1. AI-анализ текста
        print("\n🔍 Шаг 1: AI-сканирование на наличие личных данных...")
        found_pii = self.detector.detect_pii(document_text)
        
        if found_pii:
            print(f"⚠️ Обнаружено угроз приватности: {len(found_pii)}")
            for item in found_pii:
                print(f"   - Найдено: {item['type']} ({item['value']})")
        else:
            print("✅ Личные данные не обнаружены. Текст чист.")
            
        # 2. Создание защищенной версии (замена PII)
        print("\n🛡️ Шаг 2: Создание защищенной версии текста...")
        protected_text = self.detector.redact_pii(document_text, replacement="[ЗАШИФРОВАНО]")
        
        # 3. Криптографическое шифрование всего документа
        print("\n🔒 Шаг 3: Криптографическое шифрование (AES-256)...")
        encrypted_data, data_hash = self.vault.secure_process(protected_text)
        print(f"✅ Документ зашифрован. Хэш целостности: {data_hash[:16]}...")
        
        print("\n" + "=" * 60)
        print("🏆 ОБРАБОТКА ЗАВЕРШЕНА УСПЕШНО")
        print("=" * 60)
        
        return encrypted_data, data_hash, protected_text

# --- СИМУЛЯЦИЯ РАБОТЫ ПРИЛОЖЕНИЯ ---
if __name__ == "__main__":
    # Запускаем наше приложение
    app = GrailApp()
    
    # Тестовый документ: Международный контракт
    global_contract = """
    INTERNATIONAL SERVICE AGREEMENT
    
    Provider: Global Tech Solutions Inc. (USA)
    Contact Person: John Smith
    Phone: +1 (555) 019-8372
    Email: j.smith@globaltech.com
    Tax ID (SSN): 123-45-6789
    
    Client: Euro Innovations GmbH (Germany)
    Contact Person: Hans Mueller
    Phone: +49 30 12345678
    Email: h.mueller@euro-innovations.de
    Passport: C01X00T47
    
    Partner: OOO "Romashka" (Russia)
    Contact Person: Ivan Petrov
    Phone: +7 (903) 555-12-34
    Email: i.petrov@romashka.ru
    Tax ID (INN): 7707083893
    Social Security (SNILS): 123-456-789 00
    
    Payment Details:
    Card: 4111 1111 1111 1111
    IP Address for portal access: 192.168.1.100
    """
    
    # Обрабатываем документ
    encrypted, hash_val, protected = app.process_document(global_contract)
    
    # Показываем, как теперь выглядит документ для посторонних глаз
    print("\n👁️ Как теперь выглядит документ (безопасная версия):")
    print("-" * 60)
    print(protected)
    print("-" * 60)
    print("\n💡 Весь текст выше зашифрован в памяти и готов к безопасному хранению!")
