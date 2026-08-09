"""
Grail PII Detector (Regex-based + optional Presidio NER)
Автоматически находит личные данные через регулярные выражения.
Если установлен Microsoft Presidio — дополнительно включается NER-детекция.
Локально, без интернета.
"""

import re
from typing import List, Dict

try:
    from presidio_analyzer import AnalyzerEngine
    PRESIDIO_AVAILABLE = True
except ImportError:
    PRESIDIO_AVAILABLE = False


def luhn_check(card_number: str) -> bool:
    """Проверка банковской карты по алгоритму Луна"""
    digits = [int(d) for d in card_number.replace(' ', '').replace('-', '')]
    if len(digits) < 13 or len(digits) > 19:
        return False

    total = 0
    reverse_digits = digits[::-1]
    for i, d in enumerate(reverse_digits):
        if i % 2 == 1:
            d *= 2
            if d > 9:
                d -= 9
        total += d
    return total % 10 == 0


class RegexPIIDetector:
    """Детектор PII на основе регулярных выражений (без AI)"""

    def __init__(self):
        self.patterns = {
            'phone': r'(?:\+7|8|\+\d{1,3})[\s\-]?\(?\d{1,4}\)?[\s\-]?\d{1,4}[\s\-]?\d{1,9}',
            'email': r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}',
            'card_16': r'\b\d{4}[\s\-]?\d{4}[\s\-]?\d{4}[\s\-]?\d{4}\b',
            'card_15': r'\b\d{4}[\s\-]?\d{6}[\s\-]?\d{5}\b',
            'passport_ru': r'\b\d{2}\s*\d{2}\s*\d{6}\b',
            'passport_us': r'\b\d{9}\b',
            'ssn_us': r'\b\d{3}[\s\-]?\d{2}[\s\-]?\d{4}\b',
            'nino_uk': r'\b[A-Z]{2}\s*\d{2}\s*\d{2}\s*\d{2}\s*[A-Z]\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
            'date_of_birth': r'\b\d{2}[./]\d{2}[./]\d{4}\b',
        }

    def detect_pii(self, text: str) -> List[Dict]:
        """Находит PII с базовой валидацией"""
        found_items = []

        for pii_type, pattern in self.patterns.items():
            matches = re.finditer(pattern, text)
            for match in matches:
                value = match.group()

                # Валидация карт по Luhn
                if pii_type.startswith('card_'):
                    if not luhn_check(value):
                        continue

                found_items.append({
                    'type': pii_type,
                    'value': value,
                    'start': match.start(),
                    'end': match.end(),
                })

        seen = set()
        unique_items = []
        for item in found_items:
            if item['value'] not in seen:
                seen.add(item['value'])
                unique_items.append(item)

        unique_items.sort(key=lambda x: x['start'])
        return unique_items

    def redact_pii(self, text: str, replacement: str = '[ЗАЩИЩЕНО]') -> str:
        """Заменяет PII на placeholder"""
        items = self.detect_pii(text)
        for item in reversed(items):
            text = text[:item['start']] + replacement + text[item['end']:]
        return text

    def get_statistics(self, text: str) -> Dict:
        """Статистика найденных PII"""
        items = self.detect_pii(text)
        stats = {'total_found': len(items), 'by_type': {}}
        for item in items:
            pii_type = item['type']
            stats['by_type'][pii_type] = stats['by_type'].get(pii_type, 0) + 1
        return stats


class SmartPIIDetector:
    """Regex-детектор + Presidio NER (если установлен)"""

    def __init__(self):
        self.regex = RegexPIIDetector()
        self.analyzer = None
        if PRESIDIO_AVAILABLE:
            try:
                self.analyzer = AnalyzerEngine()
            except Exception:
                self.analyzer = None

    @property
    def presidio_active(self) -> bool:
        return self.analyzer is not None

    @staticmethod
    def _overlaps(a: Dict, b: Dict) -> bool:
        return a['start'] < b['end'] and b['start'] < a['end']

    def detect_pii(self, text: str) -> List[Dict]:
        """Regex + NER без дубликатов"""
        items = self.regex.detect_pii(text)
        if self.analyzer is not None:
            try:
                results = self.analyzer.analyze(text=text, language="en")
            except Exception:
                results = []
            for r in results:
                finding = {
                    'type': f"ner_{r.entity_type.lower()}",
                    'value': text[r.start:r.end],
                    'start': r.start,
                    'end': r.end,
                }
                if not any(self._overlaps(finding, i) for i in items):
                    items.append(finding)
            items.sort(key=lambda x: x['start'])
        return items

    def redact_pii(self, text: str, replacement: str = '[ЗАЩИЩЕНО]') -> str:
        items = self.detect_pii(text)
        for item in reversed(items):
            text = text[:item['start']] + replacement + text[item['end']:]
        return text

    def get_statistics(self, text: str) -> Dict:
        items = self.detect_pii(text)
        stats = {'total_found': len(items), 'by_type': {}}
        for item in items:
            pii_type = item['type']
            stats['by_type'][pii_type] = stats['by_type'].get(pii_type, 0) + 1
        return stats


if __name__ == "__main__":
    print("🔍 Инициализация Grail PII Detector...")
    detector = SmartPIIDetector()
    if detector.presidio_active:
        print("✅ Presidio активен: NER-детекция включена")
    else:
        print("ℹ️ Presidio не установлен — работает regex-детекция")

    sample_text = """
    Клиент 1 (Россия):
    Телефон: +7 (903) 123-45-67
    Email: ivan.petrov@example.com
    Паспорт: 45 10 123456
    Банковская карта: 4111 1111 1111 1111

    Клиент 2 (США):
    My name is John Smith.
    SSN: 123-45-6789
    Карта: 5500 0000 0000 0004
    """

    print(f"\n📥 Исходный текст:\n{sample_text}")

    found = detector.detect_pii(sample_text)
    print(f"\n🔍 Найдено {len(found)} элементов PII:")
    for item in found:
        print(f"  - {item['type']}: {item['value']}")

    protected = detector.redact_pii(sample_text)
    print(f"\n🛡️ Защищенный текст:\n{protected}")
    print("\n🏆 Grail PII Detector готов к работе!")
