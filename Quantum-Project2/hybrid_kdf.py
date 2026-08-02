"""Hybrid key derivation: combine X25519 ECDH + ML-KEM shared secrets via HKDF."""

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.hkdf import HKDF


def derive_hybrid_key(
    x25519_shared: bytes,
    kem_shared: bytes,
    context: bytes = b"hybrid-handshake-v1",
    length: int = 32,
) -> bytes:
    """Combine classical and post-quantum shared secrets into one AES-256 key."""
    ikm = x25519_shared + kem_shared
    return HKDF(
        algorithm=hashes.SHA256(),
        length=length,
        salt=None,
        info=context,
    ).derive(ikm)
