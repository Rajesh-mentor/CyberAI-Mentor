import streamlit as st
from groq import Groq

# API Key configuration
# Replace with your actual key
client = Groq(api_key="gsk_VfT2T0kk9X8BJq7AxejrWGdyb3FY4HYcbebj siyMYL2A41UJvDex")

st.title("CyberAI Mentor 🛡️")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history from session state
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask your cybersecurity doubts here..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    try:
        with st.chat_message("assistant"):
            # Prepare the message list correctly for the API
            chat_completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": m["role"], "content": m["content"]}
                    for m in st.session_state.messages
                ]
            )
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            # Add assistant response to chat history
            st.session_state.messages.append({"role": "assistant", "content": response})
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
