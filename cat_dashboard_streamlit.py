# cat_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Helper functions ---
def prob_2pl(theta, a, b):
    """Probability of correct response under 2PL model."""
    return 1 / (1 + np.exp(-a * (theta - b)))

def item_information(theta, a, b):
    """Item Information under 2PL."""
    p = prob_2pl(theta, a, b)
    return a**2 * p * (1 - p)

def mle_theta(responses, a_vals, b_vals):
    """Maximum likelihood estimation of theta."""
    resp = np.array(responses, dtype=float)
    a_ = np.array(a_vals, dtype=float)
    b_ = np.array(b_vals, dtype=float)
    theta_grid = np.linspace(-4, 4, 161)
    best_ll = -np.inf
    best_theta = 0.0
    for th in theta_grid:
        p = prob_2pl(th, a_, b_)
        ll = np.sum(resp * np.log(p + 1e-9) + (1-resp) * np.log(1-p + 1e-9))
        if ll > best_ll:
            best_ll = ll
            best_theta = th
    return best_theta

def compute_se(theta, a_vals, b_vals):
    """Compute standard error of theta estimate."""
    infos = [item_information(theta, a, b) for a, b in zip(a_vals, b_vals)]
    total = np.sum(infos)
    return 1/np.sqrt(total) if total > 0 else None

def get_difficulty_label(b):
    """Return difficulty category based on b parameter."""
    if b <= -0.5:
        return "Easy"
    elif -0.5 < b <= 0.5:
        return "Medium"
    else:
        return "Hard"

# --- Load item bank ---
item_bank = pd.read_csv('data/item_bank2.csv').set_index('ItemID')

def initialize_state():
    """Initialize session state variables."""
    if 'asked' not in st.session_state:
        st.session_state.asked = []
        st.session_state.responses = []
        st.session_state.theta = [0.0]
        st.session_state.se = [None]
        init = item_bank['b'].abs().idxmin()
        st.session_state.current = init

initialize_state()

# --- Stop Rule ---
MAX_ITEMS = 10
if len(st.session_state.asked) >= MAX_ITEMS:
    st.title("🎯 CAT Complete!")
    st.write(f"✅ Test finished after {MAX_ITEMS} items.")
    st.write(f"Final estimated ability θ̂ = **{st.session_state.theta[-1]:.2f}**")
    if st.button("🔄 Reset CAT"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()
    st.stop()

# --- Layout ---
st.title("🧮 CAT Dashboard - Math Items")

# --- Score and Difficulty Display ---
col1, col2 = st.columns(2)

with col1:
    score = sum(st.session_state.responses)
    st.markdown(f"""
    <div style="background-color:#00c0f2;padding:15px;border-radius:10px">
    <h5 style="color:white;">🏆 Current Score</h5>
    <h2 style="color:white;text-align:center;">{score}</h2>
    </div>
    """, unsafe_allow_html=True)

with col2:
    cur_id = st.session_state.current
    row = item_bank.loc[cur_id]
    difficulty_label = get_difficulty_label(row['b'])
    st.markdown(f"""
    <div style="background-color:#00c0f2;padding:15px;border-radius:10px">
    <h5 style="color:white;">📈 Difficulty Level</h5>
    <h2 style="color:white;text-align:center;">{difficulty_label}</h2>
    </div>
    """, unsafe_allow_html=True)

# --- Display Question
step = len(st.session_state.asked) + 1
st.write(f"### Question {step} of {MAX_ITEMS}")
st.write(f"**{row['Question']}**")

opts = [row['OptionA'], row['OptionB'], row['OptionC'], row['OptionD']]
selected_key = f"choice_{cur_id}"
selected = st.radio("Options", opts, key=selected_key)

# --- Submission callback ---
def on_submit():
    # Identify the correct option
    correct_letter = row['CorrectAnswer']
    correct_idx = {'A': 0, 'B': 1, 'C': 2, 'D': 3}[correct_letter]
    correct_option = opts[correct_idx]

    # Compare selected choice with correct choice
    resp = 1 if selected == correct_option else 0

    # Update session state
    st.session_state.asked.append(cur_id)
    st.session_state.responses.append(resp)

    # Update theta estimate
    a_list = [item_bank.loc[i,'a'] for i in st.session_state.asked]
    b_list = [item_bank.loc[i,'b'] for i in st.session_state.asked]
    th_new = mle_theta(st.session_state.responses, a_list, b_list)
    se_new = compute_se(th_new, a_list, b_list)
    st.session_state.theta.append(th_new)
    st.session_state.se.append(se_new)

    # Choose next best item
    remain = item_bank.drop(index=st.session_state.asked)
    infos = remain.apply(lambda r: item_information(th_new, r['a'], r['b']), axis=1)
    st.session_state.current = infos.idxmax()

    # Clear previous radio button state
    del st.session_state[selected_key]

st.button("✅ Submit Answer", on_click=on_submit)

# --- Diagnostics Plots (2x2 layout) ---
steps = list(range(len(st.session_state.theta)))
theta_vals = np.linspace(-4, 4, 200)
th_cur = st.session_state.theta[-1]

st.markdown("## 📊 Diagnostics")

col3, col4 = st.columns(2)
col5, col6 = st.columns(2)

# Row 1
with col3:
    st.subheader("📈 Current Item ICC")
    fig1, ax1 = plt.subplots()
    ax1.plot(theta_vals, prob_2pl(theta_vals, row['a'], row['b']), color='blue')
    ax1.axvline(th_cur, color='red', linestyle='--')
    ax1.set_ylabel('P(correct)')
    st.pyplot(fig1)

with col4:
    st.subheader("📊 Current Item IIC")
    fig2, ax2 = plt.subplots()
    ax2.plot(theta_vals, item_information(theta_vals, row['a'], row['b']), color='blue')
    ax2.axvline(th_cur, color='red', linestyle='--')
    ax2.set_ylabel('Information')
    st.pyplot(fig2)

# Row 2
with col5:
    st.subheader("📉 Standard Error History")
    fig3, ax3 = plt.subplots()
    ax3.plot(steps, st.session_state.se, marker='o', color='green')
    ax3.set_ylabel('SE(θ)')
    st.pyplot(fig3)

with col6:
    st.subheader("📈 Theta Estimate History")
    fig4, ax4 = plt.subplots()
    ax4.plot(steps, st.session_state.theta, marker='o', color='purple')
    ax4.set_ylabel('θ')
    st.pyplot(fig4)

# --- Reset Button at the Bottom
st.markdown("---")
st.subheader("🔄 Restart CAT Session")
if st.button("Reset and Start Over"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

