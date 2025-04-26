# cat_dashboard.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

# ========== Load Data ==========
item_bank = pd.read_csv("data/calibrated_item_bank.csv")
response_matrix = pd.read_csv("data/simulated_responses.csv", index_col=0)

# Ensure plots folder exists
os.makedirs("plots", exist_ok=True)

# ========== Define Functions ==========

def item_information_2pl(theta, a, b):
    """Calculate item information for given theta using the 2PL model."""
    p_theta = 1 / (1 + np.exp(-a * (theta - b)))
    info = a**2 * p_theta * (1 - p_theta)
    return info

def mle_theta_2pl(responses, a_list, b_list):
    """Estimate theta by maximizing likelihood (simple grid search)."""
    theta_grid = np.linspace(-3, 3, 61)
    max_ll = -np.inf
    best_theta = 0
    for theta in theta_grid:
        ll = 0
        for i in range(len(responses)):
            a, b = a_list[i], b_list[i]
            p = 1 / (1 + np.exp(-a * (theta - b)))
            r = responses[i]
            ll += r * np.log(p + 1e-6) + (1 - r) * np.log(1 - p + 1e-6)
        if ll > max_ll:
            max_ll = ll
            best_theta = theta
    return best_theta

def plot_icc_iic(a, b, item_id, theta_est):
    """Plot ICC and IIC for a given item at the estimated theta."""
    theta_vals = np.linspace(-3, 3, 200)
    p_theta = 1 / (1 + np.exp(-a * (theta_vals - b)))
    info_vals = a**2 * p_theta * (1 - p_theta)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    # ICC
    axs[0].plot(theta_vals, p_theta)
    axs[0].axvline(theta_est, color='red', linestyle='--', label=f'θ est = {theta_est:.2f}')
    axs[0].set_title(f"Item Characteristic Curve (ICC) for {item_id}")
    axs[0].set_xlabel("Theta (Ability)")
    axs[0].set_ylabel("P(correct)")
    axs[0].legend()

    # IIC
    axs[1].plot(theta_vals, info_vals)
    axs[1].axvline(theta_est, color='red', linestyle='--', label=f'θ est = {theta_est:.2f}')
    axs[1].set_title(f"Item Information Curve (IIC) for {item_id}")
    axs[1].set_xlabel("Theta (Ability)")
    axs[1].set_ylabel("Information")
    axs[1].legend()

    plt.tight_layout()
    st.pyplot(fig)

def run_cat_2pl(respondent_id, max_items=6):
    """Run the CAT simulation for a single respondent."""
    responses = response_matrix.loc[respondent_id]
    item_pool = item_bank.copy()
    asked_items = []
    est_thetas = []

    theta_est = 0  # Initial ability estimate

    for step in range(1, max_items + 1):
        item_pool['info'] = item_pool.apply(
            lambda row: item_information_2pl(theta_est, row['a_est'], row['b_est']),
            axis=1
        )

        next_item = item_pool.loc[~item_pool['ItemID'].isin(asked_items)].sort_values('info', ascending=False).iloc[0]
        item_id = next_item['ItemID']
        asked_items.append(item_id)

        actual_response = responses[item_id]
        est_thetas.append((step, theta_est, item_id, actual_response, next_item['a_est'], next_item['b_est'], next_item['info']))

        # Update theta
        resp_vals = [responses[i] for i in asked_items]
        a_vals = [item_bank.set_index("ItemID").loc[i, "a_est"] for i in asked_items]
        b_vals = [item_bank.set_index("ItemID").loc[i, "b_est"] for i in asked_items]
        theta_est = mle_theta_2pl(resp_vals, a_vals, b_vals)

    return pd.DataFrame(est_thetas, columns=[
        'Step',               # Step number
        'Theta_Est',           # Estimated ability before selecting the item
        'ItemID',              # ID of the item selected
        'Response',            # 1 = correct, 0 = incorrect
        'a',                   # Discrimination parameter
        'b',                   # Difficulty parameter
        'Info'                 # Information value at theta
    ])

def plot_theta_trajectory(df):
    """Plot the evolution of estimated theta across CAT steps."""
    plt.figure(figsize=(8, 5))
    plt.plot(df['Step'], df['Theta_Est'], marker='o')
    plt.title('Ability (θ) Estimation Trajectory')
    plt.xlabel('Step')
    plt.ylabel('Estimated Ability (θ)')
    plt.grid(True)
    st.pyplot(plt)

# Highlight correct and incorrect responses
def highlight_response(val):
    """Color code correct and incorrect responses."""
    color = 'lightgreen' if val == 1 else 'salmon'
    return f'background-color: {color}'

# ========== Streamlit App ==========

st.title("📚 Computerized Adaptive Testing (CAT) Demo - 2PL Model")

# 🎉 Welcome message
st.success("👋 Welcome to Idriss Moluh, Haichun Kang, Xiaolong Zhou, Qingqing Cheng's DSAN6550 Final Project - Adaptive Measurement with AI!")

st.markdown("""
This dashboard simulates a **Computerized Adaptive Test** using math items.  
- Select a respondent
- Run CAT session
- View item selections, ICC, IIC, and θ̂ trajectory
""")

respondent_id = st.selectbox("Select a Respondent ID", response_matrix.index.tolist())

if st.button("Run CAT Simulation"):
    st.success(f"Running CAT simulation for {respondent_id}...")

    cat_result = run_cat_2pl(respondent_id)

    # 📄 Explain table columns meaning
    st.subheader("📄 CAT Results Table")

    st.markdown("""
| Column | Meaning |
|:-------|:--------|
| **Step** | Which step in the CAT process (first item, second item, etc.) |
| **Theta_Est** | Estimated latent ability (θ̂) before selecting this item |
| **ItemID** | ID of the item selected at this step (e.g., Q5, Q12) |
| **Response** | 1 = Correct answer (green), 0 = Incorrect answer (red) |
| **a** | Discrimination parameter of the item |
| **b** | Difficulty parameter of the item |
| **Info** | Information provided by this item at current θ̂ |
    """)

    # 🎨 Apply color highlighting to Response column
    styled_cat_result = cat_result.style.applymap(highlight_response, subset=['Response'])
    st.dataframe(styled_cat_result, use_container_width=True)

    # 📈 Plot θ trajectory
    st.subheader("📈 Ability (θ) Estimation Trajectory")
    plot_theta_trajectory(cat_result)

    # 📊 Show ICC + IIC plots and explanation for each selected item
    st.subheader("📊 ICC and IIC for Selected Items + Selection Explanation")
    for idx, row in cat_result.iterrows():
        st.markdown(f"### Step {row['Step']}: Item {row['ItemID']}")
        plot_icc_iic(row['a'], row['b'], row['ItemID'], row['Theta_Est'])

        # Explanation why item was selected
        st.markdown(f"""
        🔍 **Selection Reason:**  
        At estimated ability θ̂ = {row['Theta_Est']:.2f}, item {row['ItemID']} was selected because it provided the highest information (**Info = {row['Info']:.2f}**) among available items.
        """)

    # 📥 Option to download results
    st.subheader("📥 Download CAT Results")
    csv = cat_result.to_csv(index=False).encode('utf-8')
    st.download_button("Download Results as CSV", data=csv, file_name=f"{respondent_id}_cat_results.csv", mime='text/csv')

    # 🔄 Add Reset Button
    st.subheader("🔄 Restart CAT Session")
    if st.button("Reset and Choose Another Respondent"):
        st.experimental_rerun()

st.markdown("---")
st.caption("DSAN 6550 Final Project • Adaptive Measurement with AI")

