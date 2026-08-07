"""
Grail Steganography Module
Скрытие зашифрованных данных внутри обычных изображений.
Уровень защиты: Спецслужбы.
"""

from PIL import Image
import numpy as np
import io
from typing import Tuple, Optional

class Steganography:
    """Система стеганографии для скрытия данных в изображениях"""
    
    def __init__(self):
        print("🖼️ Инициализация Grail Steganography Module...")
        print("   Метод: LSB (Least Significant Bit) - наименее значимый бит")
        print("   Форматы: PNG, BMP (без сжатия)")
        print("✅ Модуль готов к работе\n")
    
    def encode_data_to_image(self, image_path: str, secret_data: str, output_path: str) -> bool:
        """
        Скрывает текст внутри изображения
        
        Args:
            image_path: Путь к исходному изображению
            secret_data: Секретный текст для скрытия
            output_path: Путь для сохранения результата
        """
        try:
            # Открываем изображение
            img = Image.open(image_path)
            
            # Проверяем формат (должен быть без сжатия)
            if img.format not in ['PNG', 'BMP']:
                print("⚠️ Рекомендуется использовать PNG или BMP формат!")
                return False
            
            # Конвертируем в RGB если нужно
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Преобразуем изображение в массив пикселей
            img_array = np.array(img)
            
            # Преобразуем секретные данные в биты
            secret_bytes = secret_data.encode('utf-8')
            secret_bits = ''.join([format(byte, '08b') for byte in secret_bytes])
            
            # Добавляем маркер конца данных
            secret_bits += '0000000000000000'  # 16 нулей = конец данных
            
            # Проверяем, хватает ли места в изображении
            max_bits = img_array.size // 3  # Каждый пиксель имеет 3 канала (RGB)
            if len(secret_bits) > max_bits:
                print(f"❌ Данные слишком большие! Максимум: {max_bits // 8} байт")
                return False
            
            # Встраиваем биты в наименее значимые биты пикселей
            bit_index = 0
            for i in range(img_array.shape[0]):
                for j in range(img_array.shape[1]):
                    for k in range(3):  # RGB каналы
                        if bit_index < len(secret_bits):
                            # Заменяем последний бит пикселя на бит секретных данных
                            img_array[i, j, k] = (img_array[i, j, k] & 0xFE) | int(secret_bits[bit_index])
                            bit_index += 1
            
            # Сохраняем результат
            result_img = Image.fromarray(img_array)
            result_img.save(output_path)
            
            print(f"✅ Данные успешно скрыты в изображении!")
            print(f"   Исходное: {image_path}")
            print(f"   Результат: {output_path}")
            print(f"   Размер данных: {len(secret_data)} символов")
            
            return True
            
        except Exception as e:
            print(f"❌ Ошибка при кодировании: {e}")
            return False
    
    def decode_data_from_image(self, image_path: str) -> Optional[str]:
        """
        Извлекает скрытые данные из изображения
        
        Args:
            image_path: Путь к изображению со скрытыми данными
        """
        try:
            # Открываем изображение
            img = Image.open(image_path)
            
            # Преобразуем в массив пикселей
            img_array = np.array(img)
            
            # Извлекаем биты из наименее значимых битов
            bits = []
            for i in range(img_array.shape[0]):
                for j in range(img_array.shape[1]):
                    for k in range(3):
                        bits.append(img_array[i, j, k] & 1)
            
            # Преобразуем биты в байты
            secret_bytes = []
            for i in range(0, len(bits) - 16, 8):  # -16 для маркера конца
                byte = 0
                for j in range(8):
                    byte = (byte << 1) | bits[i + j]
                secret_bytes.append(byte)
                
                # Проверяем маркер конца (16 нулей подряд)
                if len(secret_bytes) >= 2:
                    if secret_bytes[-2] == 0 and secret_bytes[-1] == 0:
                        break
            
            # Удаляем маркер конца
            if len(secret_bytes) >= 2 and secret_bytes[-1] == 0:
                secret_bytes = secret_bytes[:-2]
            
            # Преобразуем байты в текст
            secret_data = bytes(secret_bytes).decode('utf-8', errors='ignore')
            
            print(f"✅ Данные успешно извлечены из изображения!")
            print(f"   Источник: {image_path}")
            print(f"   Размер: {len(secret_data)} символов")
            
            return secret_data
            
        except Exception as e:
            print(f"❌ Ошибка при декодировании: {e}")
            return None
    
    def get_capacity(self, image_path: str) -> int:
        """Возвращает максимальный размер данных, который можно скрыть"""
        try:
            img = Image.open(image_path)
            img_array = np.array(img)
            max_bits = img_array.size // 3
            max_bytes = max_bits // 8
            return max_bytes
        except:
            return 0

# --- ДЕМОНСТРАЦИЯ РАБОТЫ ---
if __name__ == "__main__":
    print("="*60)
    print("️ GRAIL STEGANOGRAPHY MODULE - ДЕМОНСТРАЦИЯ")
    print("="*60)
    
    steg = Steganography()
    
    # Создаем тестовое изображение (100x100 пикселей, белый фон)
    print("\n📝 Шаг 1: Создаем тестовое изображение...")
    test_img = Image.new('RGB', (100, 100), color='white')
    test_img.save('test_image.png')
    print("✅ Изображение создано: test_image.png")
    
    # Секретное сообщение
    secret_message = "GRAIL: Пароль от сейфа - 7749. Встреча в 18:00."
    print(f"\n🔐 Шаг 2: Секретное сообщение: '{secret_message}'")
    
    # Проверяем вместимость
    capacity = steg.get_capacity('test_image.png')
    print(f"   Вместимость изображения: {capacity} байт")
    print(f"   Размер сообщения: {len(secret_message)} байт")
    
    if len(secret_message) <= capacity:
        # Скрываем данные
        print("\n️ Шаг 3: Скрываем данные в изображении...")
        success = steg.encode_data_to_image('test_image.png', secret_message, 'secret_image.png')
        
        if success:
            # Извлекаем данные
            print("\n Шаг 4: Извлекаем данные из изображения...")
            decoded = steg.decode_data_from_image('secret_image.png')
            
            if decoded:
                print(f"\n✅ ИЗВЛЕЧЕННОЕ СООБЩЕНИЕ: '{decoded}'")
                
                if decoded == secret_message:
                    print("\n🏆 СТЕГАНОГРАФИЯ РАБОТАЕТ ИДЕАЛЬНО!")
                    print("   Сообщение совпадает с оригиналом!")
                else:
                    print("\n⚠️ Сообщения не совпадают!")
            else:
                print("\n❌ Не удалось извлечь данные!")
        else:
            print("\n❌ Не удалось скрыть данные!")
    else:
        print("\n❌ Сообщение слишком большое для этого изображения!")
    
    print("\n" + "="*60)
    print("💡 В реальном использовании:")
    print("   1. Берете обычную фотографию")
    print("   2. Скрываете в ней зашифрованный текст")
    print("   3. Отправляете картинку - никто не заподозрит!")
    print("="*60)
