import streamlit as st
import pandas as pd
import time

# --- Placeholder for your Backend API ---
# In a real app, this would make a request to your backend service.
def api_login(username, password):
    """Simulates calling a backend API to authenticate a user."""
    if username == "admin" and password == "password":
        return True
    else:
        return False

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
                login_successful = api_login(username, password)

                if login_successful:
                    st.session_state['authenticated'] = True
                    st.session_state['username'] = username
                    st.rerun() # Rerun the script to show the main app
                else:
                    st.error("Invalid username or password")

# --- UI for the Main Application Page ---
def show_main_page():
    """Displays the main application content after login."""
    st.title("The Global Payment Network DAO")
    st.write(f"Welcome, **{st.session_state.get('username', 'User')}**!")
    st.sidebar.button("Logout", on_click=logout)

    st.markdown("---")

    st.subheader("Founders Table")

    # Create a sample DataFrame for the founders table
    data = {
        'Founder': ['Alice', 'Bob', 'Charlie'],
        'Role': ['CEO & Architect', 'Lead Protocol Dev', 'Head of Operations'],
        'Allocation (%)': [40, 30, 30]
    }
    df = pd.DataFrame(data)

    # Display the table using st.dataframe
    st.dataframe(df, use_container_width=True)

def logout():
    """Resets the session state to log the user out."""
    st.session_state['authenticated'] = False
    st.session_state['username'] = ""


# --- Main App Logic ---
# This part of the code controls which page is displayed.

# Initialize session state
if 'authenticated' not in st.session_state:
    st.session_state['authenticated'] = False

# Display pages based on authentication status
if st.session_state['authenticated']:
    show_main_page()
else:
    show_login_page()