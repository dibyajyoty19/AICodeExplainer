import sys
import os
import streamlit as st
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from models.code_explainer import explain_code
from models.bug_detector.python_detector import detect_bugs as detect_python_bugs
from models.bug_detector.java_detector import detect_bugs as detect_java_bugs
st.set_page_config(page_title="AI Code Explainer & Bug Finder", layout="wide")
st.title("🧠 AI Code Explainer & Bug Finder")

# Sidebar settings
st.sidebar.title("Settings")
language = st.sidebar.selectbox("Language", ["Python", "Java"])
mode = st.sidebar.radio("Mode", ["Explain Code", "Detect Bugs", "Analyze Structure"])

# Upload or paste section
input_method = st.radio("Input Method", ["Upload File", "Paste Code"])
code = ""

if input_method == "Upload File":
    uploaded_file = st.file_uploader("Upload your code", type=["py", "java"])
    if uploaded_file:
        code = uploaded_file.read().decode("utf-8")
elif input_method == "Paste Code":
    code = st.text_area("Paste your code here")

# Display uploaded/pasted code
if code.strip():
    st.subheader("📄 Input Code")
    st.code(code, language.lower())

result = ""

# Run the selected operation
if st.button("Run"):
    if not code.strip():
        st.warning("Please provide code to analyze.")
    else:
        try:
            if mode == "Explain Code":
                result = explain_code(code, language)

            elif mode == "Detect Bugs":
                if language == "Python":
                    result = detect_python_bugs(code)
                else:
                    result = detect_java_bugs(code)

            elif mode == "Analyze Structure":
                if language == "Python":
                    info = extract_python_info(code)
                    result = summarize_python_structure(info)
                else:
                    info = extract_java_info(code)
                    result = summarize_java_structure(info)

        except Exception as e:
            result = f"❌ Error: {e}"

st.subheader("🔍 Output")
st.text_area("Result", value=result, height=300)
