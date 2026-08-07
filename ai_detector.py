"""
Grail AI PII Detector
Автоматически находит личные данные в тексте и защищает их.
Работает локально, без отправки данных в интернет.
"""

import re
from typing import List, Dict, Tuple

class PIIDetector:
    """Детектор персональных данных"""
    
    def __init__(self):
        # Паттерны для поиска PII
        self.patterns = {
            'phone': r'(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'card': r'\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}',
            'passport': r'\d{2}\s*\d{2}\s*\d{6}',
            'inn': r'\d{10}|\d{12}',
            'snils': r'\d{3}[\s\-]?\d{3}[\s\-]?\d{3}[\s\-]?\d{2}',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'date_of_birth': r'\b\d{2}[./]\d{2}[./]\d{4}\b'
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
        
        # Сортируем по позиции в тексте
        found_items.sort(key=lambda x: x['start'])
        
        return found_items
    
    def redact_pii(self, text: str, replacement: str = '[ЗАЩИЩЕНО]') -> str:
        """Заменяет все найденные PII на placeholder"""
        items = self.detect_pii(text)
        
        # Заменяем с конца, чтобы не сдвигать позиции
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
    print("🤖 Инициализация Grail AI PII Detector...")
    detector = PIIDetector()
    
    sample_text = """
    Контактная информация клиента:
    Телефон: +7 (903) 123-45-67
    Email: ivan.petrov@example.com
    Паспорт: 45 10 123456
    СНИЛС: 123-456-789 01
    Дата рождения: 15.03.1985
    IP адрес: 192.168.1.100
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
    
    print("\n🏆 AI-детектор Grail готов к работе!")
