"""Hybrid handshake server: X25519 + ML-KEM (Kyber768)."""

import json
import os
import struct
from http.server import BaseHTTPRequestHandler, HTTPServer

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

HOST = "127.0.0.1"
PORT = 8443


class HybridServer:
    def __init__(self) -> None:
        self.x25519_private = X25519PrivateKey.generate()
        self.x25519_public = self.x25519_private.public_key()

        if oqs is None:
            raise RuntimeError(
                "liboqs not available. Install Git + CMake, then: pip install liboqs-python"
            )

        with oqs.KeyEncapsulation(KEM_ALG) as kem:
            self.kem_public = kem.generate_keypair()
            self.kem_secret = kem.export_secret_key()

    def public_keys(self) -> dict:
        return {
            "x25519_public": self.x25519_public.public_bytes(
                Encoding.Raw, PublicFormat.Raw
            ).hex(),
            "kem_public": self.kem_public.hex(),
            "kem_alg": KEM_ALG,
        }

    def complete_handshake(
        self, client_x25519_hex: str, kem_ciphertext_hex: str
    ) -> tuple[bytes, bytes]:
        client_x25519 = X25519PublicKey.from_public_bytes(
            bytes.fromhex(client_x25519_hex)
        )
        x25519_shared = self.x25519_private.exchange(client_x25519)

        kem_ciphertext = bytes.fromhex(kem_ciphertext_hex)
        with oqs.KeyEncapsulation(KEM_ALG, self.kem_secret) as kem:
            kem_shared = kem.decap_secret(kem_ciphertext)

        session_key = derive_hybrid_key(x25519_shared, kem_shared)
        return session_key, kem_shared


server_state = HybridServer()


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        print(f"[server] {self.address_string()} - {fmt % args}")

    def _json_response(self, code: int, payload: dict) -> None:
        body = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self) -> None:
        if self.path == "/public-keys":
            self._json_response(200, server_state.public_keys())
        else:
            self._json_response(404, {"error": "not found"})

    def do_POST(self) -> None:
        if self.path != "/handshake":
            self._json_response(404, {"error": "not found"})
            return

        length = int(self.headers.get("Content-Length", 0))
        data = json.loads(self.rfile.read(length))

        session_key, _ = server_state.complete_handshake(
            data["client_x25519_public"],
            data["kem_ciphertext"],
        )

        # Encrypt a confirmation token with the derived AES-256-GCM key
        nonce = os.urandom(12)
        aesgcm = AESGCM(session_key)
        ciphertext = aesgcm.encrypt(nonce, b"handshake-ok", None)

        self._json_response(
            200,
            {
                "status": "ok",
                "nonce": nonce.hex(),
                "ciphertext": ciphertext.hex(),
                "key_fingerprint": session_key[:8].hex(),
            },
        )


def main() -> None:
    print(f"Hybrid server starting on http://{HOST}:{PORT}")
    print(f"KEM algorithm: {KEM_ALG}")
    print(
        f"Server X25519 public: {server_state.public_keys()['x25519_public'][:32]}..."
    )
    HTTPServer((HOST, PORT), Handler).serve_forever()


if __name__ == "__main__":
    main()
