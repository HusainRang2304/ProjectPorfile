
import streamlit as st
import pandas as pd
import numpy as np
import joblib
from pathlib import Path

#BASE_DIR = Path(__file__).resolve().parent

#MODEL_PATH = BASE_DIR / "telco_churn_model.joblib"

print("Joblib installed successfully")
print("Joblib version:", joblib.__version__)

# -------------------------------
# Page configuration
# -------------------------------

st.set_page_config(
    page_title="Customer Churn Intelligence",
    page_icon="📊",
    layout="wide"
)

# -------------------------------
# Load trained model
# -------------------------------

#@st.cache_resource
#def load_model():
  #  if not MODEL_PATH.exists():
  #      st.error(f"Model file not found: {MODEL_PATH}")
 #       st.stop()

 #   return joblib.load(MODEL_PATH)

#artifact = load_model()

#model = artifact["model"]
#threshold = artifact["threshold"]
#feature_columns = artifact["feature_columns"]


@st.cache_resource
def load_model():
    return joblib.load("telco_churn_model.joblib")

    
artifact = load_model()

model = artifact["model"]
threshold = artifact["threshold"]
feature_columns = artifact["feature_columns"]

# -------------------------------
# Application header
# -------------------------------

st.title("📊 Customer Churn & Retention Intelligence")
st.write(
    "Predict customer churn probability, assess risk "
    "and identify potential retention actions."
)

st.info(
    "This is a portfolio demonstration using the IBM Telco "
    "Customer Churn dataset. Predictions are estimates, not guarantees."
)

# -------------------------------
# Customer input form
# -------------------------------

st.subheader("Customer Information")

with st.form("customer_form"):

    col1, col2, col3 = st.columns(3)

    with col1:
        gender = st.selectbox(
            "Gender", ["Female", "Male"]
        )

        senior = st.selectbox(
            "Senior Citizen", [0, 1]
        )

        partner = st.selectbox(
            "Partner", ["Yes", "No"]
        )

        dependents = st.selectbox(
            "Dependents", ["Yes", "No"]
        )

        tenure = st.number_input(
            "Tenure (months)",
            min_value=0,
            max_value=72,
            value=12
        )

        phone = st.selectbox(
            "Phone Service", ["Yes", "No"]
        )

    with col2:
        multiple_lines = st.selectbox(
            "Multiple Lines",
            ["No", "Yes", "No phone service"]
        )

        internet = st.selectbox(
            "Internet Service",
            ["DSL", "Fiber optic", "No"]
        )

        online_security = st.selectbox(
            "Online Security",
            ["Yes", "No", "No internet service"]
        )

        online_backup = st.selectbox(
            "Online Backup",
            ["Yes", "No", "No internet service"]
        )

        device_protection = st.selectbox(
            "Device Protection",
            ["Yes", "No", "No internet service"]
        )

        tech_support = st.selectbox(
            "Tech Support",
            ["Yes", "No", "No internet service"]
        )

    with col3:
        streaming_tv = st.selectbox(
            "Streaming TV",
            ["Yes", "No", "No internet service"]
        )

        streaming_movies = st.selectbox(
            "Streaming Movies",
            ["Yes", "No", "No internet service"]
        )

        contract = st.selectbox(
            "Contract",
            ["Month-to-month", "One year", "Two year"]
        )

        paperless = st.selectbox(
            "Paperless Billing", ["Yes", "No"]
        )

        payment = st.selectbox(
            "Payment Method",
            [
                "Electronic check",
                "Mailed check",
                "Bank transfer (automatic)",
                "Credit card (automatic)"
            ]
        )

    st.subheader("Billing Information")

    col4, col5 = st.columns(2)

    with col4:
        monthly_charges = st.number_input(
            "Monthly Charges",
            min_value=0.0,
            value=70.0
        )

    with col5:
        total_charges = st.number_input(
            "Total Charges",
            min_value=0.0,
            value=840.0
        )

    submitted = st.form_submit_button(
        "Predict Customer Churn",
        use_container_width=True
    )

# -------------------------------
# Prediction
# -------------------------------

if submitted:

    customer = pd.DataFrame([{
        "gender": gender,
        "SeniorCitizen": senior,
        "Partner": partner,
        "Dependents": dependents,
        "tenure": tenure,
        "PhoneService": phone,
        "MultipleLines": multiple_lines,
        "InternetService": internet,
        "OnlineSecurity": online_security,
        "OnlineBackup": online_backup,
        "DeviceProtection": device_protection,
        "TechSupport": tech_support,
        "StreamingTV": streaming_tv,
        "StreamingMovies": streaming_movies,
        "Contract": contract,
        "PaperlessBilling": paperless,
        "PaymentMethod": payment,
        "MonthlyCharges": monthly_charges,
        "TotalCharges": total_charges
    }])

    # Ensure the exact training feature order
    customer = customer[feature_columns]

    probability = model.predict_proba(customer)[0, 1]

    prediction = int(probability >= threshold)

    # Risk segmentation
    if probability >= 0.60:
        risk = "High Risk"
        action = "Prioritize customer retention outreach."
    elif probability >= 0.30:
        risk = "Medium Risk"
        action = "Consider a targeted engagement campaign."
    else:
        risk = "Low Risk"
        action = "Continue regular customer engagement."

    st.divider()
    st.subheader("Prediction Results")

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Churn Probability",
        f"{probability:.1%}"
    )

    c2.metric(
        "Risk Category",
        risk
    )

    c3.metric(
        "Model Classification",
        "Churn" if prediction == 1 else "No Churn"
    )

    st.progress(float(probability))

    st.subheader("Recommended Retention Action")
    st.write(action)

    st.caption(
        f"Classification threshold: {threshold:.2f}. "
        "Risk bands are illustrative business segments and "
        "should be validated against campaign capacity and costs."
    )
