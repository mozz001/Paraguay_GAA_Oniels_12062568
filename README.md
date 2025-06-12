# Paraguay_GAA_Oniels_12062568
This is a platform for players to arrange their O'Niel Jerseys
# Instructions for Google Drive setup
with st.expander("🔧 Google Drive Setup Instructions"):
    st.markdown("""
    ### Setting up Google Drive Integration:
    
    1. **Create a Google Cloud Project:**
       - Go to [Google Cloud Console](https://console.cloud.google.com/)
       - Create a new project or select existing one
    
    2. **Enable Google Drive API:**
       - Go to APIs & Services > Library
       - Search for "Google Drive API" and enable it
    
    3. **Create Service Account:**
       - Go to APIs & Services > Credentials
       - Click "Create Credentials" > "Service Account"
       - Download the JSON key file
    
    4. **Share Google Drive Folder:**
       - Create a folder in Google Drive
       - Share it with the service account email (found in JSON file)
       - Copy the folder ID from the URL (optional)
    
    5. **Add to Streamlit Secrets:**
       - Add the JSON content to `.streamlit/secrets.toml`:
       ```toml
       [google_service_account]
       type = "service_account"
       project_id = "your-project-id"
       private_key_id = "your-private-key-id"
       private_key = "-----BEGIN PRIVATE KEY-----\\nYOUR-PRIVATE-KEY\\n-----END PRIVATE KEY-----\\n"
       client_email = "your-service-account@your-project.iam.gserviceaccount.com"
       client_id = "your-client-id"
       auth_uri = "https://accounts.google.com/o/oauth2/auth"
       token_uri = "https://oauth2.googleapis.com/token"
       auth_provider_x509_cert_url = "https://www.googleapis.com/oauth2/v1/certs"
       client_x509_cert_url = "your-cert-url"
       ```
    
    ### Required Dependencies:
    Add to your `requirements.txt`:
    ```
    google-auth
    google-auth-oauthlib
    google-auth-httplib2
    google-api-python-client
    ```
    """)
