"""
Grail Core - ядро шифрования.
AES-256-GCM с уникальным nonce для каждого сообщения.
"""

import os
import secrets
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag


class SecurityError(Exception):
    """Исключение при попытке вмешательства в данные"""
    pass


NONCE_SIZE = 12


class GrailVault:
    def __init__(self):
        # Ключ AES-256 (хранится только в RAM)
        self.key = AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    def secure_process(self, sensitive_data: str) -> tuple:
        """Шифрует текст. Возвращает (nonce+шифротекст, хэш целостности)."""
        if not sensitive_data:
            raise ValueError("Нет данных для обработки")

        nonce = os.urandom(NONCE_SIZE)
        plaintext = sensitive_data.encode('utf-8')
        encrypted = self.aesgcm.encrypt(nonce, plaintext, None)
        del plaintext

        packed = nonce + encrypted
        # Хэш считается по ВСЕМУ пакуету (nonce + шифротекст)
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
