import joblib
import streamlit as st
import pandas as pd
import base64
import os

# Load the model from disk
model_path = 'PID_Model.joblib'
if os.path.exists(model_path):
    loaded_model = joblib.load(model_path)
else:
    st.error(f"Model file not found at: {model_path}")

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

# Define the function to render the prediction page
def render_prediction_page():
    st.title("Prediction Page")

    # Getting the input data from the user
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

    if st.button("Diagnose"):
        new_prediction = predict_pid(age, stds_uti_history, iud_use, past_pelvic_pain, imaging_results, abnormal_discharge, irregular_periods, dyspareunia, dysuria, wbc_count, esr, crp_level)

        if new_prediction == 0:
            st.success("PID Negative")
        else:
            st.error("PID Positive")

# Define the main function to render the Streamlit app
def main():
    # Add background image
    bg_image_path = 'img.png'
    if os.path.exists(bg_image_path):
        with open(bg_image_path, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()
        
        # Adding custom CSS for background image
        st.markdown(
            f"""
            <style>
            .stApp {{
                background-image: url("data:image/png;base64,{encoded_string}");
                background-size: cover;
                background-position: center;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Background image not found")

    # Create a sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Prediction"])

    # Render the selected page based on the sidebar selection
    if page == "Home":
        st.title("")
        st.markdown("""
    ## <span style="color:#9370DB;"><b>Welcome to the PID Prediction System</b></span>
    
    This web application allows you to predict the likelihood of Pelvic Inflammatory Disease (PID) based on various medical factors. 
    
    ### <span style="color:#9370DB;"><b>What is PID?</b></span>

    Pelvic Inflammatory Disease (PID) is an infection of the female reproductive organs, including the uterus, fallopian tubes, and ovaries. It typically occurs when sexually transmitted bacteria, such as chlamydia or gonorrhea, spread from the vagina to these organs. 
    
    PID can cause various symptoms, including pelvic pain, abnormal vaginal discharge, painful urination, irregular menstrual bleeding, and fever. If left untreated, PID can lead to serious complications such as chronic pelvic pain, ectopic pregnancy, infertility, and an increased risk of pelvic adhesions.

    Prompt diagnosis and treatment of PID are essential to prevent long-term complications. Treatment usually involves antibiotics to eradicate the infection and may require hospitalization in severe cases. Additionally, individuals diagnosed with PID should receive counseling and testing for sexually transmitted infections (STIs) to prevent future episodes.    
    ### <span style="color:#9370DB;"><b>How to Use</b></span>
    
    Navigate to the Prediction page from the sidebar to input your medical information and get a prediction on whether you may have PID.
    
    """, unsafe_allow_html=True)

    elif page == "Prediction":
        render_prediction_page()

# Run the Streamlit app
if __name__ == "__main__":
    main()
