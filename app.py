import streamlit as st
import google.generativeai as genai

# --- 1. AI SETUP ---
# This line tells the app to look for your secret key in the Streamlit settings
try:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
except:
    st.error("API Key not found! Please add it to Streamlit Secrets.")

model = genai.GenerativeModel(
    model_name="gemini-2.5-flash",
    system_instruction=(
        "You are the IGNOU RC Noida Assistant. Be helpful and polite. "
        "Your main job is to help students find status links for RC Noida (Code 39). "
        "If a student wants to check status, ask for their Enrollment Number and Program. "
        "Always share these links when needed: "
        "- Assignments: https://isms.ignou.ac.in/changeadmdata/StatusAssignment.asp "
        "- Exam Results: https://termendresult.ignou.ac.in/ "
        "- Admission: https://isms.ignou.ac.in/changeadmdata/AdmissionStatusNew.ASP "
        "Remind students that assignments at RC Noida take 45 days to update."
    )
)

# --- 2. PAGE DESIGN ---
st.set_page_config(page_title="IGNOU Noida Assistant", page_icon="🎓")

# Sidebar with download button and info
with st.sidebar:
    st.title("📌 Student Tools")
    st.write("Regional Centre Noida")
    
    # Official Front Page Link
    front_page_url = "https://rcnoida.ignou.ac.in/Ignou-RC-Noida/userfiles/file/ASSIGNMENT%20FRONT%20PAGE.pdf"
    st.link_button("📄 Download Front Page", front_page_url)
    
    st.divider()
    st.write("📧 Email: rcnoida@ignou.ac.in")
    st.write("📍 Address: Plot 88, Knowledge Park 5, Greater Noida")

# Main Chat Interface
st.title("🤖 IGNOU RC Noida Smart Bot")
st.write("Ask me about assignment status, results, or contact details!")

# Chat History Setup
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input Logic
if prompt := st.chat_input("How can I help you?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        chat = model.start_chat(history=[
            {"role": m["role"], "parts": [m["content"]]} for m in st.session_state.messages[:-1]
        ])
        response = chat.send_message(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
