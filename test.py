import pandas as pd
import numpy as np
import joblib


def get_recommendations(model, scaler, df, feature_cols):

    actionable_features = [
        "Income",
        "CreditScore",
        "MonthsEmployed",
        "DTIRatio"
    ]

    recommendations = []

    current_prob = model.predict_proba(
        scaler.transform(df)
    )[0][1]

    for feature in actionable_features:

        temp_df = df.copy()
        original_value = temp_df[feature].iloc[0]

        if feature == "DTIRatio":

            test_values = np.arange(
                original_value,
                max(0, original_value - 0.60),  # floor at 0, wider range
                -0.01
            )

        else:

            test_values = np.arange(
                original_value,
                min(original_value * 15, 850) if feature == "CreditScore" else original_value * 15,  # CreditScore capped at 850
                max(1, original_value * 0.05)
            )

        found = False

        for value in test_values:

            temp_df[feature] = value

            temp_scaled = scaler.transform(
                temp_df.reindex(columns=feature_cols, fill_value=0)
            )

            prob = model.predict_proba(temp_scaled)[0][1]

            # Assuming 1 = Default
            if prob < 0.40:

                recommendations.append({
                    "Feature": feature,
                    "Current": original_value,
                    "Suggested": round(float(value), 2),
                    "New_Default_Probability": round(float(prob), 4)
                })

                found = True
                break

        if not found:

            recommendations.append({
                "Feature": feature,
                "Current": original_value,
                "Suggested": "Not achievable alone",
                "New_Default_Probability": None
            })

    return recommendations

# Load saved model
model, scaler, feature_cols = joblib.load("defaulter_model.pkl")

# Load new file
#new_df = pd.read_excel("New_Customers.xlsx")
new_df = pd.DataFrame([{
    "Income": 15000,
    "LoanAmount": 600000,
    "CreditScore": 430,
    "MonthsEmployed": 48,
    "NumCreditLines": 8,
    "InterestRate": 12.5,
    "LoanTerm": 36,
    "DTIRatio": 0.62,
    "Education": "High School",          # Bachelor's
    "EmploymentType": "Full-time",     # Full-time
    "HasMortgage": "Yes",        # Yes
    "HasDependents": "Yes"       # No
}])

# Apply SAME preprocessing
new_df["HasMortgage"] = np.where(new_df["HasMortgage"] == "Yes", 1, 0)
new_df["HasDependents"] = np.where(new_df["HasDependents"] == "Yes", 1, 0)

# new_df["Education"] = np.where(new_df["Education"] == "High School", 1,
#                         np.where(new_df["Education"] == "Bachelor's", 2,
#                         np.where(new_df["Education"] == "Master's", 3, 4)))

# new_df["EmploymentType"] = np.where(new_df["EmploymentType"] == "Full-time", 1,
#                         np.where(new_df["EmploymentType"] == "Part-time", 2,
#                         np.where(new_df["EmploymentType"] == "Self-employed", 3, 4)))

new_df = pd.get_dummies(new_df,columns=["Education", "EmploymentType"],drop_first=True)

# Ensure correct column order
new_df = new_df.reindex(columns=feature_cols,fill_value=0)

# Scale new data
new_scaled = scaler.transform(new_df)

# Predict
pred = model.predict(new_scaled)
prob = model.predict_proba(new_scaled)[:, 1]

new_df["Prediction_Default"] = pred
new_df["Probability_Default"] = prob

print(new_df)

print(f"\nDefault Probability: {prob[0]:.2%}")

if prob[0] > 0.4:

    recommendations = get_recommendations(
        model,
        scaler,
        new_df[feature_cols].copy(),
        feature_cols
    )

    print("\nPossible ways to qualify:")

    for rec in recommendations:

        if rec["Suggested"] == "Not achievable alone":
            print(
                f"{rec['Feature']}: "
                f"{rec['Current']} -> "
                f"Not achievable by changing this alone"
            )
        else:
            print(
                f"{rec['Feature']}: "
                f"{rec['Current']} -> "
                f"{rec['Suggested']} "
                f"(Default Probability: "
                f"{rec['New_Default_Probability']:.2%})"
            )

if prob[0] > 0.7:
    print("High Risk Customer")
elif prob[0] > 0.4:
    print("Medium Risk Customer")
else:
    print("Low Risk Customer")