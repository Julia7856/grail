"""
Grail Core Module
Локальное криптографически стойкое ядро. Без интернета.
"""
import os
import secrets
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.exceptions import InvalidTag

class SecurityError(Exception):
    """Исключение при попытке вмешательства в данные"""
    pass

NONCE_SIZE = 12  # 96 бит — стандарт GCM

class GrailVault:
    def __init__(self, key: bytes = None):
        # Ключ 256 бит из CSPRNG; внешний ключ можно передать (для persistence/self_destruct)
        self.key = key or AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    def secure_process(self, sensitive_data: str) -> tuple:
        """Шифрует данные. НОВЫЙ nonce на каждое сообщение — критично для GCM."""
        if not sensitive_data:
            raise ValueError("Нет данных для обработки")

        nonce = os.urandom(NONCE_SIZE)
        plaintext = sensitive_data.encode('utf-8')
        encrypted_data = self.aesgcm.encrypt(nonce, plaintext, None)
        del plaintext  # best-effort: см. docs/threat-model (Python не даёт полной гарантии)

        data_hash = hashlib.sha256(encrypted_data).hexdigest()
        # nonce пакуется ВМЕСТЕ с шифртекстом: расшифровка не зависит от состояния объекта
        return nonce + encrypted_data, data_hash

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

    secret_info = "Конфиденциально: проект Grail, доступ уровня Alpha."
    print(f"📥 Исходные данные: {secret_info}")

    encrypted, hash_val = vault.secure_process(secret_info)
    # второе сообщение — демонстрация, что nonce теперь уникальный
    encrypted2, _ = vault.secure_process("Второй секрет")
    assert encrypted[:NONCE_SIZE] != encrypted2[:NONCE_SIZE], "nonce повторился!"

    decrypted = vault.verify_and_decrypt(encrypted, hash_val)
    print(f"✅ Успешно восстановлено: {decrypted}")
    print("🎉 Ядро Grail готово к работе!")
