# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import joblib

# ------------------- Load Model -------------------
model = joblib.load("electric_range_model.pkl")

# ------------------- Load Cleaned Dataset -------------------
df = pd.read_csv("Cleaned data.csv")

# Extract unique values for dropdowns
make_options = sorted(df["Make"].dropna().unique())
model_options = sorted(df["Model"].dropna().unique())
ev_type_options = sorted(df["EV_Type"].dropna().unique())
cafv_options = sorted(df["CAFV_Eligibility"].dropna().unique())
utility_options = sorted(df["Electric_Utility"].dropna().unique())

# ------------------- Page Config -------------------
st.set_page_config(page_title="CyberEV Range Predictor", layout="wide")

# ------------------- CUSTOM CYBERPUNK CSS -------------------
cyberpunk_css = """
<style>
body {
    background-color: #0a0f1f;
    color: #c3f8ff;
}

.sidebar .sidebar-content {
    background: linear-gradient(180deg, #0a0f1f 0%, #06101f 100%);
}

h1 {
    color: #00eaff;
    text-shadow: 0 0 20px #00eaff;
    text-align: center;
}

label {
    color: #9be4ff !important;
}

.css-1cpxqw2, .css-znku1x, .css-145kmo2 {
    color: #c3f8ff !important;
}

.stButton>button {
    background: linear-gradient(90deg, #003cff, #00eaff);
    color: white;
    border-radius: 10px;
    padding: 12px 25px;
    border: none;
    box-shadow: 0 0 15px #0066ff;
    transition: 0.3s;
}

.stButton>button:hover {
    box-shadow: 0 0 25px #00eaff;
    transform: scale(1.05);
}

.result-box {
    background: rgba(0, 255, 255, 0.06);
    padding: 25px;
    border-radius: 15px;
    border: 1px solid #00eaff33;
    text-align: center;
    box-shadow: 0 0 25px #00eaff55;
}
</style>
"""

st.markdown(cyberpunk_css, unsafe_allow_html=True)

# ------------------- TITLE -------------------
st.markdown("<h1>⚡ CYBER EV RANGE PREDICTOR ⚡</h1>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# ------------------- SIDEBAR INPUT FORM -------------------
st.sidebar.header("🔧 Input Vehicle Features")

Make = st.sidebar.selectbox("Make", make_options)
Model = st.sidebar.selectbox("Model", model_options)
EV_Type = st.sidebar.selectbox("EV Type", ev_type_options)
CAFV_Eligibility = st.sidebar.selectbox("CAFV Eligibility", cafv_options)

Vehicle_Age = st.sidebar.number_input(
    "Vehicle Age (years)", min_value=0, max_value=30, value=3
)

Electric_Utility = st.sidebar.selectbox("Electric Utility Provider", utility_options)

predict_btn = st.sidebar.button("🔮 Predict Electric Range")

# ------------------- MAIN AREA -------------------
if predict_btn:
    input_df = pd.DataFrame({
        "Make": [Make],
        "Model": [Model],
        "EV_Type": [EV_Type],
        "CAFV_Eligibility": [CAFV_Eligibility],
        "Vehicle_Age": [Vehicle_Age],
        "Electric_Utility": [Electric_Utility]
    })

    try:
        pred = model.predict(input_df)[0]

        st.markdown(
            f"""
            <div class="result-box">
                <h2 style="color:#00eaff;">Estimated Electric Range</h2>
                <h1 style="font-size:60px; color:#00f7ff; text-shadow:0 0 30px #00f7ff;">
                    {pred:.2f} miles
                </h1>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Prediction Error: {e}")
