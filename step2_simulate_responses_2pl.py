import numpy as np
import pandas as pd
import os

# create the data folder 
# os.makedirs("data", exist_ok=True)

# Set random seed for reproducibility
np.random.seed(42)

# Step 2: Simulate item parameters for 30 items using 2PL
n_items = 30
item_ids = [f"Q{i+1}" for i in range(n_items)]

# Discrimination 'a' from [1.0 to 2.5], Difficulty 'b' from [-2 to 2]
a_params = np.random.uniform(1.0, 2.5, size=n_items)
b_params = np.linspace(-2, 2, n_items)

item_bank = pd.DataFrame({
    "ItemID": item_ids,
    "a": a_params,
    "b": b_params
})

# Simulate 500 respondents
n_respondents = 500
theta = np.random.normal(0, 1, n_respondents)

# 2PL probability function
def prob_2pl(theta, a, b):
    return 1 / (1 + np.exp(-a * (theta - b)))

# Create response matrix
response_matrix = pd.DataFrame(index=[f"R{i+1}" for i in range(n_respondents)], columns=item_ids)

# Generate responses
for i, item in item_bank.iterrows():
    p_correct = prob_2pl(theta, item['a'], item['b'])
    responses = np.random.binomial(1, p_correct)
    response_matrix[item['ItemID']] = responses

# Save files
item_bank.to_csv("data/item_bank.csv", index=False)
response_matrix.to_csv("data/simulated_responses.csv")

print("✅ Step 2 complete: Item bank and simulated responses saved.")