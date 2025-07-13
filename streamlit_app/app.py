import streamlit as st
import pandas as pd
import time

# --- Placeholder for your Backend API ---
def api_login(username, password):
    """
    Simulates calling a backend API.
    Returns a tuple: (is_successful, user_role)
    """
    if username == "founder_user" and password == "password":
        return (True, "founder")
    elif username == "regular_user" and password == "password":
        return (True, "regular")
    else:
        return (False, None)

# --- UI for the Login Page ---
def show_login_page():
    """Displays the login form."""
    st.title("Login or Register")

    with st.form("login_form"):
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            with st.spinner("Authenticating..."):
                time.sleep(1) # Simulates network latency
                login_successful, user_role = api_login(username, password)

                if login_successful:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.session_state['role'] = user_role # <-- Store the role
                    st.rerun() # Rerun the script to show the main app
                else:
                    st.error("Invalid username or password")

# --- Views for different roles ---
def show_founders_view():
    st.subheader("Founders Dashboard")
    st.write("Displaying sensitive founder information.")
    data = {
        'Founder': ['Alice', 'Bob', 'Charlie'],
        'Role': ['CEO & Architect', 'Lead Protocol Dev', 'Head of Operations'],
        'Allocation (%)': [40, 30, 30]
    }
    st.dataframe(pd.DataFrame(data), use_container_width=True)


def show_regular_user_view():
    st.subheader("User Dashboard")
    st.write("Welcome! Here is the public information for regular users.")
    # You can add other content for regular users here

def logout():
    """Resets the session state to log the user out."""
    st.session_state['authenticated'] = False
    st.session_state['username'] = ""
    st.session_state['role'] = ""

def show_main_page():
    st.title("The Global Payment Network DAO")
    st.write(f"Welcome, **{st.session_state.get('username')}**!")
    st.sidebar.button("Logout", on_click=logout)
    st.markdown("---")

    # --- Use the role to show the correct view ---
    if st.session_state.get('role') == 'founder':
        show_founders_view()
    elif st.session_state.get('role') == 'regular':
        show_regular_user_view()
    else:
        st.error("User role not found. Please contact support.")

# --- Main App Logic ---
# This part of the code controls which page is displayed.

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False
    st.session_state['role'] = "" # Also init role

# Display pages based on authentication status
if st.session_state['authenticated']:
    show_main_page()
else:
    show_login_page()