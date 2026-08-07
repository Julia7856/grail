"""
Grail AI PII Detector (International Edition)
Автоматически находит личные данные в тексте и защищает их.
Работает локально, без отправки данных в интернет.
Универсальная система для всех стран мира.
"""

import re
from typing import List, Dict

class PIIDetector:
    """Детектор персональных данных (международный)"""
    
    def __init__(self):
        # Паттерны для поиска PII с универсальными названиями
        self.patterns = {
            # === ТЕЛЕФОНЫ ===
            'phone': r'(?:\+7|8|\+\d{1,3})[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,9}',
            
            # === EMAIL ===
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            
            # === БАНКОВСКИЕ КАРТЫ ===
            'card_16': r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
            'card_15': r'\b\d{4}[\s\-]?\d{6}[\s\-]?\d{5}\b',
            'card_universal': r'\b\d{13,19}\b',
            
            # === ПАСПОРТА И УДОСТОВЕРЕНИЯ ЛИЧНОСТИ ===
            'passport_national': r'\b\d{2}\s*\d{2}\s*\d{6}\b',  # РФ формат
            'passport_us': r'\b\d{9}\b',  # США
            'passport_eu': r'\b[A-Z]{2}\d{7,9}\b',  # ЕС
            'passport_universal': r'\b\d{8,12}\b',
            
            # === НАЛОГОВЫЕ ИДЕНТИФИКАТОРЫ ===
            'tax_id': r'\b\d{10}\b|\b\d{12}\b',  # ИНН РФ и аналоги
            'ssn_us': r'\b\d{3}[\s\-]?\d{2}[\s\-]?\d{4}\b',  # SSN США
            'nino_uk': r'\b[A-Z]{2}\s*\d{2}\s*\d{2}\s*\d{2}\s*[A-Z]\b',  # UK
            'tax_id_universal': r'\b\d{6,12}\b',
            
            # === СОЦИАЛЬНЫЕ СТРАХОВЫЕ НОМЕРА ===
            'social_security': r'\b\d{3}[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}\b',  # СНИЛС РФ
            
            # === IP-АДРЕСА ===
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'ip_address_v6': r'\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b',
            
            # === ДАТЫ РОЖДЕНИЯ ===
            'date_of_birth': r'\b\d{2}[./]\d{2}[./]\d{4}\b',
            
            # === ПОЧТОВЫЕ ИНДЕКСЫ ===
            'postal_code': r'\b\d{5,6}\b',  # Универсальный
            'postal_code_us': r'\b\d{5}(?:-\d{4})?\b',  # США
            'postal_code_uk': r'\b[A-Z]{1,2}\d[A-Z\d]?\s*\d[A-Z]{2}\b',  # UK
        }
    
    def detect_pii(self, text: str) -> List[Dict]:
        """Находит все PII в тексте"""
        found_items = []
        
        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                found_items.append({
                    'type': pii_type,
                    'value': match.group(),
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.95
                })
        
        # Удаляем дубликаты
        seen = set()
        unique_items = []
        for item in found_items:
            if item['value'] not in seen:
                seen.add(item['value'])
                unique_items.append(item)
        
        # Сортируем по позиции
        unique_items.sort(key=lambda x: x['start'])
        
        return unique_items
    
    def redact_pii(self, text: str, replacement: str = '[ЗАЩИЩЕНО]') -> str:
        """Заменяет все найденные PII на placeholder"""
        items = self.detect_pii(text)
        
        for item in reversed(items):
            text = text[:item['start']] + replacement + text[item['end']:]
        
        return text
    
    def get_statistics(self, text: str) -> Dict:
        """Статистика найденных PII"""
        items = self.detect_pii(text)
        
        stats = {
            'total_found': len(items),
            'by_type': {}
        }
        
        for item in items:
            pii_type = item['type']
            stats['by_type'][pii_type] = stats['by_type'].get(pii_type, 0) + 1
        
        return stats

# --- ДЕМОНСТРАЦИЯ РАБОТЫ ---
if __name__ == "__main__":
    print(" Инициализация Grail AI PII Detector (International)...")
    detector = PIIDetector()
    
    sample_text = """
    Международная база клиентов Grail:
    
    Клиент 1 (Россия):
    Телефон: +7 (903) 123-45-67
    Email: ivan.petrov@example.com
    Паспорт: 45 10 123456
    Социальный номер: 123-456-789 01
    Налоговый ID: 7707083893
    Почтовый индекс: 101000
    Дата рождения: 15.03.1985
    
    Клиент 2 (США):
    Телефон: +1 (555) 234-5678
    Email: john.smith@company.com
    SSN: 123-45-6789
    Почтовый индекс: 90210
    Банковская карта: 4111 1111 1111 1111
    IP адрес: 192.168.1.100
    
    Клиент 3 (Великобритания):
    Телефон: +44 20 7946 0958
    Email: james.bond@mi6.gov.uk
    NINO: AB 12 34 56 C
    Почтовый индекс: SW1A 1AA
    
    Клиент 4 (Германия):
    Телефон: +49 30 12345678
    Email: hans.mueller@firma.de
    Паспорт: C01X00T47
    Банковская карта: 5500 0000 0000 0004
    """
    
    print(f"\n📥 Исходный текст:\n{sample_text}")
    
    # Находим PII
    found = detector.detect_pii(sample_text)
    print(f"\n🔍 Найдено {len(found)} элементов PII:")
    for item in found:
        print(f"  - {item['type']}: {item['value']}")
    
    # Статистика
    stats = detector.get_statistics(sample_text)
    print(f"\n📊 Статистика: {stats}")
    
    # Защищаем текст
    protected = detector.redact_pii(sample_text)
    print(f"\n🛡️ Защищенный текст:\n{protected}")
    
    print("\n🏆 Grail International готов к работе!")
