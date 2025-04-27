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

    # choose next item by max information at new
