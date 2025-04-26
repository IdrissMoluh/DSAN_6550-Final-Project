# main.py

## Let's run all project steps automatically

import step2_simulate_responses_2pl
import step3_reliability_check
import step4_Calibration_Logistic
import step5_Cat_Engine

def main():
    print("🚀 Starting full CAT pipeline...")

    print("\n=== Step 2: Simulating responses ===")
    step2_simulate_responses_2pl.run_simulation()

    print("\n=== Step 3: Checking reliability ===")
    step3_reliability_check.run_reliability_check()

    print("\n=== Step 4: Calibrating item parameters ===")
    step4_Calibration_Logistic.run_calibration()

    print("\n=== Step 5: Running sample CAT engine ===")
    step5_Cat_Engine.run_sample_cat()

    print("\n✅ All steps completed successfully!")

if __name__ == "__main__":
    main()
