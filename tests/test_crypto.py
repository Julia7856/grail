"""Tests for cryptographic modules.
Тесты криптографических модулей."""
import os
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


def test_password_mode_roundtrip():
    """Password mode: same password + salt decrypts correctly.
    Парольный режим: тот же пароль + соль расшифровывают корректно."""
    password = "test_password_123"
    vault1 = GrailVault(password=password)
    secret = "Password-protected secret"
    packed, hash_val = vault1.secure_process(secret)

    vault2 = GrailVault(password=password, salt=vault1.salt)
    assert vault2.verify_and_decrypt(packed, hash_val) == secret


def test_password_mode_different_passwords():
    """Different passwords produce different keys.
    Разные пароли дают разные ключи."""
    vault1 = GrailVault(password="password1")
    vault2 = GrailVault(password="password2")
    assert vault1.key != vault2.key


def test_password_mode_wrong_password_fails():
    """Wrong password cannot decrypt.
    Неверный пароль не может расшифровать."""
    vault1 = GrailVault(password="correct_password")
    secret = "Secret data"
    packed, hash_val = vault1.secure_process(secret)

    vault_wrong = GrailVault(password="wrong_password", salt=vault1.salt)
    with pytest.raises(SecurityError):
        vault_wrong.verify_and_decrypt(packed, hash_val)


def test_password_mode_salt_persistence():
    """Salt can be saved and reused across sessions.
    Соль можно сохранить и использовать в новых сессиях."""
    password = "persistent_password"
    salt = os.urandom(16)

    vault1 = GrailVault(password=password, salt=salt)
    secret = "Persistent secret"
    packed, hash_val = vault1.secure_process(secret)

    # Simulate new session with saved salt
    # Имитация новой сессии с сохранённой солью
    vault2 = GrailVault(password=password, salt=salt)
    assert vault2.verify_and_decrypt(packed, hash_val) == secret
    assert vault1.key == vault2.key
