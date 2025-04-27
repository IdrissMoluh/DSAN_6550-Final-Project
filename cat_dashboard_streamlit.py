import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# --- Helper functions ---
def prob_2pl(theta, a, b):
    return 1 / (1 + np.exp(-a * (theta - b)))

def item_information(theta, a, b):
    p = prob_2pl(theta, a, b)
    return a**2 * p * (1 - p)

def mle_theta(responses, a_vals, b_vals):
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
    infos = [item_information(theta, a, b) for a, b in zip(a_vals, b_vals)]
    total = np.sum(infos)
    return 1/np.sqrt(total) if total>0 else None

# --- Load item bank ---
item_bank = pd.read_csv('data/item_bank2.csv').set_index('ItemID')

def initialize_state():
    # Initialize session state variables
    if 'asked' not in st.session_state:
        st.session_state.asked = []
        st.session_state.responses = []
        st.session_state.theta = [0.0]
        st.session_state.se = [None]
        # Pick medium-difficulty item to start
        init = item_bank['b'].abs().idxmin()
        st.session_state.current = init

initialize_state()

# Stop rule
MAX_ITEMS = 10
if len(st.session_state.asked) >= MAX_ITEMS:
    st.title("CAT Complete")
    st.write(f"Test finished after {MAX_ITEMS} items.")
    st.write("Final θ estimate:", st.session_state.theta[-1])
    st.stop()

# Display question
st.title("CAT Dashboard")
step = len(st.session_state.asked) + 1
st.write(f"Question {step} of {MAX_ITEMS}")
cur_id = st.session_state.current
row = item_bank.loc[cur_id]
st.write(f"**{row['Question']}**")
opts = [row['OptionA'], row['OptionB'], row['OptionC'], row['OptionD']]
selected_key = f"choice_{cur_id}"
selected = st.radio("Options", opts, key=selected_key)

# Submission callback
def on_submit():
    # record response
    correct = row['CorrectAnswer']
    resp = 1 if selected == correct else 0
    st.session_state.asked.append(cur_id)
    st.session_state.responses.append(resp)
    # update θ and SE
    a_list = [item_bank.loc[i,'a'] for i in st.session_state.asked]
    b_list = [item_bank.loc[i,'b'] for i in st.session_state.asked]
    th_new = mle_theta(st.session_state.responses, a_list, b_list)
    se_new = compute_se(th_new, a_list, b_list)
    st.session_state.theta.append(th_new)
    st.session_state.se.append(se_new)
    # choose next item
    remain = item_bank.drop(index=st.session_state.asked)
    infos = remain.apply(lambda r: item_information(th_new, r['a'], r['b']), axis=1)
    st.session_state.current = infos.idxmax()
    # clear previous selection to avoid stale key
    del st.session_state[selected_key]

st.button("Submit Answer", on_click=on_submit)

# Plots
steps = list(range(len(st.session_state.theta)))
theta_vals = np.linspace(-4,4,200)
th_cur = st.session_state.theta[-1]

st.subheader("Current Item ICC")
fig1, ax1 = plt.subplots()
ax1.plot(theta_vals, prob_2pl(theta_vals, row['a'], row['b']))
ax1.axvline(th_cur, color='red', linestyle='--')
ax1.set_ylabel('P(correct)')
st.pyplot(fig1)

st.subheader("Current Item IIC")
fig2, ax2 = plt.subplots()
ax2.plot(theta_vals, item_information(theta_vals, row['a'], row['b']))
ax2.axvline(th_cur, color='red', linestyle='--')
ax2.set_ylabel('Information')
st.pyplot(fig2)

st.subheader("Standard Error History")
fig3, ax3 = plt.subplots()
ax3.plot(steps, st.session_state.se, marker='o')
ax3.set_ylabel('SE(θ)')
st.pyplot(fig3)

st.subheader("Theta Estimate History")
fig4, ax4 = plt.subplots()
ax4.plot(steps, st.session_state.theta, marker='o')
ax4.set_ylabel('θ')
st.pyplot(fig4)
