"""
Grail Blockchain Audit Module
Неизменяемый журнал всех действий.
Каждая запись защищена криптографически.
"""

import hashlib
import json
from datetime import datetime
from typing import List, Dict

class Block:
    """Один блок в блокчейне"""
    
    def __init__(self, index: int, timestamp: str, action: str, data: str, previous_hash: str):
        self.index = index
        self.timestamp = timestamp
        self.action = action  # Что произошло (например, "DATA_ENCRYPTED")
        self.data = data  # Детали действия
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash()
    
    def calculate_hash(self) -> str:
        """Вычисляет хэш блока"""
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'action': self.action,
            'data': self.data,
            'previous_hash': self.previous_hash
        }, sort_keys=True).encode()
        
        return hashlib.sha256(block_string).hexdigest()
    
    def verify_integrity(self) -> bool:
        """Проверяет целостность блока"""
        return self.hash == self.calculate_hash()


class BlockchainAudit:
    """Система аудита на блокчейне"""
    
    def __init__(self):
        self.chain: List[Block] = []
        # Создаем первый блок (Genesis Block)
        self.create_block("GENESIS", "Инициализация Grail Blockchain Audit")
    
    def create_block(self, action: str, data: str) -> Block:
        """Создает новый блок в цепочке"""
        index = len(self.chain)
        timestamp = datetime.utcnow().isoformat()
        previous_hash = self.chain[-1].hash if self.chain else "0" * 64
        
        new_block = Block(index, timestamp, action, data, previous_hash)
        self.chain.append(new_block)
        
        return new_block
    
    def log_action(self, action: str, details: str):
        """Записывает действие в блокчейн"""
        block = self.create_block(action, details)
        print(f"🔗 Блок #{block.index} добавлен: {action}")
        print(f"   Хэш: {block.hash[:32]}...")
    
    def verify_chain(self) -> bool:
        """Проверяет целостность всей цепочки"""
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i-1]
            
            # Проверяем хэш текущего блока
            if not current_block.verify_integrity():
                print(f"❌ Блок #{i} поврежден!")
                return False
            
            # Проверяем связь с предыдущим блоком
            if current_block.previous_hash != previous_block.hash:
                print(f"❌ Нарушена связь между блоками #{i-1} и #{i}!")
                return False
        
        print("✅ Блокчейн целостен. Все записи подлинные.")
        return True
    
    def get_audit_trail(self) -> List[Dict]:
        """Возвращает весь журнал аудита"""
        return [
            {
                'index': block.index,
                'timestamp': block.timestamp,
                'action': block.action,
                'data': block.data,
                'hash': block.hash
            }
            for block in self.chain
        ]
    
    def print_audit_log(self):
        """Выводит журнал в красивом виде"""
        print("\n" + "="*60)
        print(" GRAIL BLOCKCHAIN AUDIT LOG")
        print("="*60)
        
        for block in self.chain:
            print(f"\n Блок #{block.index}")
            print(f"   Время: {block.timestamp}")
            print(f"   Действие: {block.action}")
            print(f"   Данные: {block.data[:50]}...")
            print(f"   Хэш: {block.hash[:16]}...")
        
        print("\n" + "="*60)
        print(f"Всего блоков: {len(self.chain)}")
        print("="*60)

# --- ДЕМОНСТРАЦИЯ РАБОТЫ ---
if __name__ == "__main__":
    print("🔗 Инициализация Grail Blockchain Audit...")
    audit = BlockchainAudit()
    
    # Симуляция действий
    audit.log_action("USER_LOGIN", "User: admin, IP: 192.168.1.100")
    audit.log_action("FILE_UPLOADED", "File: secret_document.pdf, Size: 2.4MB")
    audit.log_action("DATA_ENCRYPTED", "Algorithm: AES-256-GCM, Records: 150")
    audit.log_action("DATA_DOWNLOADED", "User: admin, File: encrypted_data.grail")
    audit.log_action("KEY_ROTATION", "Old key destroyed, new key generated")
    
    # Проверяем целостность
    is_valid = audit.verify_chain()
    
    # Показываем журнал
    audit.print_audit_log()
    
    if is_valid:
        print("\n✅ Blockchain Audit готов к работе!")
    else:
        print("\n❌ ОБНАРУЖЕНО ВМЕШАТЕЛЬСТВО!")
