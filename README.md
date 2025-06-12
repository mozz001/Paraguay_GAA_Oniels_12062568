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


    # Instructions for Google Sheets setup
with st.expander("🔧 Google Sheets Setup Instructions"):
    st.markdown("""
    ### Complete Google Sheets Setup Guide:
    
    #### Step 1: Create Google Cloud Project
    1. Go to [Google Cloud Console](https://console.cloud.google.com/)
    2. Click "Select a project" → "New Project"
    3. Enter project name (e.g., "jersey-orders") → Create
    
    #### Step 2: Enable Google Sheets API
    1. In your project, go to **APIs & Services** → **Library**
    2. Search for "Google Sheets API"
    3. Click on it and press **Enable**
    
    #### Step 3: Create Service Account
    1. Go to **APIs & Services** → **Credentials**
    2. Click **Create Credentials** → **Service Account**
    3. Enter name (e.g., "sheets-service") → Create
    4. Skip optional steps → Done
    
    #### Step 4: Generate JSON Key
    1. Click on your service account email
    2. Go to **Keys** tab → **Add Key** → **Create new key**
    3. Choose **JSON** → Create
    4. **Download and save this file securely!**
    
    #### Step 5: Create Google Sheet
    1. Go to [Google Sheets](https://sheets.google.com)
    2. Create a new spreadsheet
    3. Name it "Jersey Orders" or similar
    4. Copy the **Sheet ID** from URL:
       ```
       https://docs.google.com/spreadsheets/d/[SHEET_ID]/edit
       ```
    
    #### Step 6: Share Sheet with Service Account
    1. In your Google Sheet, click **Share**
    2. Add the service account email (from JSON file)
    3. Give it **Editor** permissions
    4. Uncheck "Notify people" → Share
    
    #### Step 7: Configure Streamlit Secrets
    Create `.streamlit/secrets.toml` with your JSON content:
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
    
    #### Step 8: Install Dependencies
    Add to your `requirements.txt`:
    ```
    google-auth
    google-auth-oauthlib
    google-auth-httplib2
    google-api-python-client
    ```
    
    #### Step 9: Test Connection
    1. Enter your Sheet ID in the sidebar
    2. Click "🔧 Setup Sheet Headers" to test
    3. Check your Google Sheet for headers
    
    ### 🎯 Pro Tips:
    - **Sheet ID Location**: It's the long string in your Google Sheets URL
    - **Service Account Email**: Found in your downloaded JSON file
    - **Permissions**: Service account needs Editor access to write data
    - **Security**: Never commit your JSON key file to version control
    - **Testing**: Use the header setup button to verify connection
    
    ### 📊 Your Sheet Structure:
    The app will create these columns automatically:
    `order_id | name | whatsapp | number | jersey1 | jersey2 | shorts1 | shorts2 | socks1 | socks2 | polo_adult | polo_kid | total_usd | confirmation | timestamp`
    """)
