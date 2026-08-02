"""Hybrid handshake client: X25519 + ML-KEM (Kyber768)."""

import json
import sys
import urllib.error
import urllib.request

from cryptography.hazmat.primitives.asymmetric.x25519 import (
    X25519PrivateKey,
    X25519PublicKey,
)
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives.serialization import Encoding, PublicFormat

from hybrid_kdf import derive_hybrid_key

try:
    import oqs

    KEM_ALG = "Kyber768"
except ImportError:
    oqs = None
    KEM_ALG = None

SERVER = "http://127.0.0.1:8443"


def fetch_json(url: str, payload: dict | None = None) -> dict:
    if payload is None:
        req = urllib.request.Request(url)
    else:
        body = json.dumps(payload).encode()
        req = urllib.request.Request(
            url, data=body, headers={"Content-Type": "application/json"}, method="POST"
        )
    with urllib.request.urlopen(req, timeout=10) as resp:
        return json.loads(resp.read())


def run_handshake(server_url: str = SERVER) -> bytes:
    if oqs is None:
        raise RuntimeError(
            "liboqs not available. Install Git + CMake, then: pip install liboqs-python"
        )

    # 1. Fetch server public keys
    print("[client] Fetching server public keys...")
    server_keys = fetch_json(f"{server_url}/public-keys")
    server_x25519 = X25519PublicKey.from_public_bytes(
        bytes.fromhex(server_keys["x25519_public"])
    )
    server_kem_public = bytes.fromhex(server_keys["kem_public"])
    print(f"[client] Server KEM: {server_keys['kem_alg']}")

    # 2. Generate ephemeral X25519 keypair
    client_x25519_private = X25519PrivateKey.generate()
    client_x25519_public = client_x25519_private.public_key()
    x25519_shared = client_x25519_private.exchange(server_x25519)
    print("[client] X25519 ECDH complete")

    # 3. ML-KEM encapsulation
    with oqs.KeyEncapsulation(KEM_ALG) as kem:
        kem_ciphertext, kem_shared = kem.encap_secret(server_kem_public)
    print(f"[client] ML-KEM encapsulation complete ({len(kem_ciphertext)} bytes)")

    # 4. Derive hybrid session key locally
    session_key = derive_hybrid_key(x25519_shared, kem_shared)
    print(f"[client] Hybrid key derived: {session_key[:8].hex()}...")

    # 5. Send handshake to server
    print("[client] Sending handshake...")
    response = fetch_json(
        f"{server_url}/handshake",
        {
            "client_x25519_public": client_x25519_public.public_bytes(
                Encoding.Raw, PublicFormat.Raw
            ).hex(),
            "kem_ciphertext": kem_ciphertext.hex(),
        },
    )

    # 6. Verify server confirmation (proves both sides derived the same key)
    nonce = bytes.fromhex(response["nonce"])
    ciphertext = bytes.fromhex(response["ciphertext"])
    aesgcm = AESGCM(session_key)
    plaintext = aesgcm.decrypt(nonce, ciphertext, None)

    if plaintext != b"handshake-ok":
        raise ValueError("Server confirmation failed")

    if response["key_fingerprint"] != session_key[:8].hex():
        raise ValueError("Key fingerprint mismatch")

    print("[client] Handshake verified — both sides share the same AES-256 key")
    return session_key


def main() -> None:
    try:
        key = run_handshake()
        print(f"\nSuccess! Session key (hex): {key.hex()}")
    except urllib.error.URLError as e:
        print(f"Connection failed: {e}", file=sys.stderr)
        print("Start the server first: python server.py", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
