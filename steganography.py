"""
Grail Steganography Module
Hides data inside images using the LSB (Least Significant Bit) method.
IMPORTANT: data must be pre-encrypted (e.g., AES-256-GCM).
Supports PNG/BMP (lossless formats).

Grail Steganography Module
Скрытие данных внутри изображений методом LSB (Least Significant Bit).
ВАЖНО: данные должны быть предварительно зашифрованы (например, AES-256-GCM).
Поддерживает PNG/BMP (без сжатия).
"""

from PIL import Image
import numpy as np
from typing import Optional


class Steganography:
    """Steganography system for hiding data in images.
    Система стеганографии для скрытия данных в изображениях.
    
    Honest disclosure: LSB is detectable by statistical steganalysis.
    This is obfuscation, not perfect invisibility. Confidentiality is
    guaranteed by pre-encryption (AES-256-GCM).
    
    Честно: LSB обнаруживается статистическим стегоанализом.
    Это обфускация, а не абсолютная невидимость. Конфиденциальность
    обеспечивается предварительным шифрованием (AES-256-GCM).
    """
    
    def __init__(self):
        print("🖼️ Initializing Grail Steganography Module...")
        print("   Method: LSB (Least Significant Bit)")
        print("   Formats: PNG, BMP (lossless)")
        print("   ⚠️  Data must be pre-encrypted")
        print("   ⚠️  LSB is detectable by steganalysis — confidentiality comes from encryption")
        print("✅ Module ready\n")
        print("🖼️ Инициализация Grail Steganography Module...")
        print("   Метод: LSB (Least Significant Bit)")
        print("   Форматы: PNG, BMP (без сжатия)")
        print("   ⚠️  Данные должны быть предварительно зашифрованы")
        print("   ⚠️  LSB обнаруживается стегоанализом — конфиденциальность от шифрования")
        print("✅ Модуль готов к работе\n")
    
    def encode_data_to_image(self, image_path: str, encrypted_data: bytes, output_path: str) -> bool:
        """
        Hides encrypted data inside an image.
        Скрывает зашифрованные данные внутри изображения.
        
        Args:
            image_path: Path to the source image / Путь к исходному изображению
            encrypted_data: Encrypted bytes to hide / Зашифрованные байты для скрытия
            output_path: Path to save the result / Путь для сохранения результата
        """
        try:
            img = Image.open(image_path)
            
            if img.format not in ['PNG', 'BMP']:
                print("⚠️ PNG or BMP format recommended! / Рекомендуется PNG или BMP!")
                return False
            
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            img_array = np.array(img)
            
            # Convert data to bits / Преобразуем данные в биты
            data_length = len(encrypted_data)
            data_bits = ''.join([format(byte, '08b') for byte in encrypted_data])
            
            # Protocol: 4-byte length (32 bits) + data
            # Протокол: 4 байта длины (32 бита) + данные
            length_bits = format(data_length, '032b')
            all_bits = length_bits + data_bits
            
            max_bits = img_array.size * 3  # Each RGB channel = 1 bit / Каждый канал RGB = 1 бит
            if len(all_bits) > max_bits:
                print(f"❌ Data too large! / Данные слишком большие! Max: {max_bits // 8} bytes / байт")
                return False
            
            # Embed bits into LSB / Встраиваем биты в LSB
            bit_index = 0
            for i in range(img_array.shape[0]):
                for j in range(img_array.shape[1]):
                    for k in range(3):  # RGB channels / RGB каналы
                        if bit_index < len(all_bits):
                            img_array[i, j, k] = (img_array[i, j, k] & 0xFE) | int(all_bits[bit_index])
                            bit_index += 1
            
            result_img = Image.fromarray(img_array)
            result_img.save(output_path)
            
            print(f"✅ Data hidden successfully! / Данные успешно скрыты!")
            print(f"   Source: / Исходное: {image_path}")
            print(f"   Result: / Результат: {output_path}")
            print(f"   Data size: / Размер данных: {data_length} bytes / байт")
            
            return True
            
        except Exception as e:
            print(f"❌ Encoding error: / Ошибка при кодировании: {e}")
            return False
    
    def decode_data_from_image(self, image_path: str) -> Optional[bytes]:
        """
        Extracts hidden data from an image.
        Извлекает скрытые данные из изображения.
        
        Args:
            image_path: Path to the image with hidden data / Путь к изображению со скрытыми данными
            
        Returns:
            Extracted bytes (must be decrypted separately)
            Извлечённые байты (должны быть расшифрованы отдельно)
        """
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            
            # Extract bits from LSB / Извлекаем биты из LSB
            bits = []
            for i in range(img_array.shape[0]):
                for j in range(img_array.shape[1]):
                    for k in range(3):
                        bits.append(img_array[i, j, k] & 1)
            
            # Extract length (first 32 bits) / Извлекаем длину (первые 32 бита)
            if len(bits) < 32:
                print("❌ Image too small / Изображение слишком маленькое")
                return None
            
            length_bits = ''.join(str(b) for b in bits[:32])
            data_length = int(length_bits, 2)
            
            if data_length == 0 or data_length > len(bits) // 8:
                print("❌ Invalid data length / Некорректная длина данных")
                return None
            
            # Extract data / Извлекаем данные
            data_bits = bits[32:32 + data_length * 8]
            secret_bytes = []
            for i in range(0, len(data_bits), 8):
                byte = 0
                for j in range(8):
                    byte = (byte << 1) | data_bits[i + j]
                secret_bytes.append(byte)
            
            print(f"✅ Data extracted successfully! / Данные успешно извлечены!")
            print(f"   Source: / Источник: {image_path}")
            print(f"   Size: / Размер: {len(secret_bytes)} bytes / байт")
            
            return bytes(secret_bytes)
            
        except Exception as e:
            print(f"❌ Decoding error: / Ошибка при декодировании: {e}")
            return None
    
    def get_capacity(self, image_path: str) -> int:
        """Returns maximum data size that can be hidden.
        Возвращает максимальный размер данных, который можно скрыть."""
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            max_bits = img_array.size * 3
            max_bytes = (max_bits - 32) // 8  # minus 32 bits for length / минус 32 бита на длину
            return max_bytes
        except Exception:
            return 0


if __name__ == "__main__":
    print("=" * 60)
    print("🖼️ GRAIL STEGANOGRAPHY MODULE - DEMONSTRATION")
    print("🖼️ GRAIL STEGANOGRAPHY MODULE - ДЕМОНСТРАЦИЯ")
    print("=" * 60)
    
    steg = Steganography()
    
    print("\n📝 Step 1: Creating test image... / Шаг 1: Создаем тестовое изображение...")
    test_img = Image.new('RGB', (100, 100), color='white')
    test_img.save('test_image.png')
    print("✅ Image created: / Изображение создано: test_image.png")
    
    # Simulated encrypted data (in real usage, this would be AES-256-GCM)
    # Имитация зашифрованных данных (в реальном использовании здесь AES-256-GCM)
    secret_message = "GRAIL: Safe password is 7749. Meeting at 18:00."
    encrypted_data = secret_message.encode('utf-8')
    print(f"\n🔐 Step 2: Data to hide / Данные для скрытия ({len(encrypted_data)} bytes / байт)")
    
    capacity = steg.get_capacity('test_image.png')
    print(f"   Image capacity: / Вместимость изображения: {capacity} bytes / байт")
    
    if len(encrypted_data) <= capacity:
        print("\n🖼️ Step 3: Hiding data in image... / Шаг 3: Скрываем данные в изображении...")
        success = steg.encode_data_to_image('test_image.png', encrypted_data, 'secret_image.png')
        
        if success:
            print("\n📤 Step 4: Extracting data from image... / Шаг 4: Извлекаем данные из изображения...")
            decoded = steg.decode_data_from_image('secret_image.png')
            
            if decoded:
                decoded_text = decoded.decode('utf-8', errors='ignore')
                print(f"\n✅ EXTRACTED DATA: / ИЗВЛЕЧЕННЫЕ ДАННЫЕ: '{decoded_text}'")
                
                if decoded == encrypted_data:
                    print("\n🏆 STEGANOGRAPHY WORKS PERFECTLY! / СТЕГАНОГРАФИЯ РАБОТАЕТ ИДЕАЛЬНО!")
                    print("   Data matches original! / Данные совпадают с оригиналом!")
                else:
                    print("\n⚠️ Data mismatch! / Данные не совпадают!")
            else:
                print("\n❌ Failed to extract data! / Не удалось извлечь данные!")
        else:
            print("\n❌ Failed to hide data! / Не удалось скрыть данные!")
    else:
        print("\n❌ Data too large for this image! / Данные слишком большие для этого изображения!")
    
    print("\n" + "=" * 60)
    print("💡 In real usage / В реальном использовании:")
    print("   1. Encrypt data with AES-256-GCM / Шифруете данные через AES-256-GCM")
    print("   2. Hide encrypted bytes in the image / Скрываете зашифрованные байты в картинке")
    print("   3. Send the image — even if steganography is suspected,")
    print("      only encrypted garbage is extracted")
    print("   3. Отправляете картинку — даже если заподозрят стеганографию,")
    print("      извлекут только зашифрованный мусор")
    print("=" * 60)
