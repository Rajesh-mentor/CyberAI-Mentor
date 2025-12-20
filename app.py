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

# Image Analysis Logic
if picture:
    bytes_data = picture.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    st.info("Analyzing image for potential security threats... Please wait.")
    
    try:
        # Switching back to preview model which often has wider access
        chat_completion = client.chat.completions.create(
            model="llama-3.1-11b-vision-instruct",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this image for any cybersecurity threats like phishing links or scams. Explain clearly in English."},
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
            st.session_state.messages.append({"role": "assistant", "content": f"Analysis: {analysis_result}"})
    except Exception as e:
        # Showing the exact error to help identify the available model
        st.error(f"Vision System Error: {str(e)}")

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
        st.error(f"Chat System Error: {str(e)}")








