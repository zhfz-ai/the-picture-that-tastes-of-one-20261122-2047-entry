#!/usr/bin/env python3
"""Entry untuk kompetisi make.fun "The picture that tastes of one ingredient".

Ingredient tunggal: mozzarella. File entry.png di sebelah script ini
adalah close-up grilled cheese sandwich yang ditarik terpisah — untaian
mozzarella leleh yang glossy dan panjang merentang di antara dua belah
sourdough panggang keemasan, dengan uap naik. Gambar ini dipilih dari
enam kandidat yang dinilai menurut lima kriteria brief secara berurutan
(lihat JUDGE-SCORECARD.md): menang di kriteria 1 (sekali lihat langsung
terasa rasa mozzarellanya), kriteria 2 (leleh, gloss, dan uap, tidak
terasa plastik), dan kriteria 5 (cheese pull terbaca seketika di 300 px).

Program ini menyalin gambar tersebut ke /output/entry.png. File-nya
adalah JPEG 1024x1024 sebesar 211.757 byte, di dalam gate (PNG atau
JPEG utuh, maksimal 1.048.576 byte dan 1024x1024 piksel).

Hanya standard library, tanpa network, deterministik: setiap run
menulis byte yang persis sama.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE_PATH = os.path.join(HERE, "entry.png")

OUTPUT_DIR = "/output"
OUTPUT_PATH = os.path.join(OUTPUT_DIR, "entry.png")

# Izin yang diminta setelah penulisan: file bisa dibaca semua orang,
# folder bisa ditelusuri semua orang. Diterapkan best-effort saja.
FILE_MODE = 0o644
DIR_MODE = 0o755

# Batas atas ukuran gate: 1 MiB.
MAX_BYTES = 1_048_576


def best_effort_chmod(path: str, mode: int) -> None:
    # Sandbox penilai bisa saja sudah membuat /output milik user lain,
    # jadi penyesuaian izin hanya courtesy, bukan syarat: kalau chmod
    # ditolak, file yang sudah tertulis tetap dihitung.
    try:
        os.chmod(path, mode)
    except OSError:
        pass


def main() -> None:
    # Gagal dengan jelas daripada tidak menulis apa-apa kalau gambar
    # hilang atau di luar gate: /output kosong yang senyap toh skornya 0.
    size = os.path.getsize(SOURCE_PATH)
    if not 0 < size <= MAX_BYTES:
        raise SystemExit(f"entry.png is {size} bytes, outside the 1 MiB gate")
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    # Salin gambar yang sudah di-commit byte demi byte: entry-nya adalah gambar itu sendiri.
    shutil.copyfile(SOURCE_PATH, OUTPUT_PATH)
    # Penilai mengambil output sebagai user lain: biarkan file bisa dibaca
    # semua orang (0644) dan folder bisa ditelusuri (0755), best-effort
    # supaya /output milik orang lain tidak menggagalkan run.
    best_effort_chmod(OUTPUT_PATH, FILE_MODE)
    best_effort_chmod(OUTPUT_DIR, DIR_MODE)


if __name__ == "__main__":
    main()
