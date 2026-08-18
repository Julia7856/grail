"""Grail PQC layer / PQC-слой Grail

Hybrid post-quantum encryption for local secrets /
гибридное постквантовое шифрование локальных секретов.

v1.1 prototype: ML-KEM-768 (NIST FIPS 203) + X25519 -> HKDF-SHA256 -> AES-256-GCM.
Honest status / честный статус: prototype, not audited / прототип, не аудитировано.
Roadmap / план: PQC_ROADMAP.md

Why hybrid / зачем гибрид: break ML-KEM but X25519 holds, and vice versa.
HNDL: ciphertext recorded today stays secret even after Q-Day /
сломай ML-KEM — держит X25519, и наоборот. Шифртекст, записанный сегодня,
останется секретом и после Q-Day.

Install / установка: pip install kyber-py cryptography
"""

import os

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.kdf.hkdf import HKDF

try:
    from kyber import ML_KEM_768
    HAVE_PQ = True
except ImportError:
    HAVE_PQ = False


def _require_pq():
    if not HAVE_PQ:
        raise RuntimeError("kyber-py not installed / не установлен: pip install kyber-py")


def _hkdf(ikm: bytes, salt: bytes) -> bytes:
    return HKDF(
        algorithm=hashes.SHA256(), length=32, salt=salt, info=b"grail-pq-v1"
    ).derive(ikm)


def generate_identity() -> dict:
    """Long-term recipient keys / долговременные ключи получателя."""
    _require_pq()
    kem = ML_KEM_768()
    pq_pk, pq_sk = kem.keypair()
    ec = X25519PrivateKey.generate()
    return {
        "pq_pk": pq_pk,
        "pq_sk": pq_sk,
        "ec_pub": ec.public_key().public_bytes_raw(),
        "ec_priv": ec.private_bytes_raw(),
    }


def seal(plaintext: bytes, identity: dict) -> dict:
    """Encrypt for identity / зашифровать для identity."""
    _require_pq()
    kem = ML_KEM_768()
    pq_ct, ss_pq = kem.encap(identity["pq_pk"])
    eph = X25519PrivateKey.generate()
    ss_ec = eph.exchange(X25519PublicKey.from_public_bytes(identity["ec_pub"]))
    key = _hkdf(ss_pq + ss_ec, b"grail-hybrid")
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, plaintext, None)
    return {
        "v": 1,
        "pq_ct": pq_ct.hex(),
        "eph_pub": eph.public_key().public_bytes_raw().hex(),
        "nonce": nonce.hex(),
        "ct": ct.hex(),
    }


def open_env(envelope: dict, identity: dict) -> bytes:
    """Decrypt with identity / расшифровать с identity."""
    _require_pq()
    kem = ML_KEM_768()
    ss_pq = kem.decap(bytes.fromhex(envelope["pq_ct"]), identity["pq_sk"])
    eph_pub = X25519PublicKey.from_public_bytes(bytes.fromhex(envelope["eph_pub"]))
    ec_priv = X25519PrivateKey.from_private_bytes(identity["ec_priv"])
    ss_ec = ec_priv.exchange(eph_pub)
    key = _hkdf(ss_pq + ss_ec, b"grail-hybrid")
    return AESGCM(key).decrypt(
        bytes.fromhex(envelope["nonce"]), bytes.fromhex(envelope["ct"]), None
    )


if __name__ == "__main__":
    idn = generate_identity()
    env = seal("grail v1.1 PQC roundtrip".encode(), idn)
    print("roundtrip:", open_env(env, idn).decode())
    print("pq_ct bytes:", len(bytes.fromhex(env["pq_ct"])))
