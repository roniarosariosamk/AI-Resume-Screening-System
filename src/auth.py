import streamlit as st

def authenticate(username, password):
    """
    Simple username/password authentication.
    """

    ADMIN_USERNAME = "admin"
    ADMIN_PASSWORD = "admin123"

    return (
        username == ADMIN_USERNAME
        and password == ADMIN_PASSWORD
    )