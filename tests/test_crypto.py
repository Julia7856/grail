"""Тесты криптографических модулей."""
import pytest
from core import GrailVault, SecurityError
from quantum_core import QuantumGrailVault


def test_roundtrip():
    vault = GrailVault()
    secret = "Секретный текст проекта Grail"
    packed, hash_val = vault.secure_process(secret)
    assert vault.verify_and_decrypt(packed, hash_val) == secret


def test_unique_nonce():
    vault = GrailVault()
    enc1, _ = vault.secure_process("один и тот же текст")
    enc2, _ = vault.secure_process("один и тот же текст")
    assert enc1 != enc2


def test_tamper_detection():
    vault = GrailVault()
    packed, hash_val = vault.secure_process("данные")
    tampered = bytearray(packed)
    tampered[-1] ^= 0xFF
    with pytest.raises(SecurityError):
        vault.verify_and_decrypt(bytes(tampered), hash_val)


def test_empty_data_raises():
    vault = GrailVault()
    with pytest.raises(ValueError):
        vault.secure_process("")


def test_quantum_roundtrip():
    vault = QuantumGrailVault()
    secret = "Квантовые данные"
    packed, hash_val = vault.quantum_secure_process(secret)
    assert vault.verify_and_decrypt(packed, hash_val) == secret
