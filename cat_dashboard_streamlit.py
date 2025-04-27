import streamlit as st
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt

# ─── Reset matplotlib to defaults to avoid loading any custom style ───
mpl.rcParams.update(mpl.rcParamsDefault)
plt.style.use('default')

# ─── IRT helper functions (2PL) ───────────────────────────────────────
def P(theta, a, b):
    return 1.0 / (1.0 + np.exp(-a * (theta - b)))

def info(theta, a, b):
    p = P(theta, a, b)
    return a**2 * p * (1 - p)

def mle_theta(responses, a_list, b_list):
    resps = np.array(responses)
    thetas = np.linspace(-4, 4, 161)
    best_ll, best_th = -np.inf, 0.0
    for th in thetas:
        p = P(th, np.array(a_list), np.array(b_list))
        ll = np.sum(resps * np.log(p + 1e-9) + (1 - resps) * np.log(1 - p + 1e-9))
        if ll > best_ll:
            best_ll, best_th = ll, th
    return best_th

def se(theta, a_list, b_list):
    infos = [info(theta, a, b) for a, b in zip(a_list, b_list)]
    total = np.sum(infos)
    return 1/np.sqrt(total) if total > 0 else None

# ─── Configuration ────────────────────────────────────────────────────
MAX_ITEMS = 10

# ─── Load item bank ───────────────────────────────────────────────────
df = pd.read_csv("data/item_bank2.csv").set_index("ItemID")

# ─── Session state initialization ─────────────────────────────────────
if "asked" not in st.session_state:
    st.session_state.asked = []           # list of ItemIDs already seen
    st.session_state.responses = []       # corresponding 0/1 responses
    # pick first item: b closest to 0
    st.session_state.current_item = df["b"].abs().idxmin()
    st.session_state.theta_hist = [0.0]   # theta estimates
    st.session_state.se_hist = [None]     # standard errors

# ─── Submit callback ──────────────────────────────────────────────────
def on_submit():
    cid = st.session_state.current_item
    # re-fetch row
    row = df.loc[cid]
    # figure out which option text was picked
    selected_text = st.session_state[f"resp_{cid}"]
    # map correct letter -> correct text
    correct_letter = row["CorrectAnswer"]
    correct_text   = row[f"Option{correct_letter}"]
    # score
    resp = 1 if selected_text == correct_text else 0

    # log response & question
    st.session_state.responses.append(resp)
    st.session_state.asked.append(cid)

    # re-estimate theta & SE
    a_list = df.loc[st.session_state.asked, "a"].tolist()
    b_list = df.loc[st.session_state.asked, "b"].tolist()
    th     = mle_theta(st.session_state.responses, a_list, b_list)
    st.session_state.theta_hist.append(th)
    st.session_state.se_hist.append(se(th, a_list, b_list))

    # pick next item by max information at new theta
    if len(st.session_state.asked) < MAX_ITEMS:
        remaining = [i for i in df.index if i not in st.session_state.asked]
        if remaining:
            infos = df.loc[remaining].apply(lambda r: info(th, r.a, r.b), axis=1)
            st.session_state.current_item = infos.idxmax()

    # clear out old radio value so next question is blank
    del st.session_state[f"resp_{cid}"]

# ─── Sidebar: question & answer ───────────────────────────────────────
if len(st.session_state.asked) < MAX_ITEMS:
    cid = st.session_state.current_item
    row = df.loc[cid]

    st.sidebar.markdown(f"### Question: {row.Question}")
    options = [row.OptionA, row.OptionB, row.OptionC, row.OptionD]
    st.sidebar.radio("Pick one:", options, key=f"resp_{cid}")
    st.sidebar.button("Submit", on_click=on_submit)
else:
    # test complete
    final_theta = st.session_state.theta_hist[-1]
    st.sidebar.markdown("## Test Complete")
    st.sidebar.markdown(f"**Final θ estimate:** {final_theta:.2f}")

# ─── Main page: display the four plots ────────────────────────────────
st.title("Computerized Adaptive Test Demo (2PL)")

# current theta & grid
th_now = st.session_state.theta_hist[-1]
thetas = np.linspace(-4, 4, 200)

# 1. ICC
st.subheader("1. Current Item ICC")
fig1, ax1 = plt.subplots()
# if we have a current item
if len(st.session_state.asked) < MAX_ITEMS:
    row = df.loc[st.session_state.current_item]
    ax1.plot(thetas, P(thetas, row.a, row.b))
    ax1.axvline(th_now, color="red", linestyle="--", label=f"θ = {th_now:.2f}")
    ax1.set_xlabel("θ"); ax1.set_ylabel("P(correct)")
    ax1.legend()
st.pyplot(fig1)

# 2. IIC
st.subheader("2. Current Item Information (IIC)")
fig2, ax2 = plt.subplots()
if len(st.session_state.asked) < MAX_ITEMS:
    row = df.loc[st.session_state.current_item]
    ax2.plot(thetas, info(thetas, row.a, row.b))
    ax2.axvline(th_now, color="red", linestyle="--")
    ax2.set_xlabel("θ"); ax2.set_ylabel("Information")
st.pyplot(fig2)

# 3. SE History
st.subheader("3. Standard Error History")
fig3, ax3 = plt.subplots()
ax3.plot(st.session_state.se_hist, marker='o')
ax3.set_xlabel("Step"); ax3.set_ylabel("SE(θ)")
st.pyplot(fig3)

# 4. Theta History
st.subheader("4. Latent Trait Estimate History")
fig4, ax4 = plt.subplots()
ax4.plot(st.session_state.theta_hist, marker='o')
ax4.set_xlabel("Step"); ax4.set_ylabel("θ Estimate")
st.pyplot(fig4)
