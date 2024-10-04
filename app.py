import streamlit as st
import pickle
import warnings
from sklearn.exceptions import InconsistentVersionWarning

# Configure Streamlit page
st.set_page_config(
    page_title="Diabetes Risk Predictor",
    page_icon="🏥",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
        .main {
            padding: 0rem 1rem;
        }
        .section-divider {
            margin-top: 1.5rem;
            margin-bottom: 1.5rem;
        }
        .stButton > button {
            width: 100%;
        }
        .header-container {
            background-color: #f0f2f6;
            padding: 1rem;
            border-radius: 0.5rem;
            margin-bottom: 2rem;
        }
        .section-header {
            background-color: #e6e9ef;
            padding: 0.5rem;
            border-radius: 0.3rem;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

@st.cache_resource
def load_model():
    try:
        with open("predictor.pickle", 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'predictor.pickle' is in the correct location.")
        return None

def predict(feature_list):
    model = load_model()
    if model is None:
        return None
    return model.predict([feature_list])[0]

def main():
    # Header Section
    st.markdown("""
        <div class="header-container">
            <h1 style='text-align: center;'>🏥 Diabetes Risk Assessment</h1>
            <p style='text-align: center;'>Complete all fields below for an accurate assessment of diabetes risk factors.</p>
        </div>
    """, unsafe_allow_html=True)

    # Create three main columns for the form
    left_col, middle_col, right_col = st.columns([1, 1, 1])

    # Left Column - Basic Health Metrics
    with left_col:
        st.markdown("""
            <div class="section-header">
                <h3>📊 Basic Health Metrics</h3>
            </div>
        """, unsafe_allow_html=True)
        
        bmi = st.number_input(
            "BMI (Body Mass Index)",
            min_value=18.0,
            max_value=50.0,
            value=25.0,
            step=0.1,
            help="Body Mass Index is a measure of body fat based on height and weight"
        )

        high_bp = st.selectbox(
            "High Blood Pressure",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        high_chol = st.selectbox(
            "High Cholesterol",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        chol_check = st.selectbox(
            "Regular Cholesterol Check",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        stroke = st.selectbox(
            "History of Stroke",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        heart_disease = st.selectbox(
            "Heart Disease/Attack",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

    # Middle Column - Lifestyle Factors
    with middle_col:
        st.markdown("""
            <div class="section-header">
                <h3>🎯 Lifestyle & Habits</h3>
            </div>
        """, unsafe_allow_html=True)

        phys_activity = st.selectbox(
            "Regular Physical Activity",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        fruits = st.selectbox(
            "Daily Fruit Consumption",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        veggies = st.selectbox(
            "Daily Vegetable Consumption",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        smoker = st.selectbox(
            "Smoking Status",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        alcohol = st.selectbox(
            "Heavy Alcohol Consumption",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        diff_walk = st.selectbox(
            "Difficulty Walking",
            options=[("No", 0.0), ("Yes", 1.0)],
            format_func=lambda x: x[0]
        )[1]

    # Right Column - Personal Information
    with right_col:
        st.markdown("""
            <div class="section-header">
                <h3>👤 Personal Information</h3>
            </div>
        """, unsafe_allow_html=True)

        sex = st.selectbox(
            "Sex",
            options=[("Female", 0.0), ("Male", 1.0)],
            format_func=lambda x: x[0]
        )[1]

        age = st.select_slider(
            "Age Group",
            options=list(range(1, 14)),
            format_func=lambda x: [
                "18-24", "25-29", "30-34", "35-39", "40-44", "45-49",
                "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80+"
            ][x-1]
        )

        education = st.select_slider(
            "Education Level",
            options=list(range(1, 7)),
            format_func=lambda x: [
                "Never attended/kindergarten",
                "Elementary (1-8)",
                "Some high school",
                "High school graduate",
                "Some college",
                "College graduate"
            ][x-1]
        )

        income = st.select_slider(
            "Annual Income",
            options=list(range(1, 9)),
            format_func=lambda x: [
                "<$10,000", "<$20,000", "<$25,000", "<$30,000",
                "<$35,000", "<$50,000", "<$60,000", "≥$75,000"
            ][x-1]
        )

    # Health Status Section - Full Width
    st.markdown("---")
    st.markdown("""
        <div class="section-header">
            <h3>🏥 Health Status</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        gen_health = st.select_slider(
            "General Health",
            options=[1.0, 2.0, 3.0, 4.0, 5.0],
            value=3.0,
            format_func=lambda x: ["Excellent", "Very Good", "Good", "Fair", "Poor"][int(x-1)]
        )
    
    with col2:
        mental_health = st.slider(
            "Days of Poor Mental Health (Last 30 days)",
            min_value=0,
            max_value=30,
            value=0
        )
    
    with col3:
        phys_health = st.slider(
            "Days of Poor Physical Health (Last 30 days)",
            min_value=0,
            max_value=30,
            value=0
        )

    # Prediction Button and Results
    st.markdown("---")
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        if st.button("Generate Risk Assessment", type="primary"):
            feature_list = [
                high_bp, high_chol, chol_check, bmi, smoker, stroke,
                heart_disease, phys_activity, fruits, veggies, alcohol,
                gen_health, mental_health, phys_health, diff_walk, sex,
                age, education, income
            ]
            
            with st.spinner("Analyzing your data..."):
                prediction_result = predict(feature_list)
                
                if prediction_result is not None:
                    st.markdown("### Assessment Results")
                    if prediction_result == 1:
                        st.error("⚠️ **Higher Risk Detected**\n\n"
                                "Based on the provided information, you may have an elevated risk "
                                "for developing diabetes.")
                    else:
                        st.success("✅ **Lower Risk Detected**\n\n"
                                 "Based on the provided information, you appear to have a lower "
                                 "risk for developing diabetes.")
                    
                    st.info("""
                        **Important Notice**: This assessment is for informational purposes only. 
                        Please consult with a healthcare professional for proper medical advice 
                        and diagnosis.
                    """)

    # Footer
    st.markdown("---")
    st.markdown("""
        <div style='text-align: center; color: #666;'>
            <small>
                This tool is for educational purposes only. Always consult with healthcare 
                professionals for medical advice.
            </small>
        </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()