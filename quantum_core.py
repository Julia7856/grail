"""
Grail Quantum-Ready Core (Placeholder)
В v1.0: AES-256-GCM. Пост-квантовый Kyber-1024 запланирован в v1.1.
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


class QuantumGrailVault:
    def __init__(self):
        self.aes_key = AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.aes_key)

    def quantum_secure_process(self, sensitive_data: str) -> tuple:
        """Шифрует текст. Возвращает (nonce+шифротекст, хэш целостности)."""
        if not sensitive_data:
            raise ValueError("Нет данных для обработки")

        nonce = os.urandom(NONCE_SIZE)
        plaintext = sensitive_data.encode('utf-8')
        encrypted_data = self.aesgcm.encrypt(nonce, plaintext, None)
        del plaintext

        packed = nonce + encrypted_data
        # Хэш по ВСЕМУ пакету (nonce + шифротекст)
        data_hash = hashlib.sha256(packed).hexdigest()
        return packed, data_hash

    def verify_and_decrypt(self, encrypted_data: bytes, expected_hash: str) -> str:
        """Проверяет целостность и расшифровывает."""
        actual_hash = hashlib.sha256(encrypted_data).hexdigest()
        if not secrets.compare_digest(actual_hash, expected_hash):
            raise SecurityError("ОБНАРУЖЕНО ВМЕШАТЕЛЬСТВО! Данные повреждены.")

        nonce = encrypted_data[:NONCE_SIZE]
        ciphertext = encrypted_data[NONCE_SIZE:]

        try:
            return self.aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
        except InvalidTag:
            raise SecurityError("ОБНАРУЖЕНО ВМЕШАТЕЛЬСТВО! GCM-тег не совпадает.")


if __name__ == "__main__":
    print("🔐 Инициализация Grail Vault...")
    vault = QuantumGrailVault()

    secret_info = "Секретные данные проекта Grail."
    print(f"📥 Исходные данные: {secret_info}")
    encrypted, hash_val = vault.quantum_secure_process(secret_info)
    print("✅ Шифрование успешно!")
    decrypted = vault.verify_and_decrypt(encrypted, hash_val)
    print(f"🏆 Данные восстановлены: {decrypted}")
