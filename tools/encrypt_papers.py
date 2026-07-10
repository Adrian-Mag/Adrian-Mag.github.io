#!/usr/bin/env python3
"""
Encrypt in-preparation paper PDFs for the passcode-protected papers page.

Produces AES-256-GCM ciphertexts that pages/papers-in-prep.html decrypts
in the browser via WebCrypto. The access code IS the key (PBKDF2-derived),
so unlike the old hash-gate, the repository never contains readable drafts.

File format (binary):
    magic  b"AMV1"            4 bytes
    salt                     16 bytes   (PBKDF2-HMAC-SHA256, 600k iterations)
    nonce                    12 bytes   (AES-GCM)
    ciphertext || GCM tag    rest

Every file written in one run shares the salt (one key derivation per
session in the browser); each file gets a fresh nonce.

Usage:
    PAPERS_CODE='the access code' python3 tools/encrypt_papers.py draft1.pdf draft2.pdf

Writes <name>.enc plus vault-check.enc (a tiny canary the login page uses
to verify the code) into media/papers/. Never commit the plaintext PDFs.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "media" / "papers"
MAGIC = b"AMV1"
ITERATIONS = 600_000
CANARY = b"papers-vault-ok"


def derive_key(code: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", code.encode("utf-8"), salt, ITERATIONS, dklen=32)


def encrypt(data: bytes, key: bytes, salt: bytes) -> bytes:
    nonce = os.urandom(12)
    ct = AESGCM(key).encrypt(nonce, data, None)
    return MAGIC + salt + nonce + ct


def main() -> None:
    code = os.environ.get("PAPERS_CODE")
    if not code:
        sys.exit("Set the access code in the PAPERS_CODE environment variable.")
    if len(code) < 16:
        sys.exit("Access code is too short — use at least 16 characters (a multi-word passphrase).")
    files = [Path(a) for a in sys.argv[1:]]
    if not files:
        sys.exit("Usage: PAPERS_CODE='...' python3 tools/encrypt_papers.py <pdf> [<pdf> ...]")

    salt = os.urandom(16)
    key = derive_key(code, salt)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    for src in files:
        data = src.read_bytes()
        out = OUT_DIR / (src.name + ".enc")
        out.write_bytes(encrypt(data, key, salt))
        print(f"  {src.name} ({len(data)/1e6:.1f} MB) -> {out.relative_to(ROOT)}")

    canary = OUT_DIR / "vault-check.enc"
    canary.write_bytes(encrypt(CANARY, key, salt))
    print(f"  canary -> {canary.relative_to(ROOT)}")
    print("Done. Plaintext PDFs must NOT be committed.")


if __name__ == "__main__":
    main()
