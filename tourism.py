import streamlit as st
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import hashlib
from bson.objectid import ObjectId

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["coral_reef_db"]
tourism_collection = db["tourism"]
user_collection = db["users"]
booking_collection = db["bookings"]

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(username, password):
    hashed_password = hash_password(password)
    user_collection.insert_one({"username": username, "password": hashed_password, "bookings": []})

def verify_user(username, password):
    hashed_password = hash_password(password)
    user = user_collection.find_one({"username": username, "password": hashed_password})
    return user is not None

def logout():
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.user_id = None
    st.session_state.page = "login"
    st.experimental_rerun()

def run_page():
    st.title("Tourism Page")
    
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.page = "login"
        st.experimental_rerun()
    
    search_name = st.text_input("Search by Tourism Company Name")
    search_location = st.text_input("Search by Location")
    
    query = {}
    if search_name:
        query["name"] = {"$regex": search_name, "$options": "i"}
    if search_location:
        query["location"] = {"$regex": search_location, "$options": "i"}

    tourism_data = list(tourism_collection.find(query))

    if not tourism_data:
        st.write("No tourism companies found.")
    
    for entry in tourism_data:
        with st.container():
            st.subheader(entry['name'])
            
            image_url = entry.get('image_url', '')
            if image_url:
                st.image(image_url, use_column_width=True)
            
            st.write(entry['description'])
            st.write(f"Pricing: ${entry['pricing']:.2f}")
            st.write(f"Location: {entry['location']}")
            if st.button("Join", key=entry['_id']):
                st.session_state.selected_company = entry
                st.session_state.page = "booking"
                st.experimental_rerun()

    # Display user bookings if logged in
    if "user_id" in st.session_state:
        st.subheader("My Bookings")
        user = user_collection.find_one({"_id": ObjectId(st.session_state.user_id)})
        if user and 'bookings' in user:
            bookings = booking_collection.find({"_id": {"$in": [ObjectId(b) for b in user['bookings']]}})
            for booking in bookings:
                company = tourism_collection.find_one({"_id": booking['company_id']})
                with st.expander(f"Booking with {company['name']}"):
                    image_url = company.get('image_url', '')
                    if image_url:
                        st.image(image_url, use_column_width=True)
                    st.write(f"**Date:** {booking['date']}")
                    st.write(f"**Start Time:** {booking['start_time']}")
                    st.write(f"**End Time:** {booking['end_time']}")
                    st.write(f"**Number of Members:** {booking['num_members']}")
                    st.write(f"**Total Price:** ${booking['total_price']:.2f}")
        else:
            st.write("You have no bookings.")
        
        #Logout button
        if st.button("Logout"):
            logout()

def booking_page():
    st.title("Booking Page")
    
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.page = "login"
        st.experimental_rerun()
    
    company = st.session_state.get("selected_company")
    user = st.session_state.get("current_user")
    
    if company:
        st.subheader(company['name'])
        
        image_url = company.get('image_url', '')
        if image_url:
            st.image(image_url, use_column_width=True)
        
        st.write(company['description'])
        st.write(f"Pricing: ${company['pricing']:.2f}")
        st.write(f"Location: {company['location']}")
        
        date = st.date_input("Select Date")
        start_time = st.time_input("Select Start Time", value=datetime.now().time())
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=2)).time()
        st.write(f"End Time (2 hours later): {end_time.strftime('%H:%M')}")
        
        num_members = st.number_input("Number of Members", min_value=1, step=1)
        
        unit_price = company.get('pricing', 0)
        total_price = unit_price * num_members
        
        st.write(f"Total Price: ${total_price:.2f}")
        
        if st.button("Confirm Booking"):
            # Save booking details to MongoDB
            date_str = date.strftime('%Y-%m-%d')
            start_time_str = start_time.strftime('%H:%M:%S')
            end_time_str = end_time.strftime('%H:%M:%S')
            booking_id = booking_collection.insert_one({
                "company_id": company['_id'],
                "user_id": user['_id'],
                "date": date_str,
                "start_time": start_time_str,
                "end_time": end_time_str,
                "num_members": num_members,
                "total_price": total_price
            }).inserted_id
            
            # Update user's bookings
            user_collection.update_one(
                {"_id": user['_id']},
                {"$push": {"bookings": booking_id}}
            )
            
            st.success("Booking successful!")
        if st.button("Return to Tourism Page"):
            st.session_state.page = "tourism"
            st.experimental_rerun()

def login_page():
    st.title("Tourism Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = user_collection.find_one({"username": username})
        if user and verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.session_state.user_id = str(user['_id'])  # Save user ID in session state
            st.session_state.page = "tourism"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Register"):
        st.session_state.page = "register"
        st.experimental_rerun()

def register_page():
    st.title("Register Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        if user_collection.find_one({"username": username}):
            st.error("Username already exists.")
        else:
            register_user(username, password)
            st.success("Registration successful! Please log in.")
            st.session_state.page = "login"
            st.experimental_rerun()

def run_tourism_page():
    if "page" not in st.session_state:
        st.session_state.page = "login"  # Start at the login page if no page is set
    
    if st.session_state.page == "tourism":
        run_page()
    elif st.session_state.page == "booking":
        booking_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()

