"""Misc fixtures and helpers for all tests"""
import os
import pathlib

import dotenv

tests_directory = pathlib.Path(__file__).resolve().parent

# Loading test environment vars
_dotenv_path = dotenv.find_dotenv()
dotenv.load_dotenv(_dotenv_path)

tenant_id = os.getenv("DL_TENANT_ID")
client_id = os.getenv("DL_CLIENT_ID")
client_secret = os.getenv("DL_CLIENT_SECRET")
username = os.getenv("DL_USERNAME")
password = os.getenv("DL_PASSWORD")
store_name = os.getenv("DL_STORE_NAME")
