# step3_reliability_check.py

import numpy as np
import pandas as pd

# Load the simulated responses
response_matrix = pd.read_csv("data/simulated_responses.csv", index_col=0)

# Ensure that data is numeric
response_matrix = response_matrix.apply(pd.to_numeric)

# Function to compute Cronbach's Alpha
def cronbach_alpha(df):
    """
    Compute Cronbach's Alpha for a dataframe of item responses.
    Each row is a respondent, each column is an item.
    """
    item_scores = df.values
    item_variances = item_scores.var(axis=0, ddof=1)
    total_scores = item_scores.sum(axis=1)
    total_variance = total_scores.var(ddof=1)
    n_items = df.shape[1]
    alpha = (n_items / (n_items - 1)) * (1 - item_variances.sum() / total_variance)
    return alpha

# Calculate Cronbach's Alpha
alpha_score = cronbach_alpha(response_matrix)

# Display the result
print("✅ Step 3 complete: Reliability Check")
print(f"Cronbach's Alpha for the simulated response data: α = {alpha_score:.4f}")
