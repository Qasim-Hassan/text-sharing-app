import streamlit as st
import requests

API_BASE = "http://localhost:8000"

st.set_page_config(page_title="Simple Social", layout="wide")

# ----------------------------
# Session State
# ----------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "user" not in st.session_state:
    st.session_state.user = None


def get_headers():
    if st.session_state.token:
        return {"Authorization": f"Bearer {st.session_state.token}"}
    return {}


# ----------------------------
# Auth Page
# ----------------------------
def login_page():
    st.title("📝 Intuition Social")

    email = st.text_input("Email")
    password = st.text_input("Password", type="password")

    if not email or not password:
        st.info("Enter your email and password")
        return

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Login", type="primary", use_container_width=True):
            response = requests.post(
                f"{API_BASE}/auth/jwt/login",
                data={"username": email, "password": password},
            )

            if response.status_code == 200:
                st.session_state.token = response.json()["access_token"]

                user_res = requests.get(
                    f"{API_BASE}/users/me",
                    headers=get_headers(),
                )

                if user_res.status_code == 200:
                    st.session_state.user = user_res.json()
                    st.rerun()
                else:
                    st.error("Failed to fetch user info")
            else:
                st.error("Invalid credentials")

    with col2:
        if st.button("Sign Up", use_container_width=True):
            response = requests.post(
                f"{API_BASE}/auth/register",
                json={"email": email, "password": password},
            )

            if response.status_code == 201:
                st.success("Account created! Now login.")
            else:
                st.error(response.json().get("detail", "Signup failed"))


# ----------------------------
# Create Post
# ----------------------------
def post_page():
    st.title("✍️ New Post")

    # Initialize session state for the text area
    if "post_text" not in st.session_state:
        st.session_state.post_text = ""

    # Text area bound to session state
    st.text_area(
        "What's happening?",
        max_chars=280,
        placeholder="Write something...",
        key="post_text"
    )

    # Function to submit post
    def submit_post():
        text = st.session_state.post_text.strip()
        if not text:
            st.warning("Post cannot be empty")
            return

        try:
            response = requests.post(
                f"{API_BASE}/uploads",
                json={"text": text},  # json
                headers=get_headers(),            # add auth headers here if needed
            )
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to connect to backend: {e}")
            return

        if response.status_code in (200, 201):
            st.success("Posted!")
            st.session_state.post_text = ""  # clear text area
        else:
            st.error(f"Failed to post: {response.text}")

    # Post button triggers the function
    st.button("Post", on_click=submit_post)



# ----------------------------
# Feed
# ----------------------------
def feed_page():
    st.title("🏠 Feed")

    response = requests.get(
        f"{API_BASE}/feed",
        headers=get_headers(),
    )

    if response.status_code != 200:
        st.error("Failed to load feed")
        return

    posts = response.json()["posts"]

    if not posts:
        st.info("No posts yet.")
        return

    for post in posts:
        st.markdown("---")
        st.markdown(
            f"**{post['email']}** · {post['created_at'][:19].replace('T', ' ')}"
        )
        st.write(post["blog"])

        if post.get("isowner"):
            if st.button("🗑️ Delete", key=f"del_{post['id']}"):
                res = requests.delete(
                    f"{API_BASE}/posts/{post['id']}",
                    headers=get_headers(),
                )
                if res.status_code == 200:
                    st.success("Deleted")
                    st.rerun()
                else:
                    st.error("Delete failed")


# ----------------------------
# Main App
# ----------------------------
if st.session_state.user is None:
    login_page()
else:
    st.sidebar.title(f"👋 {st.session_state.user['email']}")

    if st.sidebar.button("Logout"):
        st.session_state.user = None
        st.session_state.token = None
        st.rerun()

    page = st.sidebar.radio("Navigate", ["🏠 Feed", "✍️ New Post"])

    if page == "🏠 Feed":
        feed_page()
    else:
        post_page()
