# DSAN 6550 Final Project
## Adaptive Measurement with AI – Computerized Adaptive Testing (CAT) Demo

**Authors:** Idriss Moluh, Haichun Kang, Xiaolong Zhou, Qingqing Chen  
**Course:** DSAN 6550 Adaptive Measurement with AI – Spring 2025  
**Instructor:** Dr. Qiwei (Britt) He  

---

## 📚 Project Overview (🧠 Computerized Adaptive Testing (CAT) Dashboard)

This project is a **Computerized Adaptive Test (CAT)** simulation built with **Python** and **Streamlit**.  
It dynamically selects the best math questions for a respondent based on their estimated ability (**θ̂**) after each answer.

Our item pool focuses on **General Math Assessment** — including algebra, arithmetic, geometry, and basic calculus concepts.

---

## 📋 Project Structure

- `cat_dashboard.py` → Main Streamlit app
- `data/item_bank2.csv` → Item pool (30 math items with calibrated 2PL parameters)
- `requirements.txt` → Project dependencies list

---

## 🛠 How to Run the Dashboard Locally

1. **Clone the repository** or download the project files.

2. **Install required packages**:

```bash
pip install -r requirements.txt
```

3. **Run the app**:

```bash
streamlit run cat_dashboard.py
```

4. Open the provided **localhost URL** (http://localhost:8501) in my browser.

---

## 🧩 How the CAT System Works

- **Adaptive Testing**:
  - The system starts with a **medium difficulty** question (where `b ≈ 0`).
  - After each answer, it estimates the user's **latent ability (θ̂)** using Maximum Likelihood Estimation (MLE).
  - It selects the next question by choosing the item with the **highest information** at the current θ̂.

- **Scoring and Difficulty**:
  - Real-time **score** updates after each question.
  - Each question's **difficulty level** is categorized as **Easy**, **Medium**, or **Hard**, based on its `b` parameter.

- **Stopping Rule**:
  - The CAT session stops after **10 questions**.

- **Visual Feedback**:
  - 4 diagnostic plots are displayed:
    - Current Item Characteristic Curve (ICC)
    - Current Item Information Curve (IIC)
    - Standard Error (SE) Trajectory
    - Theta (θ) Estimation Trajectory

- **Reset Button**:
  - Users can **restart** the CAT session at any time cleanly.

---

## 🎨 Dashboard Layout

- **Top**: Displays Current Score 🏆 and Current Question Difficulty 📈.
- **Middle**: Question and Multiple-Choice Options with a "Submit Answer" button ✅.
- **Bottom**: 4 Diagnostic Plots organized in 2 rows × 2 columns.
- **End**: "Reset and Start Over" 🔄 button.

---

## 📚 About the Item Bank (Sample)

The `item_bank2.csv` contains **30 calibrated math items** based on the 2PL IRT model.  
Each item includes:
- 4 answer options (A, B, C, D)
- Correct answer key
- Discrimination parameter (`a`)
- Difficulty parameter (`b`) : **Easy** `b ≈ -1` / **Medium** `b ≈ 0` / **Hard** `b ≈ 1`.

### Example Items:

| ItemID | Question | Correct Answer | Difficulty (b) |
|:------:|:---------|:---------------:|:--------------:|
| Q1 | What is 5 + 3? | 8 (Option C) | -1 |
| Q2 | Solve: 9 × 6 | 54 (Option B) | -1 |
| Q3 | What is the square root of 49? | 7 (Option B) | -1 |
| Q11 | Solve: x² = 144 | ±12 (Option A) | 0 |
| Q21 | Solve: log₁₀(1000) = ? | 3 (Option B) | 1 |

> The item bank covers basic operations, equations, factoring, percentages, derivatives, logarithms, trigonometry, and basic probability.

---

## 📈 Technologies Used

- [Python 3.8+](https://www.python.org/)
- [Streamlit](https://streamlit.io/)
- [Pandas](https://pandas.pydata.org/)
- [NumPy](https://numpy.org/)
- [Matplotlib](https://matplotlib.org/)

---

## 🚀 Future Improvements

- Dynamic stopping rule based on Standard Error (SE(θ̂)) threshold.
- Time tracking and response latency analysis.
- Adaptive test branching based on content area (e.g., Algebra vs Geometry).
- Expand item bank with higher-level math (Pre-Calculus, Statistics, etc.).

---

## 👥 Authors

- Idriss Moluh  
- Haichun Kang  
- Xiaolong Zhou  
- Qingqing Chen  

(For DSAN 6550: Adaptive Measurement with AI, Spring 2025)






