import streamlit as st
from comments import fetch_comments
from utils import get_summary
import base64


# Set page configuration
st.set_page_config(page_title="YouTube Comment Analyzer", layout="wide")

# Add custom CSS for styling
def add_custom_styles():
    custom_css = r"""
    <style>
        /* General styling */
        .stApp {{
            font-family: Arial, sans-serif;
        }}
      
        .nav-links {
            display: flex;
            justify-content: space-evenly;
            align-items: center;
            margin-top:45px;
            padding: 15px 0;
            background: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            z-index: 100;
            color: white;
        }

        .nav-links a {
            color: white;
            text-decoration: none;
            font-size: 1.2rem;
            padding: 10px 15px;
            transition: background-color 0.3s;
        }

        .nav-links a:hover {
            background-color: #575757;
            border-radius: 5px;
        }

        .banner {
            position: relative; /* Make sure the content sits on top of the video */
            height: 100vh;
            width: 100% ;
            overflow: hidden; /* Ensure the video fills the area */
            left:0;
            right : 0;
        }

        #background-video {
            position: absolute; /* Position the video behind the content */
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            object-fit: cover; /* Make the video cover the full screen */
        }

        .content {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            color: white;
            text-align: center;
            z-index: 1;  /* Ensures the text stays on top of the video */
        }

        .content h1 {
            font-size: 2.5rem; /* Adjust size of the heading */
            color: white;
        }

        .content p {
            font-size: 2rem; /* Adjust size of the heading */
            color: white;
        }

        /* About Us cards */
        .cards-container {
            display: flex;
            justify-content: center;
            gap: 20px;
            margin: 40px 0;
        }

        .card {
            background: #f9f9f9;
            padding: 20px;
            border-radius: 10px;
            width: 30%;
            text-align: center;
            box-shadow: 0px 0px 10px rgba(0, 0, 0, 0.1);
        }

        .card img {
            width: 100%;
            border-radius: 10px;
        }

        .card h3 {
            margin: 15px 0;
        }

        .card p {
            color: #555;
        }

        /* Contact form */
        .contact-form {
            margin: 0 auto;
            width: 60%;
            padding: 20px;
            border-radius: 10px;
        }

       footer {
    display: flex;
    justify-content: center; /* Center the content inside the footer */
    align-items: center;
    padding: 15px 0;
    background: rgba(0, 0, 0, 0.7); /* Semi-transparent background */
    position: auto; /* Positioning it relative to the screen */
    bottom: 0;
    left: 0;
    width: 100%; /* Make it span the full width of the screen */
    color: white;
    z-index: 100;
    margin-top: 35px; /* Adjust the spacing above the footer */
}
    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

add_custom_styles()

# Header navigation
st.markdown(
    """
    <div class="nav-links">
        <a href="#home">Home</a>
        <a href="#youtube">YouTube</a>
        <a href="#about-us">About</a>
        <a href="#contact-us">Contact</a>
    </div>
    """,
    unsafe_allow_html=True,
)

# Function to encode video to Base64
def video_to_base64(video_path):
    with open(video_path, "rb") as video_file:
        return base64.b64encode(video_file.read()).decode()

# Encode the video
video_base64 = video_to_base64("bg.mp4")

# Sections
st.markdown('<a name="home"></a>', unsafe_allow_html=True)
with st.container():
    st.markdown(
        f"""
        <div class="banner">
            <video autoplay muted loop id="background-video">
                 <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                Your browser does not support the video tag.
            </video>
            <div class="content">
                <h1>YouTube Comment Analyzer</h1>
                <p>Analyze and summarize YouTube comments efficiently.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )




# Custom CSS for styling
st.markdown(
    """
    <style>
        /* General Page Styling */
        body {
            margin: 0;
            padding: 0;
        }
        .container {
            width: 100%;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: start;
        }
        
        .left-section {
            width: 48%;
        }
        .right-section {
            width: 48%;
        }
        .stButton button {
            background: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            border-radius: 5px;
            cursor: pointer;
        }
        .stButton button:hover {
            background: #45a049;
        }
        .stTextInput > div {
            border-radius: 5px;
            border: 1px solid #ccc;
        }
        .spinner-container {
            text-align: center;
            font-size: 18px;
            margin-top: 20px;
        }
    </style>
    """,
    unsafe_allow_html=True,
)
st.markdown('<a name="youtube"></a>', unsafe_allow_html=True)
# Header and Instructions
st.title("YouTube Comment Analyzer")
st.write(
    "Use this tool to generate summaries from comments under any YouTube video. "
    "The tool uses **Google Gemini** paired with **LangChain** to generate the summaries."
)

# Main container with two sections
left, right = st.columns(2)

# Left Section - Input Form
with left:
    st.markdown("<div class='left-section'>", unsafe_allow_html=True)
    st.header("Input Section")
    form = st.form("template_form")
    url_input = form.text_input(
        "Enter YouTube video URL",
        placeholder="Paste your YouTube video link here...",
        value="",
    )
    submit = form.form_submit_button("Get Summary")
    st.markdown("</div>", unsafe_allow_html=True)

# Placeholder for Right Section - Output
with right:
    st.markdown("<div class='right-section'>", unsafe_allow_html=True)
    st.header("Summary Section")
    if submit and url_input:
        with st.spinner("Fetching Summary..."):
            # Get Comments from YouTube API - INPUT
            text = fetch_comments(url_input)
            
            if text:  # Proceed only if comments are fetched
                # Tokenization and Summarization - MAIN CODE
                final_summary = get_summary(text)
                
                # Display the output on Streamlit - OUTPUT
                st.markdown(
                    f"<p style='font-size:18px; line-height:1.6;'>{final_summary}</p>",
                    unsafe_allow_html=True,
                )
            else:
                st.error("Unable to fetch comments. Please check the video or try again.")
    else:
        st.info("Submit a YouTube URL to display the summary.")
    st.markdown("</div>", unsafe_allow_html=True)


# Streamlit "About Us" Section
st.markdown('<a name="about-us"></a>', unsafe_allow_html=True)
with st.container():
    st.header("About Us")

    # Add CSS for styling
    st.markdown(
        """
        <style>
            .cards-container {
                display: flex;
                justify-content: space-between;
                flex-wrap: wrap;
                margin-top: 20px;
                gap: 20px;
            }
            .card {
                background: #ffffff;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                border-radius: 10px;
                width: 30%;
                text-align: center;
                padding: 15px;
                box-sizing: border-box;
            }
            .card img {
                width: 100%;
                height: auto;
                border-radius: 10px 10px 0 0;
            }
            .card h3 {
                font-size: 20px;
                color: #333;
                margin: 15px 0 10px;
            }
            .card p {
                font-size: 14px;
                color: #666;
                line-height: 1.5;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )
import base64
import streamlit as st

# Function to encode image to Base64
def image_to_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

# Encode the image
img_base64 = image_to_base64("image.png")
img2_base64 = image_to_base64("image2.jpg")
img3_base64 = image_to_base64("image3.png")

# Streamlit "About Us" Section
with st.container():
    st.markdown('<a name="about-us"></a>', unsafe_allow_html=True)

    # Add CSS for styling
    st.markdown(
        f"""
        <style>
            .cards-container {{
                display: flex;
                justify-content: space-between;
                flex-wrap: nowrap; /* Prevent wrapping */
                gap: 20px;
                width: 100%; /* Ensure full width */
                margin-top: 20px;
            }}
            .card {{
                background: #000000; /* Black background */
                border: 1px solid #ffffff; /* Thin white border */
                border-radius: 10px;
                width: 30%; /* Adjust width for alignment */
                text-align: center;
                padding: 15px;
                box-sizing: border-box;
            }}
            .card img {{
                width: 100%;
                height: auto;
                border-radius: 10px 10px 0 0;
            }}
            .card h3 {{
                font-size: 20px;
                color: #ffffff; /* White text for contrast */
                margin: 15px 0 10px;
            }}
            .card p {{
                font-size: 14px;
                color: #cccccc; /* Light grey for description */
                line-height: 1.5;
            }}
        </style>
        <div class="cards-container">
            <div class="card">
                <img src="data:image/png;base64,{img_base64}" alt="Feature 1">
                <h3>Efficient Data Analysis</h3>
                <p>Our app excels at analyzing YouTube comments to extract valuable insights. Using advanced natural language processing and sentiment analysis, it identifies key trends, opinions, and sentiments in user comments, helping users gain meaningful feedback and make informed decisions effortlessly.</p>
            </div>
            <div class="card">
                <img src="data:image/jpeg;base64,{img2_base64}" alt="Feature 2">
                <h3>User-Friendly Design</h3>
                <p>Our app offers a user-friendly interface, designed to be intuitive and accessible for everyone, whether you're a beginner or an expert, ensuring a smooth and efficient experience</p>
            </div>
            <div class="card">
                <img src="data:image/png;base64,{img3_base64}" alt="Feature 3">
                <h3>AI-Powered Summaries</h3>
                <p>Leverage cutting-edge AI algorithms to generate precise summaries.Our app intelligently condenses lengthy content into clear and digestible insights.Get concise, meaningful information in seconds, saving you time and effort.</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


st.markdown('<a name="contact-us"></a>', unsafe_allow_html=True)
with st.container():
    st.header("Contact Us")
    st.markdown('<div class="contact-form">', unsafe_allow_html=True)
    name = st.text_input("Your Name")
    email = st.text_input("Your Email")
    message = st.text_area("Your Message")
    if st.button("Send Message"):
        st.success("Your message has been sent!")
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
st.markdown(
    """
    <footer>
        <p>Done by Chettim Chetty Hemasri &copy; 2024. All rights reserved.</p>
    </footer>
    """,
    unsafe_allow_html=True,
)
