"""
Grail Self-Destruct Mechanism
Автоматическое уничтожение ключей при обнаружении угроз.
Защита уровня "Scorched Earth" (Выжженная земля).
"""

import os
import secrets
import time
from typing import Optional, Callable
from datetime import datetime, timedelta

class SelfDestructMechanism:
    """Система самоуничтожения ключей"""
    
    def __init__(self):
        # Ключи шифрования (хранятся ТОЛЬКО в RAM)
        self.encryption_keys = {}
        self.master_key = secrets.token_bytes(32)
        
        # Триггеры самоуничтожения
        self.max_failed_attempts = 3
        self.failed_attempts = 0
        self.last_failed_attempt: Optional[datetime] = None
        self.inactivity_timeout = timedelta(minutes=30)
        self.last_activity: datetime = datetime.utcnow()
        
        # Флаги
        self.is_self_destructed = False
        self.destruction_callbacks: list[Callable] = []
        
        print("💣 Self-Destruct механизм активирован")
        print(f"   Максимум неудачных попыток: {self.max_failed_attempts}")
        print(f"   Таймаут бездействия: {self.inactivity_timeout}")
    
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
        """Проверяет код доступа (симуляция)"""
        if self.is_self_destructed:
            return False
        
        # В реальной системе здесь была бы проверка пароля/токена
        correct_code = "GRAIL-ALPHA-2026"
        
        if access_code == correct_code:
            self.reset_failed_attempts()
            self.update_activity()
            print("✅ Доступ разрешен")
            return True
        else:
            self.trigger_failed_attempt()
            print("❌ НЕВЕРНЫЙ КОД ДОСТУПА!")
            return False
    
    def trigger_failed_attempt(self):
        """Регистрирует неудачную попытку доступа"""
        self.failed_attempts += 1
        self.last_failed_attempt = datetime.utcnow()
        
        print(f"️ Неудачная попытка #{self.failed_attempts}/{self.max_failed_attempts}")
        
        if self.failed_attempts >= self.max_failed_attempts:
            print("🚨 ПРЕВЫШЕН ЛИМИТ ПОПЫТОК!")
            self.self_destruct("Превышен лимит неудачных попыток доступа")
    
    def check_inactivity(self):
        """Проверяет время бездействия"""
        now = datetime.utcnow()
        inactive_time = now - self.last_activity
        
        if inactive_time > self.inactivity_timeout:
            print(f"⏰ Превышен таймаут бездействия ({inactive_time})")
            self.self_destruct("Длительное бездействие системы")
    
    def update_activity(self):
        """Обновляет время последней активности"""
        self.last_activity = datetime.utcnow()
    
    def reset_failed_attempts(self):
        """Сбрасывает счетчик неудачных попыток"""
        self.failed_attempts = 0
        self.last_failed_attempt = None
    
    def register_destruction_callback(self, callback: Callable):
        """Регистрирует функцию, которая вызовется при самоуничтожении"""
        self.destruction_callbacks.append(callback)
    
    def self_destruct(self, reason: str = "Неизвестная причина"):
        """УНИЧТОЖАЕТ ВСЕ КЛЮЧИ И ДАННЫЕ"""
        if self.is_self_destructed:
            return
        
        print("\n" + "!"*60)
        print("🚨🚨 GRAIL SELF-DESTRUCT ACTIVATED 🚨🚨🚨")
        print("!"*60)
        print(f"Причина: {reason}")
        print(f"Время: {datetime.utcnow().isoformat()}")
        print("!"*60)
        
        # Вызываем все зарегистрированные функции
        for callback in self.destruction_callbacks:
            try:
                callback()
            except Exception as e:
                print(f"️ Ошибка при вызове callback: {e}")
        
        # Уничтожаем ключи (перезаписываем случайными данными)
        print("\n УНИЧТОЖЕНИЕ КЛЮЧЕЙ...")
        for key_name in list(self.encryption_keys.keys()):
            # Перезаписываем ключ случайными данными
            key_size = len(self.encryption_keys[key_name])
            self.encryption_keys[key_name] = secrets.token_bytes(key_size)
            del self.encryption_keys[key_name]
            print(f"   Ключ '{key_name}' уничтожен")
        
        # Уничтожаем мастер-ключ
        self.master_key = secrets.token_bytes(32)
        print("   Мастер-ключ уничтожен")
        
        # Очищаем память
        import gc
        gc.collect()
        
        self.is_self_destructed = True
        
        print("\n" + "!"*60)
        print("✅ ВСЕ КЛЮЧИ УНИЧТОЖЕНЫ")
        print("✅ ДАННЫЕ НЕВОССТАНОВИМЫ")
        print("!"*60)
    
    def emergency_destruct(self):
        """Экстренное самоуничтожение (вызывается вручную)"""
        self.self_destruct("Ручная активация Emergency Destruct")
    
    def get_status(self) -> dict:
        """Возвращает статус системы"""
        return {
            'is_self_destructed': self.is_self_destructed,
            'failed_attempts': self.failed_attempts,
            'last_activity': self.last_activity.isoformat(),
            'registered_keys': len(self.encryption_keys),
            'time_since_last_activity': str(datetime.utcnow() - self.last_activity)
        }

# --- ДЕМОНСТРАЦИЯ РАБОТЫ ---
if __name__ == "__main__":
    print("💣 Инициализация Grail Self-Destruct Mechanism...")
    print("="*60)
    
    sd = SelfDestructMechanism()
    
    # Регистрируем ключи
    sd.register_key("master", secrets.token_bytes(32))
    sd.register_key("session", secrets.token_bytes(16))
    
    # Симуляция работы
    print("\n🔍 Тест 1: Правильный доступ")
    sd.verify_access("GRAIL-ALPHA-2026")
    
    print("\n Тест 2: Получение ключа")
    key = sd.get_key("master")
    if key:
        print("✅ Ключ получен успешно")
    
    print("\n🔍 Тест 3: Неверные попытки доступа")
    for i in range(4):  # 4 попытки (больше лимита)
        print(f"\nПопытка #{i+1}:")
        sd.verify_access("WRONG-CODE")
        
        if sd.is_self_destructed:
            print("\n💥 СИСТЕМА УНИЧТОЖЕНА!")
            break
    
    print("\n Тест 4: Попытка получить ключ после уничтожения")
    key = sd.get_key("master")
    if key is None:
        print("✅ Ключи действительно уничтожены!")
    
    print("\n📊 Финальный статус:")
    print(sd.get_status())
