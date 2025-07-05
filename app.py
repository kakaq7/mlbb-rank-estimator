import streamlit as st
import math

st.set_page_config(page_title="MLBB Rank Match Estimator", layout="centered")
st.title("📈 Estimasi Pertandingan Naik Rank - Mobile Legends")

# Struktur rank dan divisi
rank_tiers = ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend", "Mythic"]
divisions_per_tier = {
    "Warrior": ["III", "II", "I"],
    "Elite": ["III", "II", "I"],
    "Master": ["III", "II", "I"],
    "Grandmaster": ["V", "IV", "III", "II", "I"],
    "Epic": ["V", "IV", "III", "II", "I"],
    "Legend": ["V", "IV", "III", "II", "I"],
    "Mythic": [""]  # Tanpa divisi
}

# Buat daftar linear dari semua kombinasi rank-divisi
rank_division_order = []
for tier in rank_tiers:
    for div in divisions_per_tier[tier]:
        rank_division_order.append(f"{tier} {div}".strip())

# Input pengguna
col1, col2 = st.columns(2)

with col1:
    start_rank_div = st.selectbox("Rank Sekarang", rank_division_order, index=rank_division_order.index("Legend III"))
    if "Mythic" in start_rank_div:
        start_star = st.number_input("Bintang Sekarang (Mythic)", min_value=1, max_value=1000, value=1)
    else:
        start_star = st.number_input("Bintang Sekarang", min_value=1, max_value=5, value=5)

with col2:
    end_rank_div = st.selectbox("Rank Target", rank_division_order, index=rank_division_order.index("Legend I"))
    if "Mythic" in end_rank_div:
        end_star = st.number_input("Bintang Target (Mythic)", min_value=1, max_value=1000, value=1)
    else:
        end_star = st.number_input("Bintang Target", min_value=1, max_value=5, value=1)

winrate_percent = st.slider("Winrate (%)", 1, 100, 65)
winrate = winrate_percent / 100

# Hitung total bintang berdasarkan urutan linear
def calculate_required_stars(start_rank, start_star, end_rank, end_star):
    if rank_division_order.index(end_rank) < rank_division_order.index(start_rank):
        return 0
    total = 0
    for i in range(rank_division_order.index(start_rank), rank_division_order.index(end_rank)):
        total += 5  # Tiap divisi ada 5 bintang kecuali Mythic
    total += end_star - start_star
    return max(0, total)

needed_stars = calculate_required_stars(start_rank_div, start_star, end_rank_div, end_star)

# Estimasi pertandingan
if winrate == 0:
    st.error("Winrate tidak boleh 0%")
else:
    estimated_matches = math.ceil(needed_stars / winrate)
    st.success(f"Kamu membutuhkan sekitar {estimated_matches} pertandingan untuk naik dari {start_rank_div} ⭐{start_star} ke {end_rank_div} ⭐{end_star}, dengan winrate {winrate_percent}%")

# Footer
st.markdown("---")
st.markdown("**Dibuat oleh [@al.ismaill](https://instagram.com/al.ismaill)**")
