"""
Grail Core - encryption core.
AES-256-GCM with a unique nonce per message.
Optional password mode: key derived via PBKDF2-HMAC-SHA256
(600,000 iterations, OWASP recommendation) - slow to brute-force.

Grail Core - ядро шифрования.
AES-256-GCM с уникальным nonce для каждого сообщения.
Опциональный парольный режим: ключ выводится через PBKDF2-HMAC-SHA256
(600 000 итераций, рекомендация OWASP) - медленно для перебора.
"""

import os
import secrets
import hashlib
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from cryptography.exceptions import InvalidTag


class SecurityError(Exception):
    """Raised on data tampering attempt.
    Исключение при попытке вмешательства в данные."""
    pass


NONCE_SIZE = 12
SALT_SIZE = 16
PBKDF2_ITERATIONS = 600_000


class GrailVault:
    def __init__(self, password: str = None, salt: bytes = None):
        if password is not None:
            # Password mode: key derived via PBKDF2 (slow to brute-force)
            # Парольный режим: ключ выводится через PBKDF2 (медленно для перебора)
            self.salt = salt if salt is not None else os.urandom(SALT_SIZE)
            self.key = self._derive_key(password, self.salt)
        else:
            # Ephemeral mode: random key, RAM only
            # Эфемерный режим: случайный ключ, только в RAM
            self.salt = None
            self.key = AESGCM.generate_key(bit_length=256)
        self.aesgcm = AESGCM(self.key)

    @staticmethod
    def _derive_key(password: str, salt: bytes) -> bytes:
        """PBKDF2-HMAC-SHA256, 600,000 iterations (OWASP).
        PBKDF2-HMAC-SHA256, 600 000 итераций (OWASP)."""
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=PBKDF2_ITERATIONS,
        )
        return kdf.derive(password.encode('utf-8'))

    def secure_process(self, sensitive_data: str) -> tuple:
        """Encrypts text. Returns (nonce+ciphertext, integrity hash).
        Шифрует текст. Возвращает (nonce+шифротекст, хэш целостности)."""
        if not sensitive_data:
            raise ValueError("No data to process / Нет данных для обработки")

        nonce = os.urandom(NONCE_SIZE)
        plaintext = sensitive_data.encode('utf-8')
        encrypted = self.aesgcm.encrypt(nonce, plaintext, None)
        del plaintext

        packed = nonce + encrypted
        # Hash is computed over the WHOLE package (nonce + ciphertext)
        # Хэш считается по ВСЕМУ пакету (nonce + шифротекст)
        data_hash = hashlib.sha256(packed).hexdigest()
        return packed, data_hash

    def verify_and_decrypt(self, encrypted_data: bytes, expected_hash: str) -> str:
        """Verifies integrity and decrypts.
        Проверяет целостность и расшифровывает."""
        actual_hash = hashlib.sha256(encrypted_data).hexdigest()
        if not secrets.compare_digest(actual_hash, expected_hash):
            raise SecurityError("TAMPERING DETECTED! / ОБНАРУЖЕНО ВМЕШАТЕЛЬСТВО!")

        nonce = encrypted_data[:NONCE_SIZE]
        ciphertext = encrypted_data[NONCE_SIZE:]

        try:
            return self.aesgcm.decrypt(nonce, ciphertext, None).decode('utf-8')
        except InvalidTag:
            raise SecurityError("TAMPERING DETECTED! GCM tag mismatch. / ОБНАРУЖЕНО ВМЕШАТЕЛЬСТВО! GCM-тег не совпадает.")


if __name__ == "__main__":
    print("🏆 Initializing Grail Vault...")
    vault = GrailVault()

    secret = "Confidential: Grail project, Alpha clearance."
    print(f"📥 Original data: {secret}")

    encrypted, hash_val = vault.secure_process(secret)
    print(f"✅ Encryption successful. Hash: {hash_val[:16]}...")

    # Two encryptions of the same text give different results (unique nonce)
    # Два шифрования одного текста дают разные результаты (уникальный nonce)
    enc1, _ = vault.secure_process(secret)
    enc2, _ = vault.secure_process(secret)
    assert enc1 != enc2, "Nonce is not unique!"
    print("✅ Nonce is unique per message")

    decrypted = vault.verify_and_decrypt(encrypted, hash_val)
    print(f"🏆 Data restored: {decrypted}")

    print("\n🔑 Password mode (PBKDF2, 600,000 iterations):")
    vault_pw = GrailVault(password="Secret password")
    enc_pw, hash_pw = vault_pw.secure_process(secret)

    # New session: same password + stored salt
    # Новая сессия: тот же пароль + сохранённая соль
    vault_pw2 = GrailVault(password="Secret password", salt=vault_pw.salt)
    print(f"🏆 Decryption in a new session: {vault_pw2.verify_and_decrypt(enc_pw, hash_pw)}")

    # Wrong password must fail
    # Неправильный пароль должен быть отклонён
    try:
        bad_vault = GrailVault(password="wrong", salt=vault_pw.salt)
        bad_vault.verify_and_decrypt(enc_pw, hash_pw)
        print("❌ ERROR: wrong password accepted!")
    except SecurityError:
        print("✅ Wrong password rejected (GCM tag mismatch)")
