import streamlit as st
import requests

# --- Configuration ---
# Use Streamlit Secrets! Store your webhook URL and API key (if you set one).
# In .streamlit/secrets.toml:
# N8N_WEBHOOK_URL = "https://your.n8n.instance/webhook/production/your-id"
# N8N_API_KEY = "your-secret-api-key" 
#
# If you didn't set an API key, just comment out the "headers" line below.

try:
    N8N_URL = "https://n8n.quaianalytics.com/webhook/319bf7e6-a19b-496b-912a-b3b75fcbb53a"
    #API_KEY = st.secrets["N8N_API_KEY"]
    #HEADERS = {"x-api-key": API_KEY}
except (KeyError, FileNotFoundError):
    st.error("Please configure N8N_WEBHOOK_URL and N8N_API_KEY in .streamlit/secrets.toml")
    st.stop()


st.title("Image Analyzer")
st.header("Upload an Image for Analysis")

# 1. Create the file uploader
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Display the uploaded image
    st.image(uploaded_file, caption="Image to Analyze")

    if st.button("Analyze Image"):
        with st.spinner("Sending image to workflow for analysis..."):
            
            # 2. Prepare the file for sending
            #    This is the key part: 'files' argument in requests.post
            files_payload = {
                'file': (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
            }

            try:
                # 3. Send the POST request
                response = requests.post(N8N_URL, files=files_payload)#, headers=HEADERS)

                # 4. Check the response
                if response.status_code == 200:
                    st.success("🎉 Success! Your image was sent for analysis.")
                    st.info("The workflow will now run in the background.")
                else:
                    st.error(f"Error from n8n: {response.status_code}")
                    st.text(response.text)
            
            except requests.exceptions.RequestException as e:
                st.error(f"Failed to connect to n8n: {e}")