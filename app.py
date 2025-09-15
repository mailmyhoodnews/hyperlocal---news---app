import streamlit as st
import pandas as pd
import hashlib
from datetime import datetime

def make_hash(password):
    return hashlib.sha256(str(password).encode()).hexdigest()

def check_password(password, hashed):
    return make_hash(password) == hashed

def load_users():
    try:
        return pd.read_csv("users.csv")
    except:
        return pd.DataFrame(columns=[
            "Email", "Password", "Full Name", "Phone", "Public Name",
            "Country", "State", "District", "Pin", "Area"
        ])

def load_posts():
    try:
        return pd.read_csv("posts.csv")
    except:
        return pd.DataFrame(columns=["Author", "Content", "Image", "Pin", "Area", "Timestamp"])

def save_users(df):
    df.to_csv("users.csv", index=False)

def save_posts(df):
    df.to_csv("posts.csv", index=False)

st.set_page_config(page_title="Hyperlocal News App", layout="wide")
st.title("📰 Hyperlocal News & Safety App")

menu = ["Login", "Sign Up"]
choice = st.sidebar.selectbox("Menu", menu)

users = load_users()
posts = load_posts()

if choice == "Sign Up":
    st.subheader("Create New Account")
    full_name = st.text_input("Full Name")
    phone = st.text_input("Phone Number")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Sign Up"):
        if email in users["Email"].values:
            st.error("Email already registered!")
        else:
            new_user = {
                "Email": email,
                "Password": make_hash(password),
                "Full Name": full_name,
                "Phone": phone,
                "Public Name": "",
                "Country": "",
                "State": "",
                "District": "",
                "Pin": "",
                "Area": ""
            }
            users = pd.concat([users, pd.DataFrame([new_user])], ignore_index=True)
            save_users(users)
            st.success("Account created successfully! Please login.")

elif choice == "Login":
    st.subheader("Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if email in users["Email"].values:
            user = users.loc[users["Email"] == email].iloc[0]
            if check_password(password, user["Password"]):
                st.success(f"Welcome {user['Full Name']}!")

                # ✅ FIXED condition for Public Profile Setup
                if pd.isna(user["Public Name"]) or user["Public Name"] == "":
                    st.warning("Complete your public profile setup first.")
                    public_name = st.text_input("Public Display Name")
                    country = st.selectbox("Country", ["India"])
                    state = st.selectbox("State", ["Maharashtra"])
                    district = st.selectbox("District", ["Mumbai Suburban"])
                    pin = st.selectbox("Pin Code", ["400072", "400087"])
                    if pin == "400072":
                        area = st.selectbox("Area", ["Jari Mari", "Safed Pool"])
                    else:
                        area = st.selectbox("Area", ["Powai", "Filter Pada", "Murarji Nagar"])

                    if st.button("Save Profile"):
                        users.loc[users["Email"] == email, ["Public Name", "Country", "State", "District", "Pin", "Area"]] =                             [public_name, country, state, district, pin, area]
                        save_users(users)
                        st.success("Profile setup completed. Please login again.")
                        st.stop()
                else:
                    st.subheader("🏠 Home Feed")
                    user_pin = user["Pin"]
                    user_area = user["Area"]
                    filtered_posts = posts[(posts["Pin"] == user_pin) & (posts["Area"] == user_area)]
                    for _, row in filtered_posts.iterrows():
                        st.markdown(f"**{row['Author']}** ({row['Timestamp']})")
                        st.write(row["Content"])
                        if row["Image"]:
                            st.image(row["Image"], width=250)
                        st.markdown("---")

                    st.subheader("✍️ Add New Post")
                    content = st.text_area("Post Content")
                    image_url = st.text_input("Image URL (optional)")
                    tags = st.text_input("Tags (optional)")
                    if st.button("Post"):
                        new_post = {
                            "Author": user["Public Name"],
                            "Content": content,
                            "Image": image_url,
                            "Pin": user_pin,
                            "Area": user_area,
                            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        }
                        posts = pd.concat([posts, pd.DataFrame([new_post])], ignore_index=True)
                        save_posts(posts)
                        st.success("Post added successfully!")
            else:
                st.error("Invalid password!")
        else:
            st.error("User not found!")
