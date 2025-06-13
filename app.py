import streamlit as st
import pandas as pd
import os
from datetime import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
import gspread
from google.api_core.exceptions import GoogleAPIError

# Define the scope (more restrictive)
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",  # Minimum required scope
    "https://www.googleapis.com/auth/drive.file"    # Only access created files
]

# Access the spreadsheet and sheet
spreadsheet = client.open_by_key("1KSJH2VPZGNZz3gMUdc-RUGqCSgYnwvKF7cYoKLuiZi0")
sheet = spreadsheet.worksheet("Sheet1")

def get_google_credentials():
    """Secure credential loading with enhanced validation"""
    if 'gcp_service_account' not in st.secrets:
        st.error("❌ Google Cloud credentials not found in Streamlit secrets")
        st.stop()
    
    try:
        return service_account.Credentials.from_service_account_info(
            st.secrets["gcp_service_account"],
            scopes=SCOPES
        )
    except ValueError as e:
        st.error(f"❌ Invalid credential format: {str(e)}")
        st.stop()

# Initialize services
try:
    creds = get_google_credentials()
    
    # Initialize clients with error handling
    gspread_client = gspread.authorize(creds)
    sheets_service = build('sheets', 'v4', credentials=creds)
    
    # Access spreadsheet with explicit error handling
    SPREADSHEET_ID = "1KSJH2VPZGNZz3gMUdc-RUGqCSgYnwvKF7cYoKLuiZi0"
    spreadsheet = gspread_client.open_by_key(SPREADSHEET_ID)
    worksheet = spreadsheet.worksheet("Sheet1")
    
except GoogleAPIError as e:
    st.error(f"🔐 Google API Error: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Unexpected error: {str(e)}")
    st.stop()

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


# Submission - REPLACE THIS ENTIRE SECTION
if st.button("Submit Order / Enviar pedido"):
    if not all([name, whatsapp, confirm_name_date]):
        st.error("❌ Please complete all required fields. / Por favor complete todos los campos obligatorios.")
    else:
        # Get next order ID FROM GOOGLE SHEETS (using your existing function)
        order_id = get_next_order_number()
        
        # Prepare order data
        order_data = {
            "order_id": order_id,
            "name": name,
            "whatsapp": whatsapp,
            "number": number,
            "jersey1": jersey1,
            "jersey2": jersey2,
            "shorts1": shorts1,
            "shorts2": shorts2,
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
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Better format for Sheets
        }
        
        # WRITE TO GOOGLE SHEETS (using your existing function)
        if write_to_google_sheets(order_data):
            st.success(f"✅ Order #{order_id} submitted to Google Sheets!")
            st.balloons()
        else:
            st.error("❌ Failed to save to Google Sheets. Please try again.")
