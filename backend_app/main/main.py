from flask import Flask, jsonify, request
from flask_cors import CORS
import webauthn
import json
import os

app = Flask(__name__)
CORS(app)  # Allow requests from your Streamlit app

# --- WebAuthn Configuration ---
RP_ID = "localhost"  # Relying Party ID
RP_NAME = "The Global Payment Network"
ORIGIN = "http://localhost:8501"  # The origin of your Streamlit app
webauthn_helper = webauthn.WebAuthn(RP_ID, RP_NAME, webauthn.helpers.RP_ID_HASH_ALGORITHM.SHA256)

# --- Simulated User Database ---
USER_DB_FILE = "user_database.json"


def get_users():
    """Loads users from a JSON file."""
    if not os.path.exists(USER_DB_FILE):
        return {}
    with open(USER_DB_FILE, 'r') as f:
        return json.load(f)


def save_users(users):
    """Saves the user dictionary to a JSON file."""
    with open(USER_DB_FILE, 'w') as f:
        json.dump(users, f, indent=4)


# --- Registration Endpoints ---
@app.route('/register/start', methods=['POST'])
def register_start():
    users = get_users()
    username = request.json['username']

    if username in users:
        return jsonify({"error": "Username already exists."}), 400

    user_info = webauthn.WebAuthnUser(
        user_id=username.encode('utf-8'),
        user_name=username,
        user_display_name=username,
        user_ico_url=None,
        user_credentials=[]
    )

    options = webauthn_helper.registration_challenge(user_info)
    users[username] = {"challenge": options, "credentials": []}
    save_users(users)

    return jsonify(options)


@app.route('/register/verify', methods=['POST'])
def register_verify():
    users = get_users()
    username = request.json['username']
    response = request.json['response']

    user_info = webauthn.WebAuthnUser.from_db(username, users[username]['credentials'])
    challenge = users[username]['challenge']

    try:
        new_credential = webauthn_helper.verify_registration(user_info, challenge, response)
        users[username]['credentials'].append(new_credential.to_db())
        del users[username]['challenge']
        save_users(users)
        return jsonify({"verified": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


# --- Login Endpoints ---
@app.route('/login/start', methods=['POST'])
def login_start():
    users = get_users()
    username = request.json['username']

    if username not in users:
        return jsonify({"error": "User not found."}), 404

    user_info = webauthn.WebAuthnUser.from_db(username, users[username]['credentials'])
    challenge = webauthn_helper.authentication_challenge(user_info)
    users[username]['challenge'] = challenge
    save_users(users)

    return jsonify(challenge)


@app.route('/login/verify', methods=['POST'])
def login_verify():
    users = get_users()
    username = request.json['username']
    response = request.json['response']

    user_info = webauthn.WebAuthnUser.from_db(username, users[username]['credentials'])
    challenge = users[username]['challenge']

    try:
        webauthn_helper.verify_authentication(user_info, challenge, response)
        del users[username]['challenge']
        save_users(users)
        # In a real app, you would issue a session token here.
        return jsonify({"verified": True})
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(port=5000, debug=True)