# 🏆 Grail

**Your digital sanctuary. Untouchable. Local. Eternal.**

Grail is an international-grade data protection tool. A regex detector finds personal data, the cryptographic core encrypts it, steganography hides it inside ordinary images, and a self-destruct mechanism guarantees that keys never fall into the wrong hands.

---

## 🔑 Key Features

### 🔍 Regex PII Detector
- Detects phone numbers, emails, passports, bank cards, IP addresses
- International formats (RU, US, EU, UK, etc.)
- Runs locally — no data leaves your device
- Luhn validation for bank cards

### 🔒 Cryptographic Core
- **AES-256-GCM** — industry-standard encryption (NIST)
- **Unique nonce** per message
- Fully local, no cloud
- **Roadmap v1.1:** post-quantum Kyber-1024 (NIST PQC)

### 🖼️ Steganography
- Hides encrypted data inside PNG/BMP images (LSB method)
- Honest disclosure: LSB is detectable by statistical steganalysis — this is obfuscation, not perfect invisibility
- Confidentiality is guaranteed by AES-256-GCM encryption — steganography only masks the fact of transmission
- Message-length protocol (32-bit prefix)

### 🔗 Blockchain Audit
- Immutable on-disk journal, SHA-256 protected
- Automatic chain integrity verification

### 💣 Self-Destruct
- Key destruction after failed attempts or inactivity
- Keys overwritten with random data (unrecoverable from RAM)

### 🎨 GUI
- Dark-theme desktop app (Windows, macOS, Linux)

---

## 💰 Editions

| Edition | Price |
|---------|-------|
| **Community** | Free |
| **Pro** | Individual quote |
| **Enterprise** | Individual quote |

📄 Details: [PRICING.md](PRICING.md)

---

## 🚀 Quick Start

```bash
git clone https://github.com/Julia7856/grail.git
cd grail
pip install -r requirements.txt
python ultimate_grail.py
```

📖 Full guide: [INSTALL.md](INSTALL.md)

---

## 🛡️ License

**Business Source License 1.1 (BSL)**
- ✅ Non-commercial use: free
- ✅ Commercial use: via Pro/Enterprise license
- 📅 Change Date: January 1, 2029 → becomes Apache 2.0

📄 [LICENSE](LICENSE)

🌐 Русская версия: [README.md](README.md)

---

## 📞 Contact

Commercial license / audit: open an [Issue](https://github.com/Julia7856/grail/issues) — we reply within 24 hours.

---

**Grail International. Your privacy is our mission.** 🔐
