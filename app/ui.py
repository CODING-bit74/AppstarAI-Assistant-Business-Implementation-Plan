import streamlit as st
import requests
import os

# API endpoint
API_URL = os.getenv("APP_API_URL", "http://localhost:8000/chat")

st.set_page_config(page_title="AppstarAI Assistant", page_icon="🤖", layout="centered")

st.title("🤖 AppstarAI Assistant")
st.write("Chat with your AI Assistant")

# Initialize session state for welcome message
if 'welcome_shown' not in st.session_state:
    st.session_state.welcome_shown = False

# Show welcome message on first load
if not st.session_state.welcome_shown:
    try:
        # Get welcome message
        response = requests.post(
            API_URL,
            json={"user": "guest", "message": "welcome"},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            st.markdown(f"**Assistant:** {data.get('reply')}")
            st.session_state.welcome_shown = True
    except Exception as e:
        st.error(f"Failed to load welcome message: {e}")

# Quick action buttons
col1, col2, col3, col4 = st.columns(4)
with col1:
    if st.button("📋 Menu"):
        st.session_state.quick_message = "menu"
with col2:
    if st.button("💰 Pricing"):
        st.session_state.quick_message = "pricing"
with col3:
    if st.button("📞 Contact"):
        st.session_state.quick_message = "contact"
with col4:
    if st.button("❓ Help"):
        st.session_state.quick_message = "help"

# Handle quick button messages
if 'quick_message' in st.session_state and st.session_state.quick_message:
    user_message = st.session_state.quick_message
    st.session_state.quick_message = ""
    # Process the message immediately
    try:
        response = requests.post(
            API_URL,
            json={"user": "AKM", "message": user_message},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            st.markdown(f"**You:** {user_message}")
            st.markdown(f"**Assistant:** {data.get('reply')}")
            st.caption(f"Matched: {data.get('matched')} | Source: {data.get('source')}")
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")

# user input
user_message = st.text_input("Your message:", placeholder="Type something... (or use quick buttons above)")

if st.button("Send") and user_message:
    try:
        response = requests.post(
            API_URL,
            json={"user": "AKM", "message": user_message},
            timeout=10
        )
        if response.status_code == 200:
            data = response.json()
            st.markdown(f"**Assistant:** {data.get('reply')}")
            st.caption(f"Matched: {data.get('matched')} | Source: {data.get('source')}")
        else:
            st.error(f"Error: {response.status_code}")
    except Exception as e:
        st.error(f"Request failed: {e}")

