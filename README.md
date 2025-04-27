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

- `cat_dashboard_streamlit.py` → Main Streamlit app
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
streamlit run cat_dashboard_streamlit.py
```

4. Open the provided **localhost URL** (http://localhost:8501) in our browser.

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

The `item_bank2.csv` contains **30 calibrated math items** based on the **2PL IRT model**.  
Each item includes:

- 4 answer options (**A**, **B**, **C**, **D**)
- A correct answer key
- A discrimination parameter (`a`)
- A difficulty parameter (`b`) categorized as:
  - **Easy**: `b ≈ -1`
  - **Medium**: `b ≈ 0`
  - **Hard**: `b ≈ 1`

These items cover:

- Basic operations
- Solving equations
- Factoring
- Percentages
- Trigonometric identities
- Basic probability
- Derivatives
- Logarithms
- Area formulas

---

## 📚 Full Item Bank (`item_bank2.csv`)

| ItemID | Question | Option A | Option B | Option C | Option D | Correct Answer | a | b |
|:------:|:---------|:---------|:---------|:---------|:---------|:---------------:|:-:|:-:|
| Q1 | What is 5 + 3? | 6 | 7 | 8 | 9 | C | 1 | -1 |
| Q2 | Solve: 9 × 6 | 45 | 54 | 63 | 72 | B | 1 | -1 |
| Q3 | What is the square root of 49? | 6 | 7 | 8 | 9 | B | 1 | -1 |
| Q4 | Solve for x: 2x + 3 = 11 | 3 | 4 | 5 | 6 | C | 1 | -1 |
| Q5 | Simplify: 3(2 + 4) | 18 | 12 | 9 | 21 | A | 1 | -1 |
| Q6 | 25% of 200 is | 25 | 50 | 75 | 100 | B | 1 | -1 |
| Q7 | What is 7 squared? | 49 | 42 | 56 | 36 | A | 1 | -1 |
| Q8 | If a triangle has angles 90°, 30°, the last angle? | 30° | 60° | 90° | 45° | B | 1 | -1 |
| Q9 | Simplify: 16 ÷ 4 + 2 | 2 | 4 | 6 | 8 | C | 1 | -1 |
| Q10 | Which is a prime number? | 4 | 6 | 9 | 11 | D | 1 | -1 |
| Q11 | Solve: x² = 144 | ±12 | 12 | 14 | 10 | A | 1.2 | 0 |
| Q12 | Solve: 2x - 5 = 3x + 7 | -12 | 12 | 6 | -6 | D | 1.2 | 0 |
| Q13 | Median of [7,5,3,9,1]? | 1 | 3 | 5 | 7 | C | 1.2 | 0 |
| Q14 | Factor: x² - 5x + 6 | (x-2)(x-3) | (x+2)(x-3) | (x-3)(x+1) | (x-6)(x+1) | A | 1.2 | 0 |
| Q15 | Simplify: (3x²)(2x³) | 6x⁵ | 6x⁶ | 5x⁶ | 5x⁵ | B | 1.2 | 0 |
| Q16 | Solve: 3(2x - 1) = 15 | 2 | 3 | 4 | 5 | B | 1.2 | 0 |
| Q17 | 30% of 250 | 65 | 70 | 75 | 80 | C | 1.2 | 0 |
| Q18 | f(x) = x² - 2x + 1, f(3) = ? | 4 | 2 | 1 | 0 | C | 1.2 | 0 |
| Q19 | Divisible by both 3 and 5? | 12 | 15 | 25 | 45 | B | 1.2 | 0 |
| Q20 | Convert 0.75 to fraction | 3-Jan | 4-Mar | 5-Feb | 5-Apr | B | 1.2 | 0 |
| Q21 | Solve: log₁₀(1000) = ? | 2 | 3 | 10 | 100 | B | 1.5 | 1 |
| Q22 | Derivative of x³ + 2x | 3x² + 2 | 2x + 3x² | 3x + 2x² | 2x² + 3 | A | 1.5 | 1 |
| Q23 | Solve: ∫x dx | x | x²/2 | x² | 1/x | B | 1.5 | 1 |
| Q24 | If sin(x) = 0.5, then x=? (0°–180°) | 60° | 90° | 120° | A & C | D | 1.5 | 1 |
| Q25 | Solve: 3x - 4 > 5 | x>3 | x<3 | x>4 | x>2 | A | 1.5 | 1 |
| Q26 | det([[1,2],[3,4]])? | -2 | -4 | 2 | 10 | A | 1.5 | 1 |
| Q27 | Probability of rolling 7 with 2 dice? | 6-Jan | 5-Jan | 12-Jan | Jan-36 | A | 1.5 | 1 |
| Q28 | If x = log₂(8), x=? | 2 | 3 | 4 | 5 | B | 1.5 | 1 |
| Q29 | Solve: 2ˣ = 32 | 4 | 5 | 6 | 7 | B | 1.5 | 1 |
| Q30 | Area of a circle with r=3 | 9π | 6π | 3π | π | A | 1.5 | 1 |

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

(For DSAN 6550: Adaptive Measurement with AI, Spring 2025). Thanks!






