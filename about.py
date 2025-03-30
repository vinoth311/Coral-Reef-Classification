import streamlit as st
from streamlit.components.v1 import html

def run_page():
    st.title("About")
    st.image("D:/Final Year Project/Coral Reef Sustainability/images/img1.jpg")
    st.markdown(
        """
        <div style="text-align: justify;">
            <strong>Our Mission</strong><br>
            We are committed to the protection and preservation of the coral reef ecosystems that are vital to marine life and the overall health of our oceans. 
            Coral reefs are often referred to as the rainforests of the sea because of their incredible biodiversity. 
            These ecosystems are home to thousands of marine species, providing them with shelter, food, and breeding grounds. 
            Our mission is to ensure that these vibrant underwater landscapes continue to thrive for future generations.<br><br>
            <strong>What We Do</strong><br>
            Through innovative research, education, and conservation initiatives, we work to mitigate the threats facing coral reefs today, such as climate change, overfishing, and pollution. Our team collaborates with local communities, governments, and global organizations to implement sustainable practices that protect and restore these delicate ecosystems.<br><br>
            <strong>Why It Matters</strong><br>
            Coral reefs are not just beautiful; they are essential to the balance of marine life and the livelihoods of millions of people around the world. They act as natural barriers, protecting coastal areas from storms and erosion, and they are a critical source of income through fishing and tourism. By preserving coral reefs, we are safeguarding the health of our oceans and the well-being of communities that rely on them.<br><br>
            <strong>Get Involved</strong><br>
            We believe that everyone has a role to play in protecting our oceans. Whether you are a scientist, a student, a diver, or simply someone who cares about the environment, there are many ways to get involved in our mission. Join us in making a difference through advocacy, volunteer work, or supporting our conservation projects.<br><br>
            <strong>Our Vision</strong><br>
            Our vision is a world where coral reefs are flourishing, resilient, and protected from harm. We strive to create a future where marine life thrives, and the beauty and benefits of coral reefs can be enjoyed by all.
        </div>

        """,
        unsafe_allow_html=True
    )
    st.write("")

    # Contact Form
    st.header("Send Us a Message")

    with st.form(key='contact_form'):
        st.write("Please fill out the form below and we will get back to you as soon as possible.")
        
        # Name
        name = st.text_input("Name", placeholder="Your Name")
        
        # Email
        email = st.text_input("Email", placeholder="Your Email")
        
        # Message
        message = st.text_area("Message", placeholder="Your Message")
        
        # Submit button
        submit_button = st.form_submit_button("Send Message")
        
        if submit_button:
            st.success("Thank you for your message! We will get back to you soon.")
    
    # Contact Information

    st.subheader("Our Contact Information")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Address")
        st.write("Chennai")
        st.write("Tamil Nadu")
        st.write("India")

    with col2:
        st.subheader("Phone")
        st.write("9600677177")
        st.write("Mon-Fri: 9 AM - 5 PM")

    # Email Contact
    st.subheader("Email")
    st.write("For general inquiries, please email us at:")
    st.write("[210701311@rajalakshmi.edu.in](mailto:210701311@rajalakshmi.edu.in)")

