"""Main application file for the chat interface."""
import streamlit as st
import logging
import sys
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

# Import after logging setup
try:
    from utils import (
        initialize_session_state,
        add_message,
        get_chat_history,
        clear_chat_history
    )
    from azure_openai_service import chat_service
    logger.info("Successfully imported all modules")
except Exception as e:
    logger.error(f"Error importing modules: {e}")
    raise

def setup_page():
    """Configure the Streamlit page."""
    st.set_page_config(
        page_title="Chat Bot UI",
        page_icon="💬",
        layout="centered",
        initial_sidebar_state="expanded",
    )

def setup_sidebar():
    """Setup the sidebar with controls."""
    with st.sidebar:
        st.title("Chat Bot Settings")

        # Display API status
        if chat_service and chat_service.is_configured():
            st.success("🟢 Chat API Connected")
        else:
            st.error("🔴 Chat API Not Connected")

        st.markdown("---")

        # System Message Configuration
        st.subheader("🎯 AI Behavior")

        # Initialize system message in session state if not present
        if "custom_system_message" not in st.session_state:
            st.session_state.custom_system_message = "You are a helpful AI assistant. Provide clear, concise, and helpful responses."

        # Text area for custom system message
        new_system_message = st.text_area(
            "System Message:",
            value=st.session_state.custom_system_message,
            height=120,
            help="Define the AI's behavior, personality, and restrictions."
        )

        # Update system message if changed
        if new_system_message != st.session_state.custom_system_message:
            st.session_state.custom_system_message = new_system_message
            st.success("✅ System message updated!")

        st.markdown("---")

        if st.button("Clear Chat"):
            clear_chat_history()

        st.markdown("---")
        st.markdown("""
        ### About
        This is an AI chat interface powered by:
        - Azure OpenAI / Local Chat API
        - Streamlit
        - Python
        - ❤️
        """)

def display_chat_history():
    """Display the chat history."""
    for message in get_chat_history():
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

def handle_user_input():
    """Handle user input and generate response."""
    if prompt := st.chat_input("What's on your mind?"):
        # Add user message to chat history
        add_message("user", prompt)

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response using the selected API
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                if chat_service and chat_service.is_configured():
                    chat_history = get_chat_history()
                    response = chat_service.generate_response(prompt, chat_history)
                else:
                    response = "I'm sorry, the chat service is not properly configured. Please check your settings."

                st.markdown(response)
                add_message("assistant", response)

def main():
    """Main application function."""
    try:
        logger.info("Starting main application")
        st.title("🤖 AI Chat Assistant")
        st.write("Initializing...")

        setup_page()
        logger.info("Page setup complete")

        initialize_session_state()
        logger.info("Session state initialized")

        setup_sidebar()
        logger.info("Sidebar setup complete")
        
        st.title("🤖 AI Chat Assistant")
        st.markdown("*Powered by Azure OpenAI*")
        st.markdown("---")
        
        display_chat_history()
        logger.info("Chat history displayed")

        handle_user_input()
        logger.info("User input handler setup complete")

    except Exception as e:
        logger.error(f"Error in main function: {e}")
        st.error(f"An error occurred: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        logger.info("Starting application")
        main()
    except Exception as e:
        logger.error(f"Application failed: {e}")
        st.error("Failed to start the application. Check the logs for details.")