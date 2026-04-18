import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.preprocessing import StandardScaler
import joblib

#df = pd.read_excel(r"Defaulter.xlsx")
def main(data):
    df=data.copy()
    df = df[[
        "Income","LoanAmount","CreditScore","MonthsEmployed",
        "NumCreditLines","InterestRate","LoanTerm","DTIRatio",
        "Education","EmploymentType","HasMortgage","HasDependents","Default"
    ]]

    df["HasMortgage"] = np.where(df["HasMortgage"] == "Yes", 1, 0)
    df["HasDependents"] = np.where(df["HasDependents"] == "Yes", 1, 0)

    df["Education"] = np.where(df["Education"] == "High School", 1,
                        np.where(df["Education"] == "Bachelor's", 2,
                        np.where(df["Education"] == "Master's", 3, 4)))

    df["EmploymentType"] = np.where(df["EmploymentType"] == "Full-time", 1,
                        np.where(df["EmploymentType"] == "Part-time", 2,
                        np.where(df["EmploymentType"] == "Self-employed", 3, 4)))

    X = df.drop(columns=["Default"])
    y = df["Default"]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )

    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)

    model = LogisticRegression(max_iter=1000, solver="liblinear")
    model.fit(X_train_scaled, y_train)

    y_pred = model.predict(X_test_scaled)
    y_prob = model.predict_proba(X_test_scaled)[:, 1]

    print(y_pred)
    print(y_prob)
    print(accuracy_score(y_test, y_pred) * 100)

    joblib.dump((model, scaler, X.columns.tolist()), "defaulter_model.pkl")
    print("Model saved successfully!")
