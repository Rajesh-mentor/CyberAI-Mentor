import streamlit as st
import ollama

# 1. Page Configuration (This must be the first Streamlit command)
st.set_page_config(page_title="CyberAI Mentor", page_icon="🛡️")

# 2. Sidebar Section
with st.sidebar:
    st.title("🛡️ CyberAI Mentor")
    st.info("Hello! I am your Cyber Security Mentor. Developed by [Rajesh Chandrasekhar].")
    st.markdown("---")
    st.write("🎯 Goal: Defensive Security Learning")
    st.success("🔒 Local & Secure")

# 3. Main Interface Title
st.title("🛡️ CyberAI Private Mentor")

# 4. Defensive Cybersecurity System Prompt
system_message = {
    'role': 'system',
    'content': (
        "You are an expert Defensive Cyber Security Mentor. Your primary mission is to educate users "
        "on how to identify, mitigate, and defend against various cyber threats. "
        "When a user asks about an attack vector, follow this structure: "
        "1. Briefly explain the concept of the attack. "
        "2. Provide a detailed step-by-step defense strategy. "
        "3. Recommend specific security tools (like Wireshark, Nmap, or Firewalls). "
        "Always maintain a professional, educational, and ethical tone."
    )
}

# 5. User Input Section
user_input = st.chat_input("Ask me about cyber defense (e.g., How to stop Brute Force?)")

if user_input:
    # Display user's question
    with st.chat_message("user"):
        st.write(user_input)

    # 6. Fetch Response from Ollama
    try:
        with st.spinner("Analyzing threat and finding defense..."):
            response = ollama.chat(model='gemma:2b', messages=[
                system_message,
                {'role': 'user', 'content': user_input}
            ])

            # Display AI's defense advice
            with st.chat_message("assistant"):
                st.write(response['message']['content'])

    except Exception as e:
        st.error(f"Error: {e}. Please ensure Ollama is running and 'gemma:2b' is installed.")