import streamlit as st
from google import genai
from dotenv import load_dotenv
import os

# -----------------
# Setup
# -----------------

load_dotenv()
client = genai.Client(
    api_key=st.secrets["GEMINI_API_KEY"]
)
SYSTEM_PROMPT = """
You are VARDAN AI.

Official AI assistant of Donate Life NGO,
Surat, Gujarat, India.

Your purpose:
Provide intelligent, helpful, and educational responses about organ donation and Donate Life NGO.

Answer priority:

1. Use Donate Life website information when relevant.
2. Expand naturally using Gemini knowledge.
3. Add examples only when useful.

Response Style:

- Keep responses medium length
- Usually 100–220 words
- Give direct answers first
- Use short sections
- Use bullet points only if they improve readability
- Avoid long paragraphs
- Avoid repeating information
- Explain clearly and naturally

Rules:

- Answer in a friendly and professional tone
- For Donate Life NGO questions:
  prioritize website information

- For organ donation questions:
  combine:
  • educational explanation
  • awareness information
  • website information when relevant

- If website information is limited:
  continue using Gemini knowledge

- If user asks unrelated questions:
Reply:
"I specialize in organ donation and Donate Life NGO information."

- Do not provide medical diagnosis
- Do not invent NGO details
- If user asks about:
  • organ donation pledge
  • pledge registration
  • how to register as donor
  • where to pledge organ donation
  • how to become an organ donor

  Reply that users can register their organ donation pledge at:

  https://notto.abdm.gov.in/register/

  Encourage users politely to complete registration.
End naturally.
"""
# -----------------
# Page Config
# -----------------

st.set_page_config(
    page_title="VARDAN AI",
    page_icon="🫀",
    layout="wide"
)

# -----------------
# Session Storage
# -----------------

if "all_chats" not in st.session_state:
    st.session_state.all_chats = {}

if "messages" not in st.session_state:
    st.session_state.messages = []

if "current_chat" not in st.session_state:
    st.session_state.current_chat = "New Chat"

# -----------------
# Sidebar
# -----------------

with st.sidebar:

    # LOGO
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        image_path = "images.jpg"

        if os.path.exists(image_path):

            st.image(
                image_path,
                width=170
            )

    st.markdown(
        """
        <h2 style='text-align:center;color:#1b2a57;'>
            VARDAN AI
        </h2>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <p style='text-align:center;color:gray;font-size:20px;'>
        Donate Life NGO<br>
        Surat, Gujarat
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # CONNECT
    st.markdown("### 🌐 Connect")

    st.link_button(
    "Visit Website",
    "https://donatelifengo.org",
    use_container_width=True
    )
    st.link_button(
    "🫀 Get Organ Donation Pledge",
    "https://notto.abdm.gov.in/register/",
    use_container_width=True
    )
    
    st.divider()

    st.markdown(
        """
        <p style='color:gray;font-size:17px;'>
        🩷 One organ donor can save multiple lives.
        </p>
        """,
        unsafe_allow_html=True
    )

    st.divider()

    # NEW CHAT
    if st.button(
        "＋ New Chat",
        use_container_width=True
    ):

        st.session_state.current_chat = "New Chat"
        st.session_state.messages = []

        st.rerun()

    st.markdown("### 💬 History")

    # HISTORY
    for chat in reversed(
        list(
            st.session_state.all_chats.keys()
        )
    ):

        if st.button(
            chat,
            key=chat,
            use_container_width=True
        ):

            st.session_state.current_chat = chat

            st.session_state.messages = (
                st.session_state.all_chats[
                    chat
                ]
            )

            st.rerun()
# -----------------
# Main Page
# -----------------

st.title("🫀 VARDAN AI")

st.caption(
    "Donate Life AI Assistant"
)

# -----------------
# Show Chat
# -----------------

for msg in st.session_state.messages:

    with st.chat_message(
        msg["role"]
    ):
        st.write(
            msg["content"]
        )

# -----------------
# User Input
# -----------------

prompt = st.chat_input(
    "Ask about organ donation..."
)

if prompt:

    # Save user message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    # Show user message
    with st.chat_message("user"):
        st.write(prompt)

    # Chat title
    if (
        st.session_state.current_chat
        == "New Chat"
    ):

        chat_title = prompt.strip()

        if len(chat_title) > 40:
            chat_title = (
                chat_title[:40]
                + "..."
            )

        st.session_state.current_chat = (
            chat_title
        )

    # Build conversation
    history = "\n".join(
        [
            f'{m["role"]}: {m["content"]}'
            for m in st.session_state.messages
        ]
    )

    final_prompt = (
        SYSTEM_PROMPT
        + "\n\n"
        + history
    )

    try:

        response = (
            client.models.generate_content(
                model="gemini-2.5-flash",
                contents=final_prompt
            )
        )

        answer = response.text

    except Exception as e:

        answer = (
            f"Error: {e}"
        )

    # Save AI answer
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    # Save chat
    st.session_state.all_chats[
        st.session_state.current_chat
    ] = (
        st.session_state.messages.copy()
    )

    st.rerun()
