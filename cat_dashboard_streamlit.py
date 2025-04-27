import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- IRT helper functions (2PL) ---
def P(theta, a, b):
    return 1 / (1 + np.exp(-a * (theta - b)))

def info(theta, a, b):
    p = P(theta, a, b)
    return a**2 * p * (1 - p)

def mle_theta(responses, a_list, b_list):
    """
    Grid‐search MLE for theta over [-4,4]
    """
    responses = np.array(responses)
    thetas = np.linspace(-4, 4, 161)
    best_ll = -1e9
    best_th = 0.0
    for th in thetas:
        p = P(th, np.array(a_list), np.array(b_list))
        ll = np.sum(responses * np.log(p + 1e-9) +
                    (1 - responses) * np.log(1 - p + 1e-9))
        if ll > best_ll:
            best_ll, best_th = ll, th
    return best_th

def se(theta, a_list, b_list):
    infos = [info(theta, a, b) for a, b in zip(a_list, b_list)]
    total = np.sum(infos)
    return 1/np.sqrt(total) if total > 0 else None

# --- Load item bank ---
df = pd.read_csv("data/item_bank2.csv")  # your 30‐item CSV
df = df.set_index("ItemID")

# --- Session state initialization ---
if "asked" not in st.session_state:
    st.session_state.asked = []
    # pick first item = medium difficulty (b closest to 0)
    st.session_state.current_item = df["b"].abs().idxmin()
    st.session_state.theta_hist = [0.0]
    st.session_state.se_hist = [None]

# --- Define submit callback ---
def on_submit():
    cid = st.session_state.current_item
    # check if correct
    ans = st.session_state.get(f"resp_{cid}")
    correct = df.loc[cid, "CorrectAnswer"]
    resp = 1 if ans == correct else 0

    # log response
    st.session_state.asked.append(cid)

    # re‐estimate theta & SE
    asked = st.session_state.asked
    a_list = df.loc[asked, "a"].tolist()
    b_list = df.loc[asked, "b"].tolist()
    th = mle_theta(st.session_state.responses if "responses" in st.session_state else [resp],
                   a_list, b_list)
    # note: store responses array too
    if "responses" not in st.session_state:
        st.session_state.responses = []
    st.session_state.responses.append(resp)

    st.session_state.theta_hist.append(th)
    st.session_state.se_hist.append(se(th, a_list, b_list))

    # choose next item by max information at new th
    remaining = [i for i in df.index if i not in st.session_state.asked]
    if remaining:
        infos = df.loc[remaining].apply(lambda r: info(th, r.a, r.b), axis=1)
        st.session_state.current_item = infos.idxmax()

    # clear out old answer so widget resets
    del st.session_state[f"resp_{cid}"]

# --- Sidebar: show question & collect answer ---
cid = st.session_state.current_item
row = df.loc[cid]

st.sidebar.markdown(f"### Question: {row.Question}")
options = [row.OptionA, row.OptionB, row.OptionC, row.OptionD]
st.sidebar.radio("Pick one:", options, key=f"resp_{cid}")
st.sidebar.button("Submit", on_click=on_submit)

# --- Main page: CAT Dashboard ---
st.title("Computerized Adaptive Test Demo (2PL)")

th_now = st.session_state.theta_hist[-1]
thetas = np.linspace(-4, 4, 200)

# 1. Current Item ICC
st.subheader("1. Current Item ICC")
fig1, ax1 = plt.subplots()
ax1.plot(thetas, P(thetas, row.a, row.b))
ax1.axvline(th_now, color="red", linestyle="--", label=f"θ = {th_now:.2f}")
ax1.set_xlabel("θ")
ax1.set_ylabel("P(correct)")
ax1.legend()
st.pyplot(fig1)

# 2. Current Item IIC
st.subheader("2. Current Item IIC")
fig2, ax2 = plt.subplots()
ax2.plot(thetas, info(thetas, row.a, row.b))
ax2.axvline(th_now, color="red", linestyle="--")
ax2.set_xlabel("θ")
ax2.set_ylabel("Information")
st.pyplot(fig2)

# 3. Standard Error History
st.subheader("3. Standard Error θ History")
fig3, ax3 = plt.subplots()
ax3.plot(st.session_state.se_hist, marker='o')
ax3.set_xlabel("Step")
ax3.set_ylabel("SE(θ)")
st.pyplot(fig3)

# 4. Latent Trait Estimate History
st.subheader("4. Latent Trait Estimate History")
fig4, ax4 = plt.subplots()
ax4.plot(st.session_state.theta_hist, marker='o')
ax4.set_xlabel("Step")
ax4.set_ylabel("θ Estimate")
st.pyplot(fig4)

