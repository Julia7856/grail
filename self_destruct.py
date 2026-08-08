"""
Grail Self-Destruct Mechanism
Автоматическое уничтожение ключей при обнаружении угроз.
Код доступа хранится только как хэш (SHA-256), никогда в открытом виде.
"""

import gc
import hashlib
import secrets
from datetime import datetime, timedelta, timezone
from typing import Optional, Callable


class SelfDestructMechanism:
    """Система самоуничтожения ключей"""

    def __init__(self, access_code: Optional[str] = None):
        # Ключи шифрования (хранятся ТОЛЬКО в RAM)
        self.encryption_keys = {}
        self.master_key = secrets.token_bytes(32)

        # Код доступа храним ТОЛЬКО как хэш
        self._access_hash: Optional[bytes] = (
            hashlib.sha256(access_code.encode("utf-8")).digest()
            if access_code
            else None
        )

        # Триггеры самоуничтожения
        self.max_failed_attempts = 3
        self.failed_attempts = 0
        self.last_failed_attempt: Optional[datetime] = None
        self.inactivity_timeout = timedelta(minutes=30)
        self.last_activity: datetime = datetime.now(timezone.utc)

        # Флаги
        self.is_self_destructed = False
        self.destruction_callbacks: list[Callable] = []

        print("💣 Self-Destruct механизм активирован")

    def set_access_code(self, access_code: str):
        """Задаёт код доступа (вызывается из GUI при первом запуске)"""
        self._access_hash = hashlib.sha256(access_code.encode("utf-8")).digest()

    def register_key(self, key_name: str, key_data: bytes):
        """Регистрирует ключ для защиты"""
        if self.is_self_destructed:
            raise RuntimeError("Система самоуничтожена! Ключи недоступны.")

        self.encryption_keys[key_name] = key_data
        self.update_activity()
        print(f" Ключ '{key_name}' зарегистрирован и защищен")

    def get_key(self, key_name: str) -> Optional[bytes]:
        """Получает ключ (с проверкой активности)"""
        if self.is_self_destructed:
            print("❌ СИСТЕМА САМОУНИЧТОЖЕНА! Ключи уничтожены.")
            return None

        self.check_inactivity()

        if self.is_self_destructed:
            return None

        if key_name not in self.encryption_keys:
            self.trigger_failed_attempt()
            return None

        self.update_activity()
        self.reset_failed_attempts()
        return self.encryption_keys[key_name]

    def verify_access(self, access_code: str) -> bool:
        """Проверяет код доступа по хэшу, за константное время"""
        if self.is_self_destructed:
            return False

        if self._access_hash is None:
            print("⚠️ Код доступа не задан. Вызовите set_access_code().")
            return False

        candidate = hashlib.sha256(access_code.encode("utf-8")).digest()
        if secrets.compare_digest(candidate, self._access_hash):
            self.reset_failed_attempts()
            self.update_activity()
            print("✅ Доступ разрешен")
            return True

        self.trigger_failed_attempt()
        print("❌ НЕВЕРНЫЙ КОД ДОСТУПА!")
        return False

    def trigger_failed_attempt(self):
        """Регистрирует неудачную попытку доступа"""
        self.failed_attempts += 1
        self.last_failed_attempt = datetime.now(timezone.utc)

        print(f"️ Неудачная попытка #{self.failed_attempts}/{self.max_failed_attempts}")

        if self.failed_attempts >= self.max_failed_attempts:
            print("🚨 ПРЕВЫШЕН ЛИМИТ ПОПЫТОК!")
            self.self_destruct("Превышен лимит неудачных попыток доступа")

    def check_inactivity(self):
        """Проверяет время бездействия (при обращении к ключам)"""
        now = datetime.now(timezone.utc)
        inactive_time = now - self.last_activity

        if inactive_time > self.inactivity_timeout:
            print(f"⏰ Превышен таймаут бездействия ({inactive_time})")
            self.self_destruct("Длительное бездействие системы")

    def update_activity(self):
        self.last_activity = datetime.now(timezone.utc)

    def reset_failed_attempts(self):
        self.failed_attempts = 0
        self.last_failed_attempt = None

    def register_destruction_callback(self, callback: Callable):
        self.destruction_callbacks.append(callback)

    def self_destruct(self, reason: str = "Неизвестная причина"):
        """Уничтожает все ключи (best-effort: полную очистку RAM Python не гарантирует)"""
        if self.is_self_destructed:
            return

        print("\n" + "!" * 60)
        print("🚨 GRAIL SELF-DESTRUCT ACTIVATED 🚨")
        print("!" * 60)
        print(f"Причина: {reason}")

        for callback in self.destruction_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"️ Ошибка при вызове callback: {e}")

        print("\n УНИЧТОЖЕНИЕ КЛЮЧЕЙ...")
        for key_name in list(self.encryption_keys.keys()):
            key_size = len(self.encryption_keys[key_name])
            self.encryption_keys[key_name] = secrets.token_bytes(key_size)
            del self.encryption_keys[key_name]
            print(f"   Ключ '{key_name}' уничтожен")

        self.master_key = secrets.token_bytes(32)
        print("   Мастер-ключ уничтожен")

        gc.collect()
        self.is_self_destructed = True
        print("✅ ВСЕ КЛЮЧИ УНИЧТОЖЕНЫ")

    def emergency_destruct(self):
        """Экстренное самоуничтожение (вручную)"""
        self.self_destruct("Ручная активация Emergency Destruct")

    def get_status(self) -> dict:
        return {
            'is_self_destructed': self.is_self_destructed,
            'failed_attempts': self.failed_attempts,
            'last_activity': self.last_activity.isoformat(),
            'registered_keys': len(self.encryption_keys),
        }


if __name__ == "__main__":
    print("💣 Инициализация Grail Self-Destruct Mechanism...")

    sd = SelfDestructMechanism(access_code="MySecretCode2026")

    sd.register_key("master", secrets.token_bytes(32))
    sd.register_key("session", secrets.token_bytes(16))

    print("\n🔍 Тест 1: Правильный доступ")
    sd.verify_access("MySecretCode2026")

    print("\n🔍 Тест 2: Получение ключа")
    if sd.get_key("master"):
        print("✅ Ключ получен успешно")

    print("\n🔍 Тест 3: Неверные попытки доступа")
    for i in range(4):
        print(f"\nПопытка #{i + 1}:")
        sd.verify_access("WRONG-CODE")
        if sd.is_self_destructed:
            print("\n💥 СИСТЕМА УНИЧТОЖЕНА!")
            break

    print("\n🔍 Тест 4: Ключ после уничтожения")
    if sd.get_key("master") is None:
        print("✅ Ключи действительно уничтожены!")

    print("\n📊 Финальный статус:")
    print(sd.get_status())
