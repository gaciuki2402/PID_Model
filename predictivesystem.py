# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import joblib
import pandas as pd

# Load the model from disk
model_path = 'PID_Model.joblib'
loaded_model = joblib.load(model_path)

# Define the prediction function
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

# Use the function to make a prediction
new_prediction = predict_pid(28, 'No', 'Yes', 'No', 'Normal (US)', 'None', 'Regular', 'No', 'No', 'Normal', 'Normal', 'Normal')

if new_prediction == 0:
    print("PID Negative")
else:
    print("PID Positive")
