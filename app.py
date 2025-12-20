import streamlit as st
from groq import Groq
import base64

# API Key configuration
client = Groq(api_key="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")

st.title("CyberAI Mentor 🛡️")

# Sidebar for Camera
with st.sidebar:
    st.header("Scan Image")
    picture = st.camera_input("Take a photo of a suspicious link/text")

# Chat History Section
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Image Analysis Logic using llama-3.2-11b-vision-instant
if picture:
    bytes_data = picture.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    st.info("Analyzing image for security threats...")
    
    try:
        # Updated model name here
        chat_completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-instant",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": "Analyze this image for any cybersecurity threats like phishing links or suspicious messages. Explain clearly."},
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
            st.session_state.messages.append({"role": "assistant", "content": f"Image Analysis: {analysis_result}"})
    except Exception as e:
        st.error(f"Vision Error: {e}")

# Text Chat Input Section
if prompt := st.chat_input("Ask your cybersecurity doubts here..."):
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
        st.error(f"Chat Error: {e}")



