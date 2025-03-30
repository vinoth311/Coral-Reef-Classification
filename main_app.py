import streamlit as st
from streamlit.components.v1 import components
from streamlit.components.v1 import html
import time 
import os
import base64
from PIL import Image
from io import BytesIO

# Function to load, resize, and convert an image to base64
def load_resize_encode_image(image_path, width=1200, height=650):
    try:
        img = Image.open(image_path)
        img = img.resize((width, height))
        buffered = BytesIO()
        img.save(buffered, format="PNG")
        return base64.b64encode(buffered.getvalue()).decode(), width
    except Exception as e:
        st.error(f"Error loading image {image_path}: {e}")
        return None, None
    

# Function to load, resize, and display an image with a fixed height
def load_and_display_image(image_path, height=300):
    img = Image.open(image_path)
    aspect_ratio = img.width / img.height
    new_width = int(aspect_ratio * height)
    img = img.resize((new_width, height))
    return img

# Set page configuration
st.set_page_config(page_title="Coral Reef Mapping: A Sustainable Approach for Marine Ecosystem Conservation", layout="wide")

# Navigation bar
st.sidebar.title("Navigation")
page = st.sidebar.radio("Select a page", ["Home", "Coral Reef Classification", "Coral Area Mapping", "Tourism", "Events", "Organizations", "About"])

# Dynamic page loading
if page == "Home":
    st.title("Coral Reef Ecosystem Conservation")
    # Scrollable images
    st.subheader("Gallery")
        
    # Image paths
    image_paths = [
        "D:/Final Year Project/Coral Reef Sustainability/images/gal.png",
        "D:/Final Year Project/Coral Reef Sustainability/images/savecoral2.jpg",
        "D:/Final Year Project/Coral Reef Sustainability/images/coralcolorful.jpg",
        "D:/Final Year Project/Coral Reef Sustainability/images/savecoral.jpg",
        "D:/Final Year Project/Coral Reef Sustainability/images/cor3.jpg",
        "D:/Final Year Project/Coral Reef Sustainability/images/coralcolorful2.jpg"
    ]

    # Load and convert images to base64
    image_html = ""
    for image_path in image_paths:
        img_base64, img_width = load_resize_encode_image(image_path)
        if img_base64:
            image_html += f'<div class="slide"><img src="data:image/png;base64,{img_base64}" style="width: 1200px; height: 650px; margin-right: 10px;" /></div>'
    
    # HTML for carousel with both scrolling and automatic sliding
    carousel_html = f"""
    <style>
        .carousel {{
            display: flex;
            overflow-x: auto;
            white-space: nowrap;
            scroll-behavior: smooth;
            width: 100%;
            height: 650px;
            position: relative;
        }}
        .carousel .slide {{
            display: inline-block;
            min-width: 1200px; /* Fixed width for slides */
            height: 100%;
        }}
        .carousel img {{
            height: 100%;
            width: 100%;
            object-fit: cover; /* Ensure the image covers the slide area */
        }}
    </style>

    <div class="carousel" id="carousel">
        {image_html}
    </div>

    <script>
        let currentIndex = 0;
        const slides = document.querySelectorAll('#carousel .slide');
        const totalSlides = slides.length;
        const carousel = document.getElementById('carousel');
        const slideWidth = 1200; // Fixed width for slides

        function showNextSlide() {{
            currentIndex = (currentIndex + 1) % totalSlides;
            carousel.scrollTo({{left: currentIndex * slideWidth, behavior: 'smooth'}});
        }}

        setInterval(showNextSlide, 3000);

        // Optional: Allow manual scrolling using buttons or touch
        let isMouseDown = false;
        let startX, scrollLeft;

        carousel.addEventListener('mousedown', (e) => {{
            isMouseDown = true;
            startX = e.pageX - carousel.offsetLeft;
            scrollLeft = carousel.scrollLeft;
        }});

        carousel.addEventListener('mouseleave', () => {{
            isMouseDown = false;
        }});

        carousel.addEventListener('mouseup', () => {{
            isMouseDown = false;
        }});

        carousel.addEventListener('mousemove', (e) => {{
            if (!isMouseDown) return;
            e.preventDefault();
            const x = e.pageX - carousel.offsetLeft;
            const walk = (x - startX) * 3; // scroll-fast
            carousel.scrollLeft = scrollLeft - walk;
        }});
    </script>
    """

    # Render the carousel
    st.components.v1.html(carousel_html, height=700)



    # Set up the Achievements section
    st.subheader("Achievements")
    col1, col2, col3 = st.columns(3)

    with col1:
        img1 = load_and_display_image("D:/Final Year Project/Coral Reef Sustainability/images/achieve1.jpg", height=300)
        st.image(img1, use_column_width=True)
        st.markdown("""
            <div style='text-align: justify;'>
                <strong>SAVE THE REEFS</strong><br>
                Successfully launched a global campaign to raise awareness about coral reef conservation, reaching millions worldwide.
                Developed educational programs that have reached over 200 schools, inspiring the next generation to protect marine ecosystems.
            </div>
        """, unsafe_allow_html=True)

    with col2:
        img2 = load_and_display_image("D:/Final Year Project/Coral Reef Sustainability/images/achieve6.jpeg", height=300)
        st.image(img2, use_column_width=True)
        st.markdown("""
            <div style='text-align: justify;'>
                <strong>SAVE OUR OCEANS</strong><br>
                Engaged thousands of volunteers in cleaning over 100 miles of coastline reducing pollution levels.
                Partnered with local organisations to conduct regular beach cleanups, removing plastics and waste, and raising awareness about marine pollution.
            </div>
        """, unsafe_allow_html=True)

    with col3:
        img3 = load_and_display_image("D:/Final Year Project/Coral Reef Sustainability/images/achieve3.jpg", height=300)
        st.image(img3, use_column_width=True)
        st.markdown("""
            <div style='text-align: justify;'>
                <strong>PRO PLANET ECO EARTH</strong><br>
                Successfully showcased innovative sustainability solutions at the G20 summit, fostering global collaboration on climate action and inspiring commitments towards a greener future.
                New policies aimed at reducing waste and promoting green urban planning.
            </div>
        """, unsafe_allow_html=True)

    
    # About section
    st.subheader("About")
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
        st.write("6385916287")
        st.write("Mon-Fri: 9 AM - 5 PM")

    # Email Contact
    st.subheader("Email")
    st.write("For general inquiries, please email us at:")
    st.write("[210701311@rajalakshmi.edu.in](mailto:210701311@rajalakshmi.edu.in)")
    st.write("[210701303@rajalakshmi.edu.in](mailto:210701303@rajalakshmi.edu.in)")


elif page == "Coral Reef Classification":
    from coral_reef_classification import run_page
    run_page()

elif page == "About":
    from about import run_page
    run_page()

elif page == "Coral Area Mapping":
    from coral_area_mapping import run_page
    run_page()

elif page == "Tourism":
    from tourism import run_tourism_page
    run_tourism_page()

elif page == "Organizations":
    from organisations import run_organisation_page
    run_organisation_page()
elif page == "Events":
    from events import run_events_page
    run_events_page()