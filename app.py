import streamlit as st
from groq import Groq
import base64

# API Key configuration
client = Groq(api_key="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")

# Page Configuration
st.set_page_config(page_title="CyberAI Mentor", page_icon="🛡️")
st.title("CyberAI Mentor 🛡️")

# Sidebar for Camera access
with st.sidebar:
    st.header("Scan for Threats")
    picture = st.camera_input("Capture a suspicious link, message, or QR code")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Image Analysis Logic - FIXED MODEL NAME
if picture:
    bytes_data = picture.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    st.info("Analyzing image for potential security threats... Please wait.")
    
    try:
        # Using the stable vision model: llama-3.2-11b-vision-instant
        chat_completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-instant",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this image for any cybersecurity threats like phishing links, scams, or malicious content. Provide a clear warning if dangerous."},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}",
                            },
                        },
                    ],
                }
            ],
        )
        analysis_result = chat_completion.choices[0].message.content
        with st.chat_message("assistant"):
            st.markdown(analysis_result)
            st.session_state.messages.append({"role": "assistant", "content": f"Image Analysis Result: {analysis_result}"})
    except Exception as e:
        st.error(f"Vision Analysis Error: {e}")

# Main Chat Input
if prompt := st.chat_input("Ask your cybersecurity questions here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            )
            reply = chat_completion.choices[0].message.content
            st.markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Chat System Error: {e}")






