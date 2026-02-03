import streamlit as st
import pandas as pd

st.set_page_config(page_title="Lost & Found", layout="wide")

# ---------- SESSION STATE ----------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "current_user" not in st.session_state:
    st.session_state.current_user = ""

if "items" not in st.session_state:
    st.session_state.items = pd.DataFrame([
        {"name": "Wallet", "desc": "Black leather", "status": "Lost"},
        {"name": "Phone", "desc": "Blue case", "status": "Found"},
        {"name": "Backpack", "desc": "Nike", "status": "Lost"},
        {"name": "Watch", "desc": "Silver", "status": "Found"},
        {"name": "Keys", "desc": "Red keychain", "status": "Lost"},
        {"name": "Bottle", "desc": "Steel", "status": "Found"},
        {"name": "Notebook", "desc": "Math notes", "status": "Lost"},
        {"name": "Earbuds", "desc": "White", "status": "Found"},
        {"name": "Jacket", "desc": "Black hoodie", "status": "Lost"},
        {"name": "Calculator", "desc": "Casio", "status": "Found"},
    ])

# ---------- LOGIN ----------
def login_page():
    st.title("🔐 Login / Sign Up")

    email = st.text_input("Email", key="login_email")
    password = st.text_input("Password", type="password", key="login_pass")

    if st.button("Enter", key="login_btn"):
        if not email or not password:
            st.error("Email and password required")
            return

        if email not in st.session_state.users:
            st.session_state.users[email] = password
            st.session_state.logged_in = True
            st.session_state.current_user = email
            st.experimental_rerun()
        else:
            if st.session_state.users[email] == password:
                st.session_state.logged_in = True
                st.session_state.current_user = email
                st.experimental_rerun()
            else:
                st.error("Wrong password")

# ---------- PAGES ----------
def report_lost():
    st.header("📝 Report Lost Item")

    name = st.text_input("Item Name", key="lost_name")
    desc = st.text_area("Description", key="lost_desc")

    if st.button("Submit Lost Item", key="lost_submit"):
        if not name:
            st.error("Item name required")
            return

        new_item = pd.DataFrame([{
            "name": name,
            "desc": desc,
            "status": "Lost"
        }])

        st.session_state.items = pd.concat(
            [st.session_state.items, new_item],
            ignore_index=True
        )
        st.success("Item reported")

def claim_found():
    st.header("📦 Claim Found Item")
    found = st.session_state.items[
        st.session_state.items["status"] == "Found"
    ]
    st.dataframe(found, use_container_width=True)

def recent_items():
    st.header("🕒 Recent Items")
    search = st.text_input("Search item", key="search_items")

    df = st.session_state.items
    if search:
        df = df[df["name"].str.contains(search, case=False, na=False)]

    st.dataframe(df, use_container_width=True)

# ---------- MAIN ----------
if not st.session_state.logged_in:
    login_page()
else:
    st.sidebar.title("📍 Navigation")
    page = st.sidebar.radio(
        "Go to",
        ["Report Lost", "Claim Found", "Recent Items"],
        key="nav_radio"
    )

    st.sidebar.write("👤", st.session_state.current_user)

    if st.sidebar.button("Logout", key="logout_btn"):
        st.session_state.logged_in = False
        st.experimental_rerun()

    if page == "Report Lost":
        report_lost()
    elif page == "Claim Found":
        claim_found()
    else:
        recent_items()
