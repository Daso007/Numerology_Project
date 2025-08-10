import streamlit as st
import google.generativeai as genai
import re

# Import our powerful functions from our existing calculator file.
from numerology_calculator import (
    calculate_life_path,
    identify_arrows,
    get_birth_chart_digits,
    generate_lo_shu_grid
)

# --- CONFIGURATION ---
# Paste your Google API Key here.
GOOGLE_API_KEY = "AIzaSyDEhhTw5iPc6RmiDji5aHvCzfe3P4saSBg"

# --- WEB APP INTERFACE ---

st.set_page_config(layout="wide") # Use a wider layout for more space
st.title("AI-Powered Numerology and Career Guidance")
st.write("Enter a date of birth in DD/MM/YYYY format to receive a personalized analysis based on the teachings of David A. Phillips.")

# Use columns for a cleaner layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("Your Personal Details")
    birth_date_input = st.text_input("Enter Date of Birth (DD/MM/YYYY)", "23/08/1994")
    
    # --- NEW: USER TYPE SELECTOR ---
    user_type = st.radio(
        "Select your current status:",
        ('Professional (with work history)', 'Student (exploring careers)'),
        key="user_type"
    )

with col2:
    st.subheader("Your Career Information")
    
    # --- NEW: CONDITIONAL TEXT AREA ---
    career_info = ""
    if user_type == 'Professional (with work history)':
        career_info = st.text_area(
            "Paste your resume, career history, or describe your work experience here:",
            height=200,
            placeholder="e.g., 'Worked as a software developer for 5 years at a tech company, focusing on creative problem-solving...'"
        )
    else:
        career_info = st.text_area(
            "List your favorite subjects, interests, or potential career ideas here:",
            height=200,
            placeholder="e.g., 'I enjoy biology and art, and I am considering a career in medical illustration or scientific research...'"
        )


# --- CORE LOGIC (This is adapted from our main.py file) ---
@st.cache_data
def generate_full_report(birth_date_str, user_type, career_info):
    
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        return None, None # Return nothing if connection fails

    life_path = calculate_life_path(birth_date_str)
    arrows = identify_arrows(birth_date_str)
    digits_in_chart = get_birth_chart_digits(birth_date_str)
    lo_shu_grid_text = generate_lo_shu_grid(birth_date_str)
    
    try:
        with open("Cleaned-Knowledge.txt", "r", encoding="utf-8") as f:
            full_knowledge_text = f.read()
    except FileNotFoundError:
        st.error("Crucial file 'Cleaned-Knowledge.txt' not found.")
        return None, None
        
    # --- NEW: DYNAMIC PROMPT FOR CAREER GUIDANCE ---
    career_guidance_prompt = ""
    if career_info: # Only add this section if the user provided career info
        if user_type == 'Professional (with work history)':
            career_guidance_prompt = f"""
            **5. Career Path Alignment:** The client is a Professional. Analyze their provided career history below in the context of their numerology. Advise them if their path aligns with their strengths (like practicality, creativity, idealism). Suggest potential pivots or areas of growth based on their numerology.
            Client's Career History: "{career_info}"
            """
        else: # Student
            career_guidance_prompt = f"""
            **5. Study and Career Guidance:** The client is a Student. Analyze their provided interests below. Based on their numerology (Life Path, Arrows, and the balance of numbers on their chart), suggest specific fields of study and career paths that would be a good fit for their natural talents.
            Client's Interests: "{career_info}"
            """

    # --- MASTER PROMPT (Now includes the new dynamic section) ---
    prompt = f"""
    You are a master numerologist, David Phillips. Based ONLY on the provided context from your book, generate a detailed, multi-part numerology report.
    Your tone is insightful, comprehensive, and encouraging.

    CLIENT DETAILS:
    - Birth Date: {birth_date_str}
    - Life Path Number: {life_path}
    - Arrows: {', '.join(arrows) if arrows else 'None'}
    
    CONTEXT FROM YOUR BOOK:
    {full_knowledge_text}
    
    YOUR TASK:
    Generate a report with these exact sections. Write in a flowing, personalized style.

    1. **Introduction & Your Life Path Number:** Greet the user and explain their Life Path number.
    2. **Your Lo Shu Grid Analysis (The Numbers in Your Chart):** Analyze the personality based on the numbers present.
    3. **Your Core Lessons (Missing Numbers):** Discuss the missing numbers as opportunities for growth.
    4. **Your Unique Strengths (Arrows of Individuality):** Analyze the meaning of their Arrows.
    {career_guidance_prompt}
    6. **Summary & Final Advice:** Conclude with encouraging advice on how they can best use their strengths to live a fulfilling life.
    """
    
    response = model.generate_content(prompt)
    return lo_shu_grid_text, response.text

# Create a button. The code inside this 'if' statement will only run when the button is clicked.
if st.button("Generate My Numerology Report"):

    if re.match(r"^\d{2}/\d{2}/\d{4}$", birth_date_input):
        
        with st.spinner("Analyzing your cosmic blueprint... This may take a moment."):
            grid, report = generate_full_report(birth_date_input, user_type, career_info)
        
        if grid and report:
            st.subheader("Your Lo Shu Grid")
            st.text(grid) 
            st.subheader("Your Personalized Analysis")
            st.markdown(report) # Use markdown to allow for bolding and formatting from the AI
            st.success("Report generated successfully!")
            
    else:
        st.error("Invalid date format. Please use DD/MM/YYYY.")