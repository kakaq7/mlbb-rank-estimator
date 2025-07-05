import streamlit as st
import math

st.set_page_config(page_title="Estimator Naik Rank MLBB", layout="centered")
st.title("📊 Estimasi Pertandingan Menuju Rank Target - Mobile Legends")

rank_order = [
    "Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend", "Mythic"
]

rank_bintang_default = {
    "Warrior": 3,
    "Elite": 4,
    "Master": 4,
    "Grandmaster": 5,
    "Epic": 5,
    "Legend": 5,
    "Mythic": 0
}

divisi_labels = {
    "I (tertinggi)": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V (terendah)": 5,
    "Mythic (tanpa divisi)": 0
}
divisi_options = list(divisi_labels.keys())

st.header("🔢 Input Data")
col1, col2 = st.columns(2)

with col1:
    start_rank = st.selectbox("Rank Awal", rank_order, index=4)
    start_div_label = st.selectbox("Divisi Rank Awal", divisi_options, index=2)
    start_div = divisi_labels[start_div_label]
    start_stars = st.number_input("Bintang Awal", min_value=0, max_value=999, value=2)

with col2:
    end_rank = st.selectbox("Rank Target", rank_order, index=5)
    end_div_label = st.selectbox("Divisi Rank Target", divisi_options, index=4)
    end_div = divisi_labels[end_div_label]
    end_stars = st.number_input("Bintang Target", min_value=0, max_value=999, value=1)

winrate_percent = st.slider("Winrate (%)", 1, 100, 43)
winrate = winrate_percent / 100

col3, col4 = st.columns(2)

with col3:
    star_protection_rate = st.slider("Star Protection (%)", 0, 100, 13)
with col4:
    star_raising_bonus = st.slider("Star Raising Bonus (%)", 0, 100, 17)

protection = star_protection_rate / 100
bonus = star_raising_bonus / 100

# Fungsi menghitung jumlah bintang dari start ke end
def calculate_total_stars(start_rank, start_div, start_star, end_rank, end_div, end_star):
    if start_rank == end_rank == "Mythic":
        return max(0, end_star - start_star)
    if start_rank == end_rank and start_div == end_div:
        return max(0, end_star - start_star)

    total = 0
    start_idx = rank_order.index(start_rank)
    end_idx = rank_order.index(end_rank)

    for idx in range(start_idx, end_idx + 1):
        rank = rank_order[idx]
        bintang_per_div = rank_bintang_default[rank]

        if rank == start_rank:
            for d in range(start_div, 0, -1):
                if rank == end_rank and d == end_div:
                    total += max(0, (bintang_per_div - start_star) + end_star)
                    return total
                elif d == start_div:
                    total += bintang_per_div - start_star
                else:
                    total += bintang_per_div

        elif rank == end_rank:
            for d in range(5, end_div - 1, -1):
                total += bintang_per_div
            total += end_star

        elif start_idx < idx < end_idx:
            total += 5 * bintang_per_div

    return total

# Perhitungan
total_bintang = calculate_total_stars(start_rank, start_div, start_stars, end_rank, end_div, end_stars)
bintang_per_match = (winrate * (1 + bonus)) - ((1 - winrate) * (1 - protection))

st.markdown("---")
st.header("📈 Hasil Estimasi")

if bintang_per_match <= 0:
    st.error("Dengan konfigurasi saat ini, kamu tidak akan bisa naik rank. Naikkan winrate atau tingkatkan proteksi/bonus.")
else:
    estimated_matches = math.ceil(total_bintang / bintang_per_match)
    st.success(f"Total bintang yang dibutuhkan: {total_bintang}")
    st.success(f"Estimasi pertandingan yang dibutuhkan: {estimated_matches} match")

st.markdown("---")
st.markdown("**Dibuat oleh [@al.ismaill](https://instagram.com/al.ismaill)**")
