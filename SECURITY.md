# Security Policy / Политика безопасности

## Supported Versions / Поддерживаемые версии

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |
| < 1.0   | :x:                |

## Reporting a Vulnerability / Сообщение об уязвимости

We take security seriously. If you discover a vulnerability in Grail, please report it responsibly.

Если вы обнаружили уязвимость в Grail, пожалуйста, сообщите о ней ответственно.

**How to report / Как сообщить:**
1. Do NOT open a public issue. / Не создавайте публичный issue.
2. Email us at support@grail-security.com with subject "SECURITY: [brief description]". / Напишите на support@grail-security.com с темой "SECURITY: [краткое описание]".
3. Include steps to reproduce, affected versions, and impact. / Приложите шаги воспроизведения, затронутые версии и влияние.

**What to expect / Что ожидать:**
- Acknowledgement within 24 hours. / Подтверждение в течение 24 часов.
- Status update within 72 hours. / Статус в течение 72 часов.
- Coordinated disclosure after a fix is released. / Скоординированное раскрытие после выпуска исправления.

## Security Practices in Grail / Практики безопасности в Grail

- AES-256-GCM with a unique nonce per message / AES-256-GCM с уникальным nonce для каждого сообщения
- Integrity verification via SHA-256 / Проверка целостности через SHA-256
- Keys held in RAM only, wiped on self-destruct / Ключи только в RAM, стираются при самоуничтожении
- Local-only processing, no telemetry / Только локальная обработка, без телеметрии
