import streamlit as st
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import json
# ===== GOOGLE SHEETS AUTH =====
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
#CREDS = ServiceAccountCredentials.from_json_keyfile_name("service_account.json", SCOPE)
creds_dict =st.secrets["gcp_service_account"]
CLIENT = gspread.authorize(CREDS)
SHEET = CLIENT.open("users101").sheet1  # Change to your sheet name

# ===== FUNCTIONS =====
def register_user(username, password, First_name, last_name, DoB, contact, email):
    users = SHEET.get_all_records()
    if any(user["username"] == username for user in users):
        return False, "Username already exists!"
    SHEET.append_row([First_name, last_name, DoB, contact, email, password, username])
    return True, "Registration successful!"

def login_user(username, password):
    users = SHEET.get_all_records()
    for user in users:
        if user["username"] == username and user["password"] == password:
            return True
    return False

# ===== STREAMLIT APP =====
st.set_page_config(page_title="Login System", page_icon="🔑")

# Initialize session state
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ===== LOGIN/REGISTER PAGE =====
if not st.session_state.logged_in:
    tab1, tab2 = st.tabs(["Login", "Register"])

    with tab1:
        st.subheader("Login")
        login_user_input = st.text_input("username", key="login_username")
        login_pass_input = st.text_input("password", type="password", key="login_password")
        if st.button("Login"):
            if login_user(login_user_input, int(login_pass_input)):
                st.session_state.logged_in = True
                st.session_state.username = login_user_input
                st.rerun()
            else:
                st.error("Invalid username or password")

    with tab2:
        st.subheader("Register")
        reg_user_input = st.text_input("username")
        reg_pass_input = st.text_input("password", type="password", key="reg_password")
        reg_passre_input = st.text_input("Repeat Password", type="password")
        reg_first_input = st.text_input("First name")
        reg_last_input = st.text_input("Last name")
        reg_email_input = st.text_input("email")
        reg_dob_input = st.text_input("Date of birth")
        reg_contact_input = st.text_input("Contact")
        

        if st.button("Register"):
            success, msg = register_user(reg_user_input, reg_pass_input, reg_first_input, reg_last_input, reg_dob_input, reg_contact_input,  reg_email_input)
            if success:
                st.success(msg)
            else:
                st.error(msg)

# ===== DASHBOARD PAGE =====
else:
    st.sidebar.success(f"Logged in as: {st.session_state.username}")
    st.title("📊 Dashboard")
    st.write("Welcome to your dashboard!")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""

        st.rerun()

