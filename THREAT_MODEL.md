# 🛡️ Threat Model / Модель угроз

**Grail v1.0 — honest security posture / честная позиция безопасности**

---

## 🎯 What we protect / Что защищаем

Confidentiality of user-provided text data (messages, notes, credentials).

Конфиденциальность текстовых данных пользователя (сообщения, заметки, учётные данные).

---

## 🧑‍💻 Adversary model / Модель противника

### Primary threat / Основная угроза
**Casual attacker / Случайный атакующий:**
- Access to the disk after device theft / Доступ к диску после кражи устройства
- Opportunistic data scraping / Оппортунистический сбор данных
- Basic forensic tools / Базовые инструменты цифровой криминалистики

### Secondary threat / Вторичная угроза
**Targeted attacker / Целевой атакующий:**
- Network interception (MITM) / Перехват трафика (MITM)
- Offline password brute-force / Offline-перебор пароля
- Statistical steganalysis / Статистический стегоанализ

### Out of scope / Вне области защиты
- State-level adversaries (NSA, FSB) / Противники уровня государства
- Compromised OS / kernel / Скомпрометированная ОС / ядро
- Physical access during active session / Физический доступ во время активной сессии
- Quantum computers (until v1.1 with Kyber) / Квантовые компьютеры (до v1.1 с Kyber)

---

## ✅ What Grail guarantees / Что гарантирует Grail

1. **Confidentiality at rest / Конфиденциальность в покое**
   - AES-256-GCM with unique nonce per message
   - PBKDF2-HMAC-SHA256, 600,000 iterations (OWASP) for passwords
   - GCM authentication tag prevents ciphertext tampering

2. **Integrity / Целостность**
   - SHA-256 hash over nonce+ciphertext
   - GCM AEAD detects any bit-level modification

3. **Obfuscation / Обфускация**
   - LSB steganography hides the *fact* of transmission
   - Honest disclosure: LSB is detectable — confidentiality comes from AES

4. **Audit trail / Журнал аудита**
   - Tamper-evident blockchain log on disk
   - Detects *accidental* modifications, not targeted attacks

5. **Key hygiene / Гигиена ключей**
   - Self-destruct on failed attempts / inactivity
   - Best-effort RAM wipe (Python limitation: see below)

---

## ⚠️ Known limitations / Известные ограничения

### 1. RAM cannot be reliably wiped / RAM нельзя надёжно стереть
Python objects are immutable; `del` does not overwrite memory.
Self-destruct is **best effort**, not a guarantee.

Объекты Python immutable; `del` не перезаписывает память.
Self-Destruct — **попытка**, а не гарантия.

### 2. LSB steganography is detectable / LSB обнаруживается
Steganalysis tools can identify LSB-modified images with high confidence.
The real protection is encryption, not hiding.

### 3. No forward secrecy / Нет совершенной прямой секретности
Each message uses an independent key derived from the password.
If the password is compromised, all past messages are exposed.

### 4. Side-channel attacks not mitigated / Side-channel атаки не митигируются
No constant-time implementation, no cache-line protection.
Acceptable for the target threat model, not for state-level adversaries.

### 5. Blockchain audit is tamper-evident, not tamper-proof
An attacker with write access can rewrite the entire chain.
Useful against accidents and lazy insiders, not targeted attacks.

---

## 🎯 Target use cases / Целевые сценарии

✅ **Good for / Хорошо для:**
- Personal notes and journaling / Личные заметки и дневники
- Protecting credentials at rest / Защита учётных данных в покое
- Journalists protecting sources on a clean device / Журналисты, защищающие источники на чистом устройстве
- Educational / research purposes / Образовательные и исследовательские цели

⚠️ **Use with caution / Использовать с осторожностью:**
- High-value targets (whistleblowers, activists) — consider additional layers
- Medical / financial data — requires external audit
- Jurisdictions with forced decryption laws — legal, not technical

❌ **Not suitable for / Не подходит для:**
- Communication over hostile networks (use Signal instead)
- Protection against state-level adversaries
- Regulated industries without independent security audit

---

## 🔮 Future hardening / Будущее упрочнение

| Version | Improvement / Улучшение |
|---------|-------------------------|
| **v1.1** | Post-quantum Kyber-1024 hybrid encryption / Гибридное шифрование Kyber-1024 |
| **v1.2** | Constant-time crypto primitives / Constant-time примитивы |
| **v1.3** | Hardware security module integration (TPM, YubiKey) / Интеграция с HSM |
| **v2.0** | Formal verification of cryptographic protocol / Формальная верификация протокола |

---

## 📅 Document metadata / Метаданные документа

- **Version:** 1.0
- **Last updated:** August 2026
- **Author:** Grail team
- **Review status:** Self-reviewed, pending external audit

📄 Related: [README.md](README.md) · [README.en.md](README.en.md) · [SECURITY.md](SECURITY.md)

---

**Honest security is better than marketing promises.**
**Честная безопасность лучше маркетинговых обещаний.**
