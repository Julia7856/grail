# ⏳ Grail — PQC Roadmap / Дорога к PQC

Honest living roadmap / честный живой план.

## Why / зачем

HNDL for local data / HNDL для локальных данных: an attacker copies your
encrypted archive today and waits for a quantum computer / атакующий
копирует твой зашифрованный архив сегодня и ждёт квантовый компьютер.
Classical key exchange dies; hybrid survives / классический обмен ключами
умрёт; гибрид выживет.

## v1.1 — prototype / прототип (current / сейчас)

- [x] `crypto/pq_layer.py` — hybrid ML-KEM-768 + X25519 → AES-256-GCM
- [x] roundtrip self-test / самотест раундтрипа
- [ ] integration into core vault / интеграция в ядро (core.py)

## v1.2 — integration / интеграция

- [ ] encrypt local vault with hybrid layer / шифрование локального хранилища гибридным слоем
- [ ] key migration tool: classical → hybrid / миграция ключей: классика → гибрид
- [ ] CBOM for stored data / CBOM для хранимых данных

## v1.3 — audit / аудит

- [ ] «quantum passport» for user archives / «квантовый паспорт» архивов пользователя
- [ ] THREAT_MODEL: Q-day scenarios / сценарии Q-дня

---

Status: prototype, not audited / прототип, не аудитировано.
