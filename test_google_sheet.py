import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Define the scope
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]

# Load credentials (inline, or use a JSON file instead)
creds_dict = {
    "type": "service_account",
    "project_id": "paraguay-gaa-oniels-12062568",
    "private_key_id": "cefdea10a961bac557ece512c650f505c5ed0640",
    "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDhGO2ihN1eyHZ/\n...snip...\n-----END PRIVATE KEY-----\n".replace('\\n', '\n'),
    "client_email": "paraguay-gaa-oniels-12062568@paraguay-gaa-oniels-12062568.iam.gserviceaccount.com",
    "client_id": "103444277347677347076",
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/paraguay-gaa-oniels-12062568%40paraguay-gaa-oniels-12062568.iam.gserviceaccount.com"
}

# Authorize
creds = ServiceAccountCredentials.from_json_keyfile_dict(creds_dict, scope)
client = gspread.authorize(creds)

# Access the spreadsheet and sheet
spreadsheet = client.open_by_key("1KSJH2VPZGNZz3gMUdc-RUGqCSgYnwvKF7cYoKLuiZi0")
sheet = spreadsheet.worksheet("Sheet1")

# Append test row
sheet.append_row(["Test Name", "test@example.com"])
print("Row added successfully.")
