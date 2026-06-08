import pandas as pd
import numpy as np
import joblib

# Load saved model
model, scaler, feature_cols = joblib.load("defaulter_model.pkl")

# Load new file
#new_df = pd.read_excel("New_Customers.xlsx")
new_df = pd.DataFrame([{
    "Income": 60000,
    "LoanAmount": 15000,
    "CreditScore": 720,
    "MonthsEmployed": 48,
    "NumCreditLines": 4,
    "InterestRate": 12.5,
    "LoanTerm": 36,
    "DTIRatio": 0.32,
    "Education": "High School",          # Bachelor's
    "EmploymentType": "Full-time",     # Full-time
    "HasMortgage": "Yes",        # Yes
    "HasDependents": "No"       # No
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
if prob[0] > 0.7:
    print("High Risk Customer")
elif prob[0] > 0.4:
    print("Medium Risk Customer")
else:
    print("Low Risk Customer")
