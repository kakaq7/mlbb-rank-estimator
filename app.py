import streamlit as st
import math

st.set_page_config(page_title="MLBB Rank Match Estimator", layout="centered")
st.title("📈 Estimasi Pertandingan Naik Rank - Mobile Legends")

# Rank order dan jumlah bintang per rank tier
rank_order = [
    "Warrior", "Elite", "Master", "Grandmaster",
    "Epic", "Legend", "Mythic"
]

rank_bintang_default = {
    "Warrior": 3,
    "Elite": 4,
    "Master": 4,
    "Grandmaster": 5,
    "Epic": 5,
    "Legend": 5,
    "Mythic": 999  # diasumsikan bisa naik tak terbatas
}

# Input
col1, col2 = st.columns(2)

with col1:
    current_rank = st.selectbox("Rank Sekarang", rank_order, index=5)
    current_star = st.number_input("Bintang Sekarang", min_value=0, max_value=999, value=5)

with col2:
    target_rank = st.selectbox("Rank Target", rank_order, index=5)
    target_star = st.number_input("Bintang Target", min_value=0, max_value=999, value=1)

winrate_percent = st.slider("Winrate (%)", 1, 100, 65)
winrate = winrate_percent / 100

# Hitung total bintang kumulatif dari awal sampai bintang tertentu di rank tertentu
def get_total_stars(rank, star):
    total = 0
    for r in rank_order:
        if r == rank:
            total += star
            break
        total += rank_bintang_default[r] * (5 if r != "Mythic" else 0)
    return total

# Hitung total bintang
start_total = get_total_stars(current_rank, current_star)
target_total = get_total_stars(target_rank, target_star)
needed_stars = max(0, target_total - start_total)

# Estimasi jumlah pertandingan
if winrate == 0:
    st.error("Winrate tidak boleh 0%")
else:
    estimated_matches = math.ceil(needed_stars / winrate)
    st.success(f"Kamu membutuhkan sekitar {estimated_matches} pertandingan untuk naik dari {current_rank} ⭐{current_star} ke {target_rank} ⭐{target_star}, dengan winrate {winrate_percent}%")

# Footer
st.markdown("---")
st.markdown("**Dibuat oleh [@al.ismatregill](https://instagram.com/al.ismaill)**")
