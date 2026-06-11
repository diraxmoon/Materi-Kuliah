import streamlit as st
import queue_backend as q

# ─────────────────────────────────────────────
# SINKRONISASI SESSION STATE ↔ BACKEND
# ─────────────────────────────────────────────
if "queue" not in st.session_state:
    st.session_state.queue = q.queue


def putar_audio(teks: str):
    """Render audio player HTML autoplay di Streamlit."""
    b64 = q.buat_audio(teks)
    st.markdown(
        f'<audio autoplay><source src="data:audio/mp3;base64,{b64}" type="audio/mp3"></audio>',
        unsafe_allow_html=True
    )


# ─────────────────────────────────────────────
# DATA MENU
# ─────────────────────────────────────────────
MENU = {
    "🍜 Mie": [
        "Mie Gacoan Lv 0", "Mie Gacoan Lv 1", "Mie Gacoan Lv 2",
        "Mie Gacoan Lv 3", "Mie Gacoan Lv 4", "Mie Gacoan Lv 5",
        "Mie Gacoan Lv 6", "Mie Gacoan Lv 7", "Mie Gacoan Lv 8",
        "Mie Hompimpa", "Mie Suit",
    ],
    "🥟 Dimsum": [
        "Udang Rambutan", "Udang Keju", "Lumpia Udang",
        "Siomay", "Pangsit Goreng", "Ceker", "Lobster Ball", "Fish Roll",
    ],
    "🧊 Es & Minuman": [
        "Es Gobak Sodor", "Es Teklek", "Es Petak Umpet", "Es Sluku Bathok",
        "Es Teh", "Lemon Tea", "Vanilla Latte", "Thai Tea", "Milo",
    ],
}

# ─────────────────────────────────────────────
# KONFIGURASI HALAMAN
# ─────────────────────────────────────────────
st.set_page_config(page_title="Antrian Mie Gacoan", page_icon="🍜", layout="centered")

# ─────────────────────────────────────────────
# CUSTOM CSS — SIMPEL & BERSIH
# ─────────────────────────────────────────────
st.markdown("""
<style>
:root {
    --olive:      #606C38;
    --dark-green: #283618;
    --cream:      #FEFAE0;
    --tan:        #DDA15E;
    --brown:      #BC6C25;
}

/* Background */
.stApp {
    background-color: var(--cream);
}

/* Heading */
h1, h2, h3 {
    color: var(--dark-green) !important;
}

/* Text input — textbox terang, teks gelap */
div[data-testid="stTextInput"] input {
    background-color: var(--cream) !important;
    color: var(--dark-green) !important;
    border: 1.5px solid var(--olive) !important;
    border-radius: 8px !important;
    caret-color: var(--tan) !important;
}
div[data-testid="stTextInput"] input::placeholder {
    color: rgba(254,250,224,0.45) !important;
}
div[data-testid="stTextInput"] input:focus {
    border-color: var(--tan) !important;
    outline: none !important;
}
div[data-testid="stTextInput"] label {
    color: var(--dark-green) !important;
    font-weight: 600 !important;
}

/* Multiselect tag */
span[data-baseweb="tag"] {
    background-color: var(--olive) !important;
    color: var(--cream) !important;
    border-radius: 6px !important;
}

/* Primary button */
div[data-testid="stButton"] > button[kind="primary"] {
    background-color: var(--brown) !important;
    color: var(--cream) !important;
    border: none !important;
    border-radius: 8px !important;
    font-weight: 700 !important;
}
div[data-testid="stButton"] > button[kind="primary"]:hover {
    background-color: var(--tan) !important;
    color: var(--dark-green) !important;
}

/* Secondary buttons */
div[data-testid="stButton"] > button[kind="secondary"] {
    background-color: transparent !important;
    color: var(--dark-green) !important;
    border: 1.5px solid var(--olive) !important;
    border-radius: 8px !important;
    font-weight: 600 !important;
}
div[data-testid="stButton"] > button[kind="secondary"]:hover {
    background-color: var(--olive) !important;
    color: var(--cream) !important;
}

/* Divider */
hr {
    border-top: 1.5px solid var(--tan) !important;
    opacity: 0.4 !important;
}

/* Caption */
div[data-testid="stCaptionContainer"] p {
    color: var(--brown) !important;
    font-weight: 600 !important;
}

/* Body text */
p, div[data-testid="stMarkdownContainer"] p {
    color: var(--dark-green) !important;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TAMPILAN UTAMA
# ─────────────────────────────────────────────
st.title("🍜 Sistem Antrian Restoran")
st.subheader("Mie Gacoan — Konsep Queue (FIFO)")
st.divider()

# ── BAGIAN 1: ENQUEUE ─────────────────────────
st.subheader("➕ Tambah Pelanggan (Enqueue)")

nama_input = st.text_input("Nama Pelanggan", placeholder="cth: Farhan")

pesanan_list = []
for kategori, items in MENU.items():
    with st.expander(kategori):
        pilihan = st.multiselect(f"Pilih {kategori}", items, key=kategori)
        pesanan_list.extend(pilihan)

if pesanan_list:
    st.caption(f"🛒 Pesanan dipilih: {', '.join(pesanan_list)}")

if st.button("🪑 Masukkan ke Antrian", use_container_width=True):
    if not nama_input.strip():
        st.warning("⚠️ Nama pelanggan tidak boleh kosong.")
    elif not pesanan_list:
        st.warning("⚠️ Pilih minimal satu pesanan.")
    else:
        pesanan_str = ", ".join(pesanan_list)
        q.enqueue(nama_input.strip(), pesanan_str)
        st.success(f"✅ **{nama_input}** berhasil masuk antrian. Posisi: #{q.size()}")

st.divider()

# ── BAGIAN 2: DEQUEUE ─────────────────────────
st.subheader("📢 Panggil Pelanggan (Dequeue)")

if st.button("🔔 Panggil Pelanggan Berikutnya", use_container_width=True, type="primary"):
    if q.is_empty():
        st.error("❌ Antrian kosong! Tidak ada pelanggan yang perlu dipanggil.")
    else:
        pelanggan = q.dequeue()
        nama    = pelanggan["nama"]
        pesanan = pelanggan["pesanan"]
        teks    = f"Atas nama {nama}, pesanan {pesanan} siap diambil. Silakan menuju kasir."

        st.success(f"📣 Memanggil: **{nama}** — {pesanan}")
        st.info(f"🔊 *\"{teks}\"*")

        try:
            putar_audio(teks)
        except Exception as e:
            st.warning(f"Audio tidak dapat diputar: {e}")

st.divider()

# ── BAGIAN 3: STATUS ANTRIAN ──────────────────
st.subheader("📋 Status Antrian")

col_f, col_r, col_s = st.columns(3)
with col_f:
    f = q.front()
    st.metric("🟢 Depan (Front)", f["nama"] if f else "—")
with col_r:
    r = q.rear()
    st.metric("🔴 Belakang (Rear)", r["nama"] if r else "—")
with col_s:
    st.metric("👥 Total Antrian", q.size())

# ── BAGIAN 4: ISI ANTRIAN ─────────────────────
st.subheader("🗂️ Isi Antrian Saat Ini")

if q.is_empty():
    st.info("Antrian kosong. Silakan tambahkan pelanggan.")
else:
    for i, p in enumerate(q.queue):
        label = "🟢 DEPAN" if i == 0 else ("🔴 BELAKANG" if i == q.size() - 1 else f"#{i+1}")
        st.write(f"**{label}** → {p['nama']} | {p['pesanan']}")

st.divider()

if st.button("🗑️ Reset Antrian", use_container_width=True):
    q.reset()
    st.success("Antrian telah direset.")
    st.rerun()