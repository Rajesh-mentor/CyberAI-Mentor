import streamlit as st
from groq import Groq

# API Key configuration
# Enter your actual Groq API Key (gsk_...) below
client = Groq(api_key="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")

st.title("CyberAI Mentor 🛡️")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history from the session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Handling user input
if prompt := st.chat_input("Ask your cybersecurity doubts here..."):
    # Adding user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    try:
        with st.chat_message("assistant"):
            # Using the latest model: llama-3.1-8b-instant
            chat_completion = client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            reply = chat_completion.choices[0].message.content
            st.markdown(reply)
            # Adding assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": reply})
    except Exception as e:
        st.error(f"Error: {e}")
