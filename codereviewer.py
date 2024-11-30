import streamlit as st
import google.generativeai as genai
import time
import random

# Load the API key from the specified path
key_path = "C:\\Users\\saisa\\Documents\\gemini\\google api keys\\gemini-demo api key.txt"
with open(key_path, "r") as f:
    api_key = f.read().strip()
    genai.configure(api_key=api_key)

# Initialize the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Define a system prompt for the AI model, with emphasis on giving corrected code
prompt = """
You are a Python code expert reviewing the provided code. Analyze the code for:
1. Bugs or errors, providing a clear explanation.
2. Code optimizations or improvements, suggesting how to enhance it.
3. Provide additional coding advice on best practices or clarity.
4. **Provide the corrected Python code**. If there are any issues, please fix the code and output the corrected version wrapped in triple backticks (```python).
"""

# Function to get the response from Google Gemini AI
def review_code(code_input):
    try:
        response = model.generate_content([prompt, code_input])
        return response.text
    except Exception as error:
        return f"Error: {error}"

# Streamlit UI Configuration
st.set_page_config(page_title="CodeMaster: Python Code Reviewer 🤖", page_icon="🤖", layout="wide")

# Sidebar Configuration
st.sidebar.header("📚 Navigation")
sidebar_options = ["🏠 Home", "ℹ️ About", "🧑‍💻 Developer Info"]
selected_option = st.sidebar.radio("Select a Section", sidebar_options)

# Title and Instructions
if selected_option == "🏠 Home":
    st.title("🤖 CodeMaster: Your AI Python Code Reviewer")
    st.markdown("**Paste your Python code below to get detailed feedback and suggestions from our AI-powered CodeMaster!**")

    # Code Input Section
    code_input = st.text_area("📝 Your Python Code", height=300, placeholder="Enter your Python code here...")

    # Button to trigger code review
    if st.button("🔍 Review Code"):
        if code_input:
            # Display progress bar and simulate AI processing delay
            with st.spinner("Analyzing your code..."):
                time.sleep(2)

            # Get the review from Google Gemini AI
            review = review_code(code_input)

            # Split the review into sections for dynamic display
            sections = review.split('\n')
            bug_report = [line for line in sections if "bug" in line.lower()]
            improvements = [line for line in sections if "improve" in line.lower() or "suggest" in line.lower()]
            insights = [line for line in sections if "insight" in line.lower()]

            # Try to extract corrected code by looking for "corrected code" or code wrapped in backticks
            corrected_code = None
            for line in sections:
                if "corrected code" in line.lower():  # Check if there's any label for corrected code
                    corrected_code = '\n'.join(sections[sections.index(line) + 1:]).strip()
                    break
                if line.strip().startswith("```python"):  # Look for Python code blocks
                    corrected_code = '\n'.join(sections[sections.index(line) + 1:]).strip()
                    break

            # Dynamic Feedback Structure
            st.subheader("🔎 Review Feedback")

            # Only show Bug Report if there's content
            if bug_report:
                with st.expander("🐞 Bug Report", expanded=True):
                    st.markdown(f"{' '.join(bug_report)}")
            else:
                st.success("No bugs found in your code! 🎉")

            # Only show Suggested Fixes if there's content
            if improvements:
                with st.expander("💡 Suggested Fixes", expanded=True):
                    st.markdown(f"{' '.join(improvements)}")
            else:
                st.info("No suggested fixes! Your code looks great! ✅")

            # Only show Code Insights if there's content
            if insights:
                with st.expander("🔧 Code Insights", expanded=True):
                    st.markdown(f"{' '.join(insights)}")
            else:
                st.info("No additional insights for optimization. Keep up the good work! 💪")

            # Display Corrected Code (Optimized Code)
            if corrected_code:
                with st.expander("💻 Corrected Code", expanded=True):
                    st.code(corrected_code, language='python')  # Display the corrected code in proper Python format
            else:
                st.warning("No corrected code provided. Please check your input!")

            # Add a random compliment or suggestion for more engaging feedback
            compliments = [
                "🎉 Great job! You're writing clean and readable code!",
                "🚀 Your code looks solid. Just a few minor improvements!",
                "💪 Keep going! You're doing awesome!",
                "🔥 The AI loves your coding style! Keep it up!"
            ]
            st.markdown(f"#### AI says: {random.choice(compliments)}")

        else:
            st.warning("⚠️ Please enter some Python code to review.")

# About Section
elif selected_option == "ℹ️ About":
    st.markdown("## 📚 About CodeMaster")
    st.write("""
    CodeMaster is an AI-powered Python code reviewer designed to help developers analyze their Python code.
    It identifies bugs, suggests fixes, and provides valuable insights into optimization and best practices.
    """)

# Developer Info Section
elif selected_option == "🧑‍💻 Developer Info":
    st.markdown("## 👨‍💻 Developer Info")
    st.markdown("""
    **Name**: Gude Sai Sanjana  
    **Email**: [gudesaisanjana@gmail.com](mailto:gudesaisanjana@gmail.com)  
    **LinkedIn**: [Sai Sanjana Gude](https://www.linkedin.com/in/saisanjanagude/)  
    **GitHub**: [saisanjanagude](https://github.com/saisanjanagude)
    """)

# Footer Section
st.markdown("---")
st.markdown(
    """
    <div style="background-color: #2c3e50; color: white; text-align: center; padding: 10px 0;">
        <p><strong>CodeMaster</strong> | Developed by Gude Sai Sanjana | Powered by Google Gemini AI & Streamlit</p>
        <p style="font-size: 12px;">*Disclaimer: This app is for educational purposes. The code provided is analyzed by an AI model and might not always be 100% accurate. Please verify fixes before deploying in production.*</p>
    </div>
    """, unsafe_allow_html=True)
