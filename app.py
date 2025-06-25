import streamlit as st
import pandas as pd
from email.message import EmailMessage
import smtplib
import base64
import os

# === UI Config ===
st.set_page_config(page_title="EasyPay Automation Dashboard", page_icon="✅", layout="centered")
st.image("easypay_private_limited_logo.jpeg", width=180)
st.title("📊 EasyPay Automation Dashboard")
st.markdown("""
<style>
    .stTabs [data-baseweb="tab"] {
        font-size: 18px;
        padding: 12px;
    }
</style>
""", unsafe_allow_html=True)

tabs = st.tabs(["📧 Email Onboarding", "💬 WhatsApp Messaging"])

# === TAB 1: EMAIL ONBOARDING ===
with tabs[0]:
    st.subheader("📧 Send ONDC Onboarding Emails")

    uploaded_email_excel = st.file_uploader("Upload Excel for Email (with columns: Seller Name, Email, Number, Password)", type=["xlsx"])

    grocery_file = st.file_uploader("Upload Grocery Product List .xlsx", type=["xlsx"])
    handbook_file = st.file_uploader("Upload ONDC Seller Handbook .pdf", type=["pdf"])

    sender_email = st.text_input("Sender Gmail Address")
    app_password = st.text_input("App Password (from Google App Passwords)", type="password")

    if st.button("📨 Send Emails"):
        if uploaded_email_excel and grocery_file and handbook_file and sender_email and app_password:
            df = pd.read_excel(uploaded_email_excel)
            for index, row in df.iterrows():
                name = row["Seller Name"]
                to_email = row["Email"]
                mobile = str(row["Number"])
                password = row["Password"]

                message_body = f"""
Dear Sir,

🎉 Congratulations!

You are now onboarded on ONDC Seller Network successfully.
Please find your User Credentials below -

🔗 Link: https://business.easypay.in  
📱 Mobile Number: {mobile}  
🔐 Password: {password}

We're excited that you're just one step away from launching your Online Shop.
The Easy Pay Team will soon be in touch to guide you through:
• Seller Dashboard
• Product Listing
• Order Management

If you have any questions or need further assistance, don't hesitate to contact us.

📱 Easy Pay App: https://play.google.com/store/apps/details?id=com.sellerhub  
📢 WhatsApp Channel: https://whatsapp.com/channel/0029Vb8UJy51HspsqckSPl1h  
📢 Telegram Channel: https://t.me/easypaysellerapp

--  
Thanks & Regards,  
Easy Pay Ltd  
📞 +91 75177 77468  
🌐 www.easypay.in
"""
                email = EmailMessage()
                email["Subject"] = "🎉 Welcome to ONDC Seller Network - Your EasyPay Credentials"
                email["From"] = sender_email
                email["To"] = to_email
                email.set_content(message_body)

                email.add_attachment(grocery_file.read(), maintype="application", subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet", filename="Grocery_Product_List.xlsx")
                email.add_attachment(handbook_file.read(), maintype="application", subtype="pdf", filename="ONDC_Seller_Handbook.pdf")

                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(sender_email, app_password)
                        smtp.send_message(email)
                        st.success(f"✅ Email sent to {name} ({to_email})")
                except Exception as e:
                    st.error(f"❌ Failed to send email to {to_email}: {e}")
        else:
            st.warning("⚠️ Please fill all fields and upload required files.")

# === TAB 2: WHATSAPP (DISABLED) ===
with tabs[1]:
    st.subheader("💬 WhatsApp Automation")
    st.warning("⚠️ WhatsApp automation using pywhatkit is not supported on Streamlit Cloud.\n\nPlease run the desktop script locally for WhatsApp messaging.")