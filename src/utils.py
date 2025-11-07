"""Utility functions for the chat interface."""
import streamlit as st
from typing import List, Dict

def initialize_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = None

def add_message(role: str, content: str):
    """Add a message to the chat history.
    
    Args:
        role (str): The role of the message sender ('user' or 'assistant')
        content (str): The message content
    """
    # Ensure the role is one of the allowed values
    allowed_roles = ['user', 'assistant', 'system']
    if role not in allowed_roles:
        raise ValueError(f"Role must be one of {allowed_roles}")
    
    st.session_state.messages.append({
        "role": role,
        "content": content
    })

def get_chat_history() -> List[Dict[str, str]]:
    """Get the chat history.
    
    Returns:
        List[Dict[str, str]]: List of message dictionaries
    """
    return st.session_state.messages

def clear_chat_history():
    """Clear the chat history."""
    st.session_state.messages = []
    st.session_state.conversation_id = None