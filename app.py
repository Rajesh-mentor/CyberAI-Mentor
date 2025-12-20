import streamlit as st
from groq import Groq

# API Key configuration
# Ensure the key is correct (gsk_...)
client = Groq(api_key="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")

st.title("CyberAI Mentor 🛡️")

# Camera Access
st.subheader("Scan for Threats")
picture = st.camera_input("Take a photo of a suspicious link or QR code")

if picture:
    st.image(picture, caption="Captured Image")
    st.info("Image received! Analyzing text...")

# Chat Section
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask your cybersecurity doubts here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)

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
        st.error(f"Error: {e}")

