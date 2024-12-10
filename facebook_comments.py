import requests
from dotenv import load_dotenv
import streamlit as st

# Load environment variables
load_dotenv()
facebook_access_token = st.secrets["FACEBOOK_ACCESS_TOKEN"]

facebook_api_version = st.secrets["FACEBOOK_API_VERSION"]

def start_facebook_service():
    """
    Initializes Facebook API settings.
    Returns the base URL for API calls.
    """
    base_url = f"https://graph.facebook.com/{facebook_api_version}/"
    return base_url

def extract_post_id_from_url(url):
    """
    Extracts the post ID from the Facebook URL.

    Args:
        url (str): The URL of the Facebook post.

    Returns:
        str: The extracted post ID.
    """
    post_id_part = url.split('/')[-2]
    return post_id_part

def get_post_comments(base_url, post_id, next_page_token=None):
    """
    Fetches comments for a given Facebook post.

    Args:
        base_url (str): The base URL for Facebook Graph API.
        post_id (str): ID of the Facebook post.
        next_page_token (str): Token for the next page of comments.

    Returns:
        dict: JSON response containing comments.
    """
    url = f"{base_url}{post_id}/comments"
    params = {
        "access_token": facebook_access_token,
        "fields": "id,message,from,created_time",
        "limit": 100
    }
    if next_page_token:
        params["after"] = next_page_token

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raises an HTTPError if the response was unsuccessful
    except requests.RequestException as e:
        st.error(f"An error occurred: {str(e)}")
        return None

    return response.json()

def load_comments_in_format(comments):
    """
    Formats comments into a single string for display.

    Args:
        comments (dict): JSON data of comments.

    Returns:
        str: Formatted string of comments.
    """
    all_comments_string = ""
    for comment in comments.get("data", []):
        comment_message = comment.get("message", "No message")
        comment_author = comment.get("from", {}).get("name", "Anonymous")
        comment_time = comment.get("created_time", "Unknown time")
        all_comments_string += f"{comment_author} ({comment_time}): {comment_message}\n"
    return all_comments_string

def fetch_fb_comments(url):
    """
    Fetches and formats all comments for a given post URL.

    Args:
        url (str): The URL of the Facebook post.

    Returns:
        str: Combined comments as a string.
    """
    post_id = extract_post_id_from_url(url)
    base_url = start_facebook_service()

    try:
        # Verify if the post ID exists before proceeding
        post_info_url = f"{base_url}{post_id}"
        post_info_params = {
            "access_token": facebook_access_token,
            "fields": "id"
        }
        post_info_response = requests.get(post_info_url, params=post_info_params)
        post_info_response.raise_for_status()

        all_comments = ""
        next_page_token = None
        while True:
            data = get_post_comments(base_url, post_id, next_page_token)
            if not data:
                return None  # If fetching failed, return None to indicate failure.

            all_comments += load_comments_in_format(data)

            # Check for pagination
            next_page = data.get("paging", {}).get("next")
            if not next_page:
                break
            next_page_token = data["paging"]["cursors"]["after"]

        return all_comments

    except requests.exceptions.RequestException as e:
        error_message = str(e)
        st.error(f"An error occurred: {error_message}")
        return None
