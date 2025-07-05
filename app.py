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

# Fungsi dasar

def get_rank_base(rank_name):
    if rank_name == "Mythic":
        return (6, 0)
    rank_parts = rank_name.split()
    rank = rank_parts[0]
    roman = rank_parts[1]
    roman_map = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5}
    div = roman_map[roman]
    rank_index = ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend"].index(rank)
    return (rank_index, div)

def calculate_total_stars(start_name, start_star, end_name, end_star):
    if start_name == end_name:
        return max(0, end_star - start_star)

    start_rank, start_div = get_rank_base(start_name)
    end_rank, end_div = get_rank_base(end_name)

    total = 0
    for r in range(start_rank, end_rank + 1):
        rank_name = ["Warrior", "Elite", "Master", "Grandmaster", "Epic", "Legend", "Mythic"][r]
        bintang_per_div = rank_bintang_default[rank_name]

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

# Perhitungan proteksi & bonus dari data pertandingan
with st.expander("🧠 Estimasi Otomatis Star Protection dan Bonus dari Data Match"):
    real_col1, real_col2 = st.columns(2)
    with real_col1:
        data_start_rank = st.selectbox("Rank Awal (Data Nyata)", rank_tiers, index=20)
        data_start_star = st.number_input("Bintang Awal (Data Nyata)", min_value=0, max_value=999, value=2)
    with real_col2:
        data_end_rank = st.selectbox("Rank Saat Ini (Data Nyata)", rank_tiers, index=20)
        data_end_star = st.number_input("Bintang Saat Ini", min_value=0, max_value=999, value=3)

    match_count = st.number_input("Total Pertandingan", min_value=1, max_value=9999, value=207)
    winrate_input = st.slider("Winrate dari Match Tersebut (%)", 1, 100, 43)
    winrate_real = winrate_input / 100

    net_stars = calculate_total_stars(data_start_rank, data_start_star, data_end_rank, data_end_star)
    wins = int(round(match_count * winrate_real))
    losses = match_count - wins
    net_star_theory = wins - losses
    compensations = net_stars - net_star_theory

    bonus_percent = 0
    protect_percent = 0

    if wins > 0 and losses > 0:
        bonus_percent = max(0, (compensations / wins) * 100 / 2)
        protect_percent = max(0, (compensations / losses) * 100 / 2)
    elif wins > 0:
        bonus_percent = max(0, (compensations / wins) * 100)
    elif losses > 0:
        protect_percent = max(0, (compensations / losses) * 100)

    st.write(f"Kemenangan: {wins} match")
    st.write(f"Kekalahan: {losses} match")
    st.write(f"Bintang bersih aktual: {net_stars} (teoritis: {net_star_theory})")
    st.success(f"Perkiraan Star Bonus Rate: ± {bonus_percent:.1f}%")
    st.success(f"Perkiraan Star Protection Rate: ± {protect_percent:.1f}%")

# Input kalkulator
st.header("🔢 Estimasi Pertandingan Menuju Rank Target")
col1, col2 = st.columns(2)

with col1:
    start_tier = st.selectbox("Rank Awal", rank_tiers, index=20)
    start_stars = st.number_input("Bintang Awal", min_value=0, max_value=999, value=3)

with col2:
    end_tier = st.selectbox("Rank Target", rank_tiers, index=26)
    end_stars = st.number_input("Bintang Target", min_value=0, max_value=999, value=1)

winrate_percent = st.slider("Winrate (%)", 1, 100, int(winrate_real * 100))
winrate = winrate_percent / 100

col3, col4 = st.columns(2)

with col3:
    star_protection_rate = st.slider("Star Protection (%)", 0, 100, int(protect_percent))
with col4:
    star_raising_bonus = st.slider("Star Bonus (%)", 0, 100, int(bonus_percent))

protection = star_protection_rate / 100
bonus = star_raising_bonus / 100

# Hitung
st.markdown("---")
st.header("📈 Hasil Estimasi")

total_bintang = calculate_total_stars(start_tier, start_stars, end_tier, end_stars)
bintang_per_match = (winrate * (1 + bonus)) - ((1 - winrate) * (1 - protection))

if bintang_per_match <= 0:
    st.error("Dengan konfigurasi saat ini, kamu tidak akan bisa naik rank. Naikkan winrate atau tingkatkan proteksi/bonus.")
else:
    estimated_matches = math.ceil(total_bintang / bintang_per_match)
    st.success(f"Total bintang yang dibutuhkan: {total_bintang}")
    st.success(f"Estimasi pertandingan yang dibutuhkan: {estimated_matches} match")

st.markdown("---")
st.markdown("**Dibuat oleh [@al.ismabvcill](https://instagram.com/al.ismaill)**")
