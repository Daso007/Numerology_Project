import streamlit as st
import google.generativeai as genai
import re

# We import all our powerful functions from our existing calculator file.
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

# Set the title and a simple instruction for the user.
st.title("AI-Powered Numerology Analysis")
st.write("Enter a date of birth in DD/MM/YYYY format to receive a personalized analysis based on the teachings of David A. Phillips.")

# Create a text input box for the user to enter a birth date.
# We'll use "31/03/1950" as the default example.
birth_date_input = st.text_input("Enter Date of Birth (DD/MM/YYYY)", "31/03/1950")

# --- CORE LOGIC (This is adapted from our main.py file) ---

# We use st.cache_data to save results. This way, if the same date is entered again,
# the app doesn't have to re-calculate everything and call the AI, saving you time and resources.
@st.cache_data
def generate_full_report(birth_date_str):
    
    # Configure the Google AI connection
    try:
        genai.configure(api_key=GOOGLE_API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
    except Exception as e:
        st.error(f"Error connecting to Google AI. Please check the API key. Details: {e}")
        return None, None # Return nothing if connection fails

    # --- Step 1: Calculate Numerology Data ---
    life_path = calculate_life_path(birth_date_str)
    arrows = identify_arrows(birth_date_str)
    digits_in_chart = get_birth_chart_digits(birth_date_str)
    present_numbers = sorted(list(set(digits_in_chart)))
    all_numbers = set(range(1, 10))
    missing_numbers = sorted(list(all_numbers - set(present_numbers)))
    lo_shu_grid_text = generate_lo_shu_grid(birth_date_str)

    # --- Step 2: Read Knowledge Base (Simplified) ---
    try:
        with open("Cleaned-Knowledge.txt", "r", encoding="utf-8") as f:
            full_knowledge_text = f.read()
    except FileNotFoundError:
        st.error("Crucial file 'Cleaned-Knowledge.txt' not found. Make sure it's in the project folder.")
        return None, None
        
    # --- Step 3: Build the Master Prompt ---
    prompt = f"""
    You are a master numerologist, David Phillips. Based ONLY on the provided context from your book, generate a detailed, multi-part numerology report for the client.
    Your tone is insightful, comprehensive, and encouraging.

    CLIENT DETAILS:
    - Birth Date: {birth_date_str}
    - Life Path Number: {life_path}
    - Numbers Present: {present_numbers}
    - Numbers Missing: {missing_numbers}
    - Arrows: {', '.join(arrows) if arrows else 'None'}
    
    CONTEXT FROM YOUR BOOK:
    {full_knowledge_text}
    
    YOUR TASK:
    Generate a report with these exact sections:
    1. **Introduction & Life Path:** Greet the user and explain their Life Path number.
    2. **Your Lo Shu Grid Analysis (The Numbers in Your Chart):** Analyze the personality based on the numbers present in the chart.
    3. **Your Lessons and Opportunities (Missing Numbers):** Discuss the missing numbers as areas for growth.
    4. **Your Unique Strengths (Arrows of Individuality):** Analyze the meaning of their Arrows.
    5. **Career and Life Path Guidance:** Provide specific career and life advice based on all the combined traits.
    6. **Summary:** Conclude with encouraging advice.
    """
    
    # --- Step 4: Generate the AI Report ---
    response = model.generate_content(prompt)
    return lo_shu_grid_text, response.text


# Create a button. The code inside this 'if' statement will only run when the button is clicked.
if st.button("Generate My Numerology Report"):

    # First, validate the input to make sure it's a valid date format.
    if re.match(r"^\d{2}/\d{2}/\d{4}$", birth_date_input):
        
        # Show a "spinner" message while the AI is thinking.
        with st.spinner("Calculating your numbers and consulting the cosmos..."):
            grid, report = generate_full_report(birth_date_input)
        
        # Once done, display the results!
        if grid and report:
            st.subheader("Your Lo Shu Grid")
            st.text(grid) # The st.text() command is perfect for showing pre-formatted text like our grid.
            st.subheader("Your Personalized Analysis")
            st.write(report) # The st.write() command formats the AI's text nicely.
            st.success("Report generated successfully!")
            
    else:
        # Show an error message if the date format is wrong.
        st.error("Invalid date format. Please use DD/MM/YYYY.")