
import streamlit as st
import pandas as pd
import hashlib
import os
from datetime import datetime

# File paths
USER_CSV = "users.csv"
POST_CSV = "posts.csv"

# Ensure files exist
if not os.path.exists(USER_CSV):
    pd.DataFrame(columns=["Full Name", "Email", "Password", "Public Name", "Country", "State", "District", "Pin Code", "Area"]).to_csv(USER_CSV, index=False)

if not os.path.exists(POST_CSV):
    pd.DataFrame(columns=["Author", "Content", "Image", "Location", "Timestamp"]).to_csv(POST_CSV, index=False)

# Load data
def load_users():
    return pd.read_csv(USER_CSV)

def save_users(df):
    df.to_csv(USER_CSV, index=False)

def load_posts():
    return pd.read_csv(POST_CSV)

def save_posts(df):
    df.to_csv(POST_CSV, index=False)

# Password hashing
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Signup function
def signup():
    st.subheader("Sign Up")
    full_name = st.text_input("Full Name")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if full_name and email and password:
            users = load_users()
            if email in users['Email'].values:
                st.error("Email already registered")
            else:
                new_user = pd.DataFrame([[full_name, email, hash_password(password), "", "", "", "", "", ""]],
                                        columns=users.columns)
                users = pd.concat([users, new_user], ignore_index=True)
                save_users(users)
                st.success("Account created! Please complete your profile setup.")
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                st.session_state["setup_profile"] = True
                st.rerun()
        else:
            st.error("Please fill all fields.")

# Login function
def login():
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        users = load_users()
        if email in users['Email'].values:
            stored_hash = users.loc[users['Email'] == email, 'Password'].values[0]
            if hash_password(password) == stored_hash:
                st.session_state["logged_in"] = True
                st.session_state["email"] = email
                st.session_state["setup_profile"] = False
                st.success("Welcome back!")
                st.rerun()
            else:
                st.error("Incorrect password")
        else:
            st.error("Email not found")

# Profile setup
def profile_setup():
    st.subheader("Complete your public profile setup first.")
    users = load_users()
    email = st.session_state["email"]
    user_row = users[users['Email'] == email].iloc[0]

    public_name = st.text_input("Public Display Name", value=user_row["Public Name"] if user_row["Public Name"] else "")
    country = st.selectbox("Country", ["India"], index=0)
    state = st.selectbox("State", ["Maharashtra"], index=0)
    district = st.selectbox("District", ["Mumbai Suburban"], index=0)
    pin_code = st.selectbox("Pin Code", ["400072", "400087"])
    area_options = {"400072": ["Jari Mari", "Safed Pool"], "400087": ["Powai", "Filter Pada", "Murarji Nagar"]}
    area = st.selectbox("Area", area_options[pin_code])

    if st.button("Save Profile"):
        users.loc[users['Email'] == email, ["Public Name", "Country", "State", "District", "Pin Code", "Area"]] =             [public_name, country, state, district, pin_code, area]
        save_users(users)
        st.success("Profile saved successfully!")
        st.session_state["setup_profile"] = False
        st.rerun()

# Home Feed
def home_feed():
    st.subheader("🏠 Home Feed")
    posts = load_posts()
    users = load_users()
    email = st.session_state["email"]
    user = users[users['Email'] == email].iloc[0]
    location_filter = f"{user['Pin Code']} - {user['Area']}"
    filtered_posts = posts[posts['Location'] == location_filter]

    if filtered_posts.empty:
        sample_posts = [
            {"Author": "PoliceDept", "Content": "Traffic update: Diversion near Jari Mari due to heavy congestion.", "Image": "images/jarimari_traffic.png", "Location": "400072 - Jari Mari", "Timestamp": str(datetime.now())},
            {"Author": "BMC", "Content": "Water supply maintenance scheduled today in Jari Mari.", "Image": "", "Location": "400072 - Jari Mari", "Timestamp": str(datetime.now())},
            {"Author": "Resident", "Content": "Saw a stray dog near the market, please be careful.", "Image": "", "Location": "400072 - Jari Mari", "Timestamp": str(datetime.now())},
            {"Author": "News", "Content": "A major road accident took place in Powai near Murarji Nagar. A speeding truck lost control and rammed into multiple vehicles, causing a massive fire outbreak. Emergency services rushed to the spot.", "Image": "images/accident_in_powai.png", "Location": "400087 - Murarji Nagar", "Timestamp": str(datetime.now())},
            {"Author": "Local", "Content": "Fire broke out in a residential tower at Safed Pool. Residents were evacuated quickly. Fire brigade controlled the situation in time, no casualties reported.", "Image": "images/powai_fire_broke_out.png", "Location": "400072 - Safed Pool", "Timestamp": str(datetime.now())},
        ]
        posts = pd.concat([posts, pd.DataFrame(sample_posts)], ignore_index=True)
        save_posts(posts)
        filtered_posts = posts[posts['Location'] == location_filter]

    for _, row in filtered_posts.iterrows():
        st.markdown(f"**{row['Author']}** ({row['Timestamp']})")
        st.write(row["Content"])
        if row["Image"] and os.path.exists(row["Image"]):
            st.image(row["Image"], width=300)
        st.write("---")

    # Add new post
    st.subheader("✍️ Add New Post")
    content = st.text_area("Post Content")
    image = st.file_uploader("Upload Image (optional)", type=["png", "jpg", "jpeg"])
    if st.button("Post"):
        if content:
            image_path = ""
            if image:
                image_path = f"images/{image.name}"
                with open(image_path, "wb") as f:
                    f.write(image.getbuffer())
            new_post = pd.DataFrame([[user["Public Name"], content, image_path, location_filter, str(datetime.now())]],
                                    columns=["Author", "Content", "Image", "Location", "Timestamp"])
            posts = pd.concat([posts, new_post], ignore_index=True)
            save_posts(posts)
            st.success("Post added successfully!")
            st.rerun()
        else:
            st.error("Post content cannot be empty")

# Main App
def main():
    st.title("📰 Hyperlocal News & Safety App")
    if "logged_in" not in st.session_state:
        st.session_state["logged_in"] = False

    menu = ["Login", "Sign Up"]
    choice = st.sidebar.selectbox("Menu", menu)

    if not st.session_state["logged_in"]:
        if choice == "Login":
            login()
        elif choice == "Sign Up":
            signup()
    else:
        if st.session_state.get("setup_profile", False):
            profile_setup()
        else:
            home_feed()
            if st.button("Logout"):
                st.session_state.clear()
                st.rerun()

if __name__ == "__main__":
    main()
