import streamlit as st
import pymongo
from pymongo import MongoClient
from bson.objectid import ObjectId
import hashlib
from datetime import datetime, timedelta

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client["coral_reef_db"]
organisations_collection = db["organisations"]
events_collection = db["events"]
tourism_companies_collection = db["tourism"]

# Utility functions
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def register_organisation(name, username, password):
    hashed_password = hash_password(password)
    organisations_collection.insert_one({
        "name": name,
        "username": username,
        "password": hashed_password
    })

def verify_organisation(username, password):
    hashed_password = hash_password(password)
    organisation = organisations_collection.find_one({
        "username": username,
        "password": hashed_password
    })
    return organisation

def create_event(organisation_id, event_name, event_date, location, event_description, image_url):
    event_date_str = event_date.strftime('%Y-%m-%d')
    events_collection.insert_one({
        "organisation_id": organisation_id,
        "event_name": event_name,
        "event_date": event_date_str,
        "event_description": event_description,
        "location": location,
        "image_url": image_url
    })
    st.success("Event created successfully!")

def register_tourism_company(organisation_id, company_name, location, description, pricing, image_url):
    tourism_companies_collection.insert_one({
        "organisation_id": organisation_id,
        "name": company_name,
        "location": location,
        "description": description,
        "pricing": pricing,
        "image_url": image_url
    })

def delete_event(event_id):
    events_collection.delete_one({"_id": ObjectId(event_id)})
    st.success("Event deleted successfully!")

def delete_tourism_company(company_id):
    tourism_companies_collection.delete_one({"_id": ObjectId(company_id)})
    st.success("Tourism company deleted successfully!")

def logout():
    st.session_state.logged_in = False
    st.session_state.organisation_id = None
    st.session_state.organisation_name = None
    st.session_state.page = "organisation_login"
    st.experimental_rerun()

def organisation_login_page():
    st.title("Organisation Login Page")
    
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        organisation = verify_organisation(username, password)
        if organisation:
            st.session_state.logged_in = True
            st.session_state.organisation_id = str(organisation['_id'])
            st.session_state.organisation_name = organisation['name']
            st.session_state.page = "organisation_dashboard"
            st.experimental_rerun()
        else:
            st.error("Invalid username or password")

    if st.button("Register"):
        st.session_state.page = "organisation_register"
        st.experimental_rerun()


def organisation_register_page():
    st.title("Organisation Register Page")
    
    organisation_name = st.text_input("Organisation Name")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        if organisations_collection.find_one({"username": username}):
            st.error("Username already exists.")
        else:
            register_organisation(organisation_name, username, password)
            st.success("Registration successful! Please log in.")
            st.session_state.page = "organisation_login"
            st.experimental_rerun()

def organisation_dashboard():
    if "logged_in" not in st.session_state or not st.session_state.logged_in:
        st.session_state.page = "organisation_login"
        st.experimental_rerun()
    
    st.title("Organisation Dashboard")
    st.subheader(f"Welcome, {st.session_state.organisation_name}!")

    # Button to Create Event
    st.subheader("Create Event")
    event_name = st.text_input("Event Name")
    event_date = st.date_input("Event Date")
    event_location = st.text_input("Event Location")
    event_description = st.text_area("Event Description")
    event_image_url = st.text_input("Event Image URL (optional)")
    if st.button("Submit Event"):
        create_event(st.session_state.organisation_id, event_name, event_date, event_location, event_description, event_image_url)
        st.experimental_rerun()

    # Button to Register Tourism Company
    st.subheader("Register Tourism Company")
    company_name = st.text_input("Company Name")
    location = st.text_input("Location")
    description = st.text_area("Description")
    pricing = st.number_input("Pricing", min_value=0.0, format="%.2f")
    company_image_url = st.text_input("Company Image URL (optional)")
    if st.button("Submit Company"):
        register_tourism_company(st.session_state.organisation_id, company_name, location, description, pricing, company_image_url)
        st.success("Tourism company registered successfully!")
        st.experimental_rerun()

    # Display Upcoming Events
    st.subheader("Upcoming Events")
    events = events_collection.find({"organisation_id": st.session_state.organisation_id})
    for event in events:
        st.write(f"**Event Name:** {event['event_name']}")
        if event.get('image_url'):
            st.image(event['image_url'], use_column_width=True)
        st.write(f"**Date:** {event['event_date']}")
        st.write(f"**Location:** {event['location']}")
        st.write(f"**Description:** {event['event_description']}")
        
        if st.button(f"Delete Event: {event['event_name']}", key=f"delete_event_{event['_id']}"):
            delete_event(event['_id'])
            st.experimental_rerun()
        st.write("---")

    # Display Registered Tourism Companies
    st.subheader("Registered Tourism Companies")
    companies = tourism_companies_collection.find({"organisation_id": st.session_state.organisation_id})
    for company in companies:
        st.write(f"**Company Name:** {company['name']}")
        if company.get('image_url'):
            st.image(company['image_url'], use_column_width=True)
        st.write(f"**Location:** {company['location']}")
        st.write(f"**Description:** {company['description']}")
        st.write(f"**Pricing:** ${company['pricing']:.2f}")
        
        if st.button(f"Delete Company: {company['name']}", key=f"delete_company_{company['_id']}"):
            delete_tourism_company(company['_id'])
            st.experimental_rerun()
        st.write("---")

    # Logout Button
    if st.button("Logout"):
        logout()
        
def run_organisation_page():
    if "page" not in st.session_state:
        st.session_state.page = "organisation_login"

    if st.session_state.page == "organisation_login":
        organisation_login_page()
    elif st.session_state.page == "organisation_register":
        organisation_register_page()
    elif st.session_state.page == "organisation_dashboard":
        organisation_dashboard()
