
import streamlit as st
import pandas as pd
import joblib

st.set_page_config(
    page_title="Urban Waterlogging Risk Predictor",
    page_icon="🌧️",
    layout="centered"
)

MODEL_PATH = "flood_risk_model.pkl"
model = joblib.load(MODEL_PATH)

FEATURES = [
    "Mean_Rainfall_mm",
    "Max_Rainfall_mm",
    "Rainfall_Previous_3_Days_mm",
    "Rainfall_Previous_7_Days_mm",
    "Rainfall_3_Day_Total_mm",
    "Rainfall_7_Day_Total_mm"
]

st.title("🌧️ Urban Waterlogging Risk Predictor")
st.write(
    "Machine Learning-Based Early Warning System for "
    "Predicting Urban Waterlogging Risk During Heavy Rainfall"
)

st.warning(
    "Academic prototype only. The model was trained on 2023 "
    "India-wide recorded flood events, not verified urban "
    "waterlogging labels. Predictions are experimental and "
    "must not be used for real-world safety decisions."
)

st.subheader("Enter rainfall measurements")

mean_rain = st.number_input(
    "Current mean rainfall (mm)",
    min_value=0.0, value=10.0, step=1.0
)
max_rain = st.number_input(
    "Maximum grid rainfall (mm)",
    min_value=0.0, value=20.0, step=1.0
)
previous_3 = st.number_input(
    "Rainfall in previous 3 days (mm)",
    min_value=0.0, value=30.0, step=1.0
)
previous_7 = st.number_input(
    "Rainfall in previous 7 days (mm)",
    min_value=0.0, value=80.0, step=1.0
)
total_3 = st.number_input(
    "Current day + previous 2 days (mm)",
    min_value=0.0, value=40.0, step=1.0
)
total_7 = st.number_input(
    "Current day + previous 6 days (mm)",
    min_value=0.0, value=90.0, step=1.0
)

if st.button("Estimate recorded-flood risk", type="primary"):
    inputs = pd.DataFrame([{
        "Mean_Rainfall_mm": mean_rain,
        "Max_Rainfall_mm": max_rain,
        "Rainfall_Previous_3_Days_mm": previous_3,
        "Rainfall_Previous_7_Days_mm": previous_7,
        "Rainfall_3_Day_Total_mm": total_3,
        "Rainfall_7_Day_Total_mm": total_7
    }], columns=FEATURES)

    probability = model.predict_proba(inputs)[0][1]

    st.subheader("Model output")
    st.metric(
        "Estimated recorded-event probability",
        f"{probability * 100:.2f}%"
    )
    st.progress(float(probability))

    st.caption(
        "This is the model's score for a recorded flood-event label, "
        "not a calibrated probability of urban waterlogging."
    )

    if probability >= 0.01:
        st.warning(
            "The model flags this input at the experimental 0.01 threshold."
        )
    else:
        st.info(
            "The model does not flag this input at the experimental "
            "0.01 threshold. This does not mean conditions are safe."
        )
