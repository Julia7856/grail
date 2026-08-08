"""Добавляет корень проекта в sys.path для импорта модулей."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
