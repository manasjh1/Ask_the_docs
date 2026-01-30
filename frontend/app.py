import streamlit as st
import requests
import uuid
import os

API_URL = os.getenv("API_URL", "http://localhost:8000")

st.set_page_config(page_title="Ask the Docs", page_icon="📄")
st.title("Ask the Docs")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "file_ready" not in st.session_state:
    st.session_state.file_ready = False

st.caption(f"Session ID: {st.session_state.session_id}")

uploaded = st.file_uploader("Upload a document", type=["txt", "pdf"])

if uploaded:
    
    if not st.session_state.file_ready:
        files = {"file": (uploaded.name, uploaded, uploaded.type)}
        headers = {"X-Session-ID": st.session_state.session_id}
        
        with st.spinner("Indexing document... This may take a few seconds."):
            try:
                response = requests.post(
                    f"{API_URL}/documents/upload", 
                    files=files,
                    headers=headers
                )
                
                if response.status_code == 200:
                    st.session_state.file_ready = True
                    st.success("Document indexed! You can now ask questions.")
                    st.rerun()  
                else:
                    st.error(f"Failed to upload: {response.text}")
            except Exception as e:
                st.error(f"Connection failed: {e}")

if st.session_state.file_ready:
    st.divider()
    question = st.text_input("Ask a question about your document")

    if st.button("Ask"):
        if question.strip():
            payload = {"question": question}
            headers = {"X-Session-ID": st.session_state.session_id}
            
            with st.spinner(" Thinking..."):
                try:
                    res = requests.post(
                        f"{API_URL}/query",
                        json=payload,
                        headers=headers
                    )
                    
                    if res.status_code == 200:
                        st.markdown(f"**Answer:**\n{res.json()['answer']}")
                    else:
                        st.error(f"Error: {res.text}")
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter a question.")
else:
    st.info("Please upload a document to start.")