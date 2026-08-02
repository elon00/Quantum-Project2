# Quantum-Project2 — Hybrid Handshake (X25519 + ML-KEM)

Chapter 3 exercise from **The 4-Hour PQC Developer: Survival Guide**.

A minimal client-server hybrid key exchange combining:
- **X25519** (classical elliptic-curve Diffie-Hellman)
- **ML-KEM / Kyber768** (post-quantum key encapsulation via liboqs)

Both shared secrets are combined with **HKDF-SHA256** to produce a single **AES-256-GCM** session key.

## Why Hybrid?

Production systems (Signal, Google, Cloudflare) use hybrid mode so security holds even if one layer is broken:
- If quantum computers break ECC → ML-KEM still protects the key
- If ML-KEM is ever broken → X25519 still protects the key

## Prerequisites (Windows)

```powershell
winget install Python.Python.3.12 Git.Git Kitware.CMake
```

Refresh your terminal, then:

```powershell
cd C:\Users\marti\Projects\Quantum-Project2
pip install -r requirements.txt
python -c "import oqs; print(oqs.get_enabled_KEM_mechanisms())"
```

> First `import oqs` may take a few minutes — liboqs-python builds liboqs from source automatically.

## Run the Handshake

**Terminal 1 — start server:**
```powershell
python server.py
```

**Terminal 2 — run client:**
```powershell
python client.py
```

Expected output:
```
[client] Fetching server public keys...
[client] X25519 ECDH complete
[client] ML-KEM encapsulation complete (1088 bytes)
[client] Hybrid key derived: a1b2c3d4...
[client] Handshake verified — both sides share the same AES-256 key

Success! Session key (hex): ...
```

## Architecture

```
Client                          Server
  |                               |
  |-- GET /public-keys ---------->|
  |<-- x25519_pub, kem_pub -------|
  |                               |
  |  X25519 ECDH (ephemeral)      |
  |  ML-KEM encapsulate           |
  |                               |
  |-- POST /handshake ----------->|
  |   (client_x25519, kem_ct)     |
  |                               |  X25519 ECDH
  |                               |  ML-KEM decapsulate
  |                               |  HKDF(x25519_ss || kem_ss)
  |<-- AES-GCM confirmation ------|
  |                               |
  |  Verify confirmation          |
  |  (proves matching keys)       |
```

## Files

| File | Purpose |
|------|---------|
| `hybrid_kdf.py` | HKDF key derivation combining both shared secrets |
| `server.py` | HTTP server with hybrid handshake endpoint |
| `client.py` | Client that initiates and verifies the handshake |
| `requirements.txt` | Python dependencies |

## Production Notes

- **Key sizes**: Kyber768 public keys are ~1.2 KB vs X25519's 32 bytes — plan for larger TLS records
- **Latency**: ML-KEM adds ~0.1–1 ms on modern hardware; negligible for most apps
- **Algorithm names**: NIST finalized ML-KEM (was Kyber) and ML-DSA (was Dilithium) in 2024
- **TLS 1.3**: Real deployments use hybrid in TLS extensions (e.g., `X25519Kyber768Draft00`)

## What to Skip (Chapter 2)

- Lattice math / LWE theory
- Deprecated algorithms (SIKE, Rainbow)
- Quantum physics internals

Focus on integration, not invention.
