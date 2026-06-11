"""
================================================
BACKEND — Logika Queue & Audio
File    : queue_backend.py
Dikerjakan oleh: Farhan & Naila
================================================
"""

from collections import deque
from gtts import gTTS
import os
import tempfile
import base64

# ─────────────────────────────────────────────
# STRUKTUR DATA QUEUE
# Menggunakan collections.deque agar operasi
# append (enqueue) dan popleft (dequeue) O(1)
# ─────────────────────────────────────────────

queue = deque()


# ─────────────────────────────────────────────
# FUNGSI QUEUE
# ─────────────────────────────────────────────

def enqueue(nama: str, pesanan: str):
    """ENQUEUE: Tambah pelanggan ke belakang antrian. O(1)"""
    pelanggan = {"nama": nama, "pesanan": pesanan}
    queue.append(pelanggan)  # append = tambah ke belakang (rear)


def dequeue() -> dict | None:
    """DEQUEUE: Ambil pelanggan dari depan antrian. O(1)"""
    if is_empty():
        return None
    return queue.popleft()  # popleft = ambil dari depan (front)


def front() -> dict | None:
    """Lihat pelanggan paling depan tanpa menghapus."""
    return queue[0] if not is_empty() else None


def rear() -> dict | None:
    """Lihat pelanggan paling belakang tanpa menghapus."""
    return queue[-1] if not is_empty() else None


def is_empty() -> bool:
    """Cek apakah antrian kosong."""
    return len(queue) == 0


def size() -> int:
    """Jumlah pelanggan dalam antrian."""
    return len(queue)


def reset():
    """Kosongkan seluruh antrian."""
    queue.clear()


# ─────────────────────────────────────────────
# FUNGSI AUDIO (gTTS)
# ─────────────────────────────────────────────

def buat_audio(teks: str) -> str:
    """Generate MP3 dari teks, kembalikan sebagai base64 string."""
    tts = gTTS(text=teks, lang="id")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp:
        tts.save(tmp.name)
        tmp_path = tmp.name

    with open(tmp_path, "rb") as f:
        audio_bytes = f.read()
    os.remove(tmp_path)

    return base64.b64encode(audio_bytes).decode()
