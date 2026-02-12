import streamlit as st
import requests

st.title("Qwen3 Chatbot (FastAPI + Streamlit)")

user_input = st.text_input("Ask your question")

if st.button("Submit"):
    if user_input:
        response = requests.post(
            "http://127.0.0.1:8000/ask",
            json={"question": user_input}
        )

        if response.status_code == 200:
            answer = response.json()["response"]
            st.write("### Response:")
            st.write(answer)
        else:
            st.error("Error connecting to backend")
