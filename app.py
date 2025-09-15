
import streamlit as st
import pandas as pd
from datetime import datetime

# Initialize session state
if "users" not in st.session_state:
    st.session_state.users = pd.DataFrame(columns=[
        "Full Name", "Email", "Phone", "Password",
        "Public Name", "Country", "State", "District", "Pin Code", "Area"
    ])

if "logged_in_user" not in st.session_state:
    st.session_state.logged_in_user = None

# Sample posts with images
def get_sample_posts(user_location):
    posts = [
        {
            "Author": "PoliceDept",
            "Content": "A major road accident took place early this morning in Powai near Murarji Nagar. According to eyewitnesses, a speeding truck lost control and rammed into several vehicles, causing a massive pile-up on the highway. Fire brigade and local police immediately reached the spot to control the situation and provide medical assistance. Several people sustained injuries and traffic movement was severely disrupted for hours. Authorities have urged residents to avoid this route until clearance work i...
            "Image": "images/accident.png",
            "Location": "Powai, Murarji Nagar",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "Author": "TrafficDept",
            "Content": "Heavy traffic congestion has been reported near Sakinaka in the Jari Mari area due to ongoing repair works and continuous rainfall. The narrow lanes, combined with double-parked vehicles, made movement extremely difficult for commuters during peak hours. Public transport, including buses and rickshaws, was affected, leading to delays in office travel. Authorities have deployed traffic police to manage the situation, but commuters are advised to take alternative routes until the situation improv...
            "Image": "images/traffic.png",
            "Location": "Sakinaka, Jari Mari",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "Author": "BMC",
            "Content": "A fire broke out this afternoon in a residential tower located in Filter Pada, Powai. Thick black smoke was seen billowing from the upper floors, causing panic among residents. Fire tenders rushed to the spot and immediately began evacuation efforts. Fortunately, no casualties have been reported so far, though several people were treated for smoke inhalation. The cause of the fire is still under investigation, but initial reports suggest an electrical short circuit. Residents are urged to remain a...
            "Image": "images/fire.png",
            "Location": "Powai, Filter Pada",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        },
        {
            "Author": "CommunityGroup",
            "Content": "In a positive development, residents of Jari Mari organized a community cleanliness and safety drive in collaboration with local NGOs and civic bodies. The initiative saw over 200 volunteers coming together to clean streets, remove garbage, and set up awareness camps on sanitation and waste management. Local leaders highlighted the importance of maintaining hygiene and safety in densely populated areas. The event concluded with a pledge by residents to continue such efforts regularly to make Jari Ma...
            "Image": None,
            "Location": "Jari Mari",
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    ]
    return [p for p in posts if user_location in p["Location"]]

# Login form
def login():
    st.header("🔑 Login to Your Account")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        user = st.session_state.users[
            (st.session_state.users["Email"] == email) &
            (st.session_state.users["Password"] == password)
        ]
        if not user.empty:
            st.session_state.logged_in_user = user.iloc[0].to_dict()
            st.success(f"Welcome {st.session_state.logged_in_user['Public Name']}!")
            st.experimental_rerun()
        else:
            st.error("Invalid login credentials")

# Public profile setup
def profile_setup():
    st.warning("Complete your public profile setup first.")
    public_name = st.text_input("Public Display Name")
    country = st.selectbox("Country", ["India"])
    state = st.selectbox("State", ["Maharashtra"])
    district = st.selectbox("District", ["Mumbai Suburban"])
    pin_code = st.selectbox("Pin Code", ["400072", "400087"])
    area = st.selectbox("Area", ["Jari Mari", "Safed Pool"] if pin_code == "400072" else ["Powai", "Filter Pada", "Murarji Nagar"])
    if st.button("Save Profile"):
        st.session_state.logged_in_user.update({
            "Public Name": public_name,
            "Country": country,
            "State": state,
            "District": district,
            "Pin Code": pin_code,
            "Area": area
        })
        st.success("Profile updated successfully! Redirecting to Home Feed...")
        st.experimental_rerun()

# Home feed
def home_feed():
    st.header("📰 Home Feed")
    user_location = f"{st.session_state.logged_in_user['Area']}"
    posts = get_sample_posts(user_location)
    for row in posts:
        st.subheader(f"{row['Author']} ({row['Timestamp']})")
        st.write(row["Content"])
        if row["Image"]:
            st.image(row["Image"], width=400)
        else:
            st.info("(No image attached)")
        st.markdown("---")

# Main app logic
st.title("📰 Hyperlocal News & Safety App")

if not st.session_state.logged_in_user:
    login()
else:
    if not st.session_state.logged_in_user.get("Public Name"):
        profile_setup()
    else:
        home_feed()
