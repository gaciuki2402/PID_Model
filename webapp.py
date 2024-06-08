# -*- coding: utf-8 -*-
"""
Created on Sat Jun  8 12:14:54 2024

@author: user
"""
import joblib
import streamlit as st
import pandas as pd

# Load the model from disk
model_path = 'C:/Users/user/MachineLearning/PID_Model.joblib'
loaded_model = joblib.load(model_path)

#creating a function for prediction

def predict_pid(age, stds_uti_history, iud_use, past_pelvic_pain, imaging_results, abnormal_discharge, irregular_periods, dyspareunia, dysuria, wbc_count, esr, crp_level):
    new_data = pd.DataFrame({
        'Age': [age],
        'STDs/UTI History': [stds_uti_history],
        'IUD Use': [iud_use],
        'Past Pelvic Pain': [past_pelvic_pain],
        'Imaging Results': [imaging_results],
        'Abnormal Discharge': [abnormal_discharge],
        'Irregular Periods': [irregular_periods],
        'Dyspareunia': [dyspareunia],
        'Dysuria': [dysuria],
        'WBC Count': [wbc_count],
        'ESR': [esr],
        'CRP Level': [crp_level]
    })
    
    prediction = loaded_model.predict(new_data)
    return prediction[0]

#giving a tile
st.title('PID Web Application')

#adding custom CSS for background color
st.markdown(
    """
    <style>
    .main {
        background-color: #FFC0CB;
        color: black;
    }
    </style>
    """,
    unsafe_allow_html=True
)

#getting the input data from the user
age = st.number_input("Age", min_value=0, max_value=100, value=28)
stds_uti_history = st.selectbox("STDs/UTI History", ["No", "Yes"])
iud_use = st.selectbox("IUD Use", ["No", "Yes"])
past_pelvic_pain = st.selectbox("Past Pelvic Pain", ["No", "Yes"])
imaging_results = st.selectbox("Imaging Results", ["Normal (US)", "Abnormal (US)", "Normal (CT)", "Abnormal (CT)"])
abnormal_discharge = st.selectbox("Abnormal Discharge", ["None", "Mild", "Moderate", "Severe"])
irregular_periods = st.selectbox("Irregular Periods", ["Regular", "Irregular"])
dyspareunia = st.selectbox("Dyspareunia", ["No", "Yes"])
dysuria = st.selectbox("Dysuria", ["No", "Yes"])
wbc_count = st.selectbox("WBC Count", ["Normal", "Elevated", "Low"])
esr = st.selectbox("ESR", ["Normal", "Elevated", "Low"])
crp_level = st.selectbox("CRP Level", ["Normal", "Elevated", "Low"])

if st.button("Predict"):
    new_prediction = predict_pid(age, stds_uti_history, iud_use, past_pelvic_pain, imaging_results, abnormal_discharge, irregular_periods, dyspareunia, dysuria, wbc_count, esr, crp_level)

    if new_prediction == 0:
        st.success("PID Negative")
    else:
        st.error("PID Positive")























 