import streamlit as st
from google.cloud import storage
import os

# # Set GCP credentials
# # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "path/to/your-key.json"

# # Initialize GCS client
# client = storage.Client()
# bucket = client.bucket("your-bucket-name")

# Streamlit UI
st.title("Chat & File Upload to GCS")

# Chat Section
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

user_input = st.text_input("You:", "")
if st.button("Send") and user_input:
    st.session_state.chat_history.append(("You", user_input))
    # Basic echo bot logic
    st.session_state.chat_history.append(("Bot", "File upload or GCS info coming soon!"))

for speaker, message in st.session_state.chat_history:
    st.write(f"**{speaker}:** {message}")

# File Upload Section
uploaded_file = st.file_uploader("Upload a file to GCS")
# if uploaded_file is not None:
    # blob = bucket.blob(f"user_uploads/{uploaded_file.name}")
    # blob.upload_from_file(uploaded_file)
    # st.success(f"Uploaded `{uploaded_file.name}` to GCS bucket `{bucket.name}`.")
