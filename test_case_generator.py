import streamlit as st
import openai
import os
from dotenv import load_dotenv  

load_dotenv()

# Set OpenAI API key from environment variable
# Fetch the OpenAI API key
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    st.error("Please set your OpenAI API key in the environment variable 'OPENAI_API_KEY'.")
st.set_page_config(page_title="Test Case Copilot",layout="wide",page_icon="🧪")
st.title("AI Copilot for Test Case Generation")
# Sidebar input
with st.sidebar:
    st.header("Input Settings")
    model_name = st.selectbox("Choose model", ["gpt-4.1-2025-04-14", "chatgpt-4o-latest", "gpt-3.5-turbo"])
    format_style = st.radio("Test Case Format", ["Manual", "Gherkin", "API-test cases"])
    temperature = st.slider("Creativity (temperature)", 0.0, 1.0, 0.3, step=0.1)

# Main input
feature_input = st.text_area(
    "Paste your feature description or user story here:",
    height=250,
    placeholder="e.g., As a user, I want to reset my password using a one-time link sent to my email."
)

if st.button("🎨 Generate Test Cases"):
    if not feature_input:
        st.warning("Please enter a feature description.")
    else:
        with st.spinner("Generating test cases using OpenAI..."):
            # Define output format instructions based on selected format
            if format_style == "API-test cases":
                output_format = (
                    "- For each test case, include:\n"
                    "  - endpoint\n"
                    "  - method\n"
                    "  - request_body\n"
                    "  - expected_response\n"
                    "- Present test cases in a Markdown table."
                )
            elif format_style == "Manual":
                output_format = (
                    "- For each test case, include:\n"
                    "  - test_case_id\n"
                    "  - pre-conditions\n"
                    "  - steps\n"
                    "  - expected_result\n"
                    "- Present test cases as a Markdown table or bullet points."
                )
            elif format_style == "Gherkin":
                output_format = (
                    "- Write each test case in Gherkin syntax (Given/When/Then).\n"
                    "- Use Markdown code blocks for formatting."
                )
            else:
                output_format = "- Present test cases in a clear, concise format using Markdown."

            prompt = f"""
            You are a QA assistant. Generate {format_style.lower()} test cases based on the following feature:
            ---
            {feature_input}
            ---
            Please ensure:
            - Coverage of all possible scenarios
            - Clear and concise steps
            - No assumptions beyond the input
            Output format:
            {output_format}
            - Avoid unnecessary complexity
            - Ensure all test cases are relevant to the feature
            """

            try:
                response = openai.chat.completions.create(
                    model=model_name,
                    messages=[
                        {"role": "user", "content": prompt}
                    ],
                    temperature=temperature
                )
                output = response.choices[0].message.content
                st.markdown("### 📝 Generated Test Cases:")
                st.markdown(output)
            except Exception as e:
                st.error(f"Error: {e}")