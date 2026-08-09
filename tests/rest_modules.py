"""Тесты детектора PII и блокчейн-аудита."""
import os

from ai_detector import RegexPIIDetector, luhn_check
from blockchain_audit import BlockchainAudit

AUDIT_FILE = "grail_audit.json"


def _clean_audit_file():
    if os.path.exists(AUDIT_FILE):
        os.remove(AUDIT_FILE)


def test_luhn_valid_card():
    assert luhn_check("4111 1111 1111 1111") is True


def test_luhn_invalid_card():
    assert luhn_check("4111 1111 1111 1112") is False


def test_detect_email():
    detector = RegexPIIDetector()
    found = detector.detect_pii("Почта: ivan.petrov@example.com")
    assert any(item['type'] == 'email' for item in found)


def test_detect_phone():
    detector = RegexPIIDetector()
    found = detector.detect_pii("Телефон: +7 (903) 123-45-67")
    assert any(item['type'] == 'phone' for item in found)


def test_redact_removes_pii():
    detector = RegexPIIDetector()
    text = "Email: a@b.com"
    protected = detector.redact_pii(text)
    assert "a@b.com" not in protected
    assert "[ЗАЩИЩЕНО]" in protected


def test_blockchain_integrity():
    _clean_audit_file()
    chain = BlockchainAudit()
    chain.log_action("TEST", "проверка")
    assert len(chain.chain) == 2
    assert chain.verify_chain() is True
    _clean_audit_file()


def test_blockchain_persistence():
    _clean_audit_file()
    first = BlockchainAudit()
    first.log_action("TEST", "проверка")
    second = BlockchainAudit()
    assert len(second.chain) == len(first.chain)
    _clean_audit_file()


def test_blockchain_tamper_detection():
    _clean_audit_file()
    chain = BlockchainAudit()
    chain.log_action("TEST", "данные")
    chain.chain[1].data = "ВЗЛОМАНО"
    assert chain.verify_chain() is False
    _clean_audit_file()
