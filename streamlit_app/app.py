import streamlit as st
import pandas as pd
import time
import secrets  # Used for generating secure random keys


# --- 1. SIMULATED BACKEND & DATABASE ---
# In a real app, this section would be replaced by API calls to your actual backend.

def init_db():
    """Initializes a simulated user database in the session state."""
    if 'user_db' not in st.session_state:
        st.session_state.user_db = {
            "founder_user": {"password": "password", "role": "founder", "wallet": "0xabc...def"},
            "regular_user": {"password": "password", "role": "regular", "wallet": "0x123...456"}
        }


def api_login(username, password):
    """Simulates an API call to log a user in."""
    user = st.session_state.user_db.get(username)
    if user and user["password"] == password:
        return (True, user["role"])
    return (False, None)


def api_register_founder(username, password):
    """Simulates an API call to register a new founder."""
    if username in st.session_state.user_db:
        return (False, "Username already exists.")

    # Generate a secure key and a placeholder wallet address
    key = secrets.token_hex(24)
    wallet = f"0x{secrets.token_hex(20)}"

    # Add the new founder to our simulated database
    st.session_state.user_db[username] = {"password": password, "role": "founder", "key": key, "wallet": wallet}
    return (True, key, wallet)


# --- 2. UI FUNCTIONS FOR EACH PAGE/STATE ---
# Each function is responsible for drawing one "page" of the application.

def show_login_page():
    """Displays the main login form and a button to navigate to registration."""
    st.title("Login")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            login_successful, user_role = api_login(username, password)
            if login_successful:
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = user_role
                st.rerun()  # Rerun the script to show the main app
            else:
                st.error("Invalid username or password")

    st.markdown("---")
    if st.button("Register as a New Founder"):
        st.session_state.page = "register"
        st.rerun()


def show_registration_page():
    """Displays the first step of founder registration."""
    st.title("Founder Registration")

    with st.form("register_form"):
        st.write("Step 1: Choose Your Credentials")
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Register")

        if submitted:
            success, *response = api_register_founder(username, password)
            if success:
                st.session_state.new_key = response[0]
                st.session_state.new_wallet = response[1]
                st.session_state.page = "show_key"  # Move to the next step
                st.rerun()
            else:
                st.error(response[0])

    if st.button("Back to Login"):
        st.session_state.page = "login"
        st.rerun()


def show_key_display_page():
    """Displays the newly generated secret key and wallet address."""
    st.title("Registration Successful!")
    st.success("Your Founder account has been created.")
    st.write("Step 2: Save Your Secret Key & Wallet Address")
    st.warning(
        "IMPORTANT: This is the ONLY time you will see your secret key. Save it in a password manager or a secure offline location.",
        icon="⚠️")

    st.text_area("Your Secret Key (Save this!)", st.session_state.new_key, height=100, disabled=True)
    st.text_input("Your Wallet Address", st.session_state.new_wallet, disabled=True)

    if st.button("I have saved my key. Proceed to Verification."):
        st.session_state.page = "verify_key"
        st.rerun()


def show_key_verification_page():
    """Asks the user to enter their key to confirm they saved it."""
    st.title("Key Verification")
    st.write("Step 3: To ensure you have saved your key, please enter it below.")

    with st.form("verification_form"):
        entered_key = st.text_input("Enter your secret key")
        submitted = st.form_submit_button("Verify Key")

        if submitted:
            if entered_key.strip() == st.session_state.new_key:
                st.success("Verification successful! You will now be logged in.")
                time.sleep(2)
                st.session_state.authenticated = True
                # You might want to automatically log in the new user here
                st.rerun()
            else:
                st.error("The key does not match. Please try again.")


def show_main_app_page():
    """The main application view, shown after successful login."""
    st.title("The Global Payment Network DAO")

    # --- Sidebar for user info and logout ---
    st.sidebar.write(f"Welcome, **{st.session_state.get('username')}**!")
    st.sidebar.write(f"Role: **{st.session_state.get('role')}**")
    st.sidebar.button("Logout", on_click=logout, use_container_width=True)

    # --- Role-based main content ---
    if st.session_state.get('role') == 'founder':
        show_founders_view()
    else:
        show_regular_user_view()


def show_founders_view():
    """The view specific to founder-level users."""
    st.subheader("Founders Dashboard")
    st.write("Displaying sensitive founder information and project metrics.")

    # Display the founders table
    founder_data = {
        'Founder': ['Alice', 'Bob', 'Charlie'],
        'Role': ['CEO & Architect', 'Lead Protocol Dev', 'Head of Operations'],
        'Allocation (%)': [40, 30, 30]
    }
    st.dataframe(pd.DataFrame(founder_data), use_container_width=True)

    # Display wallet address
    user_info = st.session_state.user_db.get(st.session_state.username)
    if user_info:
        st.text_input("Your Wallet Address", user_info.get("wallet", "Not found"), disabled=True)


def show_regular_user_view():
    """The view for regular, non-founder users."""
    st.subheader("User Dashboard")
    st.write("Welcome! Here is the public information about the network.")
    user_info = st.session_state.user_db.get(st.session_state.username)
    if user_info:
        st.text_input("Your Wallet Address", user_info.get("wallet", "Not found"), disabled=True)


def logout():
    """Clears the session state to log the user out."""
    keys_to_delete = ['authenticated', 'username', 'role', 'page', 'new_key', 'new_wallet']
    for key in keys_to_delete:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()


# --- 3. MAIN APP LOGIC (STATE MACHINE) ---
# This controls which page is displayed based on the session state.

init_db()  # Make sure our simulated database exists

# Initialize session state keys if they don't exist
if 'page' not in st.session_state:
    st.session_state.page = "login"
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Main router: Display the correct page based on the current state.
if st.session_state.authenticated:
    show_main_app_page()
else:
    page = st.session_state.page
    if page == "login":
        show_login_page()
    elif page == "register":
        show_registration_page()
    elif page == "show_key":
        show_key_display_page()
    elif page == "verify_key":
        show_key_verification_page()