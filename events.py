import streamlit as st
import pymongo
from pymongo import MongoClient
from datetime import datetime, timedelta
import hashlib
from bson.objectid import ObjectId

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["coral_reef_db"]
events_collection = db["events"]
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

def run_event_page():
    st.title("Events Page")
    
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.page = "login"
        st.experimental_rerun()
    
    search_name = st.text_input("Search by Event Name")
    search_location = st.text_input("Search by Location")
    
    query = {}
    if search_name:
        query["name"] = {"$regex": search_name, "$options": "i"}
    if search_location:
        query["location"] = {"$regex": search_location, "$options": "i"}

    events_data = list(events_collection.find(query))

    if not events_data:
        st.write("No events found.")
    
    for entry in events_data:
        with st.container():
            st.subheader(entry['event_name'])
            
            image_url = entry.get('image_url', '')
            if image_url:
                st.image(image_url, use_column_width=True)
            
            st.write(entry['event_description'])
            # st.write(f"Pricing: ${entry['pricing']:.2f}")
            st.write(f"Location: {entry['location']}")
            st.write(f"Date: {entry['event_date']}")
            if st.button("Book", key=entry['_id']):
                st.session_state.selected_event = entry
                st.session_state.page = "booking"
                st.experimental_rerun()

    # Display user bookings if logged in
    if "user_id" in st.session_state:
        st.subheader("My Bookings")
        user = user_collection.find_one({"_id": ObjectId(st.session_state.user_id)})
        if user and 'bookings' in user:
            bookings = booking_collection.find({"_id": {"$in": [ObjectId(b) for b in user['bookings']]}})
            for booking in bookings:
                event = events_collection.find_one({"_id": booking['event_id']})
                with st.expander(f"Booking with {event['event_name']}"):
                    if event.get('image_url'):
                        st.image(event['image_url'], use_column_width=True)
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
    
    event = st.session_state.get("selected_event")
    user = st.session_state.get("current_user")
    
    if event:
        st.subheader(event['event_name'])
        
        image_url = event.get('image_url', '')
        if image_url:
            st.image(image_url, use_column_width=True)
        
        st.write(event['event_description'])
        # st.write(f"Pricing: ${event['pricing']:.2f}")
        st.write(f"Location: {event['location']}")
        st.write(f"Date: {event['event_date']}")
        
        date = st.date_input("Select Date")
        start_time = st.time_input("Select Start Time", value=datetime.now().time())
        end_time = (datetime.combine(datetime.today(), start_time) + timedelta(hours=2)).time()
        st.write(f"End Time (2 hours later): {end_time.strftime('%H:%M')}")
        
        num_members = st.number_input("Number of Members", min_value=1, step=1)
        
        unit_price = event.get('pricing', 0)
        total_price = unit_price * num_members
        
        st.write(f"Total Price: ${total_price:.2f}")
        
        if st.button("Confirm Booking"):
            # Save booking details to MongoDB
            date_str = date.strftime('%Y-%m-%d')
            start_time_str = start_time.strftime('%H:%M:%S')
            end_time_str = end_time.strftime('%H:%M:%S')
            booking_id = booking_collection.insert_one({
                "event_id": event['_id'],
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
        if st.button("Return to Events Page"):
            st.session_state.page = "events"
            st.experimental_rerun()

def login_page():
    st.title("Events Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        user = user_collection.find_one({"username": username})
        if user and verify_user(username, password):
            st.session_state.logged_in = True
            st.session_state.current_user = user
            st.session_state.user_id = str(user['_id'])  # Save user ID in session state
            st.session_state.page = "events"
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

def run_events_page():
    if "page" not in st.session_state:
        st.session_state.page = "login"  # Start at the login page if no page is set
    
    if st.session_state.page == "events":
        run_event_page()
    elif st.session_state.page == "booking":
        booking_page()
    elif st.session_state.page == "login":
        login_page()
    elif st.session_state.page == "register":
        register_page()

# Make sure this is the entry point of your Streamlit app
if __name__ == "__main__":
    run_events_page()
