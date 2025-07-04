import streamlit as st
import math

st.set_page_config(page_title="MLBB Rank Match Estimator", layout="centered")
st.title("📈 Estimasi Pertandingan Naik Rank - Mobile Legends")

# Mapping dari urutan rank MLBB dan bintang
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
    "Mythic": 0  # Mythic tidak punya divisi
}

# Input user
col1, col2 = st.columns(2)

with col1:
    current_rank = st.selectbox("Rank Sekarang", rank_order, index=5)
    current_division = st.number_input("Divisi Rank Sekarang (V=5 s/d I=1, atau 0 untuk Mythic)", min_value=0, max_value=5, value=3)
    current_stars = st.number_input("Jumlah Bintang Sekarang", min_value=0, max_value=50, value=5)

with col2:
    target_rank = st.selectbox("Rank Target", rank_order, index=5)
    target_division = st.number_input("Divisi Rank Target (atau 0 untuk Mythic)", min_value=0, max_value=5, value=2)
    target_stars = st.number_input("Jumlah Bintang Target", min_value=0, max_value=50, value=1)

winrate_percent = st.slider("Winrate (%)", 1, 100, 65)
winrate = winrate_percent / 100

# Fungsi menghitung jumlah bintang total antara 2 rank
def calculate_total_stars(start_rank, start_div, start_star, end_rank, end_div, end_star):
    if start_rank == end_rank == "Mythic":
        return max(0, end_star - start_star)

    if start_rank == end_rank and start_div == end_div:
        return max(0, end_star - start_star)

    ranks = rank_order[rank_order.index(start_rank): rank_order.index(end_rank)+1]
    total_stars = 0
    start_found = False

    for idx, rank in enumerate(ranks):
        bintang_per_div = rank_bintang_default.get(rank, 0)

        if rank == start_rank:
            start_found = True
            if rank != "Mythic":
                for div in range(start_div, 0, -1):
                    if rank == end_rank and div == end_div:
                        if start_star == bintang_per_div:
                            total_stars += 1  # promosi ke divisi berikutnya
                        else:
                            total_stars += max(0, end_star - start_star)
                        break
                    elif div == start_div:
                        if start_star == bintang_per_div:
                            total_stars += 1  # langsung promosi
                        else:
                            total_stars += bintang_per_div - start_star
                    else:
                        total_stars += bintang_per_div
            else:
                total_stars += 0

        elif rank == end_rank:
            if rank == "Mythic":
                total_stars += end_star
            else:
                for div in range(5, end_div, -1):
                    total_stars += bintang_per_div
                total_stars += end_star

        elif start_found:
            total_stars += 5 * bintang_per_div

    return total_stars

# Hitung
total_bintang = calculate_total_stars(
    current_rank, current_division, current_stars,
    target_rank, target_division, target_stars
)

# Estimasi jumlah pertandingan
if winrate == 0:
    st.error("Winrate tidak boleh 0%")
else:
    estimated_matches = math.ceil(total_bintang / winrate)
    st.success(f"Kamu membutuhkan sekitar {estimated_matches} pertandingan untuk naik dari {current_rank} {current_division if current_rank != 'Mythic' else ''} ⭐{current_stars} ke {target_rank} {target_division if target_rank != 'Mythic' else ''} ⭐{target_stars}, dengan winrate {winrate_percent}%")

# Footer
st.markdown("---")
st.markdown("**Dibuat oleh [@al.ismaill](https://instagram.com/al.ismaill)**")
