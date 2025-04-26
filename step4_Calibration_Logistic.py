import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression

# Load the saved data
response_matrix = pd.read_csv("data/simulated_responses.csv", index_col=0)
item_bank = pd.read_csv("data/item_bank.csv")

# Regenerate the same theta used in simulation
n_respondents = response_matrix.shape[0]
theta = np.random.normal(0, 1, n_respondents)

# Initialize calibration results
calibrated_params = []

# For each item, fit logistic regression: response ~ theta
for item in item_bank["ItemID"]:
    y = response_matrix[item].values
    X = theta.reshape(-1, 1)

    if np.unique(y).size == 1:
        # Skip if no variance
        calibrated_params.append((item, np.nan, np.nan))
        continue

    model = LogisticRegression()
    model.fit(X, y)

    a_est = model.coef_[0][0]  # Discrimination (slope)
    b_est = -model.intercept_[0] / a_est if a_est != 0 else np.nan  # Difficulty (threshold)

    calibrated_params.append((item, a_est, b_est))

# Create a new calibrated item bank
calibrated_item_bank = pd.DataFrame(calibrated_params, columns=["ItemID", "a_est", "b_est"])

# Save the calibrated parameters
calibrated_item_bank.to_csv("data/calibrated_item_bank.csv", index=False)

print("✅ Step 4 complete: Calibrated item parameters saved.")