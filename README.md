# 🏦 Loan Defaulter Prediction

A machine learning project that predicts whether a loan applicant is likely to default, using Logistic Regression. Data is stored and managed in Snowflake for future reference and analysis.

---

## 📌 How It Works

1. **`upload_base_file.py`** uploads the initial dataset to Snowflake.
2. **`append.py`** adds new applicant records to the existing Snowflake table.
3. **`check_data.py`** lets you inspect and validate the data stored in Snowflake.
4. **`model_create.py`** trains a Logistic Regression model on the data and saves it as a `.pkl` file.
5. **`test.py`** loads the saved model and predicts whether a new applicant will default on their loan.

---

## 🗂️ Project Structure

```
Loan-Defaulter-Prediction/
├── upload_base_file.py   # Uploads the base dataset to Snowflake
├── append.py             # Appends new records to Snowflake table
├── check_data.py         # Validates and inspects data in Snowflake
├── model_create.py       # Trains Logistic Regression model, saves as .pkl
└── test.py               # Loads model and predicts default status for new input
```

---

## 🧠 Model

- **Algorithm:** Logistic Regression
- **Output:** Binary classification — `1` (likely to default) or `0` (not likely to default)
- **Saved as:** `.pkl` file (using `pickle` or `joblib`)

### Input Features

| Feature           | Description                                      |
|-------------------|--------------------------------------------------|
| `Income`          | Annual income of the applicant                   |
| `LoanAmount`      | Total loan amount requested                      |
| `CreditScore`     | Applicant's credit score                         |
| `MonthsEmployed`  | Number of months currently employed              |
| `NumCreditLines`  | Number of active credit lines                    |
| `InterestRate`    | Interest rate on the loan                        |
| `LoanTerm`        | Loan repayment term (in months)                  |
| `DTIRatio`        | Debt-to-income ratio                             |
| `Education`       | Highest education level of the applicant         |
| `EmploymentType`  | Type of employment (e.g. full-time, self-employed) |
| `HasMortgage`     | Whether the applicant has an existing mortgage   |
| `HasDependents`   | Whether the applicant has dependents             |

> **Target variable:** `Default` — `1` if the applicant defaulted, `0` otherwise.

---

## ⚙️ Setup

### Prerequisites

- Python 3.8+
- A [Snowflake](https://www.snowflake.com/) account with a warehouse, database, and schema ready

### Install Dependencies

```bash
pip install pandas scikit-learn snowflake-connector-python joblib python-dotenv
```

### Environment Variables

All credentials are read from environment variables. Create a `.env` file locally or set them in your environment:

| Variable      | Description                                                    |
|---------------|----------------------------------------------------------------|
| `USER`        | Snowflake username                                             |
| `PASSWORD`    | Snowflake password                                             |
| `ACCOUNT`     | Snowflake account identifier (e.g. `abc123.ap-south-1.aws`)   |
| `WAREHOUSE`   | Snowflake warehouse name                                       |
| `DATABASE`    | Snowflake database name                                        |
| `SCHEMA`      | Snowflake schema name                                          |
| `TABLE_NAME`  | Snowflake table name for loan data                             |

---

## 🚀 Usage

### 1. Upload Base Dataset

```bash
python upload_base_file.py
```

Uploads your initial loan dataset to Snowflake.

### 2. Append New Data

```bash
python append.py
```

Adds new applicant records to the existing Snowflake table.

### 3. Check Data

```bash
python check_data.py
```

Inspects and validates the data currently stored in Snowflake.

### 4. Train the Model

```bash
python model_create.py
```

Fetches data from Snowflake, trains a Logistic Regression model, and saves it as a `.pkl` file.

### 5. Test on a New Applicant

```bash
python test.py
```

Loads the trained `.pkl` model and predicts whether a new applicant is likely to default based on their details.

---

## 🗃️ Snowflake Schema

Snowflake is used as the central data store, allowing teams to retain applicant data for future analysis, retraining, or auditing.

The table contains all input features plus the `Default` target column:

```
Income, LoanAmount, CreditScore, MonthsEmployed, NumCreditLines,
InterestRate, LoanTerm, DTIRatio, Education, EmploymentType,
HasMortgage, HasDependents, Default
```

---

## 🛠️ Tech Stack

- **Python** — core scripting language
- **scikit-learn** — Logistic Regression model training and evaluation
- **Snowflake** — cloud data storage for loan records
- **pandas** — data manipulation and preprocessing
- **pickle / joblib** — model serialization

---

## 📄 License

This project is open source. Feel free to fork and build upon it!
