import joblib
import streamlit as st
import pandas as pd
import sqlite3
import base64
import os

# Load the model from disk
model_path = 'PID_Model.joblib'
if os.path.exists(model_path):
    loaded_model = joblib.load(model_path)
else:
    st.error(f"Model file not found at: {model_path}")

# Connect to SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('pid_predictions.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS predictions
             (age INTEGER, stds_uti_history TEXT, iud_use TEXT, past_pelvic_pain TEXT, imaging_results TEXT, 
             abnormal_discharge TEXT, irregular_periods TEXT, dyspareunia TEXT, dysuria TEXT, wbc_count TEXT, 
             esr TEXT, crp_level TEXT, prediction INTEGER)''')

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

    if st.button("Get Prediction"):
        new_prediction = predict_pid(age, stds_uti_history, iud_use, past_pelvic_pain, imaging_results, abnormal_discharge, irregular_periods, dyspareunia, dysuria, wbc_count, esr, crp_level)

        # Insert the input data and prediction result into the database
        c.execute("INSERT INTO predictions (age, stds_uti_history, iud_use, past_pelvic_pain, imaging_results, abnormal_discharge, irregular_periods, dyspareunia, dysuria, wbc_count, esr, crp_level, prediction) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                  (age, stds_uti_history, iud_use, past_pelvic_pain, imaging_results, abnormal_discharge, irregular_periods, dyspareunia, dysuria, wbc_count, esr, crp_level, new_prediction))
        conn.commit()

        if new_prediction == 0:
            st.success("PID Negative")
        else:
            st.error("PID Positive")

# Function to render the database page
def render_database_page():
    st.title("Database Page")
    
    # Retrieve data from the database
    c.execute("SELECT * FROM predictions")
    data = c.fetchall()
    
    if data:
        df = pd.DataFrame(data, columns=['Age', 'STDs/UTI History', 'IUD Use', 'Past Pelvic Pain', 'Imaging Results', 
                                         'Abnormal Discharge', 'Irregular Periods', 'Dyspareunia', 'Dysuria', 
                                         'WBC Count', 'ESR', 'CRP Level', 'Prediction'])
        st.dataframe(df)
    else:
        st.write("No data available.")

# Function to render the about page
def render_about_page():
    st.title("")
    st.markdown("""
        ## About This Application

        This web application is designed to predict the likelihood of Pelvic Inflammatory Disease (PID) based on various medical factors. It is developed to assist healthcare professionals in diagnosing PID and to provide valuable insights for patients.

        ### Purpose
        The main purpose of this application is to leverage machine learning techniques to analyze medical data and provide predictions that can help in the early detection and management of PID. By providing an easy-to-use interface, we aim to facilitate the diagnosis process and improve patient outcomes.

        ### The Team
        Our team comprises data scientists, healthcare professionals, and software developers who are passionate about applying technology to solve healthcare challenges. With diverse expertise in their respective fields, the team collaborates to ensure that the application is accurate, reliable, and user-friendly.

        ### Future Enhancements
        We are committed to continuously improving the application. Future enhancements may include:
        - Integration with electronic health records (EHR) systems for seamless data input.
        - Advanced analytics and visualization tools for better understanding of data trends.
        - Mobile application development for on-the-go access.

        For any inquiries or feedback, please visit the Contact page.
    """, unsafe_allow_html=True)

# Function to render the contact page
def render_contact_page():
    st.title("")
    st.markdown("""
        ## Contact Us

        We value your feedback and inquiries. Please use the information below to get in touch with our team:

        **Email:** gaciukigrace@gmail.com
        
        **Phone:** +254794376828
        
        **Address:**
        PID Predictor Team
        Health Tech 
        City, State, ZIP Code

        Our support team is available Monday to Friday, 9 AM to 5 PM (EST). We aim to respond to all inquiries within 24 hours.
    """, unsafe_allow_html=True)

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
                color: grey
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    else:
        st.error("Background image not found")

    # Create a sidebar for navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ["Home", "Prediction", "Database", "About", "Contact"])

    # Render the selected page based on the sidebar selection
    if page == "Home":
        st.title("Welcome to the PID Prediction System")
        st.markdown("""
        This web application allows you to predict the likelihood of Pelvic Inflammatory Disease (PID) based on various medical factors. 
        
        ## What is PID?
        PID is an infection of the female reproductive organs. It usually occurs when sexually transmitted bacteria spread from your vagina to your uterus, fallopian tubes, or ovaries.

        
        ## About This Application
        This application leverages machine learning techniques to provide predictions that assist healthcare professionals in diagnosing PID. Navigate to the Prediction page from the sidebar to input your medical information and get a prediction on whether you may have PID.
        """, unsafe_allow_html=True)
    elif page == "Prediction":
        render_prediction_page()
    elif page == "Database":
        render_database_page()
    elif page == "About":
        render_about_page()
    elif page == "Contact":
        render_contact_page()

# Run the Streamlit app
if __name__ == "__main__":
    main()
