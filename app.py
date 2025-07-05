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

# Divisi dalam format angka (1-5) ditampilkan sebagai label Romawi
divisi_labels = {
    "I (tertinggi)": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V (terendah)": 5,
    "Mythic (tanpa divisi)": 0
}
divisi_options = list(divisi_labels.keys())

# Input user
col1, col2 = st.columns(2)

with col1:
    current_rank = st.selectbox("Rank Sekarang", rank_order, index=5)
    current_division_label = st.selectbox("Divisi Rank Sekarang", divisi_options, index=2)
    current_division = divisi_labels[current_division_label]
    current_stars = st.number_input("Jumlah Bintang Sekarang", min_value=0, max_value=50, value=5)

with col2:
    target_rank = st.selectbox("Rank Target", rank_order, index=5)
    target_division_label = st.selectbox("Divisi Rank Target", divisi_options, index=1)
    target_division = divisi_labels[target_division_label]
    target_stars = st.number_input("Jumlah Bintang Target", min_value=0, max_value=50, value=4)

winrate_percent = st.slider("Winrate (%)", 1, 100, 65)
winrate = winrate_percent / 100

# Fungsi menghitung jumlah bintang total antara 2 rank
def calculate_total_stars(start_rank, start_div, start_star, end_rank, end_div, end_star):
    if start_rank == end_rank == "Mythic":
        return max(0, end_star - start_star)

    if start_rank == end_rank and start_div == end_div:
        return max(0, end_star - start_star)

    total_stars = 0
    start_index = rank_order.index(start_rank)
    end_index = rank_order.index(end_rank)
    promoted_early = False

    for i in range(start_index, end_index + 1):
        rank = rank_order[i]
        stars_per_div = rank_bintang_default[rank]

        if rank == start_rank:
            if rank == "Mythic":
                total_stars += 0
            else:
                for div in range(start_div, 0, -1):
                    if rank == end_rank and div == end_div:
                        if start_star == stars_per_div:
                            if start_rank == end_rank and start_div - 1 == end_div:
                                return end_star
                            elif rank_order.index(end_rank) == rank_order.index(start_rank) + 1 and end_div == 5:
                                return end_star
                            else:
                                total_stars += 1
                                promoted_early = True
                        else:
                            total_stars += max(0, (stars_per_div - start_star) + end_star)
                        return total_stars
                    elif div == start_div:
                        if start_star == stars_per_div:
                            if start_rank == end_rank and start_div - 1 == end_div:
                                return end_star
                            elif rank_order.index(end_rank) == rank_order.index(start_rank) + 1 and end_div == 5:
                                return end_star
                            else:
                                total_stars += 1
                                promoted_early = True
                        else:
                            total_stars += stars_per_div - start_star
                    else:
                        total_stars += stars_per_div

        elif rank == end_rank:
            if rank == "Mythic":
                total_stars += end_star
            else:
                for div in range(5, end_div - 1, -1):  # termasuk end_div
                    total_stars += stars_per_div
                total_stars += end_star if not promoted_early else max(0, end_star - 1)

        elif start_index < i <= end_index:
            if rank != "Mythic":
                if rank == end_rank:
                    for div in range(5, end_div - 1, -1):
                        total_stars += stars_per_div
                    total_stars += end_star if not promoted_early else max(0, end_star - 1)
                else:
                    total_stars += 5 * stars_per_div

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
    st.success(f"Kamu membutuhkan sekitar {estimated_matches} pertandingan untuk naik dari {current_rank} {current_division_label if current_rank != 'Mythic' else ''} ⭐{current_stars} ke {target_rank} {target_division_label if target_rank != 'Mythic' else ''} ⭐{target_stars}, dengan winrate {winrate_percent}%")

# Footer
st.markdown("---")
st.markdown("**Dibuat oleh [@al.ismhgfaill](https://instagram.com/al.ismaill)**")
