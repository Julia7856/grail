"""
Grail Core - ядро шифрования.
AES-256-GCM с уникальным nonce для каждого сообщения.
Опциональный парольный режим: ключ выводится через PBKDF2-HMAC-SHA256
(600 000 итераций, рекомендация OWASP) — медленно для перебора.
"""

import os
import secrets
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag


class SecurityError(Exception):
    """Исключение при попытке вмешательства в данные"""
    pass


NONCE_SIZE = 12
SALT_SIZE = 16
PBKDF2_ITERATIONS = 600_000


class GrailVault:
    def __init__(self, password: str = None, salt: bytes = None):
        if password is not None:
            # Парольный режим: ключ выводится через PBKDF2 (медленно для перебора)
            self.salt = salt if salt is not None else os.urandom(SALT_SIZE)
            self.key = self._derive_key(password, self.salt)
        else:
            # Эфемерный режим: случайный ключ, только в RAM
            self.salt = None
            self.key = AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """PBKDF2-HMAC-SHA256, 600 000 итераций (OWASP)."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
        )
        return kdf.derive(password.encode('utf-8'))

    def secure_process(self, sensitive_data: str) -> tuple:
        """Шифрует текст. Возвращает (nonce+шифротекст, хэш целостности)."""
        if not sensitive_data:
            raise ValueError("Нет данных для обработки")

        nonce = os.urandom(NONCE_SIZE)
        plaintext = sensitive_data.encode('utf-8')
        encrypted = self.aesgcm.encrypt(nonce, plaintext, None)
        del plaintext

        packed = nonce + encrypted
        # Хэш считается по ВСЕМУ пакету (nonce + шифротекст)
        data_hash = hashlib.sha256(packed).hexdigest()
        return packed, data_hash

    def verify_and_decrypt(self, encrypted_data: bytes, expected_hash: str) -> str:
        """Проверяет целостность и расшифровывает."""
        actual_hash = hashlib.sha256(encrypted_data).hexdigest()
        if not secrets.compare_digest(actual_hash, expected_hash):
            raise SecurityError("ОБНАРУЖЕНО ВМЕШАТЕЛЬСТВО! Целостность данных нарушена.")

        nonce = encrypted_data[:NONCE_SIZE]
        ciphertext = encrypted_data[NONCE_SIZE:]

        try:
            return self.aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
        except InvalidTag:
            raise SecurityError("ОБНАРУЖЕНО ВМЕШАТЕЛЬСТВО! GCM-тег не совпадает.")


if __name__ == "__main__":
    print("🏆 Инициализация Grail Vault...")
    vault = GrailVault()

    secret = "Конфиденциально: проект Grail, доступ уровня Альфа."
    print(f"📥 Исходные данные: {secret}")

    encrypted, hash_val = vault.secure_process(secret)
    print(f"✅ Шифрование успешно. Хэш: {hash_val[:16]}...")

    # Два шифрования одного текста дают разные результаты (уникальный nonce)
    enc1, _ = vault.secure_process(secret)
    enc2, _ = vault.secure_process(secret)
    assert enc1 != enc2, "Nonce не уникален!"
    print("✅ Nonce уникален для каждого сообщения")

    decrypted = vault.verify_and_decrypt(encrypted, hash_val)
    print(f"🏆 Данные восстановлены: {decrypted}")

    print("\n🔑 Парольный режим (PBKDF2, 600 000 итераций):")
    vault_pw = GrailVault(password="Секретный пароль")
    enc_pw, hash_pw = vault_pw.secure_process(secret)

    # Новая сессия: тот же пароль + сохранённая соль
    vault_pw2 = GrailVault(password="Секретный пароль", salt=vault_pw.salt)
    print(f"🏆 Расшифровка в новой сессии: {vault_pw2.verify_and_decrypt(enc_pw, hash_pw)}")

    # Неправильный пароль не проходит
    try:
        bad_vault = GrailVault(password="неверный", salt=vault_pw.salt)
        bad_vault.verify_and_decrypt(enc_pw, hash_pw)
        print("❌ ОШИБКА: неверный пароль принят!")
    except SecurityError:
        print("✅ Неверный пароль отклонён (GCM-тег не совпадает)")
