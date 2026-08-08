False
            
            # Встраиваем 
"""
Grail Steganography Module
Скрытие данных внутри изображений методом LSB (Least Significant Bit).
ВАЖНО: данные должны быть предварительно зашифрованы (например, AES-256-GCM).
Поддерживает PNG/BMP (без сжатия).
"""

from PIL import Image
import numpy as np
from typing import Optional


class Steganography:
    """Система стеганографии для скрытия данных в изображениях"""
    
    def __init__(self):
        print("🖼️ Инициализация Grail Steganography Module...")
        print("   Метод: LSB (Least Significant Bit)")
        print("   Форматы: PNG, BMP (без сжатия)")
        print("   ⚠️  Данные должны быть предварительно зашифрованы")
        print("✅ Модуль готов к работе\n")
    
    def encode_data_to_image(self, image_path: str, encrypted_data: bytes, output_path: str) -> bool:
        """
        Скрывает зашифрованные данные внутри изображения
        
        Args:
            image_path: Путь к исходному изображению
            encrypted_data: Зашифрованные байты для скрытия
            output_path: Путь для сохранения результата
        """
        try:
            img = Image.open(image_path)
            
            if img.format not in ['PNG', 'BMP']:
                print("⚠️ Рекомендуется использовать PNG или BMP формат!")
                return False
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            
            # Преобразуем данные в биты
            data_length = len(encrypted_data)
            data_bits = ''.join([format(byte, '08b') for byte in encrypted_data])
            
            # Протокол: 4 байта длины (32 бита) + данные
            length_bits = format(data_length, '032b')
            all_bits = length_bits + data_bits
            
            max_bits = img_array.size * 3  # Каждый канал RGB = 1 бит
            if len(all_bits) > max_bits:
                print(f"❌ Данные слишком большие! Максимум: {max_bits // 8} байт")
                return False
            
            # Встраиваем биты в LSB
            bit_index = 0
            for i in range(img_array.shape[0]):
                for j in range(img_array.shape[1]):
                    for k in range(3):  # RGB каналы
                        if bit_index < len(all_bits):
                            img_array[i, j, k] = (img_array[i, j, k] & 0xFE) | int(all_bits[bit_index])
                            bit_index += 1
            
            result_img = Image.fromarray(img_array)
            result_img.save(output_path)
            
            print(f"✅ Данные успешно скрыты в изображении!")
            print(f"   Исходное: {image_path}")
            print(f"   Результат: {output_path}")
            print(f"   Размер данных: {data_length} байт")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при кодировании: {e}")
            return False
    
    def decode_data_from_image(self, image_path: str) -> Optional[bytes]:
        """
        Извлекает скрытые данные из изображения
        
        Args:
            image_path: Путь к изображению со скрытыми данными
            
        Returns:
            Извлечённые байты (должны быть расшифрованы отдельно)
        """
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Извлекаем биты из LSB
            bits = []
            for i in range(img_array.shape[0]):
                for j in range(img_array.shape[1]):
                    for k in range(3):
                        bits.append(img_array[i, j, k] & 1)
            
            # Извлекаем длину (первые 32 бита)
            if len(bits) < 32:
                print("❌ Изображение слишком маленькое")
                return None
            
            length_bits = ''.join(str(b) for b in bits[:32])
            data_length = int(length_bits, 2)
            
            if data_length == 0 or data_length > len(bits) // 8:
                print("❌ Некорректная длина данных")
                return None
            
            # Извлекаем данные
            data_bits = bits[32:32 + data_length * 8]
            secret_bytes = []
            for i in range(0, len(data_bits), 8):
                byte = 0
                for j in range(8):
                    byte = (byte << 1) | data_bits[i + j]
                secret_bytes.append(byte)
            
            print(f"✅ Данные успешно извлечены из изображения!")
            print(f"   Источник: {image_path}")
            print(f"   Размер: {len(secret_bytes)} байт")
            
            return bytes(secret_bytes)
            
        except Exception as e:
            print(f"❌ Ошибка при декодировании: {e}")
            return None
    
    def get_capacity(self, image_path: str) -> int:
        """Возвращает максимальный размер данных, который можно скрыть"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            max_bits = img_array.size * 3
            max_bytes = (max_bits - 32) // 8  # минус 32 бита на длину
            return max_bytes
        except Exception:
            return 0


if __name__ == "__main__":
    print("=" * 60)
    print("🖼️ GRAIL STEGANOGRAPHY MODULE - ДЕМОНСТРАЦИЯ")
    print("=" * 60)
    
    steg = Steganography()
    
    print("\n📝 Шаг 1: Создаем тестовое изображение...")
    test_img = Image.new('RGB', (100, 100), color='white')
    test_img.save('test_image.png')
    print("✅ Изображение создано: test_image.png")
    
    # Имитация зашифрованных данных (в реальном использовании здесь AES-256-GCM)
    secret_message = "GRAIL: Пароль от сейфа - 7749. Встреча в 18:00."
    encrypted_data = secret_message.encode('utf-8')
    print(f"\n🔐 Шаг 2: Данные для скрытия ({len(encrypted_data)} байт)")
    
    capacity = steg.get_capacity('test_image.png')
    print(f"   Вместимость изображения: {capacity} байт")
    
    if len(encrypted_data) <= capacity:
        print("\n🖼️ Шаг 3: Скрываем данные в изображении...")
        success = steg.encode_data_to_image('test_image.png', encrypted_data, 'secret_image.png')
        
        if success:
            print("\n📤 Шаг 4: Извлекаем данные из изображения...")
            decoded = steg.decode_data_from_image('secret_image.png')
            
            if decoded:
                decoded_text = decoded.decode('utf-8', errors='ignore')
                print(f"\n✅ ИЗВЛЕЧЕННЫЕ ДАННЫЕ: '{decoded_text}'")
                
                if decoded == encrypted_data:
                    print("\n🏆 СТЕГАНОГРАФИЯ РАБОТАЕТ ИДЕАЛЬНО!")
                    print("   Данные совпадают с оригиналом!")
                else:
                    print("\n⚠️ Данные не совпадают!")
            else:
                print("\n❌ Не удалось извлечь данные!")
        else:
            print("\n❌ Не удалось скрыть данные!")
    else:
        print("\n❌ Данные слишком большие для этого изображения!")
    
    print("\n" + "=" * 60)
    print("💡 В реальном использовании:")
    print("   1. Шифруете данные через AES-256-GCM")
    print("   2. Скрываете зашифрованные байты в картинке")
    print("   3. Отправляете картинку — даже если заподозрят стеганографию,")
    print("      извлекут только зашифрованный мусор")
    print("=" * 60)
