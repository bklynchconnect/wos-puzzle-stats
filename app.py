import streamlit as st
from utils import get_piece, get_pieces
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

st.set_page_config(
    page_title="WOS Puzzle Pack Purchase Stats",
    page_icon="🚀",
    layout="wide",
)

st.title("WOS Puzzle Pack Purchase Stats")
st.write(f"Each mythic pack gives you 6 pieces, and each piece has a 10% chance of giving you a 5:star: piece, but it won't necessarily be new. You can get a guaranteed *new* 5:star: piece by buying a master piece for 2500 tickets, but how does that compare to buying 10 mythic packs for the same 2500 tickets?")
st.write(f"Enter the total number of 5:star: pieces (currently 289 at last count), the number of 5:star: pieces **you have**, the number of mythic packs to buy (assumed 10).")
st.write(f"You'll see the probability of getting **at least 1 new** 5:star: piece if you buy that many packs.")
st.write(f"Also enter the probability *you want to have* of getting at least 1 new 5:star: piece and you'll see how many 5:star: pieces you can have before your chances go below that.")
st.warning(f"Note this does not include the chances of getting repeat new 5:star: pieces (...maybe later...).")
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.number_input(f"Total 5:star: pieces", min_value=1, value=289, step=1, key="total_stars")
with col2:
    st.number_input(f"Number of 5:star: pieces", min_value=0, value=0, step=1, key="owned_stars")
with col3:
    st.number_input(f"Number of puzzle packs to buy\n", min_value=1, value=10, step=1, key="num_packs")
with col4:
    st.number_input(f"Target % of at least 1 new 5:star: piece", min_value=0, max_value=100,value=50, step=1, key="target_probability")

num_pieces = 6*st.session_state.num_packs
f = st.session_state.owned_stars / st.session_state.total_stars
target_probability = st.session_state.target_probability / 100

prob_no_new = (0.9 + 0.1*f)**num_pieces
print(prob_no_new)

target_f = ((1 - target_probability) ** (1 / num_pieces) - 0.9)/0.1
target_num_have = int(np.round(target_f * st.session_state.total_stars))
# st.write(f"To have a {st.session_state.target_probability}% chance of getting at least 1 new 5:star: piece, you need to have less than {target_num_have} :star::star::star::star::star: pieces.")
st.info(
    f"🎯 With **{st.session_state.owned_stars}** pieces already, you have a **{prob_no_new*100:.2f}%** chance of not getting any new 5:star: pieces if you buy 10 gold packs **({(1-prob_no_new)*100:.2f}% chance of getting at least 1 new 5:star: piece)**."
)

st.success(
    f"🎯 To have a {st.session_state.target_probability}% chance of getting **at least 1 new** 5:star: piece, "
    f"you need to have less than **{target_num_have}** already."
)


st.header("Simulator")
st.write(f"Here you can run a simulation of buying the number of packs you specified over and over (based also on the total and owned 5:star: pieces), and see how many new 5:star: pieces you would have received.")
st.number_input(f"Number of simulations to run\n", min_value=1, value=1000, step=1, key="num_simulations")
num_sims = st.session_state.num_simulations

def run_sim():
    pieces = get_pieces(num_pieces, f=f)
    num_1s = (pieces == 1).sum()
    num_2s = (pieces == 2).sum()
    num_3s = (pieces == 3).sum()
    num_4s = (pieces == 4).sum()
    expected_duplicate_5s = (pieces == 5).sum()
    expected_new_5s = (pieces == 6).sum()
    nums = np.array([num_1s, num_2s, num_3s, num_4s, expected_duplicate_5s, expected_new_5s])

    regular_counts = np.array([
        num_1s,
        num_2s,
        num_3s,
        num_4s,
        expected_duplicate_5s
    ])

    new_counts = np.array([
        0,
        0,
        0,
        0,
        expected_new_5s
    ])

    return regular_counts, new_counts, expected_new_5s, expected_duplicate_5s

expected_new_5s_sim = np.zeros(num_sims)
expected_duplicate_5s_sim = np.zeros(num_sims)
for i in range(num_sims):
    regular_counts, new_counts, expected_new_5s, expected_duplicate_5s = run_sim()
    expected_new_5s_sim[i] = int(np.round(expected_new_5s))
    expected_duplicate_5s_sim[i] = int(np.round(expected_duplicate_5s))

max_5s = int(np.max(expected_new_5s_sim))

cnts, bins = np.histogram(expected_new_5s_sim, bins=np.arange(max_5s+2)-0.5)
labels = np.arange(max_5s+1)

print(len(bins), len(cnts), len(labels))

# sb.set_style("darkgrid")
# fig, ax = plt.subplots(figsize=(8,8))
# sb.histplot(expected_new_5s_sim, bins=np.arange(max_5s+2)-0.5, ax=ax,stat='percent')
# st.pyplot(fig)
sb.set_theme(style="darkgrid")
plt.style.use("dark_background")
left, center, right = st.columns([2, 3, 2])

with center:
    fig, ax = plt.subplots(figsize=(6, 4))

    sb.barplot(
        x=100*cnts/num_sims,
        y=labels,
        orient="h",
        ax=ax,
        hue=cnts,
        palette='rainbow'
    )
    ax.get_legend().remove()
    ax.set_xlabel("Count (%)")
    ax.set_ylabel("Number of new 5-star pieces")
    ax.set_title("Distribution of New 5-star Pieces")

    st.pyplot(fig)