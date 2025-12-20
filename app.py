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

# Image Analysis Logic
if picture:
    # Convert image to base64
    bytes_data = picture.getvalue()
    base64_image = base64.b64encode(bytes_data).decode('utf-8')
    
    st.info("Analyzing image for security threats...")
    
    try:
        # Using Llama 3.2 Vision model to analyze image
        chat_completion = client.chat.completions.create(
            model="llama-3.2-11b-vision-preview",
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


