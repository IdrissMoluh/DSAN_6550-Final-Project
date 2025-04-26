# DSAN 6550 Final Project
## Adaptive Measurement with AI – Computerized Adaptive Testing (CAT) Demo

**Author:** Idriss Moluh, Haichun Kang, Xiaolong Zhou, Qingqing Cheng
**Course:** DSAN 6550 Adaptative Measurement with AI - Spring 2025  
**Instructor:** Dr. Qiwei (Britt) He  

---

## 📚 Project Overview

This project designs a **Computerized Adaptive Test (CAT)** system based on the principles studied in **Adaptive Measurement with AI**.  
The objective is to simulate the full CAT pipeline, including:
- AI-assisted item generation (Chatgpt)
- Simulating examinee responses
- Checking data quality (reliability)
- Item parameter calibration (2PL model)
- Building an adaptive item selection system
- Deploying a working **Python Dashboard (Streamlit)** for demo

We simulated 500 respondents, calibrated item parameters, and created an adaptive system that selects optimal items in real-time.

---

## 🧩 Project Structure

```
DSAN_6550-Final-Project/
│
├── data/
│   ├── item_bank.csv                 # Generated 30 math items
│   ├── simulated_responses.csv       # 500 simulated respondents
│   └── calibrated_item_bank.csv      # Calibrated item parameters (2PL)
│
├── step2_simulate_responses_2pl.py    # Simulate 2PL responses
├── step3_reliability_check.py         # Cronbach's Alpha calculation
├── step4_calibration_logistic.py      # Item parameter estimation
├── step5_cat_engine_2pl.py            # CAT engine implementation
│
├── cat_dashboard.py                   # Streamlit dashboard
├── final_report.qmd (or final_report.docx) # Final report
├── demo_presentation.pptx             # Presentation slides
└── README.md                          # (this file)
```

---

## 📋 Step-by-Step Explanation

### 1. **Item Generation**

- **30 math items** were generated using AI assistance.
- Items were designed to cover different difficulty levels: **Easy**, **Medium**, and **Hard**.
- Each item is multiple-choice with 4 options (A–D).

### 📖 Full Math Item Pool

| ID  | Question                                           | Options (A–D)                       | Correct | Difficulty |
|:---:|:---------------------------------------------------|:------------------------------------|:-------:|:----------:|
| Q1  | What is 5 + 3?                                     | A. 6, B. 7, C. 8, D. 9              | C       | Easy       |
| Q2  | Solve: 9 × 6                                       | A. 45, B. 54, C. 63, D. 72          | B       | Easy       |
| Q3  | What is the square root of 49?                     | A. 6, B. 7, C. 8, D. 9              | B       | Easy       |
| Q4  | Solve for x: 2x + 3 = 11                           | A. 3, B. 4, C. 5, D. 6              | C       | Easy       |
| Q5  | Simplify: 3(2 + 4)                                 | A. 18, B. 12, C. 9, D. 21           | A       | Easy       |
| Q6  | 25% of 200 is                                      | A. 25, B. 50, C. 75, D. 100         | B       | Easy       |
| Q7  | What is 7 squared?                                 | A. 49, B. 42, C. 56, D. 36          | A       | Easy       |
| Q8  | If a triangle has angles 90°, 30°, the last angle? | A. 30°, B. 60°, C. 90°, D. 45°     | B       | Easy       |
| Q9  | Simplify: 16 ÷ 4 + 2                               | A. 2, B. 4, C. 6, D. 8              | C       | Easy       |
| Q10 | Which is a prime number?                           | A. 4, B. 6, C. 9, D. 11             | D       | Easy       |
| Q11 | Solve: x² = 144                                    | A. ±12, B. 12, C. 14, D. 10         | A       | Medium     |
| Q12 | Solve: 2x - 5 = 3x + 7                             | A. -12, B. 12, C. 6, D. -6          | D       | Medium     |
| Q13 | Median of [7, 5, 3, 9, 1]?                         | A. 1, B. 3, C. 5, D. 7              | C       | Medium     |
| Q14 | Factor: x² - 5x + 6                                | A. (x-2)(x-3), B. (x+2)(x-3), etc. | A       | Medium     |
| Q15 | Simplify: (3x²)(2x³)                               | A. 6x⁶, B. 6x⁵, C. 5x⁶, D. 5x⁵      | B       | Medium     |
| Q16 | Solve: 3(2x - 1) = 15                              | A. 2, B. 3, C. 4, D. 5              | B       | Medium     |
| Q17 | 30% of 250                                         | A. 65, B. 70, C. 75, D. 80          | C       | Medium     |
| Q18 | f(x) = x² - 2x + 1, f(3) = ?                       | A. 4, B. 2, C. 1, D. 0              | C       | Medium     |
| Q19 | Divisible by both 3 and 5?                         | A. 12, B. 15, C. 25, D. 45          | B       | Medium     |
| Q20 | Convert 0.75 to fraction                           | A. 1/3, B. 3/4, C. 2/5, D. 4/5      | B       | Medium     |
| Q21 | Solve: log₁₀(1000) = ?                             | A. 2, B. 3, C. 10, D. 100           | B       | Hard       |
| Q22 | Derivative of x³ + 2x                              | A. 3x² + 2, B. 2x + 3x², etc.       | A       | Hard       |
| Q23 | Solve: ∫x dx                                       | A. x, B. x²/2, C. x², D. 1/x        | B       | Hard       |
| Q24 | If sin(x) = 0.5, then x=? (0°–180°)                | A. 60°, B. 90°, C. 120°, D. A & C   | D       | Hard       |
| Q25 | Solve: 3x - 4 > 5                                  | A. x>3, B. x<3, C. x>4, D. x>2      | A       | Hard       |
| Q26 | det([[1,2],[3,4]])?                                | A. -2, B. -4, C. 2, D. 10           | A       | Hard       |
| Q27 | Probability of rolling 7 with 2 dice?              | A. 1/6, B. 1/5, C. 1/12, D. 1/36    | A       | Hard       |
| Q28 | If x = log₂(8), x=?                                | A. 2, B. 3, C. 4, D. 5              | B       | Hard       |
| Q29 | Solve: 2ⁿ = 32                                     | A. 4, B. 5, C. 6, D. 7              | B       | Hard       |
| Q30 | Area of a circle with r=3                          | A. 9π, B. 6π, C. 3π, D. π           | A       | Hard       |

---

### 2. **Simulated Response Data**

- 500 respondents simulated using 2PL probability function.
- Responses reflect realistic behavior: easier items answered correctly more often.

### 3. **Reliability Check**

- Cronbach’s Alpha calculated:
  - **α = 0.8954** → Strong internal consistency.

### 4. **Item Calibration**

- Used logistic regression to estimate 2PL parameters (a, b).
- Created calibrated item bank.

### 5. **CAT Engine**

- Start with θ̂ = 0
- Select next item with **maximum information** at current θ̂
- Update θ̂ using MLE grid search
- No repeated items

### 6. **Three Respondents Example**

- R3 (Low ability), R250 (Medium), R490 (High ability)
- Demonstrated adaptivity dynamically for different abilities.

### 7. **Visualizations**

- θ̂ trajectory plot
- ICC + IIC plots at every step
- CAT session result table at every step

---

## 📈 Streamlit Dashboard

- Select respondent
- Run CAT session
- Visualize θ̂ evolution
- View ICC/IIC plots
- Download session results as CSV

---

## 🏁 How to Run the Dashboard

```bash
pip install streamlit matplotlib pandas numpy
streamlit run cat_dashboard.py
```

- Open browser: http://localhost:8501

---

## 📦 Requirements

- Python 3.8+
- Streamlit
- Matplotlib
- Pandas
- Numpy
- scikit-learn

---

## 📢 Limitations and Future Work

- Responses are simulated (no live answering).
- 2PL model only (no guessing c parameter).
- Future: add real-time user answering and standard error-based stopping rules.

---

## 🎯 Final Words

This project demonstrates a full pipeline of computerized adaptive measurement using 2PL IRT models, and delivers a working interactive CAT system.





