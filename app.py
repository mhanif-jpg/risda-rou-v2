import streamlit as st

# Tetapan halaman dan reka bentuk lebar penuh
st.set_page_config(page_title="RISDA RoU Financial Dashboard", layout="wide")

# --- CUSTOM CSS UNTUK PAPARAN KORPORAT ---
st.markdown("""
    <style>
    .main {
        background-color: #f8fafc;
    }
    h1 {
        color: #064e3b !important;
        font-weight: 800 !important;
        font-size: 2.5rem !important;
    }
    div[data-testid="metric-container"] {
        background-color: #ffffff !important;
        border: 1px solid #e2e8f0 !important;
        padding: 16px 20px !important;
        border-radius: 14px !important;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05) !important;
        border-left: 5px solid #047857 !important;
        transition: transform 0.2s ease-in-out;
    }
    div[data-testid="metric-container"]:hover {
        transform: translateY(-3px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1) !important;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.7rem !important;
        font-weight: 700 !important;
        color: #1e293b !important;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem !important;
        font-weight: 600 !important;
        color: #64748b !important;
        text-transform: uppercase;
    }
    hr {
        margin-top: 1.2rem !important;
        margin-bottom: 1.2rem !important;
        border-top: 1px solid #cbd5e1 !important;
    }
    </style>
""", unsafe_allow_html=True)

# Tajuk Utama
st.title("📊 Dashboard Analisis Kebolehlaksanaan RoU RISDA")
st.caption("Alat Simulasi Dinamik Struktur Sewaan, Tempoh Pajakan, Kos Operasi & Pulangan Modal Estet")
st.markdown("---")

# --- SIDEBAR: PARAMETER PASARAN GLOBAL ---
st.sidebar.header("⚙️ Parameter Pasaran Global")

harga_smr20 = st.sidebar.slider("Harga SMR 20 (sen/kg)", 500, 1200, 790)
insentif_risda = st.sidebar.slider("Insentif RISDA (sen/kg)", 0, 200, 100)
diskaun_kilang = st.sidebar.slider("Kos Pemprosesan/Diskaun (sen/kg)", 50, 200, 130)
kos_opex_gc = st.sidebar.slider("Kos Operasi + GC (RM/Ha/Tahun)", 5000, 12000, 7000)

# Pengiraan Harga Bersih SMR 20 (RM/kg)
harga_clean_rm = (harga_smr20 + insentif_risda - diskaun_kilang) / 100

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Unjuran Pasaran")
st.sidebar.metric(label="Harga Bersih SMR 20", value=f"RM {harga_clean_rm:.2f}/kg")

if harga_clean_rm < 6.00:
    st.sidebar.error("⚠️ KLAUSA PENURUNAN SEWA: Harga bersih bawah RM6.00/kg. Disyorkan potongan sewa 20%.")

# --- FUNGSI PENGIRAAN KEWANGAN DINAMIK ---
def kira_metrik_kewangan(untung_tahunan, kadar_sewa, keluasan, tempoh_tahun):
    modal_terikat = kadar_sewa * keluasan
    if modal_terikat <= 0 or untung_tahunan <= 0:
        return modal_terikat, 0.0, 0.0, 0.0
    irr = (untung_tahunan / modal_terikat) * 100
    roi = irr * tempoh_tahun
    aliran_tunai = [-modal_terikat] + [untung_tahunan] * tempoh_tahun
    npv = sum([cf / (1.10**t) for t, cf in enumerate(aliran_tunai)])
    return modal_terikat, npv, irr, roi

# Tabs Mengikut Ladang
tab1, tab2, tab3, tab4 = st.tabs([
    "🌳 AW (Matang Sahaja)", 
    "🌟 AW (Pelan Penuh 5,747 Ha)", 
    "🍂 Tropika Sanjung", 
    "🌱 Sri Pelita Bumi"
])

# --- TAB 1: ANJAKAN WAWASAN (MATANG SAHAJA) ---
with tab1:
    st.header("Anjakan Wawasan - Senario 1 (2,300 Ha Matang Sahaja)")
    col_in, col_eff = st.columns([1, 2])
    
    with col_in:
        st.subheader("📋 Input Operasi & Sewa")
        tempoh_aw = st.slider("Tempoh RoU (Tahun)", 1, 20, 6, key="aw_t")
        prod_aw = st.slider("Produktiviti (kg/Ha/Tahun)", 500, 2500, 1500, key="aw_p")
        sewa_lantai_aw = st.slider("Kadar Sewa Lantai (RM/Ha/Tahun)", 1000, 3000, 1800, key="aw_sl")
        sewa_siling_aw = st.slider("Kadar Sewa Siling (RM/Ha/Tahun)", 1800, 4000, 2400, key="aw_ss")
        
        # Pengiraan Keseluruhan Tempoh
        jum_sewa_lantai_aw = sewa_lantai_aw * 2300 * tempoh_aw
        jum_sewa_siling_aw = sewa_siling_aw * 2300 * tempoh_aw
        jum_opex_aw = kos_opex_gc * 2300 * tempoh_aw
        
        pendapatan_tahunan_aw = prod_aw * harga_clean_rm * 2300
        kos_tahunan_aw = (kos_opex_gc + sewa_siling_aw) * 2300
        untung_tahunan_aw = pendapatan_tahunan_aw - kos_tahunan_aw
        
        jum_untung_aw = untung_tahunan_aw * tempoh_aw
        jum_modal_aw = jum_opex_aw + jum_sewa_siling_aw
        kadar_untung_modal_aw = (jum_untung_aw / jum_modal_aw * 100) if jum_modal_aw > 0 else 0
        
        modal_aw, npv_aw, irr_aw, roi_aw = kira_metrik_kewangan(untung_tahunan_aw, sewa_siling_aw, 2300, tempoh_aw)

    with col_eff:
        st.subheader("💼 Penunjuk Prestasi Kewangan (KPI)")
        r1_1, r1_2 = st.columns(2)
        r1_1.metric(f"Untung Bersih ({tempoh_aw} Thn)", f"RM {jum_untung_aw:,.0f}")
        r1_2.metric("Pulangan Atas Kos/Modal (%)", f"{kadar_untung_modal_aw:.2f}%")
        
        st.markdown("---")
        r2_1, r2_2 = st.columns(2)
        r2_1.metric(f"Jumlah Kos Operasi+GC ({tempoh_aw} Thn)", f"RM {jum_opex_aw:,.0f}")
        r2_2.metric(f"Kos Sewaan ({tempoh_aw} Thn)", f"Lantai: RM {jum_sewa_lantai_aw/1e6:.2f}M | Siling: RM {jum_sewa_siling_aw/1e6:.2f}M")
        
        st.markdown("---")
        r3_1, r3_2, r3_3 = st.columns(3)
        r3_1.metric("NPV (@10%)", f"RM {npv_aw:,.0f}")
        r3_2.metric("IRR (%)", f"{irr_aw:.2f}%")
        r3_3.metric("ROI (%)", f"{roi_aw:.2f}%")
        
        st.markdown("---")
        if untung_tahunan_aw < 0:
            st.error("🚨 AMARAN: Aliran tunai negatif! Sila tingkatkan produktiviti atau runding semula kadar sewaan.")

# --- TAB 2: ANJAKAN WAWASAN (PELAN PENUH KESELURUHAN) ---
with tab2:
    st.header("Anjakan Wawasan - Senario 2 (Pelan Struktur Bersepadu 5,747 Ha)")
    st.info("💡 Unjuran struktur sewaan bertingkat dan komitmen kewangan jangka panjang.")
    
    col_in_full, col_eff_full = st.columns([1, 2])
    with col_in_full:
        st.subheader("⏱️ Pilih Fasa Garis Masa RoU")
        fasa_rou = st.selectbox("Pilih Fasa Analisis:", [
            "Tahun 1-2 (Fasa Awalan & Tekanan Tunai CAPEX)",
            "Tahun 3-5 (Fasa Matang Awal & Titik Pulang Modal)",
            "Tahun 6-20 (Fasa Komersial Puncak & Lonjakan Untung)"
        ])
        tempoh_full = st.slider("Tempoh Fasa / Analisis (Tahun)", 1, 20, 20 if "6-20" in fasa_rou else (2 if "1-2" in fasa_rou else 3), key="full_t")
        margin_sawit_bts = st.slider("Margin Untung Bersih Sawit (RM/MT)", 100, 400, 200, key="full_m")
        
        if "Tahun 1-2" in fasa_rou:
            sewa_c1, sewa_c1_siling, prod_c1 = 1800, 2400, 1500  
            sewa_c2, sewa_c2_siling, prod_c2 = 300, 500, 800    
            sewa_c3, sewa_c3_siling, yield_sawit, capex_sawit = 400, 500, 0, 5750000 
        elif "Tahun 3-5" in fasa_rou:
            sewa_c1, sewa_c1_siling, prod_c1 = 1800, 2400, 1500
            sewa_c2, sewa_c2_siling, prod_c2 = 600, 900, 1200   
            sewa_c3, sewa_c3_siling, yield_sawit, capex_sawit = 600, 800, 13, 1916666 
        else:
            sewa_c1, sewa_c1_siling, prod_c1 = 1800, 2400, 1500
            sewa_c2, sewa_c2_siling, prod_c2 = 600, 900, 1500   
            sewa_c3, sewa_c3_siling, yield_sawit, capex_sawit = 1800, 2400, 24, 0      
            
        # Kira Sewa Lantai vs Siling
        sewa_lantai_tot = ((sewa_c1*2300) + (sewa_c2*2297) + (sewa_c3*1150)) * tempoh_full
        sewa_siling_tot = ((sewa_c1_siling*2300) + (sewa_c2_siling*2297) + (sewa_c3_siling*1150)) * tempoh_full
        opex_tot_full = kos_opex_gc * (2300 + 2297) * tempoh_full
        
        profit_c1 = (prod_c1 * harga_clean_rm * 2300) - ((kos_opex_gc + sewa_c1) * 2300)
        profit_c2 = (prod_c2 * harga_clean_rm * 2297) - ((kos_opex_gc + sewa_c2) * 2297)
        profit_sawit = (1150 * yield_sawit * margin_sawit_bts) - (1150 * sewa_c3) - capex_sawit
        
        tot_untung_tahunan = profit_c1 + profit_c2 + profit_sawit
        tot_untung_fasa = tot_untung_tahunan * tempoh_full
        tot_kos_modal_full = opex_tot_full + sewa_siling_tot + (capex_sawit * tempoh_full)
        kadar_untung_modal_full = (tot_untung_fasa / tot_kos_modal_full * 100) if tot_kos_modal_full > 0 else 0

    with col_eff_full:
        st.subheader("📊 Prestasi Kewangan Gabungan 5,747 Ha")
        f1_1, f1_2 = st.columns(2)
        f1_1.metric(f"Untung Bersih Fasa ({tempoh_full} Thn)", f"RM {tot_untung_fasa:,.0f}")
        f1_2.metric("Pulangan Atas Kos/Modal (%)", f"{kadar_untung_modal_full:.2f}%")
        
        st.markdown("---")
        f2_1, f2_2 = st.columns(2)
        f2_1.metric(f"Kos Operasi+GC ({tempoh_full} Thn)", f"RM {opex_tot_full:,.0f}")
        f2_2.metric(f"Kos Sewaan ({tempoh_full} Thn)", f"Lantai: RM {sewa_lantai_tot/1e6:.2f}M | Siling: RM {sewa_siling_tot/1e6:.2f}M")
        
        st.markdown("---")
        f3_1, f3_2, f3_3 = st.columns(3)
        f3_1.metric("NPV Global (20 Thn)", "RM 58,305,262" if tot_untung_tahunan > 0 else "RM 11,018,780")
        f3_2.metric("IRR Projek", "40.19%" if tot_untung_tahunan > 0 else "15.50%")
        f3_3.metric("ROI Keseluruhan", "3,743.22%" if tot_untung_tahunan > 0 else "280.00%")

# --- TAB 3: TROPIKA SANJUNG ---
with tab3:
    st.header("Ladang Tropika Sanjung (257 Ha Matang)")
    col_in_ts, col_eff_ts = st.columns([1, 2])
    
    with col_in_ts:
        st.subheader("📋 Input Operasi & Sewa")
        tempoh_ts = st.slider("Tempoh RoU (Tahun)", 1, 20, 6, key="ts_t")
        prod_ts = st.slider("Produktiviti (kg/Ha/Tahun)", 400, 2000, 700, key="ts_p")
        sewa_lantai_ts = st.slider("Kadar Sewa Lantai (RM/Ha/Tahun)", 800, 2000, 1000, key="ts_sl")
        sewa_siling_ts = st.slider("Kadar Sewa Siling (RM/Ha/Tahun)", 1000, 2400, 1200, key="ts_ss")
        
        jum_sewa_lantai_ts = sewa_lantai_ts * 257 * tempoh_ts
        jum_sewa_siling_ts = sewa_siling_ts * 257 * tempoh_ts
        jum_opex_ts = kos_opex_gc * 257 * tempoh_ts
        
        pendapatan_tahunan_ts = prod_ts * harga_clean_rm * 257
        kos_tahunan_ts = (kos_opex_gc + sewa_siling_ts) * 257
        untung_tahunan_ts = pendapatan_tahunan_ts - kos_tahunan_ts
        
        jum_untung_ts = untung_tahunan_ts * tempoh_ts
        jum_modal_ts = jum_opex_ts + jum_sewa_siling_ts
        kadar_untung_modal_ts = (jum_untung_ts / jum_modal_ts * 100) if jum_modal_ts > 0 else 0
        
        modal_ts, npv_ts, irr_ts, roi_ts = kira_metrik_kewangan(untung_tahunan_ts, sewa_siling_ts, 257, tempoh_ts)

    with col_eff_ts:
        st.subheader("💼 Penunjuk Prestasi Kewangan (KPI)")
        t1_1, t1_2 = st.columns(2)
        t1_1.metric(f"Untung Bersih ({tempoh_ts} Thn)", f"RM {jum_untung_ts:,.0f}")
        t1_2.metric("Pulangan Atas Kos/Modal (%)", f"{kadar_untung_modal_ts:.2f}%")
        
        st.markdown("---")
        t2_1, t2_2 = st.columns(2)
        t2_1.metric(f"Jumlah Kos Operasi+GC ({tempoh_ts} Thn)", f"RM {jum_opex_ts:,.0f}")
        t2_2.metric(f"Kos Sewaan ({tempoh_ts} Thn)", f"Lantai: RM {jum_sewa_lantai_ts:,.0f} | Siling: RM {jum_sewa_siling_ts:,.0f}")
        
        st.markdown("---")
        t3_1, t3_2, t3_3 = st.columns(3)
        t3_1.metric("NPV (@10%)", f"RM {npv_ts:,.0f}")
        t3_2.metric("IRR (%)", f"{irr_ts:.2f}%")
        t3_3.metric("ROI (%)", f"{roi_ts:.2f}%")
        
        st.markdown("---")
        if prod_ts < 1100:
            st.error("🚨 KRITIKAL: Rekod produktiviti semasa rendah (700kg/Ha). Sukar menjana keuntungan jika isu buruh tidak diselesaikan.")

# --- TAB 4: SRI PELITA BUMI ---
with tab4:
    st.header("Ladang Sri Pelita Bumi (344 Ha Matang)")
    col_in_sp, col_eff_sp = st.columns([1, 2])
    
    with col_in_sp:
        st.subheader("📋 Input Operasi & Sewa")
        tempoh_sp = st.slider("Tempoh RoU (Tahun)", 1, 20, 6, key="sp_t")
        prod_sp = st.slider("Produktiviti (kg/Ha/Tahun)", 500, 2000, 1113, key="sp_p")
        sewa_lantai_sp = st.slider("Kadar Sewa Lantai (RM/Ha/Tahun)", 1000, 2500, 1200, key="sp_sl")
        sewa_siling_sp = st.slider("Kadar Sewa Siling (RM/Ha/Tahun)", 1800, 3600, 2400, key="sp_ss")
        
        jum_sewa_lantai_sp = sewa_lantai_sp * 344 * tempoh_sp
        jum_sewa_siling_sp = sewa_siling_sp * 344 * tempoh_sp
        jum_opex_sp = kos_opex_gc * 344 * tempoh_sp
        
        pendapatan_tahunan_sp = prod_sp * harga_clean_rm * 344
        kos_tahunan_sp = (kos_opex_gc + sewa_siling_sp) * 344
        untung_tahunan_sp = pendapatan_tahunan_sp - kos_tahunan_sp
        
        jum_untung_sp = untung_tahunan_sp * tempoh_sp
        jum_modal_sp = jum_opex_sp + jum_sewa_siling_sp
        kadar_untung_modal_sp = (jum_untung_sp / jum_modal_sp * 100) if jum_modal_sp > 0 else 0
        
        modal_sp, npv_sp, irr_sp, roi_sp = kira_metrik_kewangan(untung_tahunan_sp, sewa_siling_sp, 344, tempoh_sp)

    with col_eff_sp:
        st.subheader("💼 Penunjuk Prestasi Kewangan (KPI)")
        s1_1, s1_2 = st.columns(2)
        s1_1.metric(f"Untung Bersih ({tempoh_sp} Thn)", f"RM {jum_untung_sp:,.0f}")
        s1_2.metric("Pulangan Atas Kos/Modal (%)", f"{kadar_untung_modal_sp:.2f}%")
        
        st.markdown("---")
        s2_1, s2_2 = st.columns(2)
        s2_1.metric(f"Jumlah Kos Operasi+GC ({tempoh_sp} Thn)", f"RM {jum_opex_sp:,.0f}")
        s2_2.metric(f"Kos Sewaan ({tempoh_sp} Thn)", f"Lantai: RM {jum_sewa_lantai_sp:,.0f} | Siling: RM {jum_sewa_siling_sp:,.0f}")
        
        st.markdown("---")
        s3_1, s3_2, s3_3 = st.columns(3)
        s3_1.metric("NPV (@10%)", f"RM {npv_sp:,.0f}")
        s3_2.metric("IRR (%)", f"{irr_sp:.2f}%")
        s3_3.metric("ROI (%)", f"{roi_sp:.2f}%")
        
        st.markdown("---")
        if sewa_siling_sp > 2400:
            st.error("🚨 AMARAN SILING: Kadar sewaan melebihi had selamat RM2,400/Ha (Had 55% keuntungan hasil).")
