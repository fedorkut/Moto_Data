# driver_manager.py
from app.driver import DriverManager

# Create shared instance of DriverManager
session_handler = DriverManager()

def get_driver_manager():
    return session_handler
