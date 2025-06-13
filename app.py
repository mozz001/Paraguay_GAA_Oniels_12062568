import streamlit as st
import pandas as pd
import gspread
import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build  # ✅ Add this
import json

# Google Sheets Setup
credentials = service_account.Credentials.from_service_account_info(
    st.secrets["google_service_account"],
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)

# Access the spreadsheet and sheet
service = build('sheets', 'v4', credentials=credentials)
spreadsheet = client.open_by_key("1KSJH2VPZGNZz3gMUdc-RUGqCSgYnwvKF7cYoKLuiZi0")
sheet_id = spreadsheet.worksheet("Sheet1")

st.set_page_config(page_title="O'Niels Jersey Order Form", layout="centered")


# ✅ FIXED: Move all secrets access inside functions with error handling
@st.cache_resource
def init_google_sheets():
    try:
        # Define the scope
        scope = [
            "https://www.googleapis.com/auth/spreadsheets",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # ✅ Access secrets inside function with error handling
        try:
            credentials_info = st.secrets["google_service_account"]
            sheet_id = st.secrets["sheet_id"]
        except KeyError as e:
            st.error(f"Missing secret key: {e}")
            st.error("Please check your secrets configuration in Streamlit Cloud settings")
            # Fallback to hardcoded values for testing
            st.warning("Using fallback configuration")
            sheet_id = "1KSJH2VPZGNZz3gMUdc-RUGqCSgYnwvKF7cYoKLuiZi0"
            credentials_info = {
                "type": "service_account",
                "project_id": "paraguay-gaa-oniels-12062568",
                "private_key_id": "cefdea10a961bac557ece512c650f505c5ed0640",
                "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvgIBADANBgkqhkiG9w0BAQEFAASCBKgwggSkAgEAAoIBAQDhGO2ihN1eyHZ/\nD7b9QXgmjEHDtWjOpx9UglOfmV9JPYpCzBEy6FBZct5FV+OA8h8FJHjxNhXGOiEN\n1THm7hBgDanDMgyI1CGfBva6OMnXHnKdRs5+WcZRu+vJJ5LQP0+fYTdOFLgyp4PW\n4cCFXU/ThOZa0rWk3rhi5L6bqJRoqYRR/IVedBny/5VqCeBjnGQtGYTbcecawC9w\nAOySFPArfEoUs9+FF8NIoLmZNi+WvdWZMZBg1dH72hP8VfCZhnXJ5iW0ajIqQnwG\nM39YHPgGOuLvMfqQ6y5sCvdLaHZh7yIIUYhEj4oNPxxGZEAiIKaFAOtnYIq7RYav\nPlTIE6kLAgMBAAECggEAAsrZX9PAH0XjWm4qeffO8sN4qWHdu/qMw/Kd8PPpH7J4\nvZ1kdTo2jPWE1l1hwB7AzcKHEY73NC9Sa6aCaPf5Egf5XCeJykS/agafFu5ParDB\nATx4oU6hzC/FnAg2pQi0Bykgk4JkSpSTaR4B0mW28MvMQ8IraLEunmNyDeJIfQff\nXHb2rc3ct75H368hb/sC+NIXI+O9GiQJ2UJmqbV2Z610rZglBVMFwN+6jGAD8n9W\n5cLP2o4UEd706+UWF44jj1vrMBjpz9wwVKbz0hs6MWHiU/EMyb4ocA2lpO+hXWMB\ng9D6Vgjx4USR7IGm0/2PzMcSFdsgeRGSMWxlLZlCiQKLuiZi0",
                "client_email": "paraguay-gaa-oniels-12062568@paraguay-gaa-oniels-12062568.iam.gserviceaccount.com",
                "client_id": "103444277347677347076",
                "auth_uri": "https://accounts.google.com/o/oauth2/auth",
                "token_uri": "https://oauth2.googleapis.com/token",
                "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
                "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/paraguay-gaa-oniels-12062568%40paraguay-gaa-oniels-12062568.iam.gserviceaccount.com",
                "universe_domain": "googleapis.com"
            }
        
        # Create credentials
        credentials = Credentials.from_service_account_info(
            credentials_info, 
            scopes=scope
        )
        
        # Authorize and create client
        client = gspread.authorize(credentials)
        
        # Open the sheet
        sheet = client.open_by_key(sheet_id)
        
        return sheet, sheet_id
        
    except Exception as e:
        st.error(f"Error connecting to Google Sheets: {str(e)}")
        return None, None

# Initialize Google Sheets
sheet_data = init_google_sheets()
sheet = sheet_data[0] if sheet_data else None
current_sheet_id = sheet_data[1] if sheet_data else None

# App title
st.title("Paraguay GAA Management System")

# Debug info
with st.expander("Debug Info"):
    st.write("Available secret keys:", list(st.secrets.keys()) if hasattr(st, 'secrets') else "No secrets")
    st.write("Sheet connection:", "✅ Connected" if sheet else "❌ Failed")
    st.write("Current Sheet ID:", current_sheet_id)

if sheet is None:
    st.error("Failed to connect to Google Sheets. Please check your configuration.")
    st.info("Check the Debug Info section above for more details.")
    st.stop()

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox("Choose a page", ["Dashboard", "Add Data", "View Data", "Settings"])

if page == "Dashboard":
    st.header("Dashboard")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Total Records", "0", "0")
    
    with col2:
        st.metric("This Month", "0", "0")
    
    with col3:
        st.metric("Last Updated", "Never")

elif page == "Add Data":
    st.header("Add New Data")
    
    with st.form("add_data_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("Name")
            email = st.text_input("Email")
            
        with col2:
            phone = st.text_input("Phone")
            category = st.selectbox("Category", ["Player", "Coach", "Official", "Volunteer"])
        
        notes = st.text_area("Notes")
        
        submitted = st.form_submit_button("Add Record")
        
        if submitted:
            if name and email:
                try:
                    # Get the first worksheet
                    worksheet = sheet.get_worksheet(0)
                    
                    # Prepare data
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    row_data = [timestamp, name, email, phone, category, notes]
                    
                    # Add data to sheet
                    worksheet.append_row(row_data)
                    
                    st.success("Record added successfully!")
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error adding record: {str(e)}")
            else:
                st.error("Please fill in at least Name and Email fields.")

elif page == "View Data":
    st.header("View Data")
    
    try:
        # Get the first worksheet
        worksheet = sheet.get_worksheet(0)
        
        # Get all records
        records = worksheet.get_all_records()
        
        if records:
            df = pd.DataFrame(records)
            
            # Display data
            st.dataframe(df, use_container_width=True)
            
            # Download button
            csv = df.to_csv(index=False)
            st.download_button(
                label="Download CSV",
                data=csv,
                file_name=f"paraguay_gaa_data_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
        else:
            st.info("No data available yet.")
            
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")

elif page == "Settings":
    st.header("Settings")
    
    st.subheader("Google Sheets Configuration")
    st.write(f"**Sheet ID:** {current_sheet_id}")
    
    if st.button("Test Connection"):
        if sheet:
            try:
                worksheet = sheet.get_worksheet(0)
                st.success("✅ Connection successful!")
                st.write(f"**Sheet Title:** {sheet.title}")
                st.write(f"**Worksheet Count:** {len(sheet.worksheets())}")
            except Exception as e:
                st.error(f"Connection test failed: {str(e)}")
        else:
            st.error("❌ Connection failed!")
st.title("O'Niels Jersey Order Form - June 2025")
st.markdown("""
#### 🇬🇧 English / 🇪🇸 Español
Please fill in all the fields below. Prices will be calculated in real time.
Por favor complete todos los campos a continuación. Los precios se calcularán en tiempo real.
""")

# Google Sheets Functions
def setup_sheet_headers():
    """Setup headers in Google Sheet if they don't exist"""
    try:
        headers = [
            "order_id", "name", "whatsapp", "number", "jersey1", "jersey2", 
            "shorts1", "shorts2", "socks1", "socks2", "polo_adult", "polo_kid", 
            "total_usd", "confirmation", "timestamp"
        ]
        
        # Check if headers exist
        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range="Sheet1!A1:O1"
        ).execute()
        
        values = result.get('values', [])
        
        # If no headers, add them
        if not values:
            service.spreadsheets().values().update(
                spreadsheetId=SHEET_ID,
                range="Sheet1!A1:O1",
                valueInputOption="RAW",
                body={"values": [headers]}
            ).execute()
            return True
        return False
    except Exception as e:
        st.error(f"Error setting up headers: {str(e)}")
        return False

def write_to_google_sheets(order_data):
    """Write order data to Google Sheets"""
    try:
        # Convert order data to list format
        row_data = [
            order_data["order_id"],
            order_data["name"],
            order_data["whatsapp"],
            order_data["number"],
            order_data["jersey1"],
            order_data["jersey2"],
            order_data["shorts1"],
            order_data["shorts2"],
            order_data["socks1"],
            order_data["socks2"],
            order_data["polo_adult"],
            order_data["polo_kid"],
            order_data["total_usd"],
            order_data["confirmation"],
            order_data["timestamp"]
        ]
        
        # Append to sheet
        result = service.spreadsheets().values().append(
            spreadsheetId=SHEET_ID,
            range="Sheet1!A:O",
            valueInputOption="RAW",
            insertDataOption="INSERT_ROWS",
            body={"values": [row_data]}
        ).execute()
        
        return True
    except Exception as e:
        st.error(f"Error writing to Google Sheets: {str(e)}")
        return False

def get_next_order_number():
    """Get next order number from Google Sheets"""
    try:
        # Get all order IDs from Google Sheets
        result = service.spreadsheets().values().get(
            spreadsheetId=SHEET_ID,
            range="Sheet1!A:A"
        ).execute()
        
        values = result.get('values', [])
        
        if len(values) <= 1:  # Only headers or empty
            return "001"
        
        # Get the last order ID and increment
        order_ids = [row[0] for row in values[1:] if row]  # Skip header
        if order_ids:
            last_id = max([int(id_str) for id_str in order_ids if id_str.isdigit()])
            return f"{last_id + 1:03d}"
        else:
            return "001"
            
    except Exception as e:
        st.error(f"Error getting order number: {str(e)}")
        return "001"

# Test Google Sheets connection
def test_connection():
    """Test Google Sheets connection"""
    try:
        result = service.spreadsheets().get(spreadsheetId=SHEET_ID).execute()
        sheet_title = result.get('properties', {}).get('title', 'Unknown')
        st.success(f"✅ Connected to Google Sheet: '{sheet_title}'")
        return True
    except Exception as e:
        st.error(f"❌ Connection failed: {str(e)}")
        return False
# Sidebar for testing
with st.sidebar:
    st.header("🔧 Setup & Testing")
    
    if st.button("Test Google Sheets Connection"):
        test_connection()
    
    if st.button("Setup Sheet Headers"):
        if setup_sheet_headers():
            st.success("✅ Headers added to sheet!")
        else:
            st.info("ℹ️ Headers already exist or connection failed")

# Price mappings
jersey_prices = {
    "0-6M - Age 3/4": 31.00,
    "Age 5/6 - 13/14": 36.00,
    "Adult XS - 2XL": 38.00,
    "Adult 3XL - 5XL": 42.00,
    "Adult 6XL - 7XL": 46.00,
    "Women Size 8 - 20": 38.00,
    "No quiero esta camiseta": 0.0
}

shorts_prices = {
    "20”-26”": 21.50,
    "28”-48”": 23.50,
    "No quiero esto - I don't need it": 0.0
}

socks_prices = {
    "S": 10.00,
    "L": 10.00,
    "M": 10.00,
    "No quiero esto, I don't need this": 0.0
}

polo_prices = {
    "Kid (Age 5/6 - 13/14)": 36.70,
    "Adult": 39.00,
    "No quiero esto, I don't need this": 0.0
}

# User inputs
name = st.text_input("Full Name / Nombres y Apellido *")
whatsapp = st.text_input("Your WhatsApp / Tu WhatsApp *")
number = st.number_input("Preferred Jersey Number (1-99) / Número preferido (No 1-30) *", min_value=31, max_value=99, step=1)

jersey1 = st.selectbox("Jersey Size (1st) / Talla de camiseta (1.ª)", list(jersey_prices.keys()))
jersey2 = st.selectbox("Jersey Size (2nd) / Talla de camiseta (2.ª)", list(jersey_prices.keys()))

shorts1 = st.selectbox("Shorts (1st) / Pantalones (1.º)", list(shorts_prices.keys()))
shorts2 = st.selectbox("Shorts (2nd) / Pantalones (2.º)", list(shorts_prices.keys()))

socks1 = st.selectbox("Socks (1st pair) / Medias (1.º par)", list(socks_prices.keys()))
socks2 = st.selectbox("Socks (2nd pair) / Medias (2.º par)", list(socks_prices.keys()))

polo_adult = st.radio("Polo Adult Free Size", list(polo_prices.keys()))
polo_kid = st.radio("Polo Kid Free Size", list(polo_prices.keys()))

# Agreement text
with st.expander("📜 Agreement / Acuerdo"):
    st.markdown("""
   Kit Order Agreement – Terms & Acknowledgements Acuerdo de Pedido de Equipación – Términos y Reconocimientos
1. I acknowledge that this order is made solely by me, and I am committed to depositing 30% of the total cost of the jersey as a non-refundable payment. I understand that failure to do so may result in cancellation of my order.
Reconozco que este pedido es realizado únicamente por mí y me comprometo a depositar el 30% del costo total de la camiseta como un pago no reembolsable. Entiendo que si no lo hago, mi pedido puede ser cancelado.

2. I understand that the jersey number I request is not guaranteed, and I agree to purchase the jersey, shorts, socks, and/or polo regardless of the final number assigned.
Entiendo que el número de camiseta que solicite no está garantizado, y acepto comprar la camiseta, el short, las medias y/o el polo sin importar el número final asignado.

3. I acknowledge that all prices are listed in USD, and I agree to pay in the equivalent Paraguayan Guaraníes at the exchange rate on the day of payment. I understand that currency fluctuations are beyond the club’s control.
Reconozco que todos los precios están en dólares estadounidenses (USD), y acepto pagar el equivalente en guaraníes paraguayos, según el tipo de cambio del día del pago. Entiendo que las fluctuaciones de la moneda están fuera del control del club.

4. I understand that failure to pay the remaining 70% of the total cost may result in cancellation of my order without any refund.
Entiendo que no pagar el 70% restante del costo total puede resultar en la cancelación de mi pedido sin derecho a reembolso.

5. I acknowledge that Paraguay GAA is not responsible for the manufacture or quality control of the kits. Any issues, claims, or warranty concerns must be handled directly with O’Neills, the supplier.
Reconozco que el Paraguay GAA no es responsable de la fabricación ni del control de calidad de la equipación. Cualquier problema, reclamo o garantía debe tratarse directamente con O’Neills, el proveedor.

6. I acknowledge that the products are from O’Neills and agree to abide by their Terms & Conditions, available at:
[Insert O’Neills Terms & Conditions link]
Reconozco que los productos son de O’Neills y acepto cumplir con sus Términos y Condiciones, disponibles en:
[ Terms & Conditions  ]

7. I understand that delivery to Paraguay may take time, and the club is committed to providing regular updates, at least weekly, until the kits arrive.
Entiendo que la entrega a Paraguay puede tardar, y el club se compromete a proporcionar actualizaciones regulares, al menos una vez por semana, hasta que llegue la equipación.

8. I acknowledge that all final decisions regarding the order, including quantities, delivery, and disputes, are at the sole discretion of the club.
Reconozco que todas las decisiones finales relacionadas con el pedido, incluidas las cantidades, la entrega y cualquier disputa, están a la exclusiva discreción del club.

9. I understand that no changes to size, quantity, or item type can be made once the order is submitted.
Entiendo que no se pueden hacer cambios en la talla, cantidad o tipo de producto una vez que se haya enviado el pedido.

10. I acknowledge that it is my responsibility to check the size chart provided and understand that no exchanges or refunds will be available for incorrect sizing.
Reconozco que es mi responsabilidad revisar la tabla de tallas proporcionada y entiendo que no habrá cambios ni reembolsos por tallas incorrectas.

11. I understand that this is a bulk order to be shipped to Paraguay as a group. Individual delivery or separate shipments will not be arranged.
Entiendo que este es un pedido grupal que se enviará a Paraguay como un solo envío. No se organizarán entregas individuales ni envíos separados.

12. By agreeing to this order, I confirm that I have read and understood all terms above. I will enter my full name and the date below as confirmation.
Al aceptar este pedido, confirmo que he leído y comprendido todos los términos anteriores. Ingresaré mi nombre completo y la fecha a continuación como confirmación.

Name and date/Nombre y Fecha
    """)

confirm_name_date = st.text_input("Confirm your full name and today's date / Confirme su nombre completo y la fecha de hoy *")

# Total Calculation
total = jersey_prices[jersey1] + jersey_prices[jersey2] + \
         shorts_prices[shorts1] + shorts_prices[shorts2] + \
         socks_prices[socks1] + socks_prices[socks2] + \
         polo_prices[polo_adult] + polo_prices[polo_kid]

st.markdown(f"### 💵 Total: **${total:.2f}** USD")

# Save order with unique ID
def get_next_order_number(csv_file):
    if not os.path.exists(csv_file):
        return "001"
    df = pd.read_csv(csv_file)
    last_id = df["order_id"].iloc[-1]
    next_id = int(last_id) + 1
    return f"{next_id:03d}"

# Submission
if st.button("Submit Order / Enviar pedido"):
    if not all([name, whatsapp, confirm_name_date]):
        st.error("❌ Please complete all required fields. / Por favor complete todos los campos obligatorios.")
    else:
        csv_file = "orders.csv"
        order_id = get_next_order_number(csv_file)
        order = {
            "order_id": order_id,
            "name": name,
            "whatsapp": whatsapp,
            "number": number,
            "jersey1": jersey1,
            "jersey2": jersey2,
            "shorts1": shorts1,
            "shorts2": shorts2,
            "socks1": socks1,
            "socks2": socks2,
            "polo_adult": polo_adult,
            "polo_kid": polo_kid,
            "total_usd": total,
            "confirmation": confirm_name_date,
            "timestamp": datetime.now().isoformat()
        }
        df = pd.DataFrame([order])
        df.to_csv(csv_file, mode='a', header=not os.path.exists(csv_file), index=False)
        st.success(f"✅ Order #{order_id} submitted successfully!")
        st.balloons()
