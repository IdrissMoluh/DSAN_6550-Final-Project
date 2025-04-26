# step5_cat_engine_2pl.py

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os

# Load data
item_bank = pd.read_csv("data/calibrated_item_bank.csv")
response_matrix = pd.read_csv("data/simulated_responses.csv", index_col=0)

# Make sure plots folder exists
os.makedirs("plots", exist_ok=True)

# 2PL Item Information Function
def item_information_2pl(theta, a, b):
    p_theta = 1 / (1 + np.exp(-a * (theta - b)))
    info = a**2 * p_theta * (1 - p_theta)
    return info

# Ability estimation via Maximum Likelihood Estimation (simple grid search)
def mle_theta_2pl(responses, a_list, b_list):
    theta_grid = np.linspace(-3, 3, 61)  # grid from -3 to +3
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

# Plot and Save ICC + IIC for selected item
def plot_and_save_icc_iic_2pl(a, b, item_id, theta_est, respondent_id, step_num):
    theta_vals = np.linspace(-3, 3, 200)
    p_theta = 1 / (1 + np.exp(-a * (theta_vals - b)))
    info_vals = a**2 * p_theta * (1 - p_theta)

    fig, axs = plt.subplots(1, 2, figsize=(12, 4))

    # ICC
    axs[0].plot(theta_vals, p_theta)
    axs[0].axvline(x=theta_est, color='red', linestyle='--', label=f'θ est = {theta_est:.2f}')
    axs[0].set_title(f"ICC for {item_id}")
    axs[0].set_xlabel("Theta")
    axs[0].set_ylabel("P(correct)")
    axs[0].legend()

    # IIC
    axs[1].plot(theta_vals, info_vals)
    axs[1].axvline(x=theta_est, color='red', linestyle='--', label=f'θ est = {theta_est:.2f}')
    axs[1].set_title(f"IIC for {item_id}")
    axs[1].set_xlabel("Theta")
    axs[1].set_ylabel("Information")
    axs[1].legend()

    plt.tight_layout()

    filename = f"plots/{respondent_id}_step{step_num}_{item_id}.png"
    plt.savefig(filename)
    plt.close()

# Run CAT Simulation for One Respondent
def run_cat_2pl(respondent_id, max_items=6):
    responses = response_matrix.loc[respondent_id]
    item_pool = item_bank.copy()
    asked_items = []
    est_thetas = []

    theta_est = 0  # Start at θ = 0

    for step in range(1, max_items + 1):
        # Calculate item information at current theta
        item_pool['info'] = item_pool.apply(
            lambda row: item_information_2pl(theta_est, row['a_est'], row['b_est']),
            axis=1
        )

        # Pick the most informative item
        next_item = item_pool.loc[~item_pool['ItemID'].isin(asked_items)].sort_values('info', ascending=False).iloc[0]
        item_id = next_item['ItemID']
        asked_items.append(item_id)

        # Record the respondent's actual response
        actual_response = responses[item_id]

        # Save current step info
        est_thetas.append((step, theta_est, item_id, actual_response, next_item['a_est'], next_item['b_est'], next_item['info']))

        # Plot and save ICC and IIC
        plot_and_save_icc_iic_2pl(
            a=next_item['a_est'],
            b=next_item['b_est'],
            item_id=item_id,
            theta_est=theta_est,
            respondent_id=respondent_id,
            step_num=step
        )

        # Update theta estimate
        resp_vals = [responses[i] for i in asked_items]
        a_vals = [item_bank.set_index("ItemID").loc[i, "a_est"] for i in asked_items]
        b_vals = [item_bank.set_index("ItemID").loc[i, "b_est"] for i in asked_items]
        theta_est = mle_theta_2pl(resp_vals, a_vals, b_vals)

    # Final dataframe for the respondent
    return pd.DataFrame(est_thetas, columns=['Step', 'Theta_Est', 'ItemID', 'Response', 'a', 'b', 'Info'])

# === Main CAT Execution ===

# Run CAT for three different ability levels
cat_low = run_cat_2pl('R3')     # Low ability
cat_mid = run_cat_2pl('R250')   # Medium ability
cat_high = run_cat_2pl('R490')  # High ability

# Show results
print("✅ CAT simulation completed!\n")

print("Low Ability Respondent (R3):")
print(cat_low)

print("\nMedium Ability Respondent (R250):")
print(cat_mid)

print("\nHigh Ability Respondent (R490):")
print(cat_high)

