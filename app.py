import streamlit as st
import pandas as pd
import datetime
import smtplib
from email.message import EmailMessage
import pywhatkit
import time
import base64

st.set_page_config(page_title="EasyPay Automation", page_icon="📲", layout="wide")

# === Load EasyPay Logo ===
def show_logo():
    logo_path = "easypay_private_limited_logo.jpeg"  # Must be in the same directory or uploaded via file uploader
    try:
        with open(logo_path, "rb") as f:
            logo_data = f.read()
            encoded = base64.b64encode(logo_data).decode()
            st.markdown(
                f"""
                <div style='text-align: center;'>
                    <img src='data:image/jpeg;base64,{encoded}' width='180'/>
                    <h2 style='margin-top: 0; color: #ffffff;'>EasyPay Automation Dashboard</h2>
                    <p style='font-size: 14px; color: #cccccc;'>Organizing the Unorganized</p>
                </div>
                """,
                unsafe_allow_html=True
            )
    except:
        st.warning("⚠️ Logo not found. Please ensure 'easypay_private_limited_logo.jpeg' is in the app folder.")

show_logo()

st.markdown("""
    <style>
        body {
            background-color: #0f172a;
            color: white;
        }
        .stApp {
            background-color: #0f172a;
        }
        .stTabs [data-baseweb="tab"] {
            font-size: 16px;
            padding: 12px;
            margin-right: 4px;
            background-color: #1e293b;
            color: white;
            border-radius: 6px 6px 0 0;
        }
        .stTabs [data-baseweb="tab"]:hover {
            background-color: #2563eb;
            color: white;
        }
        .stTabs [aria-selected="true"] {
            background-color: #2563eb;
            color: white;
        }
        .block-container {
            padding-top: 1rem;
            padding-bottom: 2rem;
        }
    </style>
""", unsafe_allow_html=True)

whatsapp_tab, email_tab = st.tabs(["📲 WhatsApp Messaging", "📧 Email Onboarding"])

# (rest of your code remains unchanged)


# -------------------- WHATSAPP TAB --------------------
with whatsapp_tab:
    st.subheader("📲 Send WhatsApp Messages to Sellers")
    st.markdown("Upload Growth & Visibility Excel files and automate WhatsApp messaging to ONDC sellers.")

    growth_file = st.file_uploader("📥 Upload Growth Excel", type=["xlsx"], key="growth")
    visibility_file = st.file_uploader("📥 Upload Visibility Excel", type=["xlsx"], key="visibility")

    if growth_file and visibility_file and st.button("🚀 Send WhatsApp Messages"):
        growth_df = pd.read_excel(growth_file, header=None, names=["Seller Name", "Number", "Category", "Date", "Link"])
        visibility_df = pd.read_excel(visibility_file)

        live_sellers = growth_df[growth_df["Link"].str.lower() == "yes"]

        for index, row in live_sellers.iterrows():
            seller_name = row["Seller Name"]
            raw_number = str(row["Number"]).strip()

            try:
                if 'e' in raw_number.lower():
                    raw_number = str(int(float(raw_number)))
                elif ".0" in raw_number:
                    raw_number = raw_number.split(".")[0]
                else:
                    raw_number = ''.join(filter(str.isdigit, raw_number))

                if raw_number.isdigit() and len(raw_number) == 10:
                    mobile = "+91" + raw_number
                else:
                    st.warning(f"⚠️ Invalid number: {raw_number}")
                    continue
            except Exception as e:
                st.error(f"❌ Error processing number {raw_number}: {e}")
                continue

            match = visibility_df[visibility_df["Seller Name"].str.strip() == seller_name.strip()]
            if match.empty:
                st.warning(f"🔍 No store info found for {seller_name}, skipping.")
                continue

            row_data = match.iloc[0]
            mystore = row_data.get("Mystore", "No")
            hamaramall = row_data.get("Hamaramall", "No")
            digihaat = row_data.get("Digihaat", "No")

            live_links = []
            if mystore != "No": live_links.append(f"Mystore: {mystore}")
            if hamaramall != "No": live_links.append(f"Hamaramall: {hamaramall}")
            if digihaat != "No": live_links.append(f"Digihaat: {digihaat}")

            if not live_links:
                st.info(f"ℹ️ No active store links for {seller_name}, skipping.")
                continue

            links_text = "\n".join(live_links)
            message = f"""Great News {seller_name},\n\nYour store is now live on ONDC and visible on top buyer apps! 🚀\n\n✅ Start sharing your store link with friends, family, and customers.\n\n{links_text}\n\n📈 More promotion = more sales!\nLet\'s grow together! 💼📲\nRegards,\nTeam EasyPay ONDC"""

            now = datetime.datetime.now() + datetime.timedelta(minutes=2)
            hour, minute = now.hour, now.minute

            try:
                pywhatkit.sendwhatmsg(mobile, message, hour, minute, wait_time=10, tab_close=True)
                st.success(f"✅ Message scheduled for {seller_name} at {mobile}")
            except Exception as e:
                st.error(f"❌ Failed to send message to {mobile}: {e}")

# -------------------- EMAIL TAB --------------------
with email_tab:
    st.subheader("📧 Send Onboarding Emails")
    st.markdown("Upload seller onboarding data and attachments to automatically send personalized emails with login credentials.")

    email_file = st.file_uploader("📥 Upload Onboarded Seller Excel", type=["xlsx"], key="email")
    sender_email = st.text_input("Your Gmail Address", placeholder="you@example.com")
    app_password = st.text_input("App Password", type="password")
    grocery_file = st.file_uploader("📎 Grocery Product List (.xlsx)", type=["xlsx"], key="grocery")
    handbook_file = st.file_uploader("📎 ONDC Seller Handbook (.pdf)", type=["pdf"], key="handbook")

    if email_file and sender_email and app_password and grocery_file and handbook_file:
        if st.button("📤 Send Emails"):
            df = pd.read_excel(email_file)
            onboarded = df

            for index, row in onboarded.iterrows():
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

                email_msg = EmailMessage()
                email_msg["Subject"] = "🎉 Welcome to ONDC Seller Network - Your EasyPay Credentials"
                email_msg["From"] = sender_email
                email_msg["To"] = to_email
                email_msg.set_content(message_body)

                email_msg.add_attachment(grocery_file.read(), maintype="application",
                                         subtype="vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                         filename="Grocery_Product_List.xlsx")

                email_msg.add_attachment(handbook_file.read(), maintype="application",
                                         subtype="pdf", filename="ONDC_Seller_Handbook.pdf")

                try:
                    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
                        smtp.login(sender_email, app_password)
                        smtp.send_message(email_msg)
                        st.success(f"✅ Email sent to {name} ({to_email})")
                except Exception as e:
                    st.error(f"❌ Failed to send email to {to_email}: {e}")