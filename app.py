
import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Hyperlocal News & Safety App", layout="wide")

# ----------------------------
# Session State Initialization
# ----------------------------
if "users" not in st.session_state:
    st.session_state["users"] = pd.DataFrame(columns=["Full Name", "Phone", "Email", "Password", "DisplayName", "Country", "State", "District", "Pincode", "Area"])

if "posts" not in st.session_state:
    st.session_state["posts"] = pd.DataFrame([
        {
            "Author": "PoliceDept",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Content": "A major road accident took place early this morning in Powai near Murarji Nagar. According to eyewitnesses, a speeding truck lost control and rammed into several vehicles. Local police and fire brigade reached the spot immediately. Traffic diversions are in place, and residents are advised to avoid the area for a few hours.",
            "Location": "Powai, Murarji Nagar",
            "Image": "images/accident in powai.png"
        },
        {
            "Author": "TrafficDept",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Content": "Heavy traffic jam reported in Jarimari due to ongoing drainage repair work and rainfall. Vehicles are moving slowly, and pedestrians are facing inconvenience. Authorities have advised commuters to take alternate routes via Sakinaka to avoid long delays.",
            "Location": "Jarimari",
            "Image": "images/jarimari traffic.png"
        },
        {
            "Author": "Resident",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Content": "A fire broke out today afternoon at a residential tower in Safed Pool. Firefighters rushed to the scene and managed to contain the blaze before it could spread to nearby apartments. No casualties have been reported so far, but several families were evacuated as a precaution.",
            "Location": "Safed Pool",
            "Image": "images/powai fire broke out.png"
        },
        {
            "Author": "BMC",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Content": "Water supply in Jari Mari will be disrupted today due to urgent maintenance work on the main pipeline. The disruption is expected to last from 10:00 AM to 6:00 PM. Residents are advised to store sufficient water in advance and use it judiciously during the period.",
            "Location": "Jari Mari",
            "Image": None
        }
    ])
    
if "current_user" not in st.session_state:
    st.session_state["current_user"] = None

# ----------------------------
# Authentication
# ----------------------------
def signup():
    st.subheader("Sign Up")
    with st.form("signup_form"):
        full_name = st.text_input("Full Name")
        phone = st.text_input("Phone Number")
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if email in list(st.session_state["users"]["Email"]):
                st.error("User already exists! Please login.")
            else:
                new_user = pd.DataFrame([{
                    "Full Name": full_name,
                    "Phone": phone,
                    "Email": email,
                    "Password": password,
                    "DisplayName": "",
                    "Country": "",
                    "State": "",
                    "District": "",
                    "Pincode": "",
                    "Area": ""
                }])
                st.session_state["users"] = pd.concat([st.session_state["users"], new_user], ignore_index=True)
                st.success("Account created! Please complete your profile setup.")
                st.session_state["current_user"] = email
                st.experimental_rerun()

def login():
    st.subheader("Login to Your Account")
    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

        if submitted:
            users = st.session_state["users"]
            user = users[(users["Email"] == email) & (users["Password"] == password)]
            if not user.empty:
                st.session_state["current_user"] = email
                st.success(f"Welcome {user.iloc[0]['Full Name']}!")
                st.experimental_rerun()
            else:
                st.error("Invalid credentials. Please try again.")

# ----------------------------
# Profile Setup
# ----------------------------
def profile_setup():
    st.subheader("Complete your public profile setup first.")
    user_idx = st.session_state["users"][st.session_state["users"]["Email"] == st.session_state["current_user"]].index[0]
    user = st.session_state["users"].loc[user_idx]

    with st.form("profile_form"):
        display_name = st.text_input("Public Display Name", user["DisplayName"])
        country = st.selectbox("Country", ["India"], index=0)
        state = st.selectbox("State", ["Maharashtra"], index=0)
        district = st.selectbox("District", ["Mumbai Suburban"], index=0)
        pincode = st.text_input("Pin Code", user["Pincode"])
        area = st.text_input("Area", user["Area"])

        submitted = st.form_submit_button("Save Profile")
        if submitted:
            st.session_state["users"].at[user_idx, "DisplayName"] = display_name
            st.session_state["users"].at[user_idx, "Country"] = country
            st.session_state["users"].at[user_idx, "State"] = state
            st.session_state["users"].at[user_idx, "District"] = district
            st.session_state["users"].at[user_idx, "Pincode"] = pincode
            st.session_state["users"].at[user_idx, "Area"] = area
            st.success("Profile saved successfully!")
            st.experimental_rerun()

# ----------------------------
# Home Feed
# ----------------------------
def home_feed():
    st.header("🏠 Home Feed")
    for _, row in st.session_state["posts"].iterrows():
        st.markdown(f"**{row['Author']}** ({row['Timestamp']})")
        st.write(row["Content"])
        if row["Image"]:
            st.image(row["Image"], width=400)
        st.caption(f"📍 {row['Location']}")
        st.markdown("---")

# ----------------------------
# Main App
# ----------------------------
st.title("📰 Hyperlocal News & Safety App")

menu = st.sidebar.selectbox("Menu", ["Login", "Sign Up", "Home Feed"])

if menu == "Login":
    if st.session_state["current_user"] is None:
        login()
    else:
        user_data = st.session_state["users"][st.session_state["users"]["Email"] == st.session_state["current_user"]].iloc[0]
        if user_data["DisplayName"] == "":
            profile_setup()
        else:
            home_feed()

elif menu == "Sign Up":
    signup()

elif menu == "Home Feed":
    if st.session_state["current_user"] is None:
        st.warning("Please login to continue.")
    else:
        home_feed()
