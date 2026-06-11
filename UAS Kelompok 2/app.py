# ================================================
# FRONTEND — Streamlit App
# Sistem Antrian Restoran Mie Gacoan (FIFO Queue)
# Dikerjakan oleh: FATHIYAA & UMMI
# Jalankan: streamlit run app.py
# ================================================
 
import streamlit as st
import base64
from logic import Queue, buat_audio, estimasi_tunggu


#=========FATHIYA==========
#MENGATUR HALAMAN STREAMLIT
st.set_page_config(page_title="Antrian Mie Gacoan", page_icon="🍜", layout="wide")

#MENGATUR TAMPILAN 
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Mono:wght@400;500&family=DM+Sans:wght@300;400;500&display=swap');
html, body, [class*="css"] { 
    font-family:'DM Sans',sans-serif !important;
    background-color:#080e17 !important;
    color:#eee8da !important;
}

#MainMenu, footer, header { 
    visibility:hidden; 
}
                        
    .block-container { padding-top:1.2rem !important; }
    
    .app-header { 
        background:linear-gradient(180deg,#0d1824,rgba(8,14,23,0.8));
        border-bottom:0.5px solid rgba(212,133,58,0.25);
        padding:20px 28px 16px;
        display:flex;
        align-items:center;
        justify-content:space-between; 
        border-radius:0 0 14px 14px; 
        margin-bottom:4px; 
    }
            
    .app-title { 
        font-family:'Playfair Display',serif; 
        font-size:22px; 
        font-weight:900; 
        color:#eee8da; margin:0; 
    }
            
    .app-subtitle { 
        font-family:'DM Mono',monospace; 
        font-size:10px; 
        letter-spacing:1.5px; 
        color:#7a96b0; 
        text-transform:uppercase; 
        margin-top:2px; 
    }
    
    .fifo-badge { 
        background:rgba(123,108,246,0.15); 
        border:0.5px solid rgba(123,108,246,0.35); 
        color:#a89ff8; 
        font-family:'DM Mono',monospace; 
        font-size:10px; 
        letter-spacing:1.5px; 
        padding:4px 14px; 
        border-radius:20px; 
    }
    
    .amber-line { 
        height:3px; 
        background:linear-gradient(90deg,transparent,rgba(212,133,58,0.5),rgba(212,133,58,0.8),rgba(212,133,58,0.5),transparent); 
        margin-bottom:20px; 
        border-radius:2px; 
    }
            
    .sec-title { 
        font-family:'Playfair Display',serif; font-size:15px; font-weight:700; color:#eee8da; margin-bottom:4px; }
    .sec-sub { font-family:'DM Mono',monospace; font-size:10px; color:#7a96b0; letter-spacing:0.5px; margin-bottom:14px; }
    .stat-row { display:flex; gap:10px; margin-bottom:20px; }
    .stat-card { flex:1; background:rgba(19,33,48,0.7); border:0.5px solid rgba(212,133,58,0.18); border-radius:10px; padding:13px 15px; position:relative; overflow:hidden; }
    .stat-card::before { content:''; position:absolute; top:0; left:0; right:0; height:1px; background:linear-gradient(90deg,transparent,rgba(212,133,58,0.4),transparent); }
    .stat-label { font-family:'DM Mono',monospace; font-size:9px; letter-spacing:1.5px; text-transform:uppercase; color:#3d5068; margin-bottom:5px; }
    .stat-value { font-family:'Playfair Display',serif; font-size:26px; font-weight:700; color:#e8a55a; line-height:1; }
    .stat-unit { font-family:'DM Mono',monospace; font-size:9px; color:#7a96b0; margin-top:2px; }
    
/* Info box front/rear */
    .info-box { display:flex; gap:10px; margin-bottom:16px; }
    .info-card { flex:1; background:rgba(19,33,48,0.6); border:0.5px solid rgba(212,133,58,0.2); border-radius:10px; padding:11px 14px; }
    .info-card.front-card { border-color:rgba(212,133,58,0.5); }
    .info-card.rear-card { border-color:rgba(123,108,246,0.3); }
    .info-tag { font-family:'DM Mono',monospace; font-size:9px; letter-spacing:1.5px; text-transform:uppercase; margin-bottom:4px; }
    .info-tag.f { color:#e8a55a; } .info-tag.r { color:#a89ff8; }
    .info-name { font-size:13px; font-weight:500; color:#eee8da; }
    .info-meta { font-family:'DM Mono',monospace; font-size:10px; color:#7a96b0; margin-top:2px; }
    
/* Queue cards */
    .q-card { background:rgba(19,33,48,0.6); border:0.5px solid rgba(212,133,58,0.15); border-radius:10px; padding:12px 15px; display:flex; align-items:center; gap:13px; margin-bottom:9px; }
    .q-card.front { border-color:rgba(212,133,58,0.55); background:rgba(212,133,58,0.06); border-left:2px solid #d4853a; }
    .q-num { width:30px; height:30px; border-radius:8px; border:0.5px solid rgba(212,133,58,0.3); background:rgba(212,133,58,0.1); color:#e8a55a; font-family:'DM Mono',monospace; font-size:12px; display:flex; align-items:center; justify-content:center; flex-shrink:0; }
    .q-num.front-num { background:#d4853a; color:#1a0f00; border-color:transparent; }
    .q-name { font-size:14px; font-weight:500; color:#eee8da; }
    .next-badge { display:inline-block; background:rgba(212,133,58,0.18); border:0.5px solid rgba(212,133,58,0.35); color:#f2c882; font-family:'DM Mono',monospace; font-size:9px; letter-spacing:1px; padding:2px 7px; border-radius:10px; margin-left:6px; }
    .q-order { font-size:11px; color:#7a96b0; }
    .q-right { text-align:right; margin-left:auto; }
    .q-posisi { font-family:'DM Mono',monospace; font-size:11px; color:#e8a55a; white-space:nowrap; }
    .q-posisi.front-pos { color:#4caf7d; }
    .q-waktu { font-family:'DM Mono',monospace; font-size:10px; color:#3d5068; margin-top:2px; }
    .empty-state { text-align:center; padding:45px 20px; color:#3d5068; }
    .stButton > button { background:#d4853a !important; color:#1a0f00 !important; border:none !important; border-radius:8px !important; font-family:'DM Sans',sans-serif !important; font-size:13px !important; font-weight:500 !important; width:100% !important; }
    .stButton > button:hover { background:#e8a55a !important; }

div[data-testid="column"]:nth-child(2)         
    .stButton > button { background:transparent !important; border:0.5px solid rgba(224,86,86,0.35) !important; color:#e05656 !important; }

div[data-testid="column"]:nth-child(2)
    .stButton > button:hover { background:rgba(224,86,86,0.08) !important; }
    .stTextInput > div > div > input { background:rgba(19,33,48,0.9) !important; border:0.5px solid rgba(212,133,58,0.35) !important; border-radius:8px !important; color:#eee8da !important; }
    .stMultiSelect > div > div { background:rgba(19,33,48,0.9) !important; border:0.5px solid rgba(212,133,58,0.35) !important; border-radius:8px !important; }
    .stMultiSelect span[data-baseweb="tag"] { background:rgba(212,133,58,0.2) !important; color:#f2c882 !important; border-radius:20px !important; }
    label { color:#7a96b0 !important; font-family:'DM Mono',monospace !important; font-size:10px !important; letter-spacing:1px !important; text-transform:uppercase !important; }

        hr { border-color:rgba(212,133,58,0.15) !important; margin:16px 0 !important; }
</style>
""", unsafe_allow_html=True)

#AGAR DATA TDK HILANG SAT DI-REFRESH 
# ── SESSION STATE ──
if "queue"         not in st.session_state: st.session_state.queue         = Queue()
if "served"        not in st.session_state: st.session_state.served        = 0
if "audio"         not in st.session_state: st.session_state.audio         = None
if "just_submitted" not in st.session_state: st.session_state.just_submitted = False
q: Queue = st.session_state.queue
 
# ── HEADER ──
st.markdown("""
<div class="app-header">
  <div><p class="app-title">🍜 Sistem Antrian Restoran</p>
  <p class="app-subtitle">Mie Gacoan · Linked List Queue</p></div>
  <div class="fifo-badge">FIFO · LINKED LIST</div>
</div><div class="amber-line"></div>
""", unsafe_allow_html=True)

#Menyimpan MULTI SELECT MENU yang ada di TAG MENU 
MENU = {
    "🍜 Mie": ["Gacoan Level 0","Gacoan Level 1","Gacoan Level 2","Gacoan Level 3",
               "Gacoan Level 4","Gacoan Level 5","Gacoan Level 6","Gacoan Level 7",
               "Gacoan Level 8","Mie Hompimpa","Mie Suit"],
    "🥟 Dimsum": ["Udang Keju","Lumpia Udang","Udang Rambutan","Pangsit","Siomay"],
    "🧊 Es & Minuman": ["Es Teh Manis","Es Jeruk","Es Coklat","Air Mineral"],
}
 
col_kiri, col_kanan = st.columns([4, 5], gap="large")
 
# ╔══════════════════════════════╗
# ║  KIRI — Form Enqueue         ║
# ╚══════════════════════════════╝
with col_kiri:
    st.markdown('<div class="sec-title">+ Tambah Pelanggan</div><div class="sec-sub">Enqueue to Rear</div>', unsafe_allow_html=True)
 
    with st.form(key="form_enqueue", clear_on_submit=True):
        nama = st.text_input("Nama Pelanggan", placeholder="cth: Farhan")
        selected_items = []
        for kategori, items in MENU.items():
            with st.expander(kategori):
                pilihan = st.multiselect("Pilih", options=items, label_visibility="collapsed")
                selected_items.extend(pilihan)
 
        if selected_items and not st.session_state.just_submitted:
            tags = "".join(
                f'<span style="background:rgba(212,133,58,0.15);border:0.5px solid rgba(212,133,58,0.3);color:#f2c882;font-family:DM Mono,monospace;font-size:11px;padding:3px 10px;border-radius:20px;margin:3px;display:inline-block">{item}</span>'
                for item in selected_items
            )
            st.markdown(f'<div style="margin:8px 0 14px">{tags}</div>', unsafe_allow_html=True)
 
        submitted = st.form_submit_button("🪑 Masukkan ke Antrian")
        if submitted:
            if not nama.strip():
                st.session_state.just_submitted = False
                st.error("Nama pelanggan wajib diisi!")
            elif not selected_items:
                st.session_state.just_submitted = False
                st.error("Pilih minimal satu menu!")
            else:
                q.enqueue(nama.strip(), ", ".join(selected_items))
                st.success(f"✓ {nama.strip()} berhasil masuk antrian!")
                st.session_state.just_submitted = True
                st.rerun()
        else:
            st.session_state.just_submitted = False


#==========UMMI==========
# ╔══════════════════════════════╗
# ║  KANAN — Antrian & Kontrol   ║
# ╚══════════════════════════════╝
with col_kanan:
    total = q.size()
    front = q.front() # ini
    rear  = q.rear() # ini
 
    # Stat cards
    st.markdown(f"""
    <div class="stat-row">
      <div class="stat-card"><div class="stat-label">Total Antrian</div>
        <div class="stat-value">{total}</div><div class="stat-unit">pelanggan</div></div>
      <div class="stat-card"><div class="stat-label">Dilayani Hari Ini</div>
        <div class="stat-value">{st.session_state.served}</div><div class="stat-unit">pelanggan</div></div>
    </div>""", unsafe_allow_html=True)
 
    # Info front & rear #ini
    if front and rear:
        f_waktu = front["waktu_masuk"].strftime("%H:%M:%S")
        r_waktu = rear["waktu_masuk"].strftime("%H:%M:%S")
        st.markdown(f"""
        <div class="info-box">
          <div class="info-card front-card">
            <div class="info-tag f">HEAD / FRONT</div>
            <div class="info-name">{front["nama"]}</div>
            <div class="info-meta">Masuk: {f_waktu}</div>
          </div>
          <div class="info-card rear-card">
            <div class="info-tag r">TAIL / REAR</div>
            <div class="info-name">{rear["nama"]}</div>
            <div class="info-meta">Masuk: {r_waktu}</div>
          </div>
        </div>""", unsafe_allow_html=True)
 
    st.markdown('<div class="sec-title">≡ Antrian Saat Ini</div><div class="sec-sub">HEAD → TAIL</div>', unsafe_allow_html=True)
 
    b1, b2 = st.columns([3, 1.5])
    with b1:
        if st.button("▶ Layani Berikutnya (Dequeue)", key="btn_dequeue"):
            if q.is_empty():
                st.warning("Antrian sudah kosong!")
            else:
                removed = q.dequeue()
                st.session_state.served += 1
                teks = (f"Pelanggan atas nama {removed['nama']}, "
                        f"pesanan {removed['pesanan'].split(',')[0]}, "
                        f"silakan menuju kasir.")
                try:    st.session_state.audio = buat_audio(teks)
                except: st.session_state.audio = None
                st.success(f"✓ {removed['nama']} selesai dilayani!")
                st.rerun()
    with b2:
        if st.button("✕ Reset Antrian", key="btn_reset"):
            q.reset(); st.session_state.audio = None; st.rerun()
 
    st.markdown("<hr>", unsafe_allow_html=True)
 
    if st.session_state.audio:
        st.markdown("**🔊 Panggilan Terakhir**")
        st.audio(base64.b64decode(st.session_state.audio), format="audio/mp3")
 
    # Render kartu antrian
    antrian_list = q.to_list()
    if not antrian_list:
        st.markdown('<div class="empty-state"><p style="font-size:32px;opacity:0.3">🍜</p><p style="font-family:DM Mono,monospace;font-size:12px">Antrian masih kosong.</p></div>', unsafe_allow_html=True)
    else:
        for i, item in enumerate(antrian_list):
            is_front = i == 0
            card_cls = "front" if is_front else ""
            num_cls  = "front-num" if is_front else ""
            pos_cls  = "front-pos" if is_front else ""
            badge    = '<span class="next-badge">BERIKUTNYA</span>' if is_front else ""
            posisi   = "Giliran sekarang" if is_front else f"Antrian ke-{i+1}"
            waktu    = item["waktu_masuk"].strftime("%H:%M:%S")
            st.markdown(f"""
            <div class="q-card {card_cls}">
              <div class="q-num {num_cls}">{i+1}</div>
              <div style="flex:1;min-width:0">
                <div class="q-name">{item['nama']}{badge}</div>
                <div class="q-order">{item['pesanan']}</div>
              </div>
              <div class="q-right">
                <div class="q-posisi {pos_cls}">{posisi}</div>
                <div class="q-waktu">masuk {waktu}</div>
              </div>
            </div>""", unsafe_allow_html=True)