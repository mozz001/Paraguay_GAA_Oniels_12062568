import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="O'Niels Jersey Order Form", layout="centered")

st.title("O'Niels Jersey Order Form - June 2025")
st.markdown("""
#### 🇬🇧 English / 🇪🇸 Español
Please fill in all the fields below. Prices will be calculated in real time.
Por favor complete todos los campos a continuación. Los precios se calcularán en tiempo real.
""")

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

socksCrewSize_prices = {
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
