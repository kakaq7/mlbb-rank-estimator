import streamlit as st
import math

st.set_page_config(page_title="Estimator Naik Rank MLBB", layout="centered")
st.title("📊 Estimasi Pertandingan Menuju Rank Target - Mobile Legends")

# Rank dan divisi
rank_tiers = []
for rank in ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend"]:
    for div in ["V", "IV", "III", "II", "I"]:
        rank_tiers.append(f"{rank} {div}")
rank_tiers.append("Mythic")  # Mythic tidak punya divisi

rank_bintang_default = {
    "Warrior": 3,
    "Elite": 4,
    "Master": 4,
    "Grandmaster": 5,
    "Epic": 5,
    "Legend": 5,
    "Mythic": 0
}

# Input User
st.header("🔢 Input Data")
col1, col2 = st.columns(2)

with col1:
    start_tier = st.selectbox("Rank Awal", rank_tiers, index=20)
    start_stars = st.number_input("Bintang Awal", min_value=0, max_value=999, value=3)

with col2:
    end_tier = st.selectbox("Rank Target", rank_tiers, index=26)
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

# Fungsi menghitung bintang total
def get_rank_base(rank_name):
    if rank_name == "Mythic":
        return (6, 0)  # indeks tier, 0 divisi
    rank_parts = rank_name.split()
    rank = rank_parts[0]
    roman = rank_parts[1]
    roman_map = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}
    div = roman_map[roman]
    rank_index = ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend"].index(rank)
    return (rank_index, div)

def calculate_total_stars(start_name, start_star, end_name, end_star):
    if start_name == end_name == "Mythic":
        return max(0, end_star - start_star)

    start_rank, start_div = get_rank_base(start_name)
    end_rank, end_div = get_rank_base(end_name)

    total = 0
    for r in range(start_rank, end_rank + 1):
        rank_name = ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend", "Mythic"][r]
        bintang_per_div = rank_bintang_default[rank_name]

        if rank_name == "Mythic":
            total += end_star if r == end_rank else 0
            continue

        div_start = start_div if r == start_rank else 5
        div_end = end_div if r == end_rank else 1

        for d in range(div_start, div_end - 1, -1):
            if r == start_rank and d == start_div:
                if r == end_rank and d == end_div:
                    total += max(0, (bintang_per_div - start_star) + end_star)
                else:
                    total += bintang_per_div - start_star
            elif r == end_rank and d == end_div:
                total += end_star
            else:
                total += bintang_per_div

    return total

# Hitung total bintang dan pertandingan
total_bintang = calculate_total_stars(start_tier, start_stars, end_tier, end_stars)
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
