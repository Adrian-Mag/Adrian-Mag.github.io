#!/usr/bin/env python3
"""
Re-key the papers vault: decrypt every media/papers/*.enc with the old access
code and re-encrypt it with a new one.

Companion to encrypt_papers.py. Use this when the access code must change and
the plaintext PDFs are no longer on disk (the normal state — plaintext drafts
are never kept in the repo).

All files written in one run share a fresh salt, so the browser derives the key
once per session. Plaintext only ever exists in memory here; nothing is written
to disk except the new ciphertexts.

Usage:
    OLD_CODE='current code' NEW_CODE='new code' python3 tools/rekey_vault.py

Add --dry-run to verify the old code decrypts everything without writing.
"""

from __future__ import annotations

import hashlib
import os
import sys
from pathlib import Path

from cryptography.exceptions import InvalidTag
from cryptography.hazmat.primitives.ciphers.aead import AESGCM

ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "media" / "papers"
MAGIC = b"AMV1"
ITERATIONS = 600_000
CANARY = b"papers-vault-ok"
MIN_CODE_LEN = 16


def derive_key(code: str, salt: bytes) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", code.encode("utf-8"), salt, ITERATIONS, dklen=32)


def decrypt(blob: bytes, code: str) -> bytes:
    if blob[:4] != MAGIC:
        raise ValueError("not an AMV1 container")
    salt, nonce, ct = blob[4:20], blob[20:32], blob[32:]
    return AESGCM(derive_key(code, salt)).decrypt(nonce, ct, None)


def encrypt(data: bytes, key: bytes, salt: bytes) -> bytes:
    nonce = os.urandom(12)
    return MAGIC + salt + nonce + AESGCM(key).encrypt(nonce, data, None)


def main() -> None:
    old_code = os.environ.get("OLD_CODE")
    new_code = os.environ.get("NEW_CODE")
    if not old_code or not new_code:
        sys.exit("Set both OLD_CODE and NEW_CODE in the environment.")
    if len(new_code) < MIN_CODE_LEN:
        sys.exit(f"New code is too short — use at least {MIN_CODE_LEN} characters.")
    if old_code == new_code:
        sys.exit("New code is identical to the old one — nothing to do.")

    dry_run = "--dry-run" in sys.argv
    targets = sorted(p for p in OUT_DIR.glob("*.enc") if p.name != "vault-check.enc")
    if not targets:
        sys.exit(f"No .enc files found in {OUT_DIR.relative_to(ROOT)}.")

    # Decrypt everything up front: if the old code is wrong for any file we
    # must not leave the vault half re-keyed.
    plaintexts: dict[Path, bytes] = {}
    for src in targets:
        try:
            plaintexts[src] = decrypt(src.read_bytes(), old_code)
        except InvalidTag:
            sys.exit(f"OLD_CODE does not decrypt {src.name} — aborting, nothing written.")
        except ValueError as exc:
            sys.exit(f"{src.name}: {exc} — aborting, nothing written.")
        print(f"  decrypted {src.name} ({len(plaintexts[src]) / 1e6:.1f} MB)")

    if dry_run:
        print("Dry run: old code verified against all files. Nothing written.")
        return

    salt = os.urandom(16)
    key = derive_key(new_code, salt)
    for src, data in plaintexts.items():
        src.write_bytes(encrypt(data, key, salt))
        print(f"  re-encrypted {src.name}")

    (OUT_DIR / "vault-check.enc").write_bytes(encrypt(CANARY, key, salt))
    print("  re-encrypted vault-check.enc (canary)")
    print(f"Done — {len(plaintexts)} file(s) re-keyed. Old code no longer works.")


if __name__ == "__main__":
    main()
